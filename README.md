# Very Secure Bank 🏦

Very Secure Bank is a deliberately vulnerable banking application designed for red teaming practice. It simulates a basic banking system with intentional security flaws, allowing security professionals and ethical hackers to test exploitation techniques in a controlled environment.

## Features
  - 🏦 **Banking System Simulation** – Users can register, log in, and perform basic transactions.
  - 🔓 **Intentional Vulnerabilities** – Designed to help practice red teaming techniques, including:
  - **Unsecure JWT** – Weak token security leading to authentication issues.
  - **IDOR (Insecure Direct Object References)** – Access control flaws allowing unauthorized data retrieval.
  - **SQL Injection** – Injection vulnerabilities exposing sensitive data.
  - 🎯 **Real-World Scenario** – Mimics a typical web application used in penetration testing.
  - 💻 **Built with**:
  - **Django** – Backend framework managing authentication and transactions.
  - **Tailwind CSS** – Modern UI design.
  - **SQLite** – Lightweight database for easy deployment.