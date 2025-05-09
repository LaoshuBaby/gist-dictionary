#!/usr/bin/env python3
"""
Sample usage of the browser tab reader.

This script demonstrates how to use the browser tab reader with a sample Firefox profile.
"""

import os
import json
import tempfile
from pathlib import Path
from browser_tab_reader import get_firefox_tabs, is_dictionary_site, extract_search_term, format_timestamp

def create_sample_session_file():
    """Create a sample Firefox session file for demonstration."""
    # Create a temporary directory to simulate a Firefox profile
    temp_dir = tempfile.mkdtemp(prefix="firefox_profile_")
    session_backup_dir = Path(temp_dir) / "sessionstore-backups"
    os.makedirs(session_backup_dir, exist_ok=True)
    
    # Sample session data with dictionary sites
    session_data = {
        "windows": [
            {
                "tabs": [
                    {
                        "entries": [
                            {
                                "url": "https://www.dictionary.com/browse/example",
                                "title": "Example Definition & Meaning - Dictionary.com"
                            }
                        ],
                        "lastAccessed": 1715270400000,  # May 9, 2025
                        "createTime": 1715184000000     # May 8, 2025
                    },
                    {
                        "entries": [
                            {
                                "url": "https://www.merriam-webster.com/dictionary/vocabulary",
                                "title": "Vocabulary Definition & Meaning - Merriam-Webster"
                            }
                        ],
                        "lastAccessed": 1715270500000,
                        "createTime": 1715184100000
                    },
                    {
                        "entries": [
                            {
                                "url": "https://www.google.com/search?q=python+programming",
                                "title": "python programming - Google Search"
                            }
                        ],
                        "lastAccessed": 1715270600000,
                        "createTime": 1715184200000
                    }
                ]
            },
            {
                "tabs": [
                    {
                        "entries": [
                            {
                                "url": "https://www.etymonline.com/word/dictionary",
                                "title": "Dictionary | Etymology, origin and meaning of dictionary by etymonline"
                            }
                        ],
                        "lastAccessed": 1715270700000,
                        "createTime": 1715184300000
                    },
                    {
                        "entries": [
                            {
                                "url": "https://github.com/LaoshuBaby/gist-dictionary",
                                "title": "LaoshuBaby/gist-dictionary: A dictionary tool on GitHub Gist"
                            }
                        ],
                        "lastAccessed": 1715270800000,
                        "createTime": 1715184400000
                    }
                ]
            }
        ]
    }
    
    # Write the session data to a file
    session_file = session_backup_dir / "recovery.js"
    with open(session_file, 'w', encoding='utf-8') as f:
        json.dump(session_data, f, indent=2)
    
    return temp_dir


def main():
    """Demonstrate the browser tab reader with a sample Firefox profile."""
    # Load dictionary sites
    with open("dictionary_sites.txt", 'r', encoding='utf-8') as f:
        dictionary_sites = [line.strip() for line in f if line.strip()]
    
    # Create a sample Firefox profile
    profile_path = create_sample_session_file()
    print(f"Created sample Firefox profile at: {profile_path}")
    
    # Get tabs
    tabs = get_firefox_tabs(profile_path)
    
    # Process tabs
    print("\nAll Tabs:")
    print("=" * 80)
    for i, tab in enumerate(tabs, 1):
        print(f"{i}. {tab['title']}")
        print(f"   URL: {tab['url']}")
        print(f"   Last Accessed: {format_timestamp(tab['last_accessed'])}")
        print(f"   Creation Time: {format_timestamp(tab['creation_time'])}")
        print("-" * 80)
    
    # Process dictionary tabs
    print("\nDictionary Tabs:")
    print("=" * 80)
    dictionary_tabs = []
    for tab in tabs:
        url = tab['url']
        if is_dictionary_site(url, dictionary_sites):
            search_term = extract_search_term(url)
            print(f"• {tab['title']}")
            print(f"  URL: {url}")
            print(f"  Last Accessed: {format_timestamp(tab['last_accessed'])}")
            print(f"  Creation Time: {format_timestamp(tab['creation_time'])}")
            if search_term:
                print(f"  Search Term: {search_term}")
            print("-" * 80)
            dictionary_tabs.append({
                'url': url,
                'title': tab['title'],
                'last_accessed': format_timestamp(tab['last_accessed']),
                'creation_time': format_timestamp(tab['creation_time']),
                'search_term': search_term,
            })
    
    # Summary
    print(f"\nFound {len(tabs)} total tabs, {len(dictionary_tabs)} from dictionary sites.")
    
    # Clean up
    import shutil
    shutil.rmtree(profile_path)


if __name__ == "__main__":
    main()