#!/usr/bin/env python3

import os
import re
import glob

def load_sections():
    """Load section names from sections.txt"""
    with open('sections.txt', 'r') as f:
        sections = [line.strip() for line in f if line.strip()]
    return sections

def find_references_in_file(filepath, sections):
    """Find all references to sections in a file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    references = []

    for section in sections:
        # Simple exact match (case sensitive)
        pattern = re.escape(section)

        matches = re.finditer(pattern, content)
        for match in matches:
            # Skip if already converted to cross-reference format
            start_pos = max(0, match.start() - 10)
            end_pos = min(len(content), match.end() + 10)
            context = content[start_pos:end_pos]

            if '<<' not in context and '>>' not in context:
                # Find line number
                line_num = content[:match.start()].count('\n') + 1
                # Get the line content
                lines = content.split('\n')
                line_content = lines[line_num - 1] if line_num <= len(lines) else ""

                # Skip lines that are exactly just the section name (section headers)
                # Also skip lines that don't contain lowercase letters
                if line_content.strip() != section and re.search(r'[a-z]', line_content):
                    references.append((line_num, section, line_content.strip()))

    return references

def main():
    sections = load_sections()
    print(f"Loaded {len(sections)} sections from sections.txt")

    doc_dir = '/Users/bork/clones/git/Documentation'
    all_references = []

    for adoc_file in glob.glob(os.path.join(doc_dir, '*.adoc')):
        try:
            refs = find_references_in_file(adoc_file, sections)
            for line_num, section, line_content in refs:
                all_references.append({
                    'file': os.path.basename(adoc_file),
                    'line': line_num,
                    'section': section,
                    'content': line_content
                })
        except Exception as e:
            print(f"Error processing {adoc_file}: {e}")

    print(f"\nFound {len(all_references)} potential references:")
    for ref in all_references:
        print(f"{ref['file']}:{ref['line']} -> {ref['section']}")
        print(f"    {ref['content']}")
        print()

if __name__ == "__main__":
    main()