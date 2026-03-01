import json
import os
import collections
import argparse
from datetime import datetime

def format_conversation(conv):
    title = conv.get('title', 'Unknown Title')
    create_time = conv.get('create_time')
    date_str = datetime.fromtimestamp(create_time).strftime('%Y-%m-%d %H:%M:%S') if create_time else 'Unknown Date'
    
    output = [f"## Conversation: {title}", f"**Date:** {date_str}\n"]
    mapping = conv.get('mapping', {})
    messages = []
    
    for node in mapping.values():
        message = node.get('message')
        if not message: continue
        author = message.get('author', {}).get('role', 'unknown')
        if author not in ['user', 'assistant']: continue
        
        content = message.get('content', {})
        if content.get('content_type') == 'text':
            parts = content.get('parts', [])
            text = "".join(str(p) for p in parts if p)
            if text.strip():
                create_time = message.get('create_time') or 0
                messages.append((create_time, author, text))
                
    messages.sort(key=lambda x: x[0])
    for _, author, text in messages:
        role_label = "You" if author == 'user' else "ChatGPT"
        output.append(f"### {role_label}:\n{text}\n")
    output.append("---\n")
    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(description="Extract specific ChatGPT Projects from your data export.")
    parser.add_argument("input_file", nargs='?', default="conversations.json", help="Path to conversations.json")
    parser.add_argument("--out-dir", default="chatgpt_projects", help="Output directory")
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"❌ Error: Could not find {args.input_file}")
        return

    print("⏳ Parsing conversations.json...")
    with open(args.input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Group by gizmo_id (which acts as the Project/Workspace ID in ChatGPT Plus/Team)
    projects = collections.defaultdict(list)
    for conv in data:
        gizmo_id = conv.get('gizmo_id')
        if gizmo_id:
            projects[gizmo_id].append(conv)

    if not projects:
        print("⚠️ No Projects or Custom GPTs found in this export.")
        return

    os.makedirs(args.out_dir, exist_ok=True)
    
    # Sort projects by the number of conversations they have
    sorted_projects = sorted(projects.items(), key=lambda x: len(x[1]), reverse=True)
    
    index_content = ["# ChatGPT Projects Index\n", "Since ChatGPT's data export doesn't include the explicit human-readable names of your Projects, this index helps you map the exported files to your Projects based on the conversation titles within them.\n"]
    
    print("\n📂 Extracting Projects...")
    count = 1
    for gizmo_id, convs in sorted_projects:
        # We'll use the most common keywords or the first conversation title to help identify it
        titles = [c.get('title', 'Untitled') for c in convs]
        
        # Name the file based on the count to keep it clean
        filename = f"Project_{count:02d}_{len(convs)}_conversations.md"
        filepath = os.path.join(args.out_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# ChatGPT Project (ID: {gizmo_id})\n\n")
            f.write("## Conversations in this Project:\n")
            for t in titles:
                f.write(f"- {t}\n")
            f.write("\n---\n\n")
            
            for conv in convs:
                f.write(format_conversation(conv))
                
        # Add to index
        index_content.append(f"## [{filename}]({filename})")
        index_content.append(f"**ID:** `{gizmo_id}` | **Conversations:** {len(convs)}")
        index_content.append("**Sample Conversations to help you identify this Project:**")
        for t in titles[:5]:
            index_content.append(f"- {t}")
        if len(titles) > 5:
            index_content.append(f"- *...and {len(titles)-5} more.*")
        index_content.append("\n")
        
        print(f"  ➜ Created {filename} ({len(convs)} conversations)")
        count += 1
        
    # Write the index file
    index_file = os.path.join(args.out_dir, "Projects_Index.md")
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(index_content))
        
    print(f"\n🎉 Done! Extracted {len(sorted_projects)} Projects to the '{args.out_dir}' folder.")
    print(f"   Open '{index_file}' to see a map of all your projects and their contents.")

if __name__ == "__main__":
    main()
