#!/usr/bin/env python3
"""
Browser Tab Reader for gist-dictionary

This script reads Firefox's existing tabs, sorts them by their actual tab order,
retrieves their creation/visiting time, and identifies tabs from dictionary sites.
"""

import os
import sys
import json
import sqlite3
import argparse
import datetime
from pathlib import Path
from urllib.parse import urlparse, parse_qs


def find_firefox_profiles():
    """Find Firefox profiles on the system."""
    possible_locations = [
        # Linux
        Path.home() / ".mozilla/firefox",
        # macOS
        Path.home() / "Library/Application Support/Firefox/Profiles",
        # Windows
        Path.home() / "AppData/Roaming/Mozilla/Firefox/Profiles",
    ]
    
    profiles = []
    for location in possible_locations:
        if location.exists():
            # Look for all profile directories, not just default ones
            for profile_dir in location.glob("*"):
                if profile_dir.is_dir():
                    # Check if this looks like a Firefox profile (has places.sqlite or sessionstore files)
                    has_places = (profile_dir / "places.sqlite").exists()
                    has_session = any([
                        (profile_dir / "sessionstore.js").exists(),
                        (profile_dir / "sessionstore-backups").exists()
                    ])
                    
                    if has_places or has_session:
                        profiles.append(profile_dir)
    
    return profiles


def get_firefox_tabs(profile_path):
    """
    Get Firefox tabs from session files.
    
    Tries multiple session file formats and locations.
    """
    # List of possible session files to try
    session_files = [
        # Regular session files
        Path(profile_path) / "sessionstore.js",
        Path(profile_path) / "sessionstore.json",
        
        # Backup session files
        Path(profile_path) / "sessionstore-backups" / "recovery.js",
        Path(profile_path) / "sessionstore-backups" / "recovery.json",
        Path(profile_path) / "sessionstore-backups" / "previous.js",
        Path(profile_path) / "sessionstore-backups" / "previous.json",
        Path(profile_path) / "sessionstore-backups" / "upgrade.js",
        Path(profile_path) / "sessionstore-backups" / "upgrade.json",
        
        # Older Firefox versions
        Path(profile_path) / "sessionstore.bak",
        Path(profile_path) / "session.js",
    ]
    
    # Try to read each session file
    for session_file in session_files:
        if session_file.exists():
            print(f"Found session file: {session_file}")
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                    tabs = parse_firefox_session(session_data)
                    if tabs:
                        return tabs
                    print(f"No tabs found in {session_file}")
            except (json.JSONDecodeError, UnicodeDecodeError, IOError) as e:
                print(f"Error reading {session_file}: {e}")
    
    # Try to handle compressed lz4 files if available
    try:
        import lz4.block
        
        lz4_files = [
            Path(profile_path) / "sessionstore.jsonlz4",
            Path(profile_path) / "sessionstore-backups" / "recovery.jsonlz4",
            Path(profile_path) / "sessionstore-backups" / "previous.jsonlz4",
        ]
        
        for lz4_file in lz4_files:
            if lz4_file.exists():
                print(f"Found compressed session file: {lz4_file}")
                try:
                    with open(lz4_file, 'rb') as f:
                        # Skip the first 8 bytes (Mozilla LZ4 header)
                        f.seek(8)
                        compressed_data = f.read()
                        decompressed = lz4.block.decompress(compressed_data)
                        session_data = json.loads(decompressed.decode('utf-8'))
                        tabs = parse_firefox_session(session_data)
                        if tabs:
                            return tabs
                        print(f"No tabs found in {lz4_file}")
                except Exception as e:
                    print(f"Error reading compressed file {lz4_file}: {e}")
    except ImportError:
        print("lz4 module not available. Cannot read compressed session files.")
    
    print("Could not find or read any Firefox session files.")
    print("Firefox may be currently running with all windows in private browsing mode,")
    print("or the profile directory may not contain any saved sessions.")
    return []


