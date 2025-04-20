#!/usr/bin/env python3
# coding: utf-8

import argparse
import os
import glob
import re
import ollama

skip_has_meta = True
MAX_CONTENT_LENGTH = 8000

def clean_markdown_syntax(text):
    """Markdownの構文記号を取り除く"""
    # 強調（ボールド）
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'__(.*?)__', r'\1', text)
    
    # 斜体（イタリック）
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'_(.*?)_', r'\1', text)
    
    # リンク
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'\1', text)
    
    # コードブロック
    text = re.sub(r'```.*?\n(.*?)```', r'\1', text, flags=re.DOTALL)
    
    # インラインコード
    text = re.sub(r'`(.*?)`', r'\1', text)
    
    # 見出し
    text = re.sub(r'^#{1,6}\s+(.*?)$', r'\1', text, flags=re.MULTILINE)
    
    # リスト記号
    text = re.sub(r'^\s*[*+-]\s+(.*?)$', r'\1', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\d+\.\s+(.*?)$', r'\1', text, flags=re.MULTILINE)
    
    # 日本語特有のマークアップ
    # ルビ表記（|漢字《かんじ》）
    text = re.sub(r'\|(.*?)《(.*?)》', r'\1', text)
    
    # 傍点（《《文字》》）
    text = re.sub(r'《《(.*?)》》', r'\1', text)
    
    # その他のルビ表記（=の使用）
    text = re.sub(r'\|(.*?)=(.*?)《(.*?)》', r'\1', text)
    
    # テーブル記法を削除
    text = re.sub(r'\{\|(.*?)\|\}', '', text, flags=re.DOTALL)
    
    return text

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

def trim_result(result):
    result = result.lower()
    result = result.replace("### description","description:")
    result = result.replace("### keywords","keywords:")
    # ** で強調している場合があるので、それを取り除く
    result = re.sub(r'\*\*(.*?)\*\*', r'\1', result)
    result = result.replace('\n', '')
    result = result.replace('description:', '\ndescription:')
    result = result.replace('keywords:', '\nkeywords:')
    return result

def generate_metadata_with_ollama(content):
    """Ollamaを使用してdescriptionとkeywordを生成する"""
    # コンテンツからMarkdown構文を取り除く
    cleaned_content = clean_markdown_syntax(content)
    
    prompt = f"""
以下のmarkdownファイルの内容を分析し、以下の情報をmarkdownに書かれている言語と同じ言語で生成してください:
1. description: 内容を簡潔に説明する1〜2文の説明
2. keywords: 内容に関連するキーワードをカンマ区切りで5-7個

markdown内容:
{cleaned_content[:MAX_CONTENT_LENGTH]}  # 長すぎる場合は適当に切る

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
        ], options={"temperature": 0.0})
        
        result = response['message']['content']
        metadata = {}
        
        print("-------- 応答 --------")
        print(result)
        result = trim_result(result)
        print("-------- トリム後 --------")
        print(result)
        print("----------------------")

        # 応答からdescriptionとkeywordsを抽出
        if 'description:' in result.lower():
            description_match = re.search(r'description:(.*?)(?:\n|$)', result, re.IGNORECASE)
            if description_match:
                description = description_match.group(1).strip()
                print(f"- description: {description}")
                metadata['description'] = description
        
        if 'keywords:' in result.lower():
            keywords_match = re.search(r'keywords:(.*?)(?:\n|$)', result, re.IGNORECASE)
            if keywords_match:
                keywords = keywords_match.group(1).strip()
                print(f"- keywords: {keywords}")
                metadata['keywords'] = keywords
        
        return metadata
    except Exception as e:
        print(f"Ollamaでの処理中にエラーが発生しました: {e}")
        return {'description': '', 'keywords': ''}

def update_markdown_metadata(file_path, dry_run=False):
    """マークダウンファイルのメタデータを更新する"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # debug
    if skip_has_meta:
        if content.startswith("---"):
            return
    
    existing_metadata = get_metadata(content)
    content_without_meta = get_content_without_metadata(content)
    
    # Ollamaを使ってdescriptionとkeywordを生成
    generated_metadata = generate_metadata_with_ollama(content_without_meta)
    
    if generated_metadata['description'] == '':
        print(f"Ollamaでの処理中にエラーが発生しました: {e}")
        return
    if generated_metadata['keywords'] == '':
        print(f"Ollamaでの処理中にエラーが発生しました: {e}")
        return
    
    # 既存のメタデータと生成したメタデータをマージ
    merged_metadata = {**existing_metadata, **generated_metadata}
    
    # メタデータを整形
    metadata_text = "----------\n"
    for key, value in merged_metadata.items():
        metadata_text += f"{key}: {value}\n"
    metadata_text += "----------\n\n"
    
    # 既存のメタデータを新しいメタデータで置き換える
    match = None
    if content.startswith('---'):
        meta_pattern = r'^---*\s*$(.*?)^---*\s*$'
        match = re.search(meta_pattern, content, re.MULTILINE | re.DOTALL)
    
    if match:
        updated_content = content.replace(match.group(0), metadata_text)
    else:
        updated_content = metadata_text + content
    
    # 更新したコンテンツを書き込む
    print(f"更新します: {file_path}")
    print(updated_content[:500] + "..." if len(updated_content) > 500 else updated_content)
    
    if not dry_run:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
        print(f"更新しました: {file_path}")
    else:
        print("ドライラン: ファイルは更新されません")

def main():
    parser = argparse.ArgumentParser(description='Markdownファイルにメタデータを追加するツール')
    parser.add_argument('--dir', type=str, help='処理するディレクトリのパス')
    parser.add_argument('--test-clean', type=str, help='Markdown構文削除のテスト用入力ファイル')
    parser.add_argument('--dry-run', action='store_true', help='実際にファイルを更新せずに処理を実行')
    args = parser.parse_args()
    
    if args.test_clean:
        # テストモード: Markdown構文削除のテスト
        if not os.path.isfile(args.test_clean):
            print(f"エラー: 指定されたファイル '{args.test_clean}' が存在しません。")
            return
            
        with open(args.test_clean, 'r', encoding='utf-8') as file:
            content = file.read()
            
        cleaned_content = clean_markdown_syntax(content)
        print("-------- 元のコンテンツ --------")
        print(content)
        print("\n-------- クリーニング後 --------")
        print(cleaned_content)
        return
        
    if not args.dir:
        parser.print_help()
        return
    
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
    
    for file_path in markdown_files:
        print(f"処理中: {file_path}")
        update_markdown_metadata(file_path, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
