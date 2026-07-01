import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Union

import praw
from dotenv import load_dotenv
from praw.models import Comment, Submission

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def get_reddit_instance() -> praw.Reddit:
    """Initialize and return a praw.Reddit instance using environment variables."""
    client_id = os.environ.get("REDDIT_CLIENT_ID")
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET")
    username = os.environ.get("REDDIT_USERNAME")
    password = os.environ.get("REDDIT_PASSWORD")

    if not all([client_id, client_secret, username, password]):
        logging.error("Missing Reddit credentials in .env file. Please check your .env configuration.")
        sys.exit(1)

    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password,
        user_agent="Reddit Saved Saver by /u/tobiasvl (modernized)"
    )


def format_markdown(item: Union[Submission, Comment]) -> str:
    """Format a saved Reddit item into a Markdown string with YAML frontmatter."""
    subreddit_name = item.subreddit.display_name
    timestamp = datetime.fromtimestamp(item.created_utc, tz=timezone.utc)
    
    # Handle deleted users securely
    author_name = "[deleted]"
    if getattr(item, "author", None):
        author_name = f"/u/{item.author.name}"
        
    frontmatter = (
        "---\n"
        f"id: {item.id}\n"
        f"subreddit: /r/{subreddit_name}\n"
        f"timestamp: {timestamp}\n"
        f"author: {author_name}\n"
        f"tags: [reddit, {subreddit_name}]\n"
        f"permalink: https://reddit.com{item.permalink}\n"
        "---\n\n"
    )
    
    content = ""
    if isinstance(item, Submission):
        content += f"# {item.title}\n\n"
        if getattr(item, "is_self", False):
            content += str(getattr(item, "selftext", ""))
        else:
            content += str(getattr(item, "url", ""))
    elif isinstance(item, Comment):
        content += str(getattr(item, "body", ""))
        
    return f"{frontmatter}{content}\n\n"


def main() -> None:
    """Main execution function."""
    load_dotenv()
    
    reddit = get_reddit_instance()
    
    logging.info("Fetching saved posts and comments (this might take a moment depending on the number of items)...")
    
    try:
        # limit=None fetches all available saved items (Reddit API caps this at ~1000)
        saved_items = reddit.user.me().saved(limit=None)
    except Exception as e:
        logging.error(f"Failed to fetch saved posts. Check your credentials. Error: {e}")
        sys.exit(1)
        
    output_dir = Path("reddit")
    output_dir.mkdir(exist_ok=True)
    
    saved_count = 0
    for item in saved_items:
        subreddit_name = item.subreddit.display_name
        # Some subreddits might have characters not allowed in filepaths depending on OS, but standard Reddit subs are alphanumeric and underscores.
        sub_dir = output_dir / subreddit_name
        sub_dir.mkdir(exist_ok=True)
        
        file_path = sub_dir / f"{item.id}.md"
        markdown_content = format_markdown(item)
        
        file_path.write_text(markdown_content, encoding="utf-8")
        saved_count += 1
        
    logging.info(f"Successfully saved {saved_count} items to '{output_dir}/'.")


if __name__ == "__main__":
    main()
