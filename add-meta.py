#!/usr/bin/env python3
# coding: utf-8

import argparse
import os
import glob
import re
import ollama

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

def generate_metadata_with_ollama(content):
    """Ollamaを使用してdescriptionとkeywordを生成する"""
    prompt = f"""
以下のマークダウンファイルの内容を分析し、以下の情報を生成してください:
1. description: 内容を簡潔に説明する1〜2文の説明
2. keywords: 内容に関連するキーワードをカンマ区切りで5-7個

マークダウン内容:
{content[:2000]}  # 長すぎる場合は適当に切る

回答は以下の形式で返してください:
description: ここに説明を書く
keywords: キーワード1, キーワード2, キーワード3, キーワード4, キーワード5
"""
    
    try:
        response = ollama.chat(model='phi4', messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ])
        
        result = response['message']['content']
        metadata = {}
        
        # 応答からdescriptionとkeywordsを抽出
        if 'description:' in result.lower():
            description_match = re.search(r'description:(.*?)(?:\n|$)', result, re.IGNORECASE)
            if description_match:
                description = description_match.group(1).strip()
                print(f"description: {description}")
                metadata['description'] = description
        
        if 'keywords:' in result.lower():
            keywords_match = re.search(r'keywords:(.*?)(?:\n|$)', result, re.IGNORECASE)
            if keywords_match:
                keywords = keywords_match.group(1).strip()
                print(f"keywords: {keywords}")
                metadata['keywords'] = keywords
        
        return metadata
    except Exception as e:
        print(f"Ollamaでの処理中にエラーが発生しました: {e}")
        return {'description': '', 'keywords': ''}

def update_markdown_metadata(file_path):
    """マークダウンファイルのメタデータを更新する"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    existing_metadata = get_metadata(content)
    content_without_meta = get_content_without_metadata(content)
    
    # Ollamaを使ってdescriptionとkeywordを生成
    generated_metadata = generate_metadata_with_ollama(content_without_meta)
    
    # 既存のメタデータと生成したメタデータをマージ
    merged_metadata = {**existing_metadata, **generated_metadata}
    
    # メタデータを整形
    metadata_text = "----------\n"
    for key, value in merged_metadata.items():
        metadata_text += f"{key}: {value}\n"
    metadata_text += "----------\n\n"
    
    # 既存のメタデータを新しいメタデータで置き換える
    meta_pattern = r'^---*\s*$(.*?)^---*\s*$'
    match = re.search(meta_pattern, content, re.MULTILINE | re.DOTALL)
    
    if match:
        updated_content = content.replace(match.group(0), metadata_text)
    else:
        updated_content = metadata_text + content
    
    # 更新したコンテンツを書き込む
    print(f"更新します: {file_path}")
    print(updated_content)
    #with open(file_path, 'w', encoding='utf-8') as file:
    #    file.write(updated_content)
    
    print(f"更新しました: {file_path}")

def main():
    parser = argparse.ArgumentParser(description='Markdownファイルにメタデータを追加するツール')
    parser.add_argument('--dir', type=str, required=True, help='処理するディレクトリのパス')
    args = parser.parse_args()
    
    if not os.path.isdir(args.dir):
        print(f"エラー: 指定されたディレクトリ '{args.dir}' が存在しません。")
        return
    
    # 指定されたディレクトリ内のすべてのMarkdownファイルを取得
    markdown_files = glob.glob(os.path.join(args.dir, '**/*.md'), recursive=True)
    
    if not markdown_files:
        print(f"警告: 指定されたディレクトリ '{args.dir}' 内にMarkdownファイルが見つかりませんでした。")
        return
    
    for file_path in markdown_files:
        print(f"処理中: {file_path}")
        update_markdown_metadata(file_path)

if __name__ == "__main__":
    main()
