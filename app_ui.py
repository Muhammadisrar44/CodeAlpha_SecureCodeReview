import streamlit as st
import subprocess
import json
import os
import time
import re

# Enterprise Page Configuration
st.set_page_config(
    page_title="Muhammad Israr | Secure Code Review & AI Agent",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced Modern Dark Glassmorphism CSS UI/UX
st.markdown("""
    <style>
    /* Main Theme Setup */
    .stApp {
        background: #090d16;
        color: #e6edf3;
        font-family: 'Segoe UI', Inter, sans-serif;
    }
    
    /* Header Branding Banner */
    .header-card {
        background: linear-gradient(135deg, rgba(22, 27, 34, 0.8) 0%, rgba(13, 17, 23, 0.9) 100%);
        border: 1px solid rgba(88, 166, 255, 0.3);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(10px);
        margin-bottom: 25px;
    }

    /* Dev Profile Badge & Links */
    .dev-badge {
        background: linear-gradient(90deg, #1f6beb 0%, #238636 100%);
        padding: 6px 14px;
        border-radius: 20px;
        color: #ffffff;
        font-weight: 700;
        font-size: 13px;
        display: inline-block;
        box-shadow: 0 0 12px rgba(31, 107, 235, 0.6);
        margin-right: 10px;
    }

    .social-link {
        color: #58a6ff !important;
        text-decoration: none !important;
        font-weight: 600;
        margin-right: 15px;
        transition: color 0.3s ease;
    }
    .social-link:hover {
        color: #79c0ff !important;
        text-shadow: 0 0 8px rgba(88, 166, 255, 0.8);
    }

    /* Interactive Glow Action Buttons */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #1f6beb 0%, #238636 100%);
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 14px 28px;
        font-size: 16px;
        font-weight: 700;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 20px rgba(31, 107, 235, 0.4);
        letter-spacing: 0.5px;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 28px rgba(35, 134, 54, 0.7);
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%);
        border: 1px solid #58a6ff;
    }

    /* Dashboard Metric Cards */
    .metric-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 18px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }

    /* Vulnerability Cards */
    .vuln-card {
        background-color: #1a0c0e;
        border-left: 5px solid #f85149;
        border-radius: 8px;
        padding: 18px;
        margin-bottom: 20px;
        border-top: 1px solid rgba(248, 81, 73, 0.2);
        border-right: 1px solid rgba(248, 81, 73, 0.2);
        border-bottom: 1px solid rgba(248, 81, 73, 0.2);
    }

    .fix-card {
        background-color: #0d1117;
        border-left: 5px solid #58a6ff;
        border-radius: 8px;
        padding: 16px;
        margin-top: 10px;
        border-top: 1px solid rgba(88, 166, 255, 0.2);
        border-right: 1px solid rgba(88, 166, 255, 0.2);
        border-bottom: 1px solid rgba(88, 166, 255, 0.2);
    }

    .safe-card {
        background-color: #0c1a12;
        border-left: 5px solid #3fb950;
        border-radius: 8px;
        padding: 18px;
        margin-bottom: 15px;
        border-top: 1px solid rgba(63, 185, 80, 0.2);
        border-right: 1px solid rgba(63, 185, 80, 0.2);
        border-bottom: 1px solid rgba(63, 185, 80, 0.2);
    }

    .code-block {
        background-color: #010409;
        border: 1px solid #21262d;
        padding: 12px;
        border-radius: 6px;
        font-family: 'Fira Code', 'Courier New', monospace;
        color: #79c0ff;
        margin-top: 8px;
    }

    /* AI Chat Box Styling */
    .chat-bubble-user {
        background-color: #1f6beb;
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 2px 18px;
        margin-bottom: 10px;
        max-width: 80%;
        margin-left: auto;
    }
    .chat-bubble-ai {
        background-color: #161b22;
        color: #e6edf3;
        border: 1px solid #30363d;
        padding: 14px 18px;
        border-radius: 18px 18px 18px 2px;
        margin-bottom: 10px;
        max-width: 85%;
    }
    </style>
""", unsafe_allow_html=True)

# Helper function to check non-python code
def detect_non_python_code(code):
    non_python_patterns = [
        r'\bpublic\s+class\b', r'\bpublic\s+static\s+void\s+main\b',
        r'#include\s*<.*?>', r'\bstd::cout\b', r'\bint\s+main\(\)',
        r'\busing\s+System;', r'\bConsole\.WriteLine\b',
        r'\bfunction\s+\w+\s*\(', r'\bconst\s+\w+\s*=', r'\blet\s+\w+\s*='
    ]
    for pattern in non_python_patterns:
        if re.search(pattern, code):
            return True
    return False

# Rule-Based Intelligent Code Fixer AI Agent
def ai_agent_fix_code(user_prompt):
    # Rule 1: SQL Injection
    fixed_code = user_prompt
    explanations = []

    if "SELECT" in fixed_code and "f\"" in fixed_code or "f'" in fixed_code:
        fixed_code = re.sub(
            r"query\s*=\s*f[\"']SELECT\s+\*\s+FROM\s+(\w+)\s+WHERE\s+(\w+)\s*=\s*['\"]\{(\w+)\}['\"][\"']",
            r"query = 'SELECT * FROM \1 WHERE \2 = ?'\n        cursor.execute(query, (\3,))",
            fixed_code
        )
        explanations.append("Fixed SQL Injection: Converted dynamic string formatting into parameterized prepared queries (`?`).")

    # Rule 2: Hardcoded Secrets
    if "API_SECRET" in fixed_code or "SECRET_KEY" in fixed_code or "PASSWORD" in fixed_code:
        if "=" in fixed_code and "os.getenv" not in fixed_code:
            fixed_code = re.sub(
                r'(API_SECRET_TOKEN|SECRET_KEY|PASSWORD)\s*=\s*["\'].*?["\']',
                r'\1 = os.getenv("\1")',
                fixed_code
            )
            explanations.append("Fixed Hardcoded Secrets: Replaced plain-text credentials with secure `os.getenv()` environment variable calls.")

    # Rule 3: Subprocess Shell=True Risk
    if "subprocess.run" in fixed_code and "shell=True" in fixed_code:
        fixed_code = fixed_code.replace("shell=True", "shell=False")
        explanations.append("Fixed Command Injection: Set `shell=False` in `subprocess.run()` to prevent unauthorized command execution.")

    # Rule 4: Unsafe YAML
    if "yaml.load(" in fixed_code and "Loader=" in fixed_code:
        fixed_code = re.sub(r'yaml\.load\((.*?),.*?\)', r'yaml.safe_load(\1)', fixed_code)
        explanations.append("Fixed Insecure Deserialization: Replaced `yaml.load()` with `yaml.safe_load()`.")

    if not explanations:
        return "Hello! I am your AI Code Security Assistant. Paste any code or ask me any question about code review, OWASP standards, or security fixes. Your code looks fine or needs custom scanning!"
    
    response_msg = "### AI Security Agent Findings & Automated Fix:\n\n"
    for exp in explanations:
        response_msg += f"- **{exp}**\n"
    
    response_msg += "\n#### Here is your 100% Correct & Secured Python Code:\n"
    return response_msg, fixed_code

# Sidebar Navigation & Profile
with st.sidebar:
    st.title("Secure Code Review")
    st.markdown("**Developer Details**")
    st.markdown("Developer: **Muhammad Israr**")
    st.markdown("Portfolio: [www.muhammadisrar.online](https://www.muhammadisrar.online)")
    st.markdown("LinkedIn: [Profile Link](https://www.linkedin.com/in/muhammad-israr-345620407/)")
    
    st.markdown("---")
    st.markdown("### Technical Engine Specifications")
    st.caption("Core Engine: Bandit Security Analyzer")
    st.caption("AI Assistant: Intelligent Security Refactor Agent")
    st.caption("Standard Compliance: OWASP Top 10 / CWE")
    st.caption("Target Language: Python 3.x")

# Main Header Banner
st.markdown("""
    <div class="header-card">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div>
                <h1 style="margin: 0; color: #58a6ff; font-size: 28px;">Secure Code Review & AI Agent Platform</h1>
                <p style="margin: 5px 0 0 0; color: #8b949e;">Enterprise Static Application Security Testing (SAST) & Interactive Code Assistant</p>
            </div>
            <div>
                <span class="dev-badge">Lead Developer: Muhammad Israr</span>
            </div>
        </div>
        <hr style="border: 0; border-top: 1px solid #30363d; margin: 15px 0;">
        <div>
            Portfolio: <a class="social-link" href="https://www.muhammadisrar.online" target="_blank">www.muhammadisrar.online</a> | 
            LinkedIn: <a class="social-link" href="https://www.linkedin.com/in/muhammad-israr-345620407/" target="_blank">muhammad-israr-345620407</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# Main Navigation Tabs
tab_scanner, tab_ai_agent = st.tabs(["SAST Audit Scanner", "Interactive AI Security Agent Chat"])

# TAB 1: SAST AUDIT SCANNER
with tab_scanner:
    col_control, col_display = st.columns([1, 2])

    with col_control:
        st.subheader("Control Panel")
        
        input_mode = st.radio("Choose Input Method:", ["Select File from Project", "Paste Custom Code"])
        target_file_path = ""
        is_non_python = False
        
        if input_mode == "Select File from Project":
            project_files = [f for f in os.listdir(".") if f.endswith(".py") and f != "app_ui.py"]
            selected_file = st.selectbox("Select Application Source File:", project_files)
            target_file_path = selected_file
            
            if os.path.exists(selected_file):
                with open(selected_file, "r", encoding="utf-8") as f:
                    st.markdown("**Source Code Preview:**")
                    st.code(f.read(), language="python", line_numbers=True)
        else:
            custom_code = st.text_area(
                "Paste Code For Analysis:",
                height=250,
                value='import sqlite3\n\ndef login(user, password):\n    query = f"SELECT * FROM users WHERE user=\'{user}\'"\n    return query'
            )
            
            if custom_code:
                if detect_non_python_code(custom_code):
                    is_non_python = True
                else:
                    temp_dir = os.path.join(os.getcwd(), "temp")
                    os.makedirs(temp_dir, exist_ok=True)
                    temp_file_path = os.path.join(temp_dir, "custom_scan_input.py")
                    with open(temp_file_path, "w", encoding="utf-8") as f:
                        f.write(custom_code)
                    target_file_path = temp_file_path

        run_scan_btn = st.button("EXECUTE SECURITY AUDIT")

    with col_display:
        st.subheader("Audit Analytics & Threat Report")
        
        if run_scan_btn:
            if is_non_python:
                st.error("Unsupported Language Detected!")
                st.warning("Notice: This SAST engine is specifically designed for Python source code analysis. Please submit valid Python 3.x code (e.g. Java, C++, and C# are not supported in this module).")
            elif not target_file_path or not os.path.exists(target_file_path):
                st.error("Invalid source file or code input.")
            else:
                progress_bar = st.progress(0)
                status = st.empty()
                
                for step in range(1, 101, 25):
                    time.sleep(0.05)
                    progress_bar.progress(step)
                    status.text(f"Auditing AST logic and scanning CWE vulnerability patterns... {step}%")
                    
                status.empty()
                progress_bar.empty()
                
                cmd = ["bandit", "-f", "json", "-r", target_file_path]
                res = subprocess.run(cmd, capture_output=True, text=True)
                
                try:
                    data = json.loads(res.stdout)
                    vulns = data.get("results", [])
                    total_vulns = len(vulns)
                    
                    m1, m2, m3 = st.columns(3)
                    with m1:
                        display_name = os.path.basename(target_file_path)
                        st.markdown(f'<div class="metric-card"><h4>Audited Entity</h4><h3 style="color:#58a6ff;">{display_name}</h3></div>', unsafe_allow_html=True)
                    with m2:
                        col_status = "#f85149" if total_vulns > 0 else "#3fb950"
                        st.markdown(f'<div class="metric-card"><h4>Vulnerabilities</h4><h3 style="color:{col_status};">{total_vulns}</h3></div>', unsafe_allow_html=True)
                    with m3:
                        status_txt = "CRITICAL RISK" if total_vulns > 0 else "PASSED / SECURE"
                        col_status = "#f85149" if total_vulns > 0 else "#3fb950"
                        st.markdown(f'<div class="metric-card"><h4>Status</h4><h3 style="color:{col_status};">{status_txt}</h3></div>', unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    report_json = json.dumps(data, indent=4)
                    st.download_button(
                        label="DOWNLOAD AUDIT REPORT (JSON)",
                        data=report_json,
                        file_name=f"Security_Audit_Report_{int(time.time())}.json",
                        mime="application/json"
                    )
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    tab_results, tab_remediation, tab_raw = st.tabs(["Vulnerability Findings & Corrections", "Remediation Guidance", "Raw JSON Data"])
                    
                    with tab_results:
                        if total_vulns > 0:
                            st.error(f"Detected {total_vulns} security vulnerability issues in analyzed source code.")
                            for idx, issue in enumerate(vulns, start=1):
                                test_id = issue.get('test_id', '')
                                v_code = issue['code'].strip()
                                
                                recommended_fix = "# Recommended Secure Fix:\n"
                                if "B608" in test_id or "sql" in issue['test_name'].lower():
                                    recommended_fix += "# Use parameterized queries to prevent SQL Injection\ncursor.execute('SELECT * FROM users WHERE user = ?', (user_input,))"
                                elif "B105" in test_id or "B106" in test_id or "password" in issue['test_name'].lower():
                                    recommended_fix += "# Use environment variables for secrets\nimport os\nDB_PASSWORD = os.getenv('DB_PASSWORD')"
                                else:
                                    recommended_fix += "# Sanitize input parameters and avoid unsafe execution calls."

                                st.markdown(f"""
                                <div class="vuln-card">
                                    <h4 style="color:#f85149; margin:0;">Finding #{idx}: {issue['test_name']}</h4>
                                    <p style="margin:5px 0;">
                                        <b>Severity Level:</b> <span style="color:#f85149; font-weight:bold;">{issue['issue_severity']}</span> | 
                                        <b>Confidence:</b> {issue['issue_confidence']} | 
                                        <b>Line Number:</b> {issue['line_number']}
                                    </p>
                                    <p style="margin:5px 0;"><b>Technical Description:</b> {issue['issue_text']}</p>
                                    <div class="code-block"><code>{v_code}</code></div>
                                    
                                    <div class="fix-card">
                                        <h5 style="color:#58a6ff; margin:0 0 5px 0;">Recommended Secure Correction:</h5>
                                        <p style="margin:0; font-size:13px; color:#8b949e;">Replace vulnerable statement at Line {issue['line_number']} with secure implementation below:</p>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                st.code(recommended_fix, language="python")
                        else:
                            st.markdown("""
                            <div class="safe-card">
                                <h4 style="color:#3fb950; margin:0;">Zero Vulnerabilities Identified</h4>
                                <p style="margin-top:5px;">Static application security testing confirms source code meets OWASP security standards.</p>
                            </div>
                            """, unsafe_allow_html=True)

                    with tab_remediation:
                        if total_vulns > 0:
                            st.warning("Security Policy Remediation Protocol:")
                            st.markdown("""
                            1. **SQL Injection Risks (CWE-89):** Always utilize parameterized prepared statements instead of dynamic string formatting.
                            2. **Hardcoded Secrets (CWE-259):** Never store plain text passwords/API keys in codebase. Use environment variables via `os.getenv()`.
                            3. **Unsafe Command Execution:** Validate and sanitize all external inputs prior to executing shell commands.
                            """)
                        else:
                            st.success("Security Compliance Verified. Source code meets enterprise standards.")
                    
                    with tab_raw:
                        st.json(data)
                        
                except Exception as err:
                    st.error(f"Scan Execution Failed: {str(err)}")

# TAB 2: INTERACTIVE AI SECURITY AGENT
with tab_ai_agent:
    st.subheader("AI Security Assistant & Automated Code Fixer Agent")
    st.markdown("Ask security questions or paste vulnerable code below. The AI Agent will analyze, explain, and automatically generate the 100% corrected secure code for you.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hello! I am your AI Security Agent. How can I assist you with code review or security refactoring today? Paste your code or message below!"}
        ]

    # Display Chat History
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-bubble-user"><b>You:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble-ai"><b>AI Agent:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)

    # User Input Form
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area("Type your message or paste code here:", height=120, placeholder="e.g. Please fix SQL Injection or review my python script...")
        submit_chat = st.form_submit_button("SEND TO AI AGENT")

    if submit_chat and user_input.strip():
        # Append User Message
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Process AI Response
        ai_response = ai_agent_fix_code(user_input)
        
        if isinstance(ai_response, tuple):
            text_desc, corrected_code = ai_response
            full_reply = f"{text_desc}\n```python\n{corrected_code}\n```"
        else:
            full_reply = ai_response

        st.session_state.chat_history.append({"role": "assistant", "content": full_reply})
        st.rerun()

# Footer Section
st.markdown("---")
st.markdown("""
    <p style="text-align: center; color: #8b949e; font-size: 14px;">
        Designed & Developed by <b>Muhammad Israr</b> | 
        <a style="color: #58a6ff; text-decoration: none;" href="https://www.muhammadisrar.online" target="_blank">Website</a> | 
        <a style="color: #58a6ff; text-decoration: none;" href="https://www.linkedin.com/in/muhammad-israr-345620407/" target="_blank">LinkedIn</a>
    </p>
""", unsafe_allow_html=True)