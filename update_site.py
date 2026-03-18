#!/usr/bin/env python3
"""
Update Texas Appliances Repair site:
1. Replace phone number with new lead company number
2. Remove phone obfuscation - direct click to call
3. Remove lead form
4. Remove same-day mentions and guarantees
5. Remove commercial appliance mentions
"""

import os
import re
from pathlib import Path

# New phone number
NEW_PHONE = '8882776542'
NEW_PHONE_FORMATTED = '(888) 277-6542'

def update_html(content):
    """Apply all updates to HTML content."""

    # 1. Replace old phone number with new one (various formats)
    content = content.replace('8445782997', NEW_PHONE)
    content = content.replace('844-578-2997', '888-277-6542')
    content = content.replace('(844) 578-2997', NEW_PHONE_FORMATTED)
    content = content.replace('+1 (844) 578-2997', '+1 ' + NEW_PHONE_FORMATTED)

    # 2. Remove phone obfuscation - replace click-to-reveal with direct call
    # Update nav button to direct tel link
    content = re.sub(
        r'<button class="nav-call-btn" id="navCallNow">Call \([^)]+\) [0-9-]+</button>',
        f'<a href="tel:+1{NEW_PHONE}" class="nav-call-btn">Call {NEW_PHONE_FORMATTED}</a>',
        content
    )

    # Update form call button
    content = re.sub(
        r'<button class="form-call-now" id="formCallNow">Call \([^)]+\) [0-9-]+</button>',
        f'<a href="tel:+1{NEW_PHONE}" class="form-call-now" style="display:inline-block;text-decoration:none;text-align:center;">Call {NEW_PHONE_FORMATTED}</a>',
        content
    )

    # Remove the obfuscation JavaScript function
    obfuscation_pattern = r'''function setupCallButton\(btn\) \{[^}]+if \(btn\) \{[^}]+btn\.addEventListener\('click', function\(\) \{[^}]+if \(this\.dataset\.revealed\) return;[^}]+const num = '[0-9]+';[^}]+const formatted = '\+1 \(' \+ num\.slice\(0,3\) \+ '\) ' \+ num\.slice\(3,6\) \+ '-' \+ num\.slice\(6\);[^}]+this\.innerHTML = formatted;[^}]+this\.dataset\.revealed = 'true';[^}]+this\.onclick = function\(\) \{[^}]+window\.location\.href = 'tel:\+1' \+ num;[^}]+\};[^}]+\}\);[^}]+\}[^}]+\}'''
    content = re.sub(obfuscation_pattern, '// Phone obfuscation removed - direct tel links', content, flags=re.DOTALL)

    # Simpler approach - just remove the setupCallButton calls
    content = re.sub(r"setupCallButton\(document\.getElementById\('[^']+'\)\);?\s*", '', content)

    # 3. Remove Same-Day mentions
    content = re.sub(
        r'<li style="padding: 12px 0;[^>]*>\s*<span style="color: var\(--red\)[^>]*>.*?</span>\s*<span><strong>Same-Day[^<]*</strong>[^<]*</span>\s*</li>',
        '',
        content,
        flags=re.DOTALL
    )
    content = content.replace('Same-Day Repair Solutions', 'Fast Repair Solutions')
    content = content.replace('same-day', 'fast')
    content = content.replace('Same-Day', 'Fast')
    content = content.replace('same day', 'fast')
    content = content.replace('Same Day', 'Fast')

    # 4. Remove guarantee mentions
    content = re.sub(
        r'<li style="padding: 12px 0;[^>]*>\s*<span style="color: var\(--red\)[^>]*>.*?</span>\s*<span><strong>Best Price Guarantee:</strong>[^<]*</span>\s*</li>',
        '',
        content,
        flags=re.DOTALL
    )
    content = re.sub(
        r'<li style="padding: 12px 0;[^>]*>\s*<span style="color: var\(--red\)[^>]*>.*?</span>\s*<span><strong>Money Back Guarantee:</strong>[^<]*</span>\s*</li>',
        '',
        content,
        flags=re.DOTALL
    )
    # Remove inline guarantee mentions
    content = re.sub(r',?\s*we guarantee swift response times', ', we provide fast response times', content, flags=re.IGNORECASE)
    content = re.sub(r'guarantee[ds]?\s+', '', content, flags=re.IGNORECASE)

    # 5. Remove Commercial appliance sections
    # Remove Commercial Washer Repair section
    content = re.sub(
        r'<h4 style="color: var\(--blue\); margin: 15px 0 10px;">Commercial Washer Repair</h4>\s*<p style="margin-bottom: 12px;"><strong>commercial washer repair</strong>.*?</p>',
        '',
        content,
        flags=re.DOTALL
    )
    # Remove Commercial Dryer Repair section
    content = re.sub(
        r'<h4 style="color: var\(--blue\); margin: 15px 0 10px;">Commercial Dryer Repair</h4>\s*<p style="margin-bottom: 12px;"><strong>commercial dryer repair</strong>.*?</p>',
        '',
        content,
        flags=re.DOTALL
    )
    # Remove Commercial Microwave Repair section
    content = re.sub(
        r'<h4 style="color: var\(--blue\); margin: 15px 0 10px;">Commercial Microwave Repair</h4>\s*<p style="margin-bottom: 12px;"><strong>commercial microwave repair</strong>.*?</p>',
        '',
        content,
        flags=re.DOTALL
    )
    # Remove Commercial Ventilation Repair section
    content = re.sub(
        r'<h4 style="color: var\(--blue\); margin: 15px 0 10px;">Commercial Ventilation Repair</h4>\s*<p style="margin-bottom: 12px;"><strong>commercial ventilation repair</strong>.*?</p>',
        '',
        content,
        flags=re.DOTALL
    )
    # Remove any remaining "commercial" mentions in appliance context
    content = re.sub(r'commercial appliances?', 'household appliances', content, flags=re.IGNORECASE)
    content = re.sub(r'commercial-grade', 'professional-grade', content, flags=re.IGNORECASE)
    content = re.sub(r'commercial units?', 'large-capacity units', content, flags=re.IGNORECASE)

    # 6. Remove lead form section (the cf-schedule-container is now just a call button)
    # The section currently has just the call button, so we keep that but ensure it's a direct link

    # Remove the hero button that scrolls to form - change to direct call
    content = re.sub(
        r'<button class="btn" id="heroCallNow">Request Service Today</button>',
        f'<a href="tel:+1{NEW_PHONE}" class="btn">Call Now: {NEW_PHONE_FORMATTED}</a>',
        content
    )

    # Remove the JS that scrolls to form on hero click
    content = re.sub(
        r"const heroCallNow = document\.getElementById\('heroCallNow'\);.*?if \(heroCallNow\) \{.*?\}\);.*?\}",
        '',
        content,
        flags=re.DOTALL
    )

    return content

def main():
    base_dir = Path('/Users/globalaffiliate/Desktop/GitHub-Back-Up-Repo/texas-appliances-repair')

    # Find all HTML files
    html_files = list(base_dir.rglob('*.html'))
    total = len(html_files)

    print(f"Found {total} HTML files to update...")

    updated = 0
    errors = 0

    for i, html_file in enumerate(html_files, 1):
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()

            new_content = update_html(content)

            if new_content != content:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updated += 1

            if i % 1000 == 0:
                print(f"Processed {i}/{total} files... ({updated} updated)")

        except Exception as e:
            errors += 1
            print(f"Error processing {html_file}: {e}")

    print(f"\nComplete!")
    print(f"Total files: {total}")
    print(f"Updated: {updated}")
    print(f"Errors: {errors}")

if __name__ == "__main__":
    main()