def parse_firefox_session(session_data):
    """Parse Firefox session data to extract tabs."""
    tabs = []
    
    # Process each window
    for window_idx, window in enumerate(session_data.get('windows', [])):
        # Process each tab in the window
        for tab_idx, tab in enumerate(window.get('tabs', [])):
            # Get the active entry (current state of the tab)
            entries = tab.get('entries', [])
            if not entries:
                continue
            
            # Get the last (current) entry
            entry = entries[-1]
            
            # Extract tab information
            tab_info = {
                'window_index': window_idx,
                'tab_index': tab_idx,
                'url': entry.get('url', ''),
                'title': entry.get('title', ''),
                'last_accessed': tab.get('lastAccessed', 0),
                'creation_time': tab.get('createTime', 0),
            }
            
            tabs.append(tab_info)
    
    # Sort tabs by window index and tab index to maintain the actual tab order
    tabs.sort(key=lambda x: (x['window_index'], x['tab_index']))
    
    return tabs


def get_tab_history(profile_path):
    """Get tab history from places.sqlite database."""
    places_db = Path(profile_path) / "places.sqlite"
    if not places_db.exists():
        print(f"Places database not found at {places_db}")
        return {}
    
    # Create a copy of the database to avoid locking issues
    temp_db = Path(profile_path) / "places_temp.sqlite"
    try:
        import shutil
        shutil.copy2(places_db, temp_db)
        
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        # Query to get visit time for URLs
        cursor.execute("""
            SELECT url, MAX(visit_date) as last_visit
            FROM moz_places JOIN moz_historyvisits ON moz_places.id = moz_historyvisits.place_id
            GROUP BY url
        """)
        
        url_history = {}
        for url, visit_date in cursor.fetchall():
            # Convert from microseconds to milliseconds
            url_history[url] = visit_date // 1000
        
        conn.close()
        return url_history
    
    except Exception as e:
        print(f"Error accessing places database: {e}")
        return {}
    finally:
        # Clean up the temporary file
        if temp_db.exists():
            try:
                os.remove(temp_db)
            except:
                pass


def is_dictionary_site(url, dictionary_sites):
    """Check if the URL is from a dictionary site."""
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    
    # Remove 'www.' prefix if present
    if domain.startswith('www.'):
        domain = domain[4:]
    
    # Check if the domain matches any dictionary site
    for dict_site in dictionary_sites:
        dict_site = dict_site.strip().lower()
        if dict_site in domain:
            return True
    
    return False


def extract_search_term(url):
    """Extract search term from dictionary URL."""
    parsed_url = urlparse(url)
    path = parsed_url.path
    query = parse_qs(parsed_url.query)
    
    # Common patterns for dictionary sites
    # Example: dictionary.com/browse/word
    if '/browse/' in path or '/definition/' in path:
        parts = path.split('/')
        for part in parts:
            if part and part not in ['browse', 'definition', 'meaning']:
                return part
    
    # Example: merriam-webster.com/dictionary/word
    if '/dictionary/' in path:
        parts = path.split('/dictionary/')
        if len(parts) > 1 and parts[1]:
            return parts[1].split('/')[0]
    
    # Example: vocabulary.com/dictionary/word
    if '/dictionary/' in path:
        parts = path.split('/dictionary/')
        if len(parts) > 1 and parts[1]:
            return parts[1].split('/')[0]
    
    # Example: thefreedictionary.com/word
    domain = parsed_url.netloc.lower()
    if 'thefreedictionary.com' in domain:
        parts = path.split('/')
        if len(parts) > 1 and parts[1]:
            return parts[1]
    
    # Example: dictionary.cambridge.org/dictionary/english/word
    if '/dictionary/' in path:
        parts = path.split('/dictionary/')
        if len(parts) > 1:
            subparts = parts[1].split('/')
            if len(subparts) > 1:
                return subparts[-1]
    
    # Check query parameters (q, query, word, term, etc.)
    for param in ['q', 'query', 'word', 'term', 'search']:
        if param in query and query[param]:
            return query[param][0]
    
    return None


