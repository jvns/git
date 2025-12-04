#!/usr/bin/env python3

import os
import re
import glob

def find_section_headings(content):
    """Find all section headings in the format 'HEADING\n--------'"""
    # Pattern for section headings: word(s) followed by line of dashes
    pattern = r'^([A-Z][A-Z\s\-_]+)\n-{4,}$'
    matches = re.findall(pattern, content, re.MULTILINE)
    return [match.strip() for match in matches]

def main():
    doc_dir = '/Users/bork/clones/git/Documentation'
    all_sections = set()

    for adoc_file in glob.glob(os.path.join(doc_dir, '*.adoc')):
        try:
            with open(adoc_file, 'r', encoding='utf-8') as f:
                content = f.read()
                sections = find_section_headings(content)
                all_sections.update(sections)
        except Exception as e:
            print(f"Error reading {adoc_file}: {e}")

    print("All section headings found:")
    for section in sorted(all_sections):
        print(section)

if __name__ == "__main__":
    main()