#!/usr/bin/env python3
# coding: utf-8

import argparse
import os
import glob
import re

MAX_DESCRIPTION_LENGTH = 160

def get_metadata(content):
    """マークダウンファイルからメタデータを抽出する"""
    metadata = {}
    meta_pattern = r'^---*\s*$(.*?)^---*\s*$'
    match = re.search(meta_pattern, content, re.MULTILINE | re.DOTALL)
    
    if match:
        meta_text = match.group(1)
        for line in meta_text.strip().split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip()
    
    return metadata

def get_content_without_metadata(content):
    """メタデータを除いたマークダウンコンテンツを取得する"""
    meta_pattern = r'^---*\s*$(.*?)^---*\s*$'
    match = re.search(meta_pattern, content, re.MULTILINE | re.DOTALL)
    
    if match:
        return content.replace(match.group(0), '').strip()
    
    return content.strip()

def modify_markdown_metadata(file_path, dry_run=False):
    """マークダウンファイルのメタデータを修正する"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # メタデータがなければ処理をスキップ
    if not content.startswith("---"):
        print(f"メタデータがありません: {file_path}")
        return
    
    existing_metadata = get_metadata(content)
    content_without_meta = get_content_without_metadata(content)
    
    # メタデータが変更されたかどうかを追跡するフラグ
    metadata_modified = False
    
    # descriptionが存在し、160文字より長い場合は切り詰める
    if 'description' in existing_metadata and len(existing_metadata['description']) > MAX_DESCRIPTION_LENGTH:
        existing_metadata['description'] = existing_metadata['description'][:MAX_DESCRIPTION_LENGTH]
        print(f"descriptionを{MAX_DESCRIPTION_LENGTH}文字に切り詰めました: {file_path}")
        metadata_modified = True
    
    # メタデータが変更されていなければ処理を終了
    if not metadata_modified:
        print(f"メタデータの修正は必要ありません: {file_path}")
        return
    
    # メタデータを整形
    metadata_text = "----------\n"
    for key, value in existing_metadata.items():
        metadata_text += f"{key}: {value}\n"
    metadata_text += "----------\n\n"
    
    # 既存のメタデータを新しいメタデータで置き換える
    meta_pattern = r'^---*\s*$(.*?)^---*\s*$'
    match = re.search(meta_pattern, content, re.MULTILINE | re.DOTALL)
    
    if match:
        updated_content = content.replace(match.group(0), metadata_text)
        
        # 更新したコンテンツを書き込む
        print(f"更新します: {file_path}")
        if not dry_run:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
            print(f"更新しました: {file_path}")
        else:
            print("ドライラン: ファイルは更新されません")

def main():
    parser = argparse.ArgumentParser(description='Markdownファイルのメタデータを修正するツール')
    parser.add_argument('--dir', type=str, required=True, help='処理するディレクトリのパス')
    parser.add_argument('--dry-run', action='store_true', help='実際にファイルを更新せずに処理を実行')
    args = parser.parse_args()
    
    if not os.path.isdir(args.dir):
        print(f"エラー: 指定されたディレクトリ '{args.dir}' が存在しません。")
        return
    
    # 指定されたディレクトリ内のすべてのMarkdownファイルを取得
    # _ で始まるファイルは処理しない
    all_markdown_files = glob.glob(os.path.join(args.dir, '**/*.md'), recursive=True)
    markdown_files = [file for file in all_markdown_files if not os.path.basename(file).startswith('_')]
    
    if not markdown_files:
        print(f"警告: 指定されたディレクトリ '{args.dir}' 内にMarkdownファイルが見つかりませんでした。")
        return
    
    print(f"{len(markdown_files)}個のMarkdownファイルを処理します")
    
    for file_path in markdown_files:
        print(f"処理中: {file_path}")
        modify_markdown_metadata(file_path, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
