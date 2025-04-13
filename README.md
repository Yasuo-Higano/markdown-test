# Markdown File Lister

A simple Python script that lists all Markdown files in a directory and generates a README.md with links to these files.

## Usage

```bash
python main.py --dir <directory_path>
```

If no directory is specified, the current directory will be used.

## Example

```bash
python main.py --dir .
```

This will:
1. Scan the specified directory for all `.md` files (excluding README.md)
2. Generate a README.md with links to all found Markdown files
3. Display a summary of the operation

## Output Format

The generated README.md will list files in this format:
- [Filename](filename.md)

# markdown-test

https://gitmarkdown.com/ のマークダウンテストページ。

## 数式
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

## 数式２
インライン数式 $E=mc^2$ は有名です。

$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$

## mermaid
```mermaid
graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;
```

## ルビをふる
不意に電気が消え、モニターには《《怪物》》が写っていた。
おっと、それまでだ。俺の|邪気眼《ダークフレーム・オブ・アイズ》が目を覚ましちまうぜ。

## Wikitable
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

