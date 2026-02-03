# Figma API 的 Baseline 计算问题

## 问题：y=340 是 bounding box 顶部，不是基线

### Figma API 返回的数据

```json
{
  "type": "TEXT",
  "characters": "richard@dify.ai",
  "absoluteBoundingBox": {
    "x": 86,
    "y": 340,        // ← 这是 box 顶部！
    "width": 200,
    "height": 35
  },
  "style": {
    "fontFamily": "Söhne",
    "fontSize": 30.623,
    "fontWeight": 300,
    "lineHeightPx": 35,
    "textAlignVertical": "TOP"
  }
}
```

## 理论上的解决方案

### 方法 1: 使用字体 Metrics

SVG `<text>` 的 `y` 属性是**基线位置**，不是 box 顶部。

基线计算公式：
```
baseline_y = boundingBox.y + fontSize × ascent_ratio
```

其中 `ascent_ratio` 取决于字体：
- **西文字体**（如 Helvetica）：通常 ~0.8
- **衬线体**（如 Georgia）：通常 ~0.75-0.85
- **特殊字体**（如 Söhne）：需要查字体文件

#### 示例计算：

```python
# 从 Figma API 获取
bbox_y = 340
font_size = 30.623

# 假设 Söhne 的 ascent ratio 是 0.82（需要查字体文件）
ascent_ratio = 0.82

# 计算基线
baseline_y = bbox_y + font_size * ascent_ratio
# = 340 + 30.623 * 0.82
# = 340 + 25.11
# ≈ 365

# SVG
svg = f'<text x="86" y="365">richard@dify.ai</text>'
```

### 方法 2: 使用 Figma 的 baseline 属性

Figma 的某些节点**可能**有 baseline 信息：

```json
{
  "style": {
    "fontSize": 30.623,
    "lineHeightPx": 35,
    "textAlignVertical": "TOP",
    // 可能有这些（取决于 Figma 版本和 API）：
    "textAutoResize": "HEIGHT",
    "paragraphSpacing": 0,
    "paragraphIndent": 0
  }
}
```

但是 **Figma API 不直接返回 baseline**！

### 方法 3: 结合 lineHeight 计算

```python
bbox_y = 340
font_size = 30.623
line_height = 35

# 近似计算（假设垂直居中对齐）
baseline_y = bbox_y + line_height * 0.8

# 或更精确（如果知道 textAlignVertical）
if text_align_vertical == "TOP":
    baseline_y = bbox_y + font_size * 0.8
elif text_align_vertical == "CENTER":
    baseline_y = bbox_y + line_height / 2 + font_size * 0.3
elif text_align_vertical == "BOTTOM":
    baseline_y = bbox_y + line_height - font_size * 0.2
```

## 实际问题

### 问题 1: 字体 Metrics 未知

每个字体的 ascent/descent 比例不同：

| 字体 | Ascent | Descent | Ascent Ratio |
|------|--------|---------|--------------|
| Helvetica | 718 | 207 | 0.776 |
| Georgia | 916 | 219 | 0.806 |
| Söhne | ??? | ??? | ??? |

**如何获取 Söhne 的 metrics？**

1. **需要字体文件**（.ttf/.otf）
2. **解析字体**（使用 fontTools 等库）
3. **提取 metrics**：

```python
from fontTools.ttLib import TTFont

font = TTFont('Soehne-Buch.otf')
ascent = font['hhea'].ascent
descent = font['hhea'].descent
units_per_em = font['head'].unitsPerEm

ascent_ratio = ascent / units_per_em
# 例如：ascent=800, unitsPerEm=1000 → ratio=0.8
```

**但问题是**：你可能没有 Söhne 字体文件！

### 问题 2: Figma 内部渲染算法

Figma 的文本渲染可能有自己的逻辑：
- 可能对某些字体做了微调
- 可能有额外的 padding/offset
- 可能考虑了 optical alignment

这些细节在 API 中**不可见**。

### 问题 3: 多行文本更复杂

单行文本的 baseline 还好算，多行呢？

```json
{
  "characters": "Line 1\nLine 2\nLine 3",
  "lineHeightPx": 40,
  "fontSize": 30
}
```

需要计算：
- 第一行的 baseline
- 每行之间的间距（lineHeight）
- 最后一行的位置

### 问题 4: 不同对齐方式

```json
{
  "textAlignVertical": "TOP",     // 顶部对齐
  "textAlignVertical": "CENTER",  // 垂直居中
  "textAlignVertical": "BOTTOM"   // 底部对齐
}
```

每种对齐方式的 baseline 计算都不同！

## 完整的解决方案（理论上）

