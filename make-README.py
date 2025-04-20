#!/usr/bin/env python3
import os
import argparse
import glob

def generate_readme(directory, title):
    """
    Generate README.md with links to all Markdown files in the specified directory
    """
    # Find all markdown files
    md_files = glob.glob(os.path.join(directory, "*.md"))
    
    # Skip README.md itself and files starting with underscore
    md_files = [f for f in md_files if os.path.basename(f).lower() != "readme.md" and not os.path.basename(f).startswith("_")]
    
    # Sort files alphabetically
    md_files.sort()
    
    # Create content for README.md
    content = f"# {title}\n\n"
    
    if md_files:
        for md_file in md_files:
            filename = os.path.basename(md_file)
            name_without_ext = os.path.splitext(filename)[0]
            content += f"- [{name_without_ext}]({filename})\n"
    else:
        content += "No Markdown files found in this directory.\n"
        
    # Write to README.md
    readme_path = os.path.join(directory, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"README.md has been generated at {readme_path}")
    print(f"Listed {len(md_files)} Markdown files")

def main():
    parser = argparse.ArgumentParser(description="Generate README.md with links to Markdown files")
    parser.add_argument("--dir", type=str, default=".", 
                        help="Directory containing Markdown files (default: current directory)")
    parser.add_argument("--title", type=str, default="Markdown Files", 
                        help="Title for the README (default: Markdown Files)")
    
    args = parser.parse_args()
    
    # Ensure directory exists
    if not os.path.isdir(args.dir):
        print(f"Error: Directory '{args.dir}' does not exist")
        return 1
    
    # Generate README
    generate_readme(args.dir, args.title)
    return 0

if __name__ == "__main__":
    exit(main()) 