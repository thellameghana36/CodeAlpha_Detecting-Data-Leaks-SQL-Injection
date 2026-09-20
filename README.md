
# CodeAlpha_Detecting-Data-Leaks-SQL-Injection

### Task 2 - Detecting Data Leaks Using SQL Injection | CodeAlpha Cloud Computing Internship
### AES-256 + Capability Code Security

**Developed by: Thella Meghana**

## 📌 Project Overview
This project demonstrates how SQL Injection attacks cause data leaks in cloud databases and how to prevent them with a secure double-layer protection system using AES-256 Encryption and Capability-Based Security.

## 🎯 Objective
- To show vulnerable login bypass using `' OR '1'='1`
- To detect and block SQL Injection attempts
- To secure cloud data with AES-256 Encryption + Capability Code

## 🔐 Features
- **Vulnerable Login:** Shows how `' OR '1'='1` bypasses authentication
- **Secure Login:** Blocks injection with Parameterized Queries
- **AES-256 Encryption:** Passwords are encrypted
- **Capability Code:** Unique code generated after register (Example: `25840eaa`)
- **Real-time Alert:** `ALERT! SQL Injection Detected & Blocked - Data Leak Prevented`

## 🧪 Demo Credentials (From Video)

**1. For Registration:**
- Username: `meghana`
- Password: `meghana123`
- After Register -> You get Capability Code: `25840eaa` (example, yours will be different)

**2. For SQL Injection Attack Test (Secure Login Section):**
- Username: `' OR '1'='1`
- Password: `any`
- Capability Code: `25840eaa` (use your generated code)
- Result: **BLOCKED** -> Shows ALERT message

**3. For Normal Secure Login:**
- Username: `meghana`
- Password: `meghana123`
- Capability Code: `25840eaa`
- Result: **Login Success**

## 🚀 How to Run

```bash
pip install -r requirements.txt
python app.py
