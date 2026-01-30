# WordPress Downloader Script

## Overview

The `download_wordpress.py` script downloads all posts from a WordPress site using the WordPress REST API, converts them to Markdown format, and saves them in both JSON and Markdown formats. It also downloads associated media files.

## Configuration File

The easiest way to use the script is with a configuration file. Copy `config.example.yaml` to `config.yaml` and fill in your WordPress site details:

```bash
cp config.example.yaml config.yaml
```

Edit `config.yaml` with your WordPress site URL, username, and password:

```yaml
wordpress:
  url: https://your-site.com
  username: your_username
  password: your_application_password

settings:
  rate_limit: 0.5
  output_dir: archive/wordpress
```

**Note:** 
- The `config.yaml` file is in `.gitignore` to prevent committing credentials
- WordPress requires an "Application Password" for API authentication, not your regular login password. You can create one in your WordPress admin panel under Users → Profile → Application Passwords
- Leave `username` and `password` empty if authentication is not needed

## Usage

### Using Config File (Recommended)

Once you've set up `config.yaml`, simply run:

```bash
python scripts/download_wordpress.py
```

### Command Line Arguments

You can also provide settings via command line arguments, which will override the config file:

#### Basic Usage (Public Site)

```bash
python scripts/download_wordpress.py https://example.com
```

#### With Authentication

```bash
python scripts/download_wordpress.py https://example.com \
    --username your_username \
    --password your_application_password
```

#### Custom Config File

```bash
python scripts/download_wordpress.py --config /path/to/config.yaml
```

#### Override Settings

```bash
python scripts/download_wordpress.py \
    --output /custom/path \
    --rate-limit 1.0
```

#### Resume Interrupted Downloads

By default, the script will skip posts that have already been downloaded (checks for both JSON and Markdown files). To force re-download of all posts:

```bash
python scripts/download_wordpress.py --force
```

### Custom Output Directory

```bash
python scripts/download_wordpress.py https://example.com \
    --output /path/to/archive
```

### Rate Limiting

Adjust the delay between API requests (default: 0.5 seconds):

```bash
python scripts/download_wordpress.py https://example.com \
    --rate-limit 1.0
```

## Output Structure

The script creates the following directory structure:

```
archive/wordpress/
├── posts/          # Markdown files (one per post)
├── json/           # JSON files with full metadata (one per post)
└── media/          # Downloaded media files (images, etc.)
```

## Post Format

### Markdown Files

Each post is saved as a Markdown file with YAML front matter:

```markdown
---
id: 123
title: "Post Title"
slug: post-slug
date: 2024-01-01T00:00:00
modified: 2024-01-02T00:00:00
link: https://example.com/post-slug
author: 1
categories: [1, 2]
tags: [3, 4]
---

# Post Title

*Excerpt text*

Post content in Markdown format...
```

### JSON Files

Each post is saved as a JSON file with complete metadata:

```json
{
  "id": 123,
  "title": "Post Title",
  "slug": "post-slug",
  "date": "2024-01-01T00:00:00",
  "modified": "2024-01-02T00:00:00",
  "status": "publish",
  "link": "https://example.com/post-slug",
  "content": "<html>...</html>",
  "excerpt": "<html>...</html>",
  "author": 1,
  "featured_media": 456,
  "categories": [1, 2],
  "tags": [3, 4],
  "format": "standard",
  "_embedded": { ... }
}
```

## Features

- **Pagination**: Automatically handles pagination to download all posts
- **Rate Limiting**: Configurable delay between requests to avoid overwhelming the server
- **Media Download**: Downloads featured images and images embedded in post content
- **Dual Format**: Saves posts in both human-readable Markdown and complete JSON formats
- **Metadata Preservation**: Preserves all WordPress metadata (dates, tags, categories, authors)

## Requirements

- Python 3.11+
- Dependencies listed in `environment.yml`:
  - `requests` - For API calls
  - `beautifulsoup4` - For HTML parsing
  - `html2text` - For HTML to Markdown conversion

## WordPress REST API

The script uses the WordPress REST API v2 endpoints:

- `GET /wp-json/wp/v2/posts` - Retrieve posts
- Supports pagination via `page` and `per_page` parameters
- Uses `_embed` parameter to include related resources

## Error Handling

The script handles:
- Network errors and retries
- Rate limiting (with configurable delays)
- Missing or malformed data
- Media download failures (warns but continues)

## Next Steps

After downloading posts, you can:
1. Review the Markdown files in `archive/wordpress/posts/`
2. Use the JSON files for programmatic access
3. Set up search and indexing (Phase 4 of the project)

