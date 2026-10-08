# 🛡️ AI-Powered Secure Code Review & SAST Platform

An enterprise-grade Static Application Security Testing (SAST) platform and AI-assisted security refactoring tool built with Python, Streamlit, and Bandit. Designed to automatically detect OWASP Top 10 vulnerabilities, CWE patterns, and offer automated secure code remediation.

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?style=for-the-badge&logo=streamlit)
![Security](https://img.shields.io/badge/Security-SAST%20%2F%20OWASP-green?style=for-the-badge)

## ✨ Key Features
- **Automated Code Audit:** Powered by Bandit AST analysis engine for detection of SQL Injection (CWE-89), Hardcoded Credentials (CWE-259), Command Injection, and Insecure Deserialization.
- **Interactive AI Assistant:** Integrated AI Security Agent for real-time natural language query resolution and automated secure code generation.
- **Multi-Format Scan Input:** Supports project file selection or live custom code pasting (UTF-8 encoding enabled).
- **Language Enforcement:** Automatic detection and guidance for non-Python languages.
- **Executive JSON Reporting:** One-click downloadable threat and vulnerability analytics report.

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_GITHUB_USERNAME/secure-code-review.git](https://github.com/YOUR_GITHUB_USERNAME/secure-code-review.git)
cd secure-code-review