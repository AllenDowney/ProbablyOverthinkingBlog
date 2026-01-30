# Probably Overthinking It Blog Archive

A complete archival system for the "Probably Overthinking It" blog, preserving all posts from both the current WordPress site and the original Blogger site in a searchable, accessible format.

## Overview

This project downloads, archives, and makes searchable all blog posts from Allen Downey's "Probably Overthinking It" blog. The archive includes:

- **176 WordPress posts** (current blog)
- **193 Blogger posts** (historical archive)
- **369 total posts** across both platforms
- **46MB** of archived content including media files

All posts are stored in a unified format (JSON + Markdown) that enables easy searching, browsing, and preservation.

## Project Status

- ✅ **Phase 1:** Setup and Planning
- ✅ **Phase 2:** WordPress Downloader (176 posts, 371 media files)
- ✅ **Phase 3:** Blogger Downloader (193 posts, matching format)
- 🔄 **Phase 4:** Search and Indexing (in progress)
- ⏳ **Phase 5:** Documentation and Maintenance

## Archive Structure

```
archive/
├── wordpress/
│   ├── posts/          # 176 Markdown files
│   ├── json/           # 176 JSON files with metadata
│   └── media/          # 371 downloaded media files
├── blogger/
│   ├── posts/          # 193 Markdown files
│   ├── json/           # 193 JSON files with metadata
│   └── media/          # Media URL lists
└── search.db           # SQLite search index (Phase 4)
```

## Features

### WordPress Archive
- Downloads posts via WordPress REST API
- Preserves all metadata (dates, tags, categories, authors)
- Converts HTML to Markdown for readability
- Downloads associated media files
- Resume capability for interrupted downloads

### Blogger Archive
- Processes Google Blogger Takeout archives
- Extracts posts from Atom XML feeds
- Converts Blogger labels to WordPress tags
- Maintains format compatibility with WordPress archive

### Unified Format
- **JSON files:** Complete metadata and HTML content
- **Markdown files:** Human-readable content with YAML front matter
- **Consistent schema:** Both sources use the same data structure
- **Source tracking:** Posts marked with `source: "wordpress"` or `source: "blogger"`

## Quick Start

### Prerequisites

1. **Create conda environment:**
   ```bash
   make create_environment
   conda activate ProbablyOverthinkingBlog
   ```

2. **Configure WordPress credentials** (optional):
   ```bash
   cp config.example.yaml config.yaml
   # Edit config.yaml with your WordPress site details
   ```

### Download WordPress Posts

```bash
# Using config file (recommended)
python scripts/download_wordpress.py

# Or with command-line arguments
python scripts/download_wordpress.py https://www.allendowney.com/blog/
```

### Process Blogger Takeout

```bash
# Process Blogger takeout archive
python scripts/process_blogger_takeout.py takeout-*.zip
```

### Search Archive (Phase 4)

```bash
# Build search index
python scripts/build_search_index.py

# Search posts
python scripts/search.py "bayesian statistics"
```

## Scripts

### `scripts/download_wordpress.py`
Downloads posts from WordPress using the REST API.

**Features:**
- Automatic pagination
- Rate limiting
- Media file downloading
- Resume capability
- Config file support

See [scripts/README.md](scripts/README.md) for detailed documentation.

### `scripts/process_blogger_takeout.py`
Processes Google Blogger Takeout archives and converts to WordPress format.

**Features:**
- Extracts posts from Atom XML feeds
- Filters out comments (posts only)
- Converts HTML to Markdown
- Maps Blogger labels to tags
- Preserves all metadata

### `scripts/build_search_index.py` (Phase 4)
Builds SQLite search index from all archived posts.

### `scripts/search.py` (Phase 4)
Command-line search tool with filtering capabilities.

## Configuration

### WordPress Configuration

Edit `config.yaml`:

```yaml
wordpress:
  url: https://www.allendowney.com/blog/
  username: your_username
  password: your_application_password

settings:
  rate_limit: 0.5
  output_dir: archive/wordpress
```

**Note:** `config.yaml` is in `.gitignore` to protect credentials.

## Post Format

### Markdown Files

Each post is saved with YAML front matter:

```markdown
---
id: 123
title: "Post Title"
slug: post-slug
date: 2024-01-01T00:00:00
modified: 2024-01-02T00:00:00
link: https://example.com/post-slug
author: Allen Downey
tags: ["bayesian-statistics", "python"]
source: wordpress
---

# Post Title

Post content in Markdown format...
```

### JSON Files

Complete metadata in structured format:

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
  "author": "Allen Downey",
  "tags": ["bayesian-statistics", "python"],
  "categories": [],
  "source": "wordpress"
}
```

## Development

### Environment Setup

```bash
# Create conda environment
make create_environment

# Activate environment
conda activate ProbablyOverthinkingBlog

# Update environment
make install
```

### Project Structure

```
.
├── archive/              # Archived posts and media
├── scripts/              # Processing scripts
├── indexes/              # Navigation indexes (Phase 4)
├── config.yaml           # Configuration (gitignored)
├── config.example.yaml   # Configuration template
├── environment.yml       # Conda environment
├── Makefile              # Build commands
└── plan.md               # Project plan
```

## Documentation

- [Project Plan](plan.md) - Overall project goals and phases
- [Phase 3 Plan](PHASE3_PLAN.md) - Blogger archive processing details
- [Phase 4 Plan](PHASE4_PLAN.md) - Search and indexing strategy
- [Scripts README](scripts/README.md) - Detailed script documentation

## Requirements

- Python 3.11+
- Dependencies (see `environment.yml`):
  - `requests` - HTTP requests
  - `beautifulsoup4` - HTML parsing
  - `html2text` - HTML to Markdown conversion
  - `pyyaml` - Configuration file parsing

## License

See [LICENSE](LICENSE) file.

## Contributing

This is a personal archive project. For questions or suggestions, please open an issue.

## Acknowledgments

- WordPress REST API for post retrieval
- Google Blogger Takeout for historical archive export
- All posts by Allen Downey on "Probably Overthinking It"
