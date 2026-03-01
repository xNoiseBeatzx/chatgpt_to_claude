import json
import os
from datetime import datetime
from collections import defaultdict
import argparse

def format_conversation(conv):
    title = conv.get('title', 'Unknown Title')
    create_time = conv.get('create_time')
    date_str = datetime.fromtimestamp(create_time).strftime('%Y-%m-%d %H:%M:%S') if create_time else 'Unknown Date'
    
    output = []
    output.append(f"## Conversation: {title}")
    output.append(f"**Date:** {date_str}\n")
    
    mapping = conv.get('mapping', {})
    
    messages = []
    for node_id, node in mapping.items():
        message = node.get('message')
        if not message:
            continue
        author = message.get('author', {}).get('role', 'unknown')
        if author not in ['user', 'assistant']:
            continue
            
        content = message.get('content', {})
        if content.get('content_type') == 'text':
            parts = content.get('parts', [])
            text = "".join(str(p) for p in parts if p)
            if text.strip():
                create_time = message.get('create_time') or 0
                messages.append((create_time, author, text))
                
    # Sort messages chronologically
    messages.sort(key=lambda x: x[0])
    
    for _, author, text in messages:
        role_label = "You" if author == 'user' else "ChatGPT"
        output.append(f"### {role_label}:\n{text}\n")
        
    output.append("---\n")
    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(description="Split ChatGPT conversations by month.")
    parser.add_argument("input_file", nargs='?', default="conversations.json", help="Path to conversations.json")
    parser.add_argument("--out-dir", default="monthly_exports", help="Output directory")
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"❌ Error: Could not find {args.input_file}")
        print("Please make sure you have extracted your ChatGPT data export and that conversations.json is in this directory.")
        return
        
    print("⏳ Parsing conversations.json...")
    with open(args.input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    print(f"✅ Loaded {len(data)} conversations.")
    
    # Group by month
    monthly_data = defaultdict(list)
    
    for conv in data:
        create_time = conv.get('create_time')
        if not create_time:
            continue
        
        date_obj = datetime.fromtimestamp(create_time)
        month_key = date_obj.strftime("%Y-%m") # e.g., "2023-04"
        monthly_data[month_key].append(conv)
        
    os.makedirs(args.out_dir, exist_ok=True)
    
    # Sort by month
    sorted_months = sorted(monthly_data.keys(), reverse=True)
    
    print("\n📂 Exporting to monthly Markdown files...")
    for month in sorted_months:
        convs = monthly_data[month]
        month_file = os.path.join(args.out_dir, f"chatgpt_{month}.md")
        with open(month_file, 'w', encoding='utf-8') as f:
            f.write(f"# ChatGPT Conversations - {month}\n\n")
            for conv in convs:
                f.write(format_conversation(conv))
                
        # Get file size
        size_mb = os.path.getsize(month_file) / (1024 * 1024)
        print(f"  ➜ Created {month_file} ({len(convs)} conversations) - {size_mb:.2f} MB")
        
    print("\n🎉 Done! Your files are ready in the '{args.out_dir}' folder.")

if __name__ == "__main__":
    main()
