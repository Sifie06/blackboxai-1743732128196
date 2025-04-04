#!/usr/bin/env python3
"""
LEGAL WI-FI PASSWORD RETRIEVER
Only extracts passwords for networks already saved on this computer.
Does NOT crack or access unauthorized networks.
"""

import subprocess
import sys
import platform
from typing import List, Dict

def get_saved_wifi_profiles() -> List[str]:
    """Get list of saved Wi-Fi profiles on Windows"""
    try:
        output = subprocess.check_output(
            ['netsh', 'wlan', 'show', 'profiles'],
            stderr=subprocess.DEVNULL,
            shell=True
        ).decode('utf-8', errors='ignore')
        return [line.split(':')[1].strip() 
                for line in output.split('\n') 
                if 'All User Profile' in line]
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []

def get_wifi_password(profile: str) -> str:
    """Get password for a specific saved Wi-Fi profile"""
    try:
        output = subprocess.check_output(
            ['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'],
            stderr=subprocess.DEVNULL,
            shell=True
        ).decode('utf-8', errors='ignore')
        return next(
            (line.split(':')[1].strip()
             for line in output.split('\n')
             if 'Key Content' in line),
            '<no password>'
        )
    except subprocess.CalledProcessError:
        return '<error retrieving>'

def display_results(profiles: Dict[str, str]) -> None:
    """Display results in a formatted table"""
    print("\n{:<30}| {:<}".format("Wi-Fi Name", "Password"))
    print("-" * 50)
    for name, pwd in profiles.items():
        print("{:<30}| {:<}".format(name, pwd))

def main():
    """Main function"""
    print("=== LEGAL WI-FI PASSWORD RETRIEVER ===")
    print("This only shows passwords for networks already saved on this computer.\n")
    
    if platform.system() != 'Windows':
        print("Error: This script only works on Windows systems")
        return

    profiles = get_saved_wifi_profiles()
    if not profiles:
        print("No saved Wi-Fi profiles found")
        return

    results = {profile: get_wifi_password(profile) for profile in profiles}
    display_results(results)

if __name__ == '__main__':
    main()