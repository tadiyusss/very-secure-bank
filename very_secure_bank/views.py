from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseServerError
from .forms import *
from .models import UserInformation
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random
import string
from django.db import connection
import jwt
import datetime
from base64 import b64decode
import json

def generate_jwt(payload, secret, algorithm='HS256', expiration_minutes=60):
    """
    Generate a JWT token.
    
    :param payload: Dictionary containing the claims for the token
    :param secret: Secret key used to sign the token
    :param algorithm: Algorithm to use for encoding (default: HS256)
    :param expiration_minutes: Expiry time in minutes (default: 60)
    :return: Encoded JWT token as a string
    """
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=expiration_minutes)
    payload['exp'] = expiration_time
    
    token = jwt.encode(payload, secret, algorithm=algorithm)
    return token

def generate_wallet_address():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

def login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                jwt_token = generate_jwt({
                    'user_id': user.id,
                    'role': 'user'
                }, 'secret_key')
                auth_login(request, user)
                response = redirect('dashboard')
                response.set_cookie('jwt_token', jwt_token)
                return response
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid form submission')

    context = {
        'login_form': form
    }
    return render(request, 'login.html', context)

def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('register')
            
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
                return redirect('register')
            
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            user.save()
            
            user_info = UserInformation(user_id=user.id, address=address, wallet_address = generate_wallet_address())
            user_info.save()
            return redirect('login')
        else:
            messages.error(request, 'Invalid form submission')
    context = {
        'register_form': form
    }
    return render(request, 'register.html', context)

@login_required(login_url='login')
def dashboard(request):
    user_info = get_object_or_404(User, id=request.user.id)
    account_details = get_object_or_404(UserInformation, user_id = user_info)
    send_money_form = SendMoneyForm()
    add_money_form = AddMoneyForm()
    jwt_token = request.COOKIES.get('jwt_token')
    try:
        decoded = b64decode(jwt_token.split('.')[1] + '==').decode('utf-8')
        payload = json.loads(decoded)
        if 'role' not in payload:
            return HttpResponseServerError('role not found')
        
        if payload['role'] != 'admin':
            role = 'user'
        else:
            role = 'admin'
    except:
        return HttpResponseServerError('Invalid JWT token')
    
    

    if request.method == 'POST':
        if 'send_money' in request.POST:
            send_money_form = SendMoneyForm(request.POST)
            if send_money_form.is_valid():
                receiver = UserInformation.objects.filter(wallet_address=send_money_form.cleaned_data['receiver_wallet_address']).first()
                amount = send_money_form.cleaned_data['amount']
                if not receiver:
                    messages.error(request, 'Unable to find wallet address', extra_tags='send_money')

                if account_details.balance < amount:
                    messages.error(request, 'Insufficient balance', extra_tags='send_money')
                
                account_details.balance -= amount
                account_details.save()
                receiver.balance += amount
                receiver.save()

                transaction = Transactions(sender=account_details, receiver=receiver, amount=amount)
                transaction.save()

                messages.success(request, 'Money sent successfully', extra_tags='send_money')
            else:
                messages.error(request, 'Invalid form submission', extra_tags='send_money')

        if 'add_money' in request.POST:
            add_money_form = AddMoneyForm(request.POST)
            if add_money_form.is_valid():
                amount = add_money_form.cleaned_data['amount']
                if amount <= 0:
                    messages.error(request, 'Invalid amount', extra_tags='add_money')
                else:
                    account_details.balance += amount
                    account_details.save()
                    messages.success(request, 'Money added successfully', extra_tags='add_money')
            else:
                messages.error(request, 'Invalid form submission', extra_tags='add_money')

    context = {
        'user_info': user_info,
        'account_details': account_details,
        'send_money_form': send_money_form,
        'role': role,
        'add_money_form': add_money_form
    }

    if role == 'admin':
        user_list = User.objects.all()
        context['user_list'] = user_list

    return render(request, 'dashboard/index.html', context)

@login_required(login_url='login')
def view_profile(request, user_id):
    user_info = get_object_or_404(User, id=user_id)
    account_details = get_object_or_404(UserInformation, user_id = user_info)
    change_password_form = ChangePasswordForm()
    edit_form = EditUserForm(initial={
        'first_name': user_info.first_name,
        'last_name': user_info.last_name,
        'email': user_info.email,
        'address': account_details.address
    })

    
    if request.method == 'POST':
        if 'edit_profile' in request.POST:
            edit_form = EditUserForm(request.POST)
            if edit_form.is_valid():
                user_info.first_name = edit_form.cleaned_data['first_name']
                user_info.last_name = edit_form.cleaned_data['last_name']
                user_info.email = edit_form.cleaned_data['email']
                user_info.save()
                account_details.address = edit_form.cleaned_data['address']
                account_details.save()
                messages.success(request, 'Profile updated successfully', extra_tags='profile')
            else:
                messages.error(request, 'Invalid form submission', extra_tags='profile')

        if 'change_password' in request.POST:
            change_password_form = ChangePasswordForm(request.POST)
            if change_password_form.is_valid():
                new_password = change_password_form.cleaned_data['new_password']
                confirm_password = change_password_form.cleaned_data['confirm_password']
                if new_password == confirm_password:
                    user_info.set_password(new_password)
                    user_info.save()
                    messages.success(request, 'Password changed successfully', extra_tags='password')
                else:
                    messages.error(request, 'Passwords do not match', extra_tags='password')
            else:
                messages.error(request, 'Invalid form submission', extra_tags='password')
    context = {
        'user_info': user_info,
        'account_details': account_details,
        'edit_form': edit_form,
        'change_password_form': change_password_form
    }

    return render(request, 'dashboard/profile.html', context)


@login_required(login_url='login')
def transactions(request):
    user_id = request.GET.get('user_id')
    user_transactions = []
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM very_secure_bank_transactions WHERE sender_id = {user_id} OR receiver_id = {user_id}")
        columns = [col[0] for col in cursor.description]
        user_transactions = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
    context = {
        'user_transactions': user_transactions
    }
    return render(request, 'dashboard/transactions.html', context)

def logout(request):
    auth_logout(request)
    return redirect('login')





def handler404(request, exception):
    return render(request, '404.html', status=404)