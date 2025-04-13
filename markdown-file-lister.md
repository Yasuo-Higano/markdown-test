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