```python
import requests
from fontTools.ttLib import TTFont

def calculate_baseline(figma_node, font_file_path):
    """
    从 Figma API 节点计算正确的 baseline
    """
    # 1. 获取基本信息
    bbox = figma_node['absoluteBoundingBox']
    style = figma_node['style']

    bbox_y = bbox['y']
    font_size = style['fontSize']
    line_height = style.get('lineHeightPx', font_size * 1.2)
    align = style.get('textAlignVertical', 'TOP')

    # 2. 解析字体文件，获取 metrics
    font = TTFont(font_file_path)
    ascent = font['hhea'].ascent
    units_per_em = font['head'].unitsPerEm
    ascent_ratio = ascent / units_per_em

    # 3. 计算 baseline
    if align == 'TOP':
        baseline_y = bbox_y + font_size * ascent_ratio
    elif align == 'CENTER':
        center_offset = (line_height - font_size) / 2
        baseline_y = bbox_y + center_offset + font_size * ascent_ratio
    elif align == 'BOTTOM':
        baseline_y = bbox_y + line_height - font_size * (1 - ascent_ratio)

    return baseline_y

# 使用
baseline = calculate_baseline(
    figma_node=api_response['nodes']['1:234'],
    font_file_path='/path/to/Soehne-Buch.otf'
)

print(f'<text x="{bbox_x}" y="{baseline}">...</text>')
```

## 为什么我们没有这样做？

### 原因 1: 需要所有字体文件

```python
# 需要的字体文件：
fonts = {
    'Söhne': '/path/to/Soehne-Buch.otf',
    'Söhne Halbfett': '/path/to/Soehne-Halbfett.otf',
    'Georgia': '/System/Library/Fonts/Georgia.ttf',
    # ... 设计中用到的每个字体
}
```

**问题**：
- Söhne 是商业字体，可能没有
- 需要维护字体库
- 不同系统路径不同

### 原因 2: 复杂度 vs 收益

```
Figma API 方案：
- 需要 fontTools 库
- 需要字体文件
- 需要复杂计算
- 需要处理边缘情况
- 结果：90% 准确

直接导出 SVG：
- 无需依赖
- 无需字体
- 无需计算
- 复制粘贴
- 结果：100% 准确
```

### 原因 3: 维护成本

如果设计改了字体或调整了间距：
- **API 方案**：需要重新计算，可能要调整算法
- **SVG 方案**：重新导出即可，自动正确

## 结论

### Figma MCP 能解决 baseline 问题吗？

**理论上：能** ✅
- 通过字体 metrics 计算
- 结合 Figma API 的各种属性
- 写一个完整的转换器

**实际上：不划算** ❌
- 需要所有字体文件（可能没有）
- 需要复杂的计算逻辑
- 需要处理大量边缘情况
- 最终可能还是有 1-2px 偏差

### 什么时候值得用 Figma API？

当你需要：
- **批量生成**（如 1000 张名片）
- **动态内容**（如用户上传头像）
- **编程控制**（如自动调整布局）
- **提取 design tokens**（如颜色变量）

而不是：
- 单个静态设计（直接导出 SVG）
- 需要像素级精确（导出 SVG）
- 快速实现（导出 SVG）

## 实际对比

### 用 Figma API + 字体计算：

```python
# 代码量：~200 行
# 依赖：fontTools, requests
# 字体文件：需要所有字体
# 精确度：~95%（可能有 1-2px 偏差）
# 维护：复杂，字体改变需要调整
```

### 用导出 SVG + 模板替换：

```python
# 代码量：~100 行
# 依赖：无
# 字体文件：不需要
# 精确度：100%（Figma 已算好）
# 维护：简单，重新导出即可
```

## 我的建议

如果你真的想基于 Figma API 做像素级精确的实现：

1. **先导出一次 SVG**（获取正确的坐标作为参考）
2. **对比 API 返回的坐标**（计算偏移量）
3. **写转换函数**（bbox → baseline）
4. **测试多个字体**（建立字体 metrics 数据库）
5. **处理边缘情况**（多行、对齐、效果等）

但这个工作量是"直接用 SVG"的 **10 倍以上**。

对于名片这种**静态设计**，直接用 SVG 模板是最佳方案。

---

**简单回答你的问题**：
- Figma MCP **能**解决 baseline 问题
- 但需要字体文件 + 复杂计算
- 对于名片这种场景，**不值得**
- 直接用 SVG 模板更简单、更准确

就像用 Photoshop 做设计：
- 你可以用代码重建（复杂）
- 也可以直接导出 PNG（简单）

选哪个？当然是导出！🎯
