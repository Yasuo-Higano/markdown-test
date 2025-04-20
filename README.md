# Sitemap.xml ジェネレーター

検索エンジン向けのsitemap.xmlを生成するPythonスクリプトです。

## 使い方

```bash
python make-sitemap.py --dir <マークダウンファイルがあるディレクトリ> --base-url <ウェブサイトのベースURL>
```

### オプション

- `--dir`: マークダウンファイルがあるディレクトリを指定します（デフォルト: カレントディレクトリ）
- `--base-url`: サイトのベースURLを指定します（例: https://example.com）

### 例

```bash
python make-sitemap.py --dir ./content --base-url https://mywebsite.com
```

## 機能

- 指定したディレクトリ内のすべての.mdファイルを検索します
- XML形式のsitemap.xmlを生成します
- 各ファイルの最終更新日を追跡します
- 検索エンジン最適化（SEO）のためのXML sitemap標準に準拠しています
- README.mdおよび_（アンダースコア）から始まるファイルは無視されます

## 出力フォーマット

生成されるsitemap.xmlは以下のような形式になります：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/page1.md</loc>
    <lastmod>2023-04-01</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <!-- その他のURLエントリ -->
</urlset>
```
