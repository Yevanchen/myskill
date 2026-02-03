# Business Card Generator - Usage Examples

## Example 1: Evan Chen (Product Designer)

```python
CARD_INFO = {
    'title': 'Product Designer',
    'name': 'Evan Chen',
    'email': 'evanchen@dify.ai',
    'phone': '+86 135-5987-0609',
    'company': 'LangGenius, Inc.',
    'address': '440 N. Wolfe Road Sunnyvale, CA 94085',
    'url': 'https://dify.ai'
}
```

Output: `evan-chen-business-card.svg`

## Example 2: Richard Yan (CRO, Co-founder)

```python
CARD_INFO = {
    'title': 'CRO, Co-founder',
    'name': 'Richard Yan',
    'email': 'richard@dify.ai',
    'phone': '+1 302-250-8926',
    'company': 'LangGenius, Inc.',
    'address': '440 N. Wolfe Road Sunnyvale, CA 94085',
    'url': 'https://dify.ai'
}
```

Output: `richard-yan-business-card.svg`

## Example 3: Yeuoly (Backend Engineer)

```python
CARD_INFO = {
    'title': 'Backend Engineer / Product Designer',
    'name': 'Yeuoly',
    'email': 'yeuoly@dify.ai',
    'phone': '+44 7845-198908',
    'company': 'LangGenius, Inc.',
    'address': '440 N. Wolfe Road Sunnyvale, CA 94085',
    'url': 'https://dify.ai'
}
```

Output: `yeuoly-business-card.svg`

## Batch Generation

To generate multiple cards, modify the script to accept command-line arguments:

```python
import sys

if len(sys.argv) > 1:
    # Parse arguments: name, title, email, phone
    CARD_INFO['name'] = sys.argv[1]
    CARD_INFO['title'] = sys.argv[2]
    CARD_INFO['email'] = sys.argv[3]
    CARD_INFO['phone'] = sys.argv[4]
```

Then run:

```bash
python3 generate_card.py "Evan Chen" "Product Designer" "evanchen@dify.ai" "+86 135-5987-0609"
```

## Common Customizations

### Different Font Family

```python
FONT['family'] = 'Helvetica Neue, sans-serif'  # Modern sans-serif
```

### Larger Name

```python
FONT['name_size'] = 110  # Increase from default 95
```

### Adjust Vertical Spacing

```python
LAYOUT['email'] = (86, 360)   # Move down 20px
LAYOUT['phone'] = (86, 400)   # Move down 20px
```
