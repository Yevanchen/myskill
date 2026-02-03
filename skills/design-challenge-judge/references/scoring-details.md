# Detailed Scoring Criteria

Based on **Kevin Hale's YC Design Principles** — expanded for Design Challenge judging.

## Table of Contents
1. [Legibility Detailed Criteria](#legibility-detailed-criteria)
2. [Simplicity Detailed Criteria](#simplicity-detailed-criteria)
3. [Obviousness Detailed Criteria](#obviousness-detailed-criteria)
4. [Common Mistakes Gallery](#common-mistakes-gallery)
5. [Before/After Examples](#beforeafter-examples)
6. [Evaluation Report Template](#evaluation-report-template)
7. [中文评分指南](#中文评分指南)

---

## Legibility Detailed Criteria

### Typography Scoring

| Element | Score 0 | Score 1 | Score 2 | Score 3 |
|---------|---------|---------|---------|---------|
| **Title Size** | <40pt | 40-60pt | 60-100pt | 100pt+ |
| **Body Size** | <20pt | 20-30pt | 30-44pt | 44pt+ |
| **Font Choice** | Decorative/Script | Serif | Sans-serif | Bold Sans-serif |
| **Font Consistency** | 4+ different fonts | 3 fonts | 2 fonts | 1-2 fonts |

### Contrast Scoring

| Background | Good Text Colors | Bad Text Colors |
|------------|------------------|-----------------|
| White/Light | Black, Dark Blue, Dark Gray | Light Gray, Yellow, Light colors |
| Black/Dark | White, Light Yellow, Light Blue | Dark colors, Gray |
| Blue | White, Light Yellow | Black, Dark Blue |
| Image BG | White with shadow, Dark with glow | Any without treatment |

### The 25% Test

**How to perform:**
1. Open presentation in edit mode
2. Zoom out to 25% view
3. Can you still read all text?

| Result | Score |
|--------|-------|
| All text readable | 3 |
| Most text readable, titles clear | 2 |
| Only titles readable | 1 |
| Nothing readable | 0 |

### Distance Test

**Simulation:**
- Stand 3 meters from screen
- Can you read everything?

| Result | Score |
|--------|-------|
| Every word clear | 3 |
| Main points clear | 2 |
| Squinting required | 1 |
| Can't read | 0 |

---

## Simplicity Detailed Criteria

### Information Density Scoring

| Metric | Score 0 | Score 1 | Score 2 | Score 3 |
|--------|---------|---------|---------|---------|
| **Words per slide** | >100 | 50-100 | 20-50 | <20 |
| **Bullet points** | >7 | 5-7 | 3-4 | 0-2 |
| **Numbers/stats** | >5 | 4-5 | 3 | 1-2 |
| **Visual elements** | >4 | 3-4 | 2 | 1 |

### Idea Count Test

**Ask yourself:**
> "What is this slide trying to say?"

| Answer | Score |
|--------|-------|
| One clear point | 3 |
| One main + one supporting | 2 |
| Two competing ideas | 1 |
| Multiple ideas / confused | 0 |

### The 5-Word Test

**Can you summarize the slide in 5 words or less?**

| Example Slide | 5-Word Summary | Score |
|---------------|----------------|-------|
| Single stat "4 hours wasted/week" | "Developers waste debugging time" | 3 |
| Problem + solution + market | Can't summarize in 5 | 0 |
| Before/after comparison | "Solution improves outcome" | 3 |
| Wall of bullet points | Can't summarize in 5 | 0 |

### Layout Complexity

| Layout | Score |
|--------|-------|
| Single focal point | 3 |
| Two balanced elements | 2 |
| Three+ competing elements | 1 |
| Chaotic, no hierarchy | 0 |

---

## Obviousness Detailed Criteria

### 3-Second Test

**Show slide to someone who's never seen it:**
- Start timer
- Ask "What's the point?"
- Note response time

| Response Time | Score |
|---------------|-------|
| <3 seconds | 3 |
| 3-5 seconds | 2 |
| 5-10 seconds | 1 |
| >10 seconds or wrong | 0 |

### Chart/Graph Clarity

| Element | Required for Score 3 |
|---------|---------------------|
| Title | Clear, descriptive |
| Axes labels | Present, readable |
| Units | Specified (%, $, users) |
| Legend | If multiple series |
| Data labels | On key points |
| Trend line | If showing growth |

**Scoring:**
- All elements present: 3
- Missing 1 element: 2
- Missing 2+ elements: 1
- Unlabeled/confusing: 0

### Visual Hierarchy Test

**The eye should flow:**
1. To the most important element first
2. Then to supporting information
3. Finally to details

| Hierarchy | Score |
|-----------|-------|
| Clear path, biggest = important | 3 |
| Mostly clear, minor confusion | 2 |
| Multiple competing focal points | 1 |
| No clear hierarchy | 0 |

### Explicit vs. Implicit

| Type | Example | Score |
|------|---------|-------|
| **Explicit** | Graph titled "Revenue grew 3x" | 3 |
| **Semi-explicit** | Graph with upward line, no title | 2 |
| **Implicit** | Just a graph, audience must interpret | 1 |
| **Confusing** | Graph that could mean multiple things | 0 |

---

## Common Mistakes Gallery

### Legibility Mistakes

**❌ Small Text**
```
Problem: Body text at 16pt
Fix: Increase to 44pt+
Impact: -5 points
```

**❌ Low Contrast**
```
Problem: Light gray text on white
Fix: Use black or dark blue
Impact: -5 points
```

**❌ Fancy Fonts**
```
Problem: Script/decorative fonts
Fix: Use Helvetica, Arial, or Inter
Impact: -3 points
```

**❌ Busy Background**
```
Problem: Image background with text overlay
Fix: Solid color or darkened image with text box
Impact: -5 points
```

### Simplicity Mistakes

**❌ Wall of Text**
```
Problem: 100+ words on one slide
Fix: Extract key point, move rest to appendix
Impact: -5 points
```

**❌ Bullet Point Overload**
```
Problem: 8 bullet points listing features
Fix: Pick top 3, or use icons instead
Impact: -3 points
```

**❌ Multiple Charts**
```
Problem: 3 graphs on one slide
Fix: One chart per slide, or combine into one
Impact: -3 points
```

**❌ Competing Ideas**
```
Problem: Problem AND solution on same slide
Fix: Split into two slides
Impact: -3 points
```

### Obviousness Mistakes

**❌ Unlabeled Graph**
```
Problem: Y-axis shows numbers but no label
Fix: Add "Revenue ($M)" or "Users (K)"
Impact: -5 points
```

**❌ Cryptic Diagram**
```
Problem: Architecture diagram with no labels
Fix: Label each component
Impact: -3 points
```

**❌ Implied Message**
```
Problem: Just showing data, expecting audience to conclude
Fix: State the conclusion explicitly in title
Impact: -3 points
```

**❌ Decorative Images**
```
Problem: Stock photo that doesn't add meaning
Fix: Remove or replace with relevant visual
Impact: -2 points
```

---

## Before/After Examples

### Example 1: Legibility Fix

**BEFORE (Score: 1)**
```
┌─────────────────────────────────────┐
│ Our Revolutionary Solution          │  ← 24pt, light weight
│                                     │
│ We have developed a comprehensive   │  ← 14pt gray text
│ platform that leverages AI and ML   │
│ to provide actionable insights...   │
│ [200 more words]                    │
│                                     │
└─────────────────────────────────────┘
```

**AFTER (Score: 3)**
```
┌─────────────────────────────────────┐
│                                     │
│     AI-POWERED INSIGHTS             │  ← 100pt, bold
│                                     │
│   See problems before they happen   │  ← 48pt
│                                     │
└─────────────────────────────────────┘
```

### Example 2: Simplicity Fix

**BEFORE (Score: 0)**
```
┌─────────────────────────────────────┐
│ The Problem                         │
│ • Developers waste time debugging   │
│ • Average 4 hours per week          │
│ • Costs companies $50K per dev/year │
│ • Existing tools are complex        │
│ • No real-time detection            │
│ Our Solution                        │
│ • AI-powered bug detection          │
│ • Real-time alerts                  │
│ • 90% accuracy                      │
└─────────────────────────────────────┘
```

**AFTER (Score: 3)**
```
Slide 1:
┌─────────────────────────────────────┐
│                                     │
│           4+ hours                  │  ← 100pt
│                                     │
│   wasted per week per developer     │  ← 36pt
│         debugging                   │
│                                     │
└─────────────────────────────────────┘

Slide 2:
┌─────────────────────────────────────┐
│                                     │
│   AI catches bugs before you do     │  ← 60pt
│                                     │
│         90% accuracy                │  ← 48pt
│                                     │
└─────────────────────────────────────┘
```

### Example 3: Obviousness Fix

**BEFORE (Score: 1)**
```
┌─────────────────────────────────────┐
│ Growth                              │
│                                     │
│     /                               │
│    /                                │
│   /                                 │
│  /                                  │
│ ─────────────────                   │
│                                     │
└─────────────────────────────────────┘
(No labels, no numbers, no context)
```

**AFTER (Score: 3)**
```
┌─────────────────────────────────────┐
│ Revenue grew 3x in 6 months         │  ← Explicit title
│                                     │
│ $300K ─ ─ ─ ─ ─ ─ ─ /              │
│                    /                │
│ $100K ─ ─ ─ ─ ─ /                  │
│              /                      │
│ ────────────────────────            │
│   Jan    Mar    May    Jul          │
│                                     │
│ Revenue ($K)                        │  ← Y-axis label
└─────────────────────────────────────┘
```

---

## Evaluation Report Template

### Slide-by-Slide Analysis

```markdown
## Slide [N]: [Slide Title]

### Scores
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Legible   | X | [observation] |
| Simple    | X | [observation] |
| Obvious   | X | [observation] |
| **Total** | X/9 | |

### What Works
- [Positive observation 1]
- [Positive observation 2]

### Needs Improvement
- [Issue 1]: [Specific fix]
- [Issue 2]: [Specific fix]
```

### Overall Deck Report

```markdown
# Design Evaluation Report

## Summary
| Metric | Score | Max |
|--------|-------|-----|
| Average Slide Score | XX | 9 |
| Consistency | XX | 18 |
| Flow | XX | 18 |
| Memorability | XX | 18 |
| Red Flag Deductions | -XX | |
| **Total** | XX | 90 |
| **Grade** | X | |

## Strengths
1. [Major strength 1]
2. [Major strength 2]

## Priority Fixes
1. [Most important fix]
2. [Second most important fix]
3. [Third most important fix]

## Detailed Slide Analysis
[See slide-by-slide breakdown above]
```

---

## 中文评分指南

### 评分三原则

| 原则 | 英文 | 核心问题 | Kevin Hale 原话 |
|------|------|----------|-----------------|
| **可读性** | Legible | 能读清吗？ | "后排视力不好的老年人也能看清" |
| **简洁性** | Simple | 一个观点吗？ | "简单的想法不与其他想法纠缠" |
| **显而易见** | Obvious | 3秒能懂吗？ | "一眼就能理解的幻灯片" |

### 快速评分表

| 维度 | 0分 | 1分 | 2分 | 3分 |
|------|-----|-----|-----|-----|
| **可读性** | 3米外看不清 | 需要眯眼 | 基本清晰 | 后排也清晰 |
| **简洁性** | 多个想法混杂 | 主要观点被埋没 | 一个观点，略有杂乱 | 一个强有力的观点 |
| **显而易见** | 令人困惑 | 需要10秒+理解 | 稍加思考能懂 | 瞬间理解 |

### 扣分项 (红旗)

| 问题 | 扣分 | 违反原则 |
|------|------|----------|
| 字体小于20pt | -5 | 可读性 |
| 对比度低 | -5 | 可读性 |
| 文字墙 (>50词) | -5 | 简洁性 |
| 一页多图表 | -3 | 简洁性 |
| 图表无标签 | -5 | 显而易见 |
| 装饰性图片 | -2 | 分散注意力 |

### 字体规则

```
标题:     100pt+  | 粗体 | 无衬线字体
副标题:   60pt+   | 粗体 | 无衬线字体
正文:     44pt+   | 常规/粗体 | 无衬线字体
最小:     20pt    | 仅用于脚注
```

**推荐字体**: Helvetica, Arial, 思源黑体, 苹方

### 配色规则

```
✓ 高对比: 深色文字配浅色背景，或反之
✓ 最多2-3种颜色
✓ 全程保持一致

✗ 灰配灰
✗ 黄配白
✗ 彩虹配色
✗ 渐变背景上放文字
```

### 反馈模板

**可读性反馈:**
> "字体设计优秀 — 60pt以上的粗体确保任何位置都能阅读。深色配浅色的高对比方案效果很好。"

> "第3、5、7页字体太小（约18pt）。正文请增加到44pt以上。第4页灰配白对比度不足，请改用黑色或深蓝。"

**简洁性反馈:**
> "每页只传达一个观点。第5页的单一数据'每周4小时'令人印象深刻且聚焦。"

> "第6页试图同时覆盖问题、方案和市场。请拆分为3页，每页一个观点。"

**显而易见反馈:**
> "图表标注清晰。第4页的前后对比一目了然。"

> "第3页的图表没有Y轴标签——我们在衡量什么？请添加'收入（百万）'标签。"
