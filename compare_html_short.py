#!/usr/bin/env python3
# /// script
# dependencies = ["beautifulsoup4"]
# ///

import os
import re
from bs4 import BeautifulSoup
from pathlib import Path

def extract_text(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    text = soup.get_text()
    text = re.sub(r'Last updated \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} [+-]\d{4}', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def main():
    os.chdir("Documentation")
    master_html_dir = "/tmp/master-man-pages"
    current_html_files = list(Path(".").glob("*.html"))

    for html_file in current_html_files:
        master_file = Path(master_html_dir) / html_file.name
        master_text = extract_text(master_file)
        current_text = extract_text(html_file)
        if master_text != current_text:
            print("Changed: ", html_file.name)

    else:
        print("No changes.")

if __name__ == "__main__":
    main()