def format_timestamp(timestamp_ms):
    """Format timestamp in milliseconds to a readable date/time."""
    if not timestamp_ms:
        return "Unknown"
    
    # Convert milliseconds to seconds
    timestamp_sec = timestamp_ms / 1000
    dt = datetime.datetime.fromtimestamp(timestamp_sec)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def main():
    parser = argparse.ArgumentParser(description="Read Firefox tabs and identify dictionary sites")
    parser.add_argument("--profile-path", help="Path to Firefox profile directory")
    parser.add_argument("--dict-sites-file", help="File containing dictionary site domains, one per line")
    parser.add_argument("--output", help="Output file for dictionary tabs (default: stdout)")
    args = parser.parse_args()
    
    # Find Firefox profiles if not specified
    profile_path = args.profile_path
    if not profile_path:
        profiles = find_firefox_profiles()
        if not profiles:
            print("No Firefox profiles found. Please specify a profile path.")
            sys.exit(1)
        
        if len(profiles) == 1:
            profile_path = profiles[0]
            print(f"Using Firefox profile: {profile_path}")
        else:
            print("Multiple Firefox profiles found:")
            for i, profile in enumerate(profiles, 1):
                print(f"{i}. {profile}")
            
            try:
                choice = input("Enter profile number to use (or press Enter for first profile): ")
                if choice.strip():
                    profile_idx = int(choice) - 1
                    if 0 <= profile_idx < len(profiles):
                        profile_path = profiles[profile_idx]
                    else:
                        print(f"Invalid choice. Using first profile.")
                        profile_path = profiles[0]
                else:
                    profile_path = profiles[0]
            except ValueError:
                print("Invalid input. Using first profile.")
                profile_path = profiles[0]
            
            print(f"Using Firefox profile: {profile_path}")
    
    # Load dictionary sites
    dictionary_sites = []
    if args.dict_sites_file:
        try:
            with open(args.dict_sites_file, 'r', encoding='utf-8') as f:
                dictionary_sites = [line.strip() for line in f if line.strip()]
        except IOError as e:
            print(f"Error reading dictionary sites file: {e}")
            sys.exit(1)
    else:
        # Default dictionary sites
        dictionary_sites = [
            "dictionary.com",
            "merriam-webster.com",
            "vocabulary.com",
            "thefreedictionary.com",
            "dictionary.cambridge.org",
            "oxforddictionaries.com",
            "collinsdictionary.com",
            "macmillandictionary.com",
            "ldoceonline.com",  # Longman
            "lexico.com",
            "etymonline.com",
            "wordreference.com",
            "urbandictionary.com",
            "wiktionary.org",
            "thesaurus.com",
        ]
    
    # Get tabs and history
    tabs = get_firefox_tabs(profile_path)
    url_history = get_tab_history(profile_path)
    
    # Process tabs
    dictionary_tabs = []
    for tab in tabs:
        url = tab['url']
        
        # Update access time from history if available
        if url in url_history and not tab['last_accessed']:
            tab['last_accessed'] = url_history[url]
        
        # Check if it's a dictionary site
        if is_dictionary_site(url, dictionary_sites):
            search_term = extract_search_term(url)
            dictionary_tabs.append({
                'url': url,
                'title': tab['title'],
                'last_accessed': format_timestamp(tab['last_accessed']),
                'creation_time': format_timestamp(tab['creation_time']),
                'search_term': search_term,
            })
    
    # Output results
    output_file = args.output
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(dictionary_tabs, f, indent=2)
        print(f"Dictionary tabs saved to {output_file}")
    else:
        print("\nDictionary Tabs:")
        print("=" * 80)
        for i, tab in enumerate(dictionary_tabs, 1):
            print(f"{i}. {tab['title']}")
            print(f"   URL: {tab['url']}")
            print(f"   Last Accessed: {tab['last_accessed']}")
            print(f"   Creation Time: {tab['creation_time']}")
            if tab['search_term']:
                print(f"   Search Term: {tab['search_term']}")
            print("-" * 80)
    
    # Summary
    print(f"\nFound {len(tabs)} total tabs, {len(dictionary_tabs)} from dictionary sites.")


if __name__ == "__main__":
    main()