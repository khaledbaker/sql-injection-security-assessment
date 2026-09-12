# SQL Injection Vulnerability Assessment — My Shop E-Commerce Application

## Overview
Professional-format security assessment identifying and exploiting three 
critical SQL injection vulnerabilities in a custom-built vulnerable web 
application, using both manual testing and Burp Suite Community Edition. 
Includes the target application's source code for full reproducibility.

## Summary of Findings

| Issue | Location | Severity | Exploited |
|-------|----------|----------|-----------|
| Authentication Bypass | /login (POST) | CRITICAL | ✅ |
| Hidden Data Retrieval | /products (GET) | HIGH | ✅ |
| Credentials Extraction | /products (GET) | CRITICAL | ✅ |

## Methodology
- Manual browser-based testing to simulate real-world attacker behaviour
- Burp Suite Community Edition (Proxy, Repeater, Intruder, Comparer) for 
  systematic testing and payload refinement

## Key Findings

### 1. Authentication Bypass (Critical)
Exploited via classic SQL injection (`admin' OR '1'='1`) due to direct 
string concatenation of user input into the login query — allowing 
complete authentication bypass without valid credentials.

### 2. Hidden Data Retrieval (High)
Bypassed the `released = 1` filter on the products endpoint via 
boolean-based injection, exposing unreleased/confidential product data.

### 3. Credentials Extraction (Critical)
Used UNION-based SQL injection to extract the full `users` table — 
usernames and passwords — from the same products endpoint. Also 
identified that passwords were stored in plaintext, a secondary 
critical finding.

## Business Impact
Findings were mapped to real regulatory exposure (GDPR, PCI-DSS, CCPA), 
framing technical risk in terms of business consequences — data breach 
liability, reputational damage, and regulatory fines.

## Remediation
Delivered a prioritised, time-bound remediation roadmap:
- **24 hours:** Parameterized queries, emergency patch, force password 
  reset, implement password hashing (bcrypt/Argon2)
- **1 week:** Input validation/whitelisting, ORM migration, 
  least-privilege database accounts
- **1 month:** WAF deployment, full security code review, SAST/DAST 
  testing program, developer security training

## Target Application
A custom-built vulnerable Flask e-commerce application, intentionally 
designed with unparameterized SQL queries to demonstrate real-world 
injection vulnerabilities in a safe, controlled environment.

**Run it yourself:**
```bash
cd vulnerable-app
python init_db.py    # Initialize the database
python app.py         # Start the Flask server on localhost:5000
```

**Reproduce the authentication bypass:**
1. Navigate to `http://localhost:5000/login`
2. Username: `admin' OR '1'='1` — Password: anything
3. Observe authentication bypass

## Tools Used
Burp Suite Community Edition · Manual Browser Testing · Flask · SQLite · 
SQL Injection (Boolean-based & UNION-based)

## Full Report
See [SQL-Injection-Security-Assessment.pdf](./report/sql-injection-security-assessment.pdf) 
for complete findings, testing steps, and secure code recommendations.

## Skills Demonstrated
Web Application Penetration Testing · SQL Injection · Burp Suite · 
OWASP Top 10 · Vulnerability Reporting · Business Risk Communication
