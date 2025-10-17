#!/usr/bin/env python3
"""
Refresh icon lists for all supported icon sets.
Downloads the latest icon names from official repositories.
"""

import json
import re
import urllib.request
from urllib.error import URLError
import sys


def fetch_heroicons():
    """
    Fetch Heroicons from the Tailwind Labs GitHub repository.
    """
    print("Fetching Heroicons...")
    url = "https://api.github.com/repos/tailwindlabs/heroicons/contents/optimized/24/outline"

    try:
        headers = {'User-Agent': 'Python Script'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            icons = [item['name'].replace('.svg', '') for item in data if item['name'].endswith('.svg')]
            print(f"Found {len(icons)} Heroicons")
            return sorted(icons)
    except Exception as e:
        print(f"Failed to fetch Heroicons: {e}", file=sys.stderr)
        return None


def fetch_lucide():
    """
    Fetch Lucide icons from the GitHub repository.
    """
    print("Fetching Lucide icons...")
    url = "https://api.github.com/repos/lucide-icons/lucide/contents/icons"

    try:
        headers = {'User-Agent': 'Python Script'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            icons = [item['name'].replace('.svg', '') for item in data if item['name'].endswith('.svg')]
            print(f"Found {len(icons)} Lucide icons")
            return sorted(icons)
    except Exception as e:
        print(f"Failed to fetch Lucide icons: {e}", file=sys.stderr)
        return None


def fetch_fontawesome():
    """
    Fetch FontAwesome icons from the official metadata.
    """
    print("Fetching FontAwesome icons...")
    url = "https://raw.githubusercontent.com/FortAwesome/Font-Awesome/master/metadata/icons.json"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            # FontAwesome metadata is a dict with icon names as keys
            icons = list(data.keys())
            print(f"Found {len(icons)} FontAwesome icons")
            return sorted(icons)
    except Exception as e:
        print(f"Failed to fetch FontAwesome icons: {e}", file=sys.stderr)
        return None


def save_icon_list(filename, icons):
    """
    Save icon list to a text file.
    """
    if icons:
        with open(filename, 'w') as f:
            f.write('\n'.join(icons) + '\n')
        print(f"Saved {len(icons)} icons to {filename}")
        return True
    return False


def main():
    """
    Refresh all icon lists.
    """
    print("Refreshing icon lists...\n")

    icon_sets = {
        'heroicon-list.txt': fetch_heroicons,
        'lucide-list.txt': fetch_lucide,
        'fontawesome-list.txt': fetch_fontawesome,
    }

    failed = []
    for filename, fetcher in icon_sets.items():
        icons = fetcher()
        if not save_icon_list(filename, icons):
            failed.append(filename)
        print()

    if failed:
        print(f"Failed to refresh: {', '.join(failed)}", file=sys.stderr)
        sys.exit(1)
    else:
        print("All icon lists refreshed successfully!")
        sys.exit(0)


if __name__ == "__main__":
    main()
