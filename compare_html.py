#!/usr/bin/env python3
# /// script
# dependencies = ["beautifulsoup4"]
# ///

import os
import subprocess
import difflib
from bs4 import BeautifulSoup
from pathlib import Path

def extract_text_from_html(html_file):
    """Extract text content from HTML file"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            text = soup.get_text()

            # Just filter out timestamp and normalize whitespace
            import re
            text = re.sub(r'Last updated \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} [+-]\d{4}', '', text)
            text = re.sub(r'\s+', ' ', text).strip()
            return text
    except Exception as e:
        print(f"Error reading {html_file}: {e}")
        return ""

def show_word_diff(master_text, current_text, filename):
    """Show a word-level diff of the changes"""
    master_words = master_text.split()
    current_words = current_text.split()

    # Create a word-level diff
    matcher = difflib.SequenceMatcher(None, master_words, current_words)

    print(f"Word-level changes in {filename}:")

    changes_found = False
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'delete':
            changes_found = True
            print(f"  - REMOVED: {' '.join(master_words[i1:i2])}")
        elif tag == 'insert':
            changes_found = True
            print(f"  + ADDED: {' '.join(current_words[j1:j2])}")
        elif tag == 'replace':
            changes_found = True
            print(f"  - CHANGED FROM: {' '.join(master_words[i1:i2])}")
            print(f"  + CHANGED TO: {' '.join(current_words[j1:j2])}")

    if not changes_found:
        print("  (No significant word-level changes detected)")

    # Also show context around changes
    print(f"\nContext view:")
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag != 'equal':
            # Show some context words around the change
            start_context = max(0, i1 - 5)
            end_context = min(len(master_words), i2 + 5)
            context_before = ' '.join(master_words[start_context:i1])
            changed_words = ' '.join(master_words[i1:i2])
            context_after = ' '.join(master_words[i2:end_context])

            print(f"  Context: ...{context_before} [REMOVED: {changed_words}] {context_after}...")

            # Show the new version
            new_start_context = max(0, j1 - 5)
            new_end_context = min(len(current_words), j2 + 5)
            new_context_before = ' '.join(current_words[new_start_context:j1])
            new_changed_words = ' '.join(current_words[j1:j2])
            new_context_after = ' '.join(current_words[j2:new_end_context])

            print(f"           ...{new_context_before} [ADDED: {new_changed_words}] {new_context_after}...")
            print()

def main():
    # Build HTML on current branch
    print("Building HTML documentation on current branch...")
    os.chdir("Documentation")

    master_html_dir = "/tmp/master-man-pages"
    current_html_files = list(Path(".").glob("*.html"))

    changed_files = []

    for html_file in current_html_files:
        master_file = Path(master_html_dir) / html_file.name

        if master_file.exists():
            master_text = extract_text_from_html(master_file)
            current_text = extract_text_from_html(html_file)

            if master_text != current_text:
                changed_files.append(str(html_file.name))
                print(f"\n🔄 CHANGED: {html_file.name}")
                print("-" * 80)
                show_word_diff(master_text, current_text, html_file.name)
                print("-" * 80)
        else:
            changed_files.append(str(html_file.name))
            print(f"✨ NEW: {html_file.name}")

    # Check for deleted files
    if Path(master_html_dir).exists():
        master_files = list(Path(master_html_dir).glob("*.html"))
        for master_file in master_files:
            current_file = Path(master_file.name)
            if not current_file.exists():
                print(f"🗑️  DELETED: {master_file.name}")

    print(f"\n📊 Summary: {len(changed_files)} files changed")

if __name__ == "__main__":
    main()
