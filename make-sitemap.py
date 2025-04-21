#!/usr/bin/env python3
import os
import argparse
import glob
import datetime
import urllib.parse
import unicodedata
import re

def normalize_text(text):
    """
    ユニコードの正規化を行う
    特に、分離された濁点・半濁点を結合する（NFCフォーム）
    例: 'ホ\u309A' ('ホ' + 半濁点) を 'ポ' に変換
    """
    return unicodedata.normalize('NFC', text)

def generate_sitemap(directory, base_url):
    """
    Generate sitemap.xml with links to all Markdown files in the specified directory
    for search engine optimization
    """
    # Find all markdown files
    md_files = glob.glob(os.path.join(directory, "*.md"))
    
    # Skip files starting with underscore, but include README.md
    md_files = [f for f in md_files if not os.path.basename(f).startswith("_")]
    
    # Sort files alphabetically
    md_files.sort()
    
    # Create XML content for sitemap.xml
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    if md_files:
        for md_file in md_files:
            filename = os.path.basename(md_file)
            # Convert .md to .html for web URLs if needed
            url_path = filename
            
            # Normalize Unicode characters before URL encoding
            url_path = normalize_text(url_path)
            
            # URL encode the filename to handle multibyte Unicode characters
            url_path = urllib.parse.quote(url_path)
            
            # Get last modification time of the file
            last_mod = datetime.datetime.fromtimestamp(os.path.getmtime(md_file)).strftime("%Y-%m-%d")
            
            content += '  <url>\n'
            content += f'    <loc>{base_url}/{url_path}</loc>\n'
            content += f'    <lastmod>{last_mod}</lastmod>\n'
            content += '    <changefreq>monthly</changefreq>\n'
            content += '    <priority>0.8</priority>\n'
            content += '  </url>\n'
    
    content += '</urlset>'
        
    # Write to sitemap.xml
    sitemap_path = os.path.join(directory, "sitemap.xml")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"sitemap.xml has been generated at {sitemap_path}")
    print(f"Listed {len(md_files)} Markdown files")

def main():
    parser = argparse.ArgumentParser(description="Generate sitemap.xml for search engines")
    parser.add_argument("--dir", type=str, default=".", 
                        help="Directory containing Markdown files (default: current directory)")
    parser.add_argument("--base-url", type=str, required=True, 
                        help="Base URL of your website (e.g., https://example.com)")
    
    args = parser.parse_args()
    
    # Ensure directory exists
    if not os.path.isdir(args.dir):
        print(f"Error: Directory '{args.dir}' does not exist")
        return 1
    
    # Generate sitemap
    generate_sitemap(args.dir, args.base_url)
    return 0

if __name__ == "__main__":
    exit(main()) 