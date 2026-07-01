# Reddit Saved Saver

A modern, fast, and robust Python script for converting your saved posts and comments on Reddit into Markdown files with rich YAML frontmatter metadata. 

Originally built to backup saved Reddit content into note-taking tools like [Obsidian](https://obsidian.md), this tool has been entirely refactored to use state-of-the-art Python practices including robust logging, explicit type hints, f-strings, and modern dependency management with [`uv`](https://github.com/astral-sh/uv).

## Features

- **YAML Frontmatter**: Automatically tags files with standard YAML frontmatter for seamless integration with Obsidian, Logseq, Notion, and other modern knowledge-management platforms.
- **Robust Organization**: Automatically sorts saved posts and comments into a clean `reddit/<subreddit_name>` folder structure.
- **Limitless Pagination**: Extracts *all* available saved posts (up to Reddit's hard limit of 1000 items) by efficiently iterating through the Reddit API.
- **Modern Python Architecture**: Built with `pathlib`, `logging`, and explicit type hinting.
- **Secure Credentials**: Uses `.env` configuration, ensuring your sensitive Reddit API keys are never accidentally committed to version control.

## Prerequisites

- [Python 3.12+](https://www.python.org/)
- [`uv`](https://github.com/astral-sh/uv) (Extremely fast Python package and project manager)

## Setup and Usage

### 1. Create a Reddit App
You need a Reddit API key to authorize the script:
1. Go to your [Reddit App Preferences](https://old.reddit.com/prefs/apps/).
2. Create a new app, select **script**, and fill in the required fields (redirect URI can be `http://localhost:8080`).
3. Note your **Client ID** (under the app name) and **Client Secret**.

### 2. Configure Credentials
Copy the example environment file and fill in your details:
```bash
cp .env.example .env
```
Edit `.env` with your newly acquired Reddit Client ID and Secret, along with your normal Reddit username and password.

### 3. Run the Script
Because this project utilizes `uv`, you don't even need to manually install dependencies or create virtual environments. Simply execute:
```bash
uv run reddit-saved-saver.py
```
`uv` will automatically read `pyproject.toml`, establish a virtual environment, install the required packages (like `praw` and `python-dotenv`), and run the script in one lightning-fast step.

## Output

The script will automatically create a top-level `reddit/` directory. Inside, you will find directories named after subreddits. Each saved item (post or comment) will be generated as a discrete `.md` file containing its unique ID as the filename.
