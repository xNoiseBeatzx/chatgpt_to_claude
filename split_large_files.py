import os
import argparse

def split_file(filepath, max_size_mb=25.0):
    max_bytes = max_size_mb * 1024 * 1024
    if os.path.getsize(filepath) <= max_bytes:
        return False
        
    print(f"✂️  Splitting {os.path.basename(filepath)} (larger than {max_size_mb}MB)...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # We split at conversation boundaries ("## Conversation:")
    # This ensures we don't cut a single conversation in half
    conversations = content.split("## Conversation:")
    
    base_name = os.path.splitext(filepath)[0]
    
    part = 1
    current_chunk = conversations[0] # Usually just the header of the file
    
    for conv in conversations[1:]:
        conv_text = "\n## Conversation:" + conv
        if len(current_chunk.encode('utf-8')) + len(conv_text.encode('utf-8')) > max_bytes:
            # Reached max size, write out current chunk
            out_file = f"{base_name}_part{part}.md"
            with open(out_file, 'w', encoding='utf-8') as f:
                f.write(current_chunk)
            print(f"  ➜ Created {os.path.basename(out_file)}")
            
            part += 1
            # Next chunk starts with this conversation
            current_chunk = "## Conversation:" + conv
        else:
            current_chunk += conv_text
            
    # Write the very last chunk
    if current_chunk.strip():
        out_file = f"{base_name}_part{part}.md"
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(current_chunk)
        print(f"  ➜ Created {os.path.basename(out_file)}")
        
    return True

def main():
    parser = argparse.ArgumentParser(description="Split large Markdown files into smaller chunks for NotebookLM limits (500k words or 50MB).")
    parser.add_argument("input_path", nargs='?', default="monthly_exports", help="Path to markdown file or directory to process")
    parser.add_argument("--max-size", type=float, default=25.0, help="Maximum file size in MB")
    args = parser.parse_args()
    
    if os.path.isdir(args.input_path):
        print(f"🔍 Scanning directory '{args.input_path}' for large files...")
        count = 0
        for filename in sorted(os.listdir(args.input_path)):
            if filename.endswith('.md') and '_part' not in filename:
                filepath = os.path.join(args.input_path, filename)
                if split_file(filepath, args.max_size):
                    count += 1
                    
        if count == 0:
            print("✨ All files are neatly sized. No splitting was necessary.")
        else:
            print(f"🎉 Done! Split {count} large files.")
    else:
        if not os.path.exists(args.input_path):
            print(f"❌ Error: Could not find {args.input_path}")
            return
        split_file(args.input_path, args.max_size)

if __name__ == "__main__":
    main()
