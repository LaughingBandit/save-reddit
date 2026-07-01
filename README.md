Reddit Saved Saver
==================

A simple Python script for converting your saved posts and comments on Reddit to Markdown files with YAML frontmatter metadata.

I made this to dump all my saved Reddit stuff into [Obsidian](https://obsidian.md). It's not at all customizable or user friendly right now.

Usage
-----

You need to create a Reddit app on https://old.reddit.com/prefs/apps/ and then put the client ID, secret key, as well as your Reddit username and password into a `.env` file (see `.env.example`).

Run the script using `uv`: `uv run reddit-saved-saver.py`. This will automatically handle dependencies for you!

The script will create a directory called `reddit` and then make a new subdirectory per subreddit.
