# ChatGPT to Claude Migration Toolkit

A streamlined workflow to export your ChatGPT history and prepare it for Claude (via NotebookLM).

## The Goal

Moving from ChatGPT to Claude can mean leaving behind months (or years) of valuable, tailored conversations. This toolkit provides a lightweight set of Python scripts to extract your `conversations.json` from OpenAI, slice it by month, and prepare it for seamless ingestion into Google's NotebookLM. From there, you can query your entire chat history and extract the context Claude needs.

## Workflow Overview

1. **Request everything from ChatGPT:** Request your data export from OpenAI settings.
2. **Download your data:** You'll receive an email with a `.zip` file containing your history.
3. **Run the monthly splitter script:** Break the massive `conversations.json` file down into manageable, readable monthly Markdown files.
4. **(Optional) Run the large file chunking script:** If your monthly files exceed NotebookLM's 50MB (or 500k words) limits, break them down further automatically.
5. **(Optional) Import to NotebookLM:** Upload your chunked files as sources into a new NotebookLM project.
6. **(Optional) Extract insights:** Use NotebookLM to extract custom instructions, system prompts, and context to feed directly to Claude.

## Getting Started

> **For detailed, step-by-step visual instructions, open the included [guide.html](guide.html) file in your web browser.**

### Prerequisites
- Python 3.x
- Your ChatGPT Export folder (specifically `conversations.json`)

### Quick Start
```bash
# 1. Place conversations.json in the same directory as these scripts

# 2. Run the monthly splitter
python split_by_month.py

# 3. (Optional) If your monthly files exceed the NotebookLM limits, split them further
python split_large_files.py
```

## Contributing
Feel free to open issues or submit PRs if you want to improve the Python scripts or formatting!
