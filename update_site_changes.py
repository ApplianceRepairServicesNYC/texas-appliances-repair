#!/usr/bin/env python3
"""
Update Texas Appliances Repair site:
1. Replace "Commercial" with "Residential"
2. Remove contact form section (cf-schedule-container)
"""

import os
import re

BASE_DIR = "/Users/globalaffiliate/Desktop/GitHub-Back-Up-Repo/texas-appliances-repair"

def remove_section_by_id(content, section_id):
    """Remove a section element by its id, handling nested sections properly."""
    start_tag = f'<section id="{section_id}">'
    start_idx = content.find(start_tag)

    if start_idx == -1:
        return content

    # Find the matching closing tag by counting section depth
    search_content = content[start_idx:]
    depth = 0
    i = 0
    while i < len(search_content):
        if search_content[i:i+8] == '<section':
            depth += 1
            i += 8
        elif search_content[i:i+10] == '</section>':
            depth -= 1
            if depth == 0:
                end_idx = start_idx + i + 10
                # Remove the section and any trailing whitespace
                return content[:start_idx] + content[end_idx:].lstrip('\n\r\t ')
            i += 10
        else:
            i += 1

    return content

def remove_div_by_id(content, div_id):
    """Remove a div element by its id."""
    # Pattern for self-contained div
    pattern = rf'<div[^>]*id="{div_id}"[^>]*>.*?</div>'
    content = re.sub(pattern, '', content, flags=re.DOTALL)
    return content

def remove_modal_elements(content):
    """Remove modal overlay and success modal divs."""
    # Remove modal overlay
    content = re.sub(r'<div class="cf-modal-overlay" id="cfModalOverlay"></div>\s*', '', content)

    # Remove success modal (has nested div)
    pattern = r'<div class="cf-success-modal" id="cfSuccessModal">.*?</div>\s*</div>'
    content = re.sub(pattern, '', content, flags=re.DOTALL)

    return content

def update_file(filepath):
    """Update a single HTML file with all required changes."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

    original = content

    # 1. Replace "Commercial" with "Residential"
    content = content.replace("Commercial & Multi-Unit Appliance Services", "Residential Appliance Services")
    content = content.replace("Commercial Washers", "Residential Washers")
    content = content.replace("Residential & Commercial", "Residential")
    content = content.replace("Commercial Microwaves", "Residential Microwaves")
    content = content.replace("Commercial Ventilation", "Residential Ventilation")
    content = content.replace("Commercial", "Residential")
    content = content.replace("commercial", "residential")

    # 2. Remove the cf-schedule-container section (contains the contact form)
    content = remove_section_by_id(content, "cf-schedule-container")

    # 3. Remove modal elements
    content = remove_modal_elements(content)

    # Only write if changes were made
    if content != original:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error writing {filepath}: {e}")
            return False
    return False

def main():
    print("Starting Texas Appliances Repair site update...")
    print("Changes:")
    print("  1. Replace Commercial -> Residential")
    print("  2. Remove contact form section")
    print()

    updated = 0
    total = 0

    for root, dirs, files in os.walk(BASE_DIR):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for filename in files:
            if filename.endswith('.html'):
                filepath = os.path.join(root, filename)
                total += 1

                if update_file(filepath):
                    updated += 1
                    if updated % 500 == 0:
                        print(f"  Updated {updated} files...")

    print()
    print(f"Complete!")
    print(f"  Total HTML files: {total}")
    print(f"  Files updated: {updated}")

if __name__ == "__main__":
    main()
