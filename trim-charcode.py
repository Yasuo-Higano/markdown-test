#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import unicodedata
import re

def normalize_text(text):
    """
    ユニコードの正規化を行う
    特に、分離された濁点・半濁点を結合する（NFCフォーム）
    例: 'ホ\u309A' ('ホ' + 半濁点) を 'ポ' に変換
    """
    return unicodedata.normalize('NFC', text)

def process_file(file_path):
    """
    ファイルを読み込み、ユニコード正規化を行い、必要であれば上書き保存する
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 正規化
        normalized_content = normalize_text(content)
        
        # 変更があった場合のみ保存
        if content != normalized_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(normalized_content)
            print(f"正規化しました: {file_path}")
        else:
            print(f"変更なし: {file_path}")
    
    except Exception as e:
        print(f"エラー ({file_path}): {e}")

def find_md_files(directory):
    """
    指定されたディレクトリ以下の全ての .md ファイルを見つける
    """
    md_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md') or file.endswith('.xml') or file.endswith('.txt'):
                md_files.append(os.path.join(root, file))
    return md_files

def main():
    parser = argparse.ArgumentParser(description='Markdownファイルのユニコード正規化を行います')
    parser.add_argument('--dir', required=True, help='処理するディレクトリを指定')
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.dir):
        print(f"エラー: ディレクトリが存在しません: {args.dir}")
        sys.exit(1)
    
    md_files = find_md_files(args.dir)
    
    if not md_files:
        print(f"警告: {args.dir} 以下にMarkdownファイルが見つかりませんでした")
        sys.exit(0)
    
    print(f"{len(md_files)} 個のMarkdownファイルを処理します...")
    
    for file_path in md_files:
        process_file(file_path)
    
    print("処理が完了しました")

if __name__ == "__main__":
    main()
