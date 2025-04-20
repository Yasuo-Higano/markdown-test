# markdown-test

https://gitmarkdown.com/ のマークダウンテストページ。

## 数式
```text
$$
\left[ \begin{array}{a} a^l_1 \\ ⋮ \\ a^l_{d_l} \end{array}\right]
= \sigma(
 \left[ \begin{matrix} 
    w^l_{1,1} & ⋯  & w^l_{1,d_{l-1}} \\  
    ⋮ & ⋱  & ⋮  \\ 
    w^l_{d_l,1} & ⋯  & w^l_{d_l,d_{l-1}} \\  
 \end{matrix}\right]  ·
 \left[ \begin{array}{x} a^{l-1}_1 \\ ⋮ \\ ⋮ \\ a^{l-1}_{d_{l-1}} \end{array}\right] + 
 \left[ \begin{array}{b} b^l_1 \\ ⋮ \\ b^l_{d_l} \end{array}\right])
 $$

インライン数式 $E=mc^2$ は有名です。

$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$
```

$$
\left[ \begin{array}{a} a^l_1 \\ ⋮ \\ a^l_{d_l} \end{array}\right]
= \sigma(
 \left[ \begin{matrix} 
    w^l_{1,1} & ⋯  & w^l_{1,d_{l-1}} \\  
    ⋮ & ⋱  & ⋮  \\ 
    w^l_{d_l,1} & ⋯  & w^l_{d_l,d_{l-1}} \\  
 \end{matrix}\right]  ·
 \left[ \begin{array}{x} a^{l-1}_1 \\ ⋮ \\ ⋮ \\ a^{l-1}_{d_{l-1}} \end{array}\right] + 
 \left[ \begin{array}{b} b^l_1 \\ ⋮ \\ b^l_{d_l} \end{array}\right])
 $$

インライン数式 $E=mc^2$ は有名です。

$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$

## mermaid
```text
graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;
```

```mermaid
graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;
```

## Ruby
```text
Master of the |Gun=Katas《Geometric and Tactical Analysis》 an adversary not to be taken lightly.
```
Master of the |Gun=Katas《Geometric and Tactical Analysis》 an adversary not to be taken lightly.

## ルビと傍点
```text
不意に電気が消え、モニターには《《怪物》》が写っていた。
おっと、それまでだ。俺の|邪気眼《ダークフレーム・オブ・アイズ》が目を覚ましちまうぜ。
```
不意に電気が消え、モニターには《《怪物》》が写っていた。
おっと、それまでだ。俺の|邪気眼《ダークフレーム・オブ・アイズ》が目を覚ましちまうぜ。

## [平家物語](heike.md)　冒頭
```text
|祇園精舍《ぎおんしょうじゃ》の鐘の声、|諸行無常《しょぎょうむじょう》の響きあり。
|娑羅双樹《さらそうじゅ》の花の色、|盛者必衰《じょうしゃひっすい》の|理《ことわり》をあらはす。
|驕《おごれる》れる人も久しからず、ただ春の夜の夢のごとし。
猛き者もつひにはほろびぬ、ひとへに風の前の|塵《ちり》に同じ。
```
|祇園精舍《ぎおんしょうじゃ》の鐘の声、|諸行無常《しょぎょうむじょう》の響きあり。
|娑羅双樹《さらそうじゅ》の花の色、|盛者必衰《じょうしゃひっすい》の|理《ことわり》をあらはす。
|驕《おごれる》れる人も久しからず、ただ春の夜の夢のごとし。
猛き者もつひにはほろびぬ、ひとへに風の前の|塵《ちり》に同じ。

## Wikitable
```text
{| class="wikitable"
!colspan="6"|Shopping List
|-
|rowspan="2"|Bread & Butter
|Pie
|Buns
|Danish
|colspan="2"|Croissant
|-
|Cheese
|colspan="2"|Ice cream
|Butter
|Yogurt
|}

```
{| class="wikitable"
!colspan="6"|Shopping List
|-
|rowspan="2"|Bread & Butter
|Pie
|Buns
|Danish
|colspan="2"|Croissant
|-
|Cheese
|colspan="2"|Ice cream
|Butter
|Yogurt
|}

## Folio-Scientia
- [Folio-Scientia](folio-scientia/README.md)

# Markdown メタデータ追加ツール

このツールは、指定されたディレクトリ内のMarkdownファイルを処理し、OLLAMAを使用して自動的にdescriptionとkeywordsを生成して追加するPythonスクリプトです。

## 機能

- 指定されたディレクトリ内のすべての `.md` ファイルを再帰的に検索
- Markdownファイルのメタデータセクションを解析（存在する場合）
- ファイルの内容からOLLAMAを使ってdescriptionとkeywordsを自動生成
- 既存のメタデータフィールドを保持しながら、新しいメタデータを追加または更新

## 必要条件

- Python 3.6以上
- ollama パッケージ
- OLLAMA（ローカルで実行されていること）

## インストール

```bash
pip install ollama
```

## 使い方

```bash
python add-meta.py --dir <ディレクトリパス>
```

### 例：

```bash
python add-meta.py --dir ./docs
```

これにより、`./docs` ディレクトリとそのサブディレクトリにあるすべての `.md` ファイルが処理されます。

## メタデータ形式

スクリプトは以下のフォーマットのメタデータを処理します：

```markdown
---
title: タイトル
author: 著者名
date: 2023-06-15
description: 自動生成された説明
keywords: キーワード1, キーワード2, キーワード3, キーワード4, キーワード5
---

マークダウンの本文...
```

既存のメタデータがある場合は保持され、`description`と`keywords`フィールドのみが追加または更新されます。

## 注意事項

- OLLAMA APIへのアクセスが必要です
- 大量のファイルを処理する場合、時間がかかる場合があります
- 非常に大きなMarkdownファイルの場合、内容の最初の2000文字のみが分析対象となります

