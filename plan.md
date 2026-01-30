# ProbablyOverthinkingBlog Archive Project

## Goal
Create an archival system for the "Probably Overthinking It" blog that downloads, stores, and makes searchable all blog posts from both the current WordPress site and the original Blogger site.

## Project Objectives

### 1. WordPress Blog Archive
- Develop scripts to use the WordPress API to download blog posts
- Archive blog posts in both Markdown and JSON formats
- Preserve all metadata (dates, tags, categories, authors)
- Download and archive associated media (images, attachments)

### 2. Blogger Archive
- Download older articles from the original Blogger site
- Convert Blogger posts to a consistent archival format
- Extract and preserve metadata from Blogger posts
- Ensure compatibility with the WordPress archive format

### 3. Search and Accessibility
- Create a searchable interface for archived content
- Index all blog posts for full-text search
- Maintain cross-references between related posts
- Generate navigation aids (table of contents, tag indexes, date indexes)

## Technical Approach

### WordPress API Integration
- Use WordPress REST API to retrieve posts
- Implement pagination for large post collections
- Handle rate limiting and API authentication
- Convert HTML content to Markdown format

### Blogger Archive Strategy
- Scrape or use Blogger API (if available)
- Parse HTML/XML feeds from Blogger
- Clean and normalize content
- Map Blogger metadata to standard schema

### Storage Format
- **JSON**: Complete post data with all metadata
- **Markdown**: Human-readable content for easy browsing and editing
- **Index files**: Separate indexes by date, tag, category for navigation

### Search Implementation
- Consider options: static site search, SQLite database, or full-text search engine
- Implement keyword search across all posts
- Support filtering by date, tags, and categories

## Implementation Phases

### Phase 1: Setup and Planning ✓
- [x] Copy Makefile and requirements from ProbablyOverthinkingIt repository
- [x] Initialize project plan document

### Phase 2: WordPress Downloader
- [ ] Research WordPress REST API endpoints
- [ ] Implement authentication (if required)
- [ ] Write script to download all posts
- [ ] Convert posts to Markdown format
- [ ] Save posts in JSON format with full metadata
- [ ] Download and archive media files

### Phase 3: Blogger Downloader
- [ ] Identify Blogger site URL and access method
- [ ] Determine best approach (API vs. scraping)
- [ ] Write script to download Blogger posts
- [ ] Convert and normalize Blogger content
- [ ] Match format to WordPress archive

### Phase 4: Search and Indexing
- [ ] Design search architecture
- [ ] Build content indexes
- [ ] Implement search functionality
- [ ] Create browsing interface (if needed)

### Phase 5: Documentation and Maintenance
- [ ] Document API usage and rate limits
- [ ] Create usage guide for archive
- [ ] Set up update procedures for new posts
- [ ] Add automated testing

## Next Steps
1. Research and document the WordPress API endpoints for "Probably Overthinking It"
2. Identify the URL and access method for the original Blogger site
3. Begin implementing the WordPress downloader script
