# 模板：内容不变的石墨极简排版

当用户强调「只排版」「内容不变」「不要改内容」「不能有任何内容改动」「直接进入正文」时使用本模板。

目标不是白板排版，而是**只改呈现，不改内容**：可见文字逐字一致，同时通过留白、引用块、重点句、分组、细线和字重建立公众号阅读节奏。

## 硬规则

- 不新增任何原文没有的可见文字：不要加 `QUOTE`、`本文看点`、章节标题、英文标签、签名、CTA、图片占位文案。
- 不改写、不删减、不调换原文可见正文顺序；原标点（含半角符号、直引号）逐字保留，不做全角规范化。
- 原文 `# 标题` 默认作为公众号后台标题，不进入正文；原文 HTML 注释（如图片位置说明）不进入可复制正文。
- 原文引号句可做引用块；原文 `**加粗**` 可做重点锚点；原文连续短句可做灰底分组；这些都属于呈现层。
- 如果原文含图片注释但图片需用户后台手动插入，不在正文里生成可见占位。交付说明里单独提示图片位置。
- 交付前必须跑 `scripts/check_visible_text_match.py <原文.md> <生成.html>`，再跑 `scripts/validate_gzh_html.py <生成.html>`。文字一致检查必须通过，平台 ERROR 必须清零；原文已有标点引起的 WARNING 按 [主流程第 5 步](../SKILL.md#5-校验合规强制) 核对后保留，不为消除提示改原文。其他 WARNING 仍需检查处理。

## 视觉规格

- 全局容器：`max-width:677px`，白底，系统中文字体，正文 `15px`，行高 `1.85-1.9`。
- 主文字色：`#3F3F46`；重点色：`#111827`；辅助线：`#E4E4E7`；灰底：`#FAFAFA`。
- 开篇第一句可略放大加粗，直接进入正文，不加题头。
- 段落之间用 `margin-bottom:16-28px` 控制节奏；大转折处可用 1px 细线。
- 引用块：灰底 + 左竖线，不添加标签。
- 原文加粗核心句：用上下细线重点块，保留原文可见文字。
- 三问三答：可合并为一个灰底线框组，每组只展示原问题和原例子，不添加编号或标题。

## 组件片段

全局容器：

```html
<section style="max-width:677px;margin:0 auto;background:#FFFFFF;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif;color:#52525B;line-height:1.8;letter-spacing:0.3px;overflow-x:hidden;padding:34px 0 28px;">
  <!-- 原文内容 -->
</section>
```

普通段落：

```html
<p style="margin:0 0 20px;font-size:15px;line-height:1.9;text-align:justify;color:#3F3F46;letter-spacing:0.3px;">
  <span leaf="">原文段落</span>
</p>
```

开篇第一句：

```html
<p style="margin:0 0 28px;font-size:17px;line-height:1.9;color:#111827;font-weight:700;letter-spacing:0.5px;">
  <span leaf="">原文第一句</span>
</p>
```

引用句：

```html
<section style="margin:0 0 24px;padding:16px 18px 16px 20px;border-left:3px solid #A1A1AA;background:#FAFAFA;">
  <p style="margin:0;font-size:15px;line-height:1.85;color:#27272A;font-weight:650;text-align:justify;letter-spacing:0.3px;">
    <span leaf="">原文引号句</span>
  </p>
</section>
```

强引用/关键判断：

```html
<section style="margin:0 0 24px;padding:16px 18px 16px 20px;border-left:3px solid #111827;background:#FAFAFA;">
  <p style="margin:0;font-size:16px;line-height:1.85;color:#27272A;font-weight:800;text-align:justify;letter-spacing:0.3px;">
    <span leaf="">原文关键判断</span>
  </p>
</section>
```

原文加粗句重点块：

```html
<section style="margin:32px 0 34px;padding:24px 20px;border-top:1px solid #D4D4D8;border-bottom:1px solid #D4D4D8;background:#FFFFFF;text-align:center;">
  <p style="margin:0;font-size:20px;line-height:1.75;color:#111827;font-weight:850;letter-spacing:0.4px;">
    <strong style="color:#111827;font-weight:800;"><span leaf="">原文加粗句</span></strong>
  </p>
</section>
```

灰底分组：

```html
<section style="margin:0 10px 28px;padding:18px 18px 2px;background:#FAFAFA;border:1px solid #E4E4E7;">
  <p style="margin:0 0 18px;font-size:14px;line-height:1.9;text-align:justify;color:#52525B;letter-spacing:0.3px;">
    <span leaf="">原文短句一</span>
  </p>
  <p style="margin:0 0 18px;font-size:14px;line-height:1.9;text-align:justify;color:#52525B;letter-spacing:0.3px;">
    <span leaf="">原文短句二</span>
  </p>
</section>
```

三问三答分组：

```html
<section style="margin:0 10px 28px;padding:18px 18px 2px;background:#FAFAFA;border:1px solid #E4E4E7;">
  <section style="margin:0 0 18px;padding:0 0 16px;border-bottom:1px solid #E4E4E7;">
    <p style="margin:0 0 8px;font-size:15px;line-height:1.75;color:#111827;font-weight:800;letter-spacing:0.3px;">
      <span leaf="">原文问题</span>
    </p>
    <p style="margin:0;font-size:14px;line-height:1.85;color:#52525B;text-align:justify;letter-spacing:0.3px;">
      <span leaf="">原文例子</span>
    </p>
  </section>
</section>
```

细线分隔：

```html
<section style="height:1px;background:#E4E4E7;margin:34px 10px;">
  <span leaf=""><br></span>
</section>
```

## 交付说明口径

交付时说明：已使用内容不变模板；可见文字与原文正文一致；图片注释未进入正文，图片请按原发布包说明在公众号后台手动插入。
