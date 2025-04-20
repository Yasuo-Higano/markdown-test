#!/usr/bin/env python3
# coding: utf-8

import argparse
import os
import glob
import re

def get_metadata(file_path):
    """マークダウンファイルからメタデータを抽出する"""
    metadata = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        meta_pattern = r'^---*\s*$(.*?)^---*\s*$'
        match = re.search(meta_pattern, content, re.MULTILINE | re.DOTALL)
        
        if match:
            meta_text = match.group(1)
            for line in meta_text.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()
    except Exception as e:
        print(f"ファイル読み込みエラー: {file_path} - {e}")
    
    return metadata

def generate_index(directory, output_file="README.md", dry_run=False):
    """指定されたディレクトリ内のマークダウンファイルを列挙し、READMEを生成する"""
    # 指定されたディレクトリ内のすべてのMarkdownファイルを取得
    # _ で始まるファイルは処理しない
    all_markdown_files = glob.glob(os.path.join(directory, '**/*.md'), recursive=True)
    markdown_files = [file for file in all_markdown_files if not os.path.basename(file).startswith('_') and os.path.basename(file) != "README.md"]
    
    if not markdown_files:
        print(f"警告: 指定されたディレクトリ '{directory}' 内にMarkdownファイルが見つかりませんでした。")
        return
    
    # 相対パスに変換
    rel_markdown_files = [os.path.relpath(file, directory) for file in markdown_files]
    rel_markdown_files.sort()  # アルファベット順に並べ替え
    
    # README.mdの内容を生成
    content = "# ドキュメント一覧\n\n"
    
    for file_path in rel_markdown_files:
        # ファイル名（拡張子なし）を取得
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        
        # メタデータからdescriptionを取得（あれば）
        full_path = os.path.join(directory, file_path)
        metadata = get_metadata(full_path)
        description = metadata.get('description', '')
        
        # [ファイル名](ファイル名.md) 形式でリンクを作成
        if description:
            content += f"- [{file_name}]({file_path}) - {description}\n"
        else:
            content += f"- [{file_name}]({file_path})\n"
    
    output_path = os.path.join(directory, output_file)
    
    if dry_run:
        print(f"ドライラン: {output_path} を生成します")
        print("------- 生成される内容 -------")
        print(content)
        print("-----------------------------")
    else:
        # README.mdを書き込む
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"インデックスを生成しました: {output_path}")

def main():
    parser = argparse.ArgumentParser(description='ディレクトリ内のマークダウンファイルを列挙し、README.mdを生成するツール')
    parser.add_argument('--dir', type=str, required=True, help='処理するディレクトリのパス')
    parser.add_argument('--output', type=str, default="README.md", help='出力ファイル名（デフォルト: README.md）')
    parser.add_argument('--dry-run', action='store_true', help='実際にファイルを更新せずに処理を実行')
    args = parser.parse_args()
    
    if not os.path.isdir(args.dir):
        print(f"エラー: 指定されたディレクトリ '{args.dir}' が存在しません。")
        return
    
    generate_index(args.dir, args.output, args.dry_run)

if __name__ == "__main__":
    main() 