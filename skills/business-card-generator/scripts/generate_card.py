#!/usr/bin/env python3
"""
Evan Chen - Dify Business Card
"""

# 名片信息
CARD_INFO = {
    'title': 'Product Designer',
    'name': 'Evan Chen',
    'email': 'evanchen@dify.ai',
    'phone': '+86 135-5987-0609',
    'company': 'LangGenius, Inc.',
    'address': '440 N. Wolfe Road Sunnyvale, CA 94085',
    'url': 'https://dify.ai'
}

# 字体配置
FONT = {
    'family': 'Georgia, Garamond, serif',
    'title_size': 20,
    'name_size': 95,
    'contact_size': 28,
    'company_size': 22,
    'address_size': 18,
    'url_size': 16
}

# 布局坐标
LAYOUT = {
    'title': (84, 155),
    'name': (84, 245),
    'email': (86, 340),
    'phone': (86, 380),
    'company': (84, 530),
    'address': (84, 565),
    'url': (940, 470)
}

# 颜色
COLOR = {
    'black': '#000000',
    'blue': '#0033FF'
}

# SVG 模板
TEMPLATE_START = '''<svg width="1015" height="625" viewBox="0 0 1015 625" fill="none" xmlns="http://www.w3.org/2000/svg">
<g filter="url(#filter0_d_1_488)">

<!-- 白色背景 -->
<rect x="19.1387" width="976.58" height="585.94" rx="3.82792" fill="white" shape-rendering="crispEdges"/>

<!-- Dify Logo -->
<path d="M850.58 66.9241C855.198 66.9241 856.911 64.0884 856.911 60.5826C856.911 57.0769 855.206 54.2412 850.58 54.2412C845.955 54.2412 844.25 57.0769 844.25 60.5826C844.25 64.0884 845.955 66.9241 850.58 66.9241Z" fill="#0033FF"/>
<path d="M797.921 54.249H778.709V113.112H797.921C821.652 113.112 828.432 99.5298 828.432 83.6762C828.432 67.8226 821.652 54.249 797.921 54.249ZM798.149 104.057H789.559V63.3035H798.149C811.798 63.3035 817.59 70.0127 817.59 83.6762C817.59 97.3397 811.798 104.049 798.149 104.049V104.057Z" fill="black"/>
<path d="M872.73 68.2884V72.3662H862.336V81.4207H872.73V104.065H855.549V72.3581H832.951V81.4126H845.604V104.057H830.684V113.112H898.484V104.057H882.666V81.4126H898.484V72.3581H882.666V63.3035H898.484V54.249H886.729C879.003 54.249 872.713 60.5496 872.713 68.2884H872.73Z" fill="#0033FF"/>
<path d="M930.708 72.3584L921.669 101.794L912.63 72.3584H901.895L915.004 110.431C916.367 114.395 914.058 117.639 909.873 117.639H905.28V126.694H912.035C917.925 126.694 923.228 122.959 925.218 117.41L941.444 72.3584H930.708Z" fill="black"/>

'''

TEMPLATE_END = '''
</g>

<!-- 阴影滤镜 -->
<defs>
<filter id="filter0_d_1_488" x="-0.00094223" y="0" width="1014.86" height="624.22" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
<feFlood flood-opacity="0" result="BackgroundImageFix"/>
<feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0" result="hardAlpha"/>
<feOffset dy="19.1396"/>
<feGaussianBlur stdDeviation="9.56981"/>
<feComposite in2="hardAlpha" operator="out"/>
<feColorMatrix type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.1 0"/>
<feBlend mode="normal" in2="BackgroundImageFix" result="effect1_dropShadow_1_488"/>
<feBlend mode="normal" in="SourceGraphic" in2="effect1_dropShadow_1_488" result="shape"/>
</filter>
</defs>
</svg>
'''

def generate_text(x, y, text, font_size, weight, color, spacing=0):
    style = f"font-family: {FONT['family']}; font-size: {font_size}px; font-weight: {weight}; fill: {color}; letter-spacing: {spacing}px;"
    return f'<text x="{x}" y="{y}" style="{style}">{text}</text>\n'

def generate_email(x, y, email):
    style = f"font-family: {FONT['family']}; font-size: {FONT['contact_size']}px; font-weight: 300; fill: {COLOR['black']}; letter-spacing: -0.5px;"

    # 提取 dify 部分高亮
    if '@dify.ai' in email:
        username = email.split('@')[0]
        tspan = f'<tspan style="fill: {COLOR['blue']}; font-weight: 400;">dify</tspan>'
        text = f'{username}@{tspan}.ai'
    else:
        text = email

    return f'<text x="{x}" y="{y}" style="{style}">{text}</text>\n'

def generate_vertical_text(x, y, text):
    style = f"font-family: {FONT['family']}; font-size: {FONT['url_size']}px; font-weight: 300; fill: {COLOR['black']};"
    return f'<g transform="translate({x}, {y})">\n  <text style="{style}" writing-mode="tb" glyph-orientation-vertical="0">\n    {text}\n  </text>\n</g>\n'

def generate_svg():
    svg = TEMPLATE_START

    # 职位
    svg += generate_text(
        LAYOUT['title'][0], LAYOUT['title'][1],
        CARD_INFO['title'],
        FONT['title_size'], 400, COLOR['black'], 0.3
    )

    # 姓名
    svg += generate_text(
        LAYOUT['name'][0], LAYOUT['name'][1],
        CARD_INFO['name'],
        FONT['name_size'], 700, COLOR['black'], -1.5
    )

    # 邮箱
    svg += generate_email(
        LAYOUT['email'][0], LAYOUT['email'][1],
        CARD_INFO['email']
    )

    # 电话
    svg += generate_text(
        LAYOUT['phone'][0], LAYOUT['phone'][1],
        CARD_INFO['phone'],
        FONT['contact_size'], 300, COLOR['black'], -0.5
    )

    # 公司名
    svg += generate_text(
        LAYOUT['company'][0], LAYOUT['company'][1],
        CARD_INFO['company'],
        FONT['company_size'], 500, COLOR['blue']
    )

    # 地址
    svg += generate_text(
        LAYOUT['address'][0], LAYOUT['address'][1],
        CARD_INFO['address'],
        FONT['address_size'], 300, COLOR['black']
    )

    # 竖排网址
    svg += generate_vertical_text(
        LAYOUT['url'][0], LAYOUT['url'][1],
        CARD_INFO['url']
    )

    svg += TEMPLATE_END
    return svg

# 生成并保存
svg = generate_svg()
output = 'evan-chen-business-card.svg'

with open(output, 'w', encoding='utf-8') as f:
    f.write(svg)

print(f'✅ Evan Chen 名片已生成: {output}')
print(f'   姓名: {CARD_INFO["name"]}')
print(f'   职位: {CARD_INFO["title"]}')
print(f'   邮箱: {CARD_INFO["email"]}')
print(f'   电话: {CARD_INFO["phone"]}')
