"""
Example Vulnerable Code for Testing

This file contains intentionally vulnerable code patterns
for testing the code analyzer.
"""

# SECURITY: SQL Injection Vulnerability - FIXED
def secure_sql_query(user_id):
    """Secure SQL query using parameterized queries."""
    # FIXED: Use parameterized queries to prevent SQL injection
    # Example with sqlite3:
    # cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    # Example with psycopg2:
    # cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    # Example with MySQL:
    # cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    import sqlite3
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result


# SECURITY: Hardcoded Credentials - FIXED
# FIXED: Use environment variables or secret manager instead of hardcoded credentials
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Secure: Load from environment variables
API_KEY = os.getenv("API_KEY")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

# Alternative: Use secret manager (e.g., AWS Secrets Manager, Azure Key Vault)
# from azure.keyvault.secrets import SecretClient
# client = SecretClient(vault_url="https://your-vault.vault.azure.net/", credential=credential)
# API_KEY = client.get_secret("api-key").value
# DATABASE_PASSWORD = client.get_secret("database-password").value

if not API_KEY or not DATABASE_PASSWORD:
    raise ValueError("API_KEY and DATABASE_PASSWORD must be set in environment variables")

# SECURITY: XSS Vulnerability - FIXED
import html

def secure_web_page(user_input):
    """Secure web page with XSS protection."""
    # FIXED: Sanitize user input to prevent XSS attacks
    # Option 1: Use html.escape() for HTML content
    sanitized_input = html.escape(str(user_input))
    html_content = f"<div>Welcome {sanitized_input}</div>"
    
    # Option 2: Use a templating engine with auto-escaping (e.g., Jinja2)
    # from jinja2 import Template
    # template = Template("<div>Welcome {{ user_input }}</div>")
    # html_content = template.render(user_input=user_input)  # Jinja2 auto-escapes
    
    # Option 3: Use a sanitization library (e.g., bleach)
    # import bleach
    # sanitized_input = bleach.clean(user_input, tags=[], strip=True)
    # html_content = f"<div>Welcome {sanitized_input}</div>"
    
    return html_content

# Legacy vulnerable function kept for reference (DO NOT USE IN PRODUCTION)
def vulnerable_web_page(user_input):
    """VULNERABLE: Do not use this function - kept only for demonstration."""
    html = f"<div>Welcome {user_input}</div>"  # VULNERABLE: XSS risk
    return html


# BUG: Null Pointer Risk
def process_user(user):
    """Function with potential null pointer."""
    name = user.name  # user might be None
    return name.upper()


# BUG: Resource Leak
def read_file_vulnerable(file_path):
    """File reading without proper cleanup."""
    file = open(file_path, 'r')
    content = file.read()
    # Missing: file.close()
    return content


# QUALITY: Code Smell - Long Function
def long_function():
    """Function that's too long (code smell)."""
    # ... 200+ lines of code ...
    pass


# QUALITY: Duplicate Code
def calculate_total_v1(items):
    """First version of calculation."""
    total = 0
    for item in items:
        total += item.price
    return total


def calculate_total_v2(items):
    """Second version - duplicate of v1."""
    total = 0
    for item in items:
        total += item.price
    return total


# SECURITY: Insecure Random
import random

def generate_token():
    """Insecure random token generation."""
    return random.randint(1000, 9999)
    # Should use: secrets.token_urlsafe()


# SECURITY: Command Injection - FIXED
import subprocess
import shlex

def execute_command_secure(user_input):
    """Secure command execution using subprocess with proper escaping."""
    # FIXED: Use subprocess with proper argument handling
    # Validate input first
    if not user_input or not user_input.isalnum():
        raise ValueError("Invalid input: only alphanumeric characters allowed")
    
    # Use subprocess with list of arguments (prevents injection)
    try:
        result = subprocess.run(
            ["ls", user_input],
            capture_output=True,
            text=True,
            timeout=5,
            check=False
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        raise ValueError("Command execution timed out")
    except Exception as e:
        raise ValueError(f"Command execution failed: {e}")
    
# Legacy vulnerable function kept for reference (DO NOT USE IN PRODUCTION)
def execute_command_vulnerable(user_input):
    """VULNERABLE: Do not use this function - kept only for demonstration."""
    import os
    os.system(f"ls {user_input}")  # VULNERABLE: Command injection risk


# BUG: Division by Zero
def calculate_average(numbers):
    """Potential division by zero."""
    total = sum(numbers)
    return total / len(numbers)  # len(numbers) might be 0


# QUALITY: Missing Error Handling
def risky_operation(data):
    """Operation without error handling."""
    result = data["key"]["nested"]["value"]
    # Should have try-except
    return result

