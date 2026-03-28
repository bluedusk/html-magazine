#!/usr/bin/env python3
"""
Export an HTML magazine to PDF.

Uses Playwright to render each page of the magazine and combine them into
a single PDF with proper page dimensions matching the magazine layout.

Usage:
    python3 export-pdf.py magazine.html
    python3 export-pdf.py magazine.html --output my-magazine.pdf
    python3 export-pdf.py magazine.html --width 210 --height 297  # A4 in mm

Requirements:
    pip install playwright
    playwright install chromium
"""

import argparse
import sys
import os
from pathlib import Path


def check_dependencies():
    try:
        from playwright.sync_api import sync_playwright
        return True
    except ImportError:
        print("Error: playwright is not installed.")
        print()
        print("Install it with:")
        print("  pip install playwright")
        print("  playwright install chromium")
        sys.exit(1)


def export_pdf(html_path, output_path=None, width_mm=210, height_mm=297):
    from playwright.sync_api import sync_playwright

    html_path = Path(html_path).resolve()
    if not html_path.exists():
        print(f"Error: {html_path} not found")
        sys.exit(1)

    if output_path is None:
        output_path = html_path.with_suffix('.pdf')
    else:
        output_path = Path(output_path).resolve()

    print(f"  Source:  {html_path}")
    print(f"  Output:  {output_path}")
    print(f"  Size:    {width_mm}x{height_mm}mm")
    print()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": 1400, "height": 900}
        )

        # Load the magazine
        page.goto(f"file://{html_path}")
        page.wait_for_load_state("networkidle")

        # Get total page count from the magazine's JS
        total_pages = page.evaluate("""
            () => document.querySelectorAll('.page, [data-page]').length || 1
        """)

        print(f"  Found {total_pages} magazine pages")

        # Switch to single-page mode for clean captures
        page.evaluate("""
            () => {
                const surface = document.querySelector('.magazine-surface');
                if (surface) {
                    surface.classList.remove('spread-mode');
                    surface.classList.add('single-mode');
                }
                // Hide navigation UI
                document.querySelectorAll('.nav-btn, .page-indicator, .view-toggle').forEach(
                    el => el.style.display = 'none'
                );
                // Hide the dark surface background
                if (surface) surface.style.background = 'white';
            }
        """)

        # Capture each page as a separate PDF, then we'll note them
        pdf_pages = []

        for i in range(total_pages):
            # Navigate to this page
            page.evaluate(f"""
                () => {{
                    const pages = document.querySelectorAll('.page, [data-page]');
                    pages.forEach(p => {{
                        p.classList.remove('active', 'active-left', 'active-right');
                        p.style.position = 'absolute';
                        p.style.opacity = '0';
                        p.style.pointerEvents = 'none';
                    }});
                    if (pages[{i}]) {{
                        pages[{i}].classList.add('active');
                        pages[{i}].style.position = 'relative';
                        pages[{i}].style.opacity = '1';
                        pages[{i}].style.pointerEvents = 'auto';
                    }}
                }}
            """)

            page.wait_for_timeout(300)  # Let transitions settle

            temp_pdf = str(output_path.with_suffix(f'.page{i}.pdf'))
            page.pdf(
                path=temp_pdf,
                width=f"{width_mm}mm",
                height=f"{height_mm}mm",
                print_background=True,
                margin={"top": "0", "right": "0", "bottom": "0", "left": "0"}
            )
            pdf_pages.append(temp_pdf)
            print(f"  Exported page {i + 1}/{total_pages}")

        browser.close()

    # Merge PDFs
    try:
        from pypdf import PdfMerger
        merger = PdfMerger()
        for pdf_file in pdf_pages:
            merger.append(pdf_file)
        merger.write(str(output_path))
        merger.close()
        # Clean up temp files
        for pdf_file in pdf_pages:
            os.remove(pdf_file)
        print(f"\n  ✓ PDF saved to {output_path}")
    except ImportError:
        # pypdf not available — just keep individual pages
        if len(pdf_pages) == 1:
            os.rename(pdf_pages[0], str(output_path))
            print(f"\n  ✓ PDF saved to {output_path}")
        else:
            print(f"\n  ⚠ pypdf not installed — could not merge pages into one PDF.")
            print(f"  Individual page PDFs saved as {output_path.stem}.page0.pdf, etc.")
            print(f"  To merge: pip install pypdf")


def main():
    parser = argparse.ArgumentParser(
        description="Export HTML magazine to PDF"
    )
    parser.add_argument("html_file", help="Path to the magazine HTML file")
    parser.add_argument("--output", "-o", help="Output PDF path (default: same name as input with .pdf)")
    parser.add_argument("--width", type=int, default=210, help="Page width in mm (default: 210 = A4)")
    parser.add_argument("--height", type=int, default=297, help="Page height in mm (default: 297 = A4)")

    args = parser.parse_args()

    check_dependencies()

    print()
    print("  HTML Magazine → PDF Export")
    print("  ==========================")
    print()

    export_pdf(args.html_file, args.output, args.width, args.height)


if __name__ == "__main__":
    main()
