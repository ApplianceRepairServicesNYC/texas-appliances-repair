#!/usr/bin/env python3
"""
Texas Appliances Repair - Lead Company Compliance Update
=========================================================
Changes:
1. Replace obfuscated phone with direct click-to-call: 844-578-2997
2. Remove lead form and "Book Online" button
3. Remove "same day" mentions and guarantees
4. Remove "commercial" appliance mentions
"""

import os
import re
from datetime import datetime

# Configuration
SITE_DIR = "/Users/globalaffiliate/Desktop/GitHub-Back-Up-Repo/texas-appliances-repair"
NEW_PHONE = "8445782997"
NEW_PHONE_FORMATTED = "(844) 578-2997"
NEW_PHONE_TEL = "tel:+1" + NEW_PHONE

# Backup directory
BACKUP_DIR = "/Users/globalaffiliate/LeadGen-Strategy/backups"
timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")

def backup_file(filepath):
    """Create backup of file before modifying."""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    filename = os.path.basename(filepath)
    backup_path = os.path.join(BACKUP_DIR, f"texas-{filename}-{timestamp}.bak")
    # Only backup key files, not all 21k
    if filename == "index.html" and "county" not in filepath:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)

def update_html_file(filepath):
    """Apply all updates to a single HTML file."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

    original = content

    # =========================================================================
    # 1. PHONE: Replace obfuscated phone with direct click-to-call
    # =========================================================================

    # Replace the obfuscated phone JS function with direct tel link behavior
    # Old: const digits = [8, 0, 0, 9, 8, 8, 5, 5, 6, 1];
    # New: Direct call on click

    # Replace the setupCallButton function with direct call
    old_phone_pattern = r"const digits = \[[\d, ]+\];\s*const num = digits\.join\(''\);"
    new_phone_code = f"const num = '{NEW_PHONE}';"
    content = re.sub(old_phone_pattern, new_phone_code, content)

    # Replace the click handler to call immediately (no reveal step)
    # Old behavior: first click reveals, second click calls
    # New behavior: single click calls directly
    old_reveal_pattern = r"""btn\.addEventListener\('click', function\(\) \{
                        if \(this\.dataset\.revealed\) return;
                        const digits = \[[\d, ]+\];
                        const num = digits\.join\(''\);
                        const formatted = '\+1 \(' \+ num\.slice\(0,3\) \+ '\) ' \+ num\.slice\(3,6\) \+ '-' \+ num\.slice\(6\);
                        this\.innerHTML = formatted;
                        this\.dataset\.revealed = 'true';
                        this\.onclick = function\(\) \{
                            window\.location\.href = 'tel:\+1' \+ num;
                        \};
                    \}\);"""

    new_click_handler = f"""btn.addEventListener('click', function() {{
                        window.location.href = '{NEW_PHONE_TEL}';
                    }});"""

    content = re.sub(old_reveal_pattern, new_click_handler, content, flags=re.DOTALL)

    # Also handle simpler patterns
    content = re.sub(
        r"const digits = \[8, 0, 0, 9, 8, 8, 5, 5, 6, 1\];",
        f"const num = '{NEW_PHONE}';",
        content
    )

    # Replace any hardcoded phone patterns
    content = re.sub(r'tel:\+?1?8009885561', NEW_PHONE_TEL, content)
    content = re.sub(r'tel:\+?1?800-988-5561', NEW_PHONE_TEL, content)
    content = re.sub(r'\+1 \(800\) 988-5561', NEW_PHONE_FORMATTED, content)
    content = re.sub(r'800-988-5561', NEW_PHONE_FORMATTED, content)
    content = re.sub(r'8009885561', NEW_PHONE, content)

    # Update "Call Toll-Free" buttons to show number directly
    content = re.sub(
        r'>Call Toll-Free</button>',
        f'>Call {NEW_PHONE_FORMATTED}</button>',
        content
    )
    content = re.sub(
        r'>Call Toll-Free</a>',
        f'>Call {NEW_PHONE_FORMATTED}</a>',
        content
    )

    # Make nav call button a direct tel link
    content = re.sub(
        r'<a href="tel:\+18005551234" class="nav-call-btn">Call Now</a>',
        f'<a href="{NEW_PHONE_TEL}" class="nav-call-btn">Call {NEW_PHONE_FORMATTED}</a>',
        content
    )

    # =========================================================================
    # 2. REMOVE LEAD FORM and "Book Online" button
    # =========================================================================

    # Remove the entire form section
    content = re.sub(
        r'<button class="cf-book-button" id="cfBookButton">Book Online</button>',
        '',
        content
    )

    # Remove the contact form section (from opening div to closing div)
    content = re.sub(
        r'<div class="cf-contact-form-section" id="cfContactFormSection">.*?</div>\s*</section>',
        '</section>',
        content,
        flags=re.DOTALL
    )

    # Remove form-related CSS
    content = re.sub(
        r'\.cf-contact-form-section \{[^}]+\}',
        '',
        content
    )
    content = re.sub(
        r'\.cf-contact-form-section\.active \{[^}]+\}',
        '',
        content
    )
    content = re.sub(
        r'\.cf-contact-form \{[^}]+\}',
        '',
        content
    )
    content = re.sub(
        r'\.cf-form-group[^{]*\{[^}]+\}',
        '',
        content
    )
    content = re.sub(
        r'\.cf-form-button[^{]*\{[^}]+\}',
        '',
        content
    )

    # Remove form-related JS
    content = re.sub(
        r"const cfBookButton = document\.getElementById\('cfBookButton'\);.*?cfBookButton\.addEventListener\('click'[^}]+\}\);",
        '',
        content,
        flags=re.DOTALL
    )

    # Remove "Schedule Your Repair Online" text
    content = re.sub(
        r'<div class="cf-schedule-text">Schedule Your Repair Online</div>',
        '',
        content
    )

    # Remove success modal
    content = re.sub(
        r'<div class="cf-modal-overlay" id="cfModalOverlay"></div>',
        '',
        content
    )
    content = re.sub(
        r'<div class="cf-success-modal" id="cfSuccessModal">.*?</div>\s*</div>',
        '',
        content,
        flags=re.DOTALL
    )

    # =========================================================================
    # 3. REMOVE "SAME DAY" MENTIONS AND GUARANTEES
    # =========================================================================

    # Meta descriptions
    content = re.sub(
        r'Same-day service, genuine parts,',
        'Fast service, quality parts,',
        content,
        flags=re.IGNORECASE
    )

    # Keywords meta
    content = re.sub(
        r'same day repair',
        'fast repair',
        content,
        flags=re.IGNORECASE
    )

    # OG descriptions
    content = re.sub(
        r'Same-day repair for',
        'Fast repair for',
        content,
        flags=re.IGNORECASE
    )

    # Hero section
    content = re.sub(
        r'Same-Day Service •',
        'Fast Service •',
        content,
        flags=re.IGNORECASE
    )
    content = re.sub(
        r'• Same-Day Service',
        '• Fast Service',
        content,
        flags=re.IGNORECASE
    )

    # Body text variations
    content = re.sub(
        r'same-day service available',
        'fast service available',
        content,
        flags=re.IGNORECASE
    )
    content = re.sub(
        r'Same-Day Service Available',
        'Fast Service Available',
        content,
        flags=re.IGNORECASE
    )
    content = re.sub(
        r'same-day appliance repair',
        'fast appliance repair',
        content,
        flags=re.IGNORECASE
    )
    content = re.sub(
        r', same-day',
        ', fast',
        content,
        flags=re.IGNORECASE
    )
    content = re.sub(
        r'same day service',
        'fast service',
        content,
        flags=re.IGNORECASE
    )

    # Footer mentions
    content = re.sub(
        r'Same-day service available across Texas!',
        'Fast service available across Texas!',
        content,
        flags=re.IGNORECASE
    )

    # Remove guarantee mentions
    content = re.sub(
        r'<span><strong>Repair Warranty:</strong> All repairs include our service guarantee\. If issues recur, we return at no additional cost\.</span>',
        '<span><strong>Repair Warranty:</strong> All repairs include a service warranty.</span>',
        content
    )
    content = re.sub(
        r'<span><strong>Clean Work Guarantee:</strong> Technicians protect your floors and clean up completely after every repair\.</span>',
        '<span><strong>Clean Workspace:</strong> Technicians protect your floors and clean up after every repair.</span>',
        content
    )
    content = re.sub(
        r'service guarantee',
        'service warranty',
        content,
        flags=re.IGNORECASE
    )
    content = re.sub(
        r'satisfaction guarantee',
        'quality service',
        content,
        flags=re.IGNORECASE
    )

    # =========================================================================
    # 4. REMOVE "COMMERCIAL" APPLIANCE MENTIONS
    # =========================================================================

    # Replace specific commercial mentions
    content = re.sub(
        r'<li>Commercial & Multi-Unit Appliance Services</li>',
        '<li>Residential Appliance Services</li>',
        content
    )
    content = re.sub(
        r'<li>Commercial Washers</li>',
        '<li>High-Capacity Washers</li>',
        content
    )
    content = re.sub(
        r'<li>Commercial Dryers</li>',
        '<li>High-Capacity Dryers</li>',
        content
    )
    content = re.sub(
        r'<li>Residential & Commercial</li>',
        '<li>All Residential Models</li>',
        content
    )
    content = re.sub(
        r'<li>Commercial Microwaves</li>',
        '<li>Built-In Microwaves</li>',
        content
    )
    content = re.sub(
        r'<li>Commercial Ventilation</li>',
        '<li>Kitchen Ventilation</li>',
        content
    )
    content = re.sub(
        r'<li>Commercial Refrigerators</li>',
        '<li>Large Capacity Refrigerators</li>',
        content
    )
    content = re.sub(
        r'<li>Commercial Ovens</li>',
        '<li>Double Ovens</li>',
        content
    )
    content = re.sub(
        r'<li>Commercial Dishwashers</li>',
        '<li>Built-In Dishwashers</li>',
        content
    )
    content = re.sub(
        r'<li>Commercial Cooktops</li>',
        '<li>Professional Cooktops</li>',
        content
    )
    content = re.sub(
        r'<li>Commercial Freezers</li>',
        '<li>Upright Freezers</li>',
        content
    )

    # Generic commercial mentions in text
    content = re.sub(
        r'commercial and residential',
        'residential',
        content,
        flags=re.IGNORECASE
    )
    content = re.sub(
        r'residential and commercial',
        'residential',
        content,
        flags=re.IGNORECASE
    )
    content = re.sub(
        r'commercial appliances',
        'home appliances',
        content,
        flags=re.IGNORECASE
    )
    content = re.sub(
        r'commercial-grade',
        'professional-grade',
        content,
        flags=re.IGNORECASE
    )

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
    print("=" * 60)
    print("Texas Appliances Repair - Lead Company Compliance Update")
    print("=" * 60)
    print(f"\nNew phone: {NEW_PHONE_FORMATTED}")
    print("Changes:")
    print("  1. Direct click-to-call (no obfuscation)")
    print("  2. Remove lead form")
    print("  3. Remove 'same day' mentions")
    print("  4. Remove 'guarantee' mentions")
    print("  5. Remove 'commercial' mentions")
    print()

    # Find all HTML files
    html_files = []
    for root, dirs, files in os.walk(SITE_DIR):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))

    print(f"Found {len(html_files)} HTML files")
    print("Processing...")

    updated = 0
    for i, filepath in enumerate(html_files):
        if i % 500 == 0:
            print(f"  Progress: {i}/{len(html_files)} ({round(i/len(html_files)*100)}%)")

        # Backup homepage
        backup_file(filepath)

        if update_html_file(filepath):
            updated += 1

    print(f"\nComplete!")
    print(f"  Files processed: {len(html_files)}")
    print(f"  Files updated: {updated}")
    print(f"\nBackup saved to: {BACKUP_DIR}")

if __name__ == "__main__":
    main()
