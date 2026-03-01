# ChatGPT to Claude Migration Guide

The definitive workflow to migrate your context, instructions, and history over to Claude using Google's NotebookLM.

## 1. Request everything from ChatGPT
Your first step is to get your data out of OpenAI. Head over to ChatGPT on your web browser. 
Navigate to **Settings** > **Data Controls** > **Export Data** and request an export. It may take a few minutes for them to compile it.

## 2. Download when it's ready
Check your email. OpenAI will send you a secure link to download a `.zip` file containing your data. Download it and extract the folder to your computer.
Inside, find the file named `conversations.json`. Move this file into the same directory as the Python scripts provided in this repository.

## 3. Run the monthly splitter
NotebookLM and Claude cannot ingest a massive JSON file directly. We need to split it into readable Markdown texts grouped by month.
Open your terminal in the repository folder and run:
```bash
python split_by_month.py
```
This will generate a new folder called `monthly_exports/`, filled with beautiful Markdown files labeled by month.

## 4. Extract ChatGPT Projects (Optional)
If you are a ChatGPT Plus or Team user, you've likely created "Projects" (or Custom GPTs) with multiple conversations inside. The official ChatGPT data export doesn't clearly label these, but it saves them as "gizmos" behind the scenes.
Run this script to analyze your export, group conversations by their original Projects, and create an index map so you can see which Project is which:
```bash
python extract_projects.py
```
This will create a `chatgpt_projects/` directory containing a Markdown file for each Project, plus a handy `Projects_Index.md` map.

## 5. Run the chunking script (Optional)
Google's NotebookLM has a strict upload limit of 500,000 words or 50MB per source. If you are a heavy ChatGPT user, your monthly chunks or project chunks might still be too large!
Run the secondary script to automatically slice large files into smaller parts:
```bash
python split_large_files.py monthly_exports
python split_large_files.py chatgpt_projects
```
It will safely split files without breaking conversations across files.

## 6. Take the files into NotebookLM (Optional)
Now, head over to [Google NotebookLM](https://notebooklm.google.com) and create a new notebook.
Drag and drop your generated Markdown files into the Sources panel. It will take a minute or two to index your entire chat history.

## 7. Extract useful data (Optional)
Use NotebookLM to analyze your history and build a robust **Project Knowledge** payload for Claude.
Try prompting NotebookLM with the following:
- *"Analyze these conversations and write a comprehensive 'Custom Instructions' guide that captures my communication style and preferences."*
- *"Summarize my ongoing projects and their current context based on my chat history over the last 3 months."*
- *"What are the most common formatting requirements I ask the AI to adhere to?"*

Copy NotebookLM's output, and paste it straight into Claude's **Project Knowledge** to hit the ground running!
