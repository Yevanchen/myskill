---
name: business-card-generator
description: Generate pixel-perfect Dify-branded business cards in SVG format using a template-based approach. Use when users request business cards for Dify team members, need to create professional cards with consistent branding, or want to generate cards with name, title, email, phone, and company information. Handles automatic email highlighting (dify.ai domain) and vertical URL text.
---

# Business Card Generator

## Overview

Generate professional Dify-branded business cards using a template-based SVG approach. This skill provides a Python script that preserves the exact visual design (white background, Dify logo, shadow effects) while allowing easy customization of contact information.

## Quick Start

Generate a business card by running the script with customized contact information:

```python
# Edit the CARD_INFO dictionary in scripts/generate_card.py
CARD_INFO = {
    'title': 'Product Designer',
    'name': 'Evan Chen',
    'email': 'evanchen@dify.ai',
    'phone': '+86 135-5987-0609',
    'company': 'LangGenius, Inc.',
    'address': '440 N. Wolfe Road Sunnyvale, CA 94085',
    'url': 'https://dify.ai'
}

# Run the script
python3 scripts/generate_card.py
```

Output: `{name}-business-card.svg` (e.g., `evan-chen-business-card.svg`)

## Workflow

1. **Receive request** - User provides name, title, email, phone for a new business card
2. **Update CARD_INFO** - Modify the dictionary in `scripts/generate_card.py` with the new information
3. **Run script** - Execute `python3 scripts/generate_card.py`
4. **Output SVG** - Script generates a pixel-perfect SVG file ready for use or conversion

## Script Features

The generation script (`scripts/generate_card.py`) includes:

- **Zero dependencies** - Uses only Python standard library
- **Template preservation** - Maintains exact Dify logo, background, and shadow filter from original design
- **Automatic email highlighting** - "dify" in email addresses is automatically colored blue (#0033FF)
- **Vertical URL text** - Website URL displayed vertically on the right side
- **Font substitution** - Uses Georgia/Garamond serif fonts as elegant replacement for commercial Söhne font
- **Configurable layout** - Easy adjustment of font sizes and positions via dictionaries

## Customization

### Font Sizes

Modify the `FONT` dictionary:

```python
FONT = {
    'family': 'Georgia, Garamond, serif',
    'title_size': 20,      # Job title
    'name_size': 95,       # Name (large)
    'contact_size': 28,    # Email/phone
    'company_size': 22,    # Company name
    'address_size': 18,    # Address
    'url_size': 16         # Vertical URL
}
```

### Layout Positions

Modify the `LAYOUT` dictionary:

```python
LAYOUT = {
    'title': (84, 155),     # (x, y) coordinates
    'name': (84, 245),
    'email': (86, 340),
    'phone': (86, 380),
    'company': (84, 530),
    'address': (84, 565),
    'url': (940, 470)
}
```

## Export to Other Formats

### PNG (High Resolution)

```bash
# Using Inkscape
inkscape input.svg --export-filename=output.png --export-dpi=300

# Using ImageMagick
convert -density 300 input.svg output.png
```

### PDF (Print)

Open SVG in browser → Print → Save as PDF (set margins to none, size to 90mm × 54mm)

## Why Template-Based Approach?

This skill uses a template-based approach (export SVG → replace content) rather than Figma API reconstruction for several key reasons:

- **100% pixel accuracy** - Template preserves exact visual design without font metric calculations
- **Zero dependencies** - No need for font files or fontTools library
- **Simple implementation** - ~100 lines vs ~200+ lines for API-based approach
- **No baseline calculations** - Avoids complex y-coordinate calculations for text positioning
- **Maintainability** - Design updates only require re-exporting the template SVG

For detailed technical comparison, see `references/FIGMA-API-VS-SVG.md` and `references/BASELINE-CALCULATION.md`.

## Resources

- **scripts/generate_card.py** - Main card generation script with configurable CARD_INFO
- **assets/template.svg** - Base SVG template with Dify logo and design elements
- **references/FIGMA-API-VS-SVG.md** - Technical comparison of approaches
- **references/BASELINE-CALCULATION.md** - Deep dive into SVG text baseline calculations
