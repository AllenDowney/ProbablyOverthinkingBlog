#!/usr/bin/env python3
"""
WordPress Blog Archive Downloader

Downloads all posts from a WordPress site using the REST API,
converts them to Markdown, and saves them in both JSON and Markdown formats.
Also downloads associated media files.
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse

import requests
import yaml
from bs4 import BeautifulSoup
import html2text


class WordPressDownloader:
    """Downloads and archives WordPress blog posts."""
    
    def __init__(
        self,
        base_url: str,
        output_dir: Path,
        username: Optional[str] = None,
        password: Optional[str] = None,
        rate_limit_delay: float = 0.5,
    ):
        """
        Initialize the WordPress downloader.
        
        Args:
            base_url: Base URL of the WordPress site (e.g., 'https://example.com')
            output_dir: Directory to save archived posts
            username: WordPress username for authentication (optional)
            password: WordPress application password for authentication (optional)
            rate_limit_delay: Delay between API requests in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.api_url = f"{self.base_url}/wp-json/wp/v2"
        self.output_dir = Path(output_dir)
        self.rate_limit_delay = rate_limit_delay
        
        # Create output directories
        self.posts_dir = self.output_dir / "posts"
        self.json_dir = self.output_dir / "json"
        self.media_dir = self.output_dir / "media"
        
        for dir_path in [self.posts_dir, self.json_dir, self.media_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Set up authentication if provided
        self.auth = None
        if username and password:
            self.auth = (username, password)
        
        # Session for connection pooling
        self.session = requests.Session()
        if self.auth:
            self.session.auth = self.auth
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> requests.Response:
        """
        Make an API request with rate limiting.
        
        Args:
            endpoint: API endpoint (relative to api_url)
            params: Query parameters
            
        Returns:
            Response object
        """
        url = f"{self.api_url}/{endpoint}"
        time.sleep(self.rate_limit_delay)
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        
        # Check if response is actually JSON
        content_type = response.headers.get('Content-Type', '')
        if 'application/json' not in content_type:
            print(f"Warning: Expected JSON but got Content-Type: {content_type}", file=sys.stderr)
            print(f"Response preview (first 500 chars): {response.text[:500]}", file=sys.stderr)
        
        return response
    
    def get_all_posts(self) -> List[Dict]:
        """
        Download all posts from the WordPress site using pagination.
        
        Returns:
            List of post dictionaries
        """
        all_posts = []
        page = 1
        per_page = 100  # Maximum allowed by WordPress API
        
        print(f"Downloading posts from {self.base_url}...")
        
        while True:
            try:
                params = {
                    'page': page,
                    'per_page': per_page,
                    '_embed': 'true',  # Include embedded resources (must be string, not boolean)
                }
                
                response = self._make_request('posts', params=params)
                
                # Try to parse JSON, with better error handling
                try:
                    posts = response.json()
                except json.JSONDecodeError as e:
                    print(f"Error: Failed to parse JSON response", file=sys.stderr)
                    print(f"Response status: {response.status_code}", file=sys.stderr)
                    print(f"Response headers: {dict(response.headers)}", file=sys.stderr)
                    print(f"Response preview (first 1000 chars): {response.text[:1000]}", file=sys.stderr)
                    raise
                
                if not posts:
                    break
                
                all_posts.extend(posts)
                print(f"  Downloaded page {page} ({len(posts)} posts, {len(all_posts)} total)")
                
                # Check if there are more pages
                total_pages = int(response.headers.get('X-WP-TotalPages', 1))
                if page >= total_pages:
                    break
                
                page += 1
                
            except requests.exceptions.RequestException as e:
                print(f"Error downloading posts: {e}", file=sys.stderr)
                if hasattr(e, 'response') and e.response is not None:
                    print(f"Response status: {e.response.status_code}", file=sys.stderr)
                    print(f"Response preview: {e.response.text[:500]}", file=sys.stderr)
                break
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}", file=sys.stderr)
                break
        
        print(f"Total posts downloaded: {len(all_posts)}")
        return all_posts
    
    def html_to_markdown(self, html_content: str) -> str:
        """
        Convert HTML content to Markdown.
        
        Args:
            html_content: HTML string
            
        Returns:
            Markdown string
        """
        # Use html2text for conversion
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = False
        h.body_width = 0  # Don't wrap lines
        return h.handle(html_content)
    
    def extract_media_urls(self, post: Dict) -> List[str]:
        """
        Extract media URLs from a post (featured image, embedded media, etc.).
        
        Args:
            post: Post dictionary from WordPress API
            
        Returns:
            List of media URLs
        """
        media_urls = []
        
        # Featured image
        if 'featured_media' in post and post['featured_media']:
            if '_embedded' in post and 'wp:featuredmedia' in post['_embedded']:
                featured = post['_embedded']['wp:featuredmedia'][0]
                if 'source_url' in featured:
                    media_urls.append(featured['source_url'])
        
        # Media in content (images, etc.)
        if 'content' in post and 'rendered' in post['content']:
            soup = BeautifulSoup(post['content']['rendered'], 'html.parser')
            for img in soup.find_all('img'):
                src = img.get('src')
                if src:
                    # Skip data URIs (base64-encoded images)
                    if src.startswith('data:'):
                        continue
                    # Convert relative URLs to absolute
                    if not src.startswith('http'):
                        src = urljoin(self.base_url, src)
                    media_urls.append(src)
        
        return media_urls
    
    def download_media(self, url: str) -> Optional[Path]:
        """
        Download a media file and save it locally.
        
        Args:
            url: URL of the media file
            
        Returns:
            Path to saved file, or None if download failed
        """
        try:
            response = self.session.get(url, stream=True)
            response.raise_for_status()
            
            # Extract filename from URL
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            if not filename:
                filename = f"media_{hash(url)}.jpg"
            
            # Save file
            file_path = self.media_dir / filename
            
            # Handle duplicate filenames
            counter = 1
            original_path = file_path
            while file_path.exists():
                stem = original_path.stem
                suffix = original_path.suffix
                file_path = self.media_dir / f"{stem}_{counter}{suffix}"
                counter += 1
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return file_path
            
        except Exception as e:
            # Truncate long URLs in error messages to avoid noise
            url_display = url if len(url) < 100 else url[:97] + "..."
            print(f"  Warning: Failed to download media {url_display}: {e}", file=sys.stderr)
            return None
    
    def post_exists(self, post_id: int, slug: str) -> bool:
        """
        Check if a post has already been downloaded.
        
        Args:
            post_id: Post ID
            slug: Post slug
            
        Returns:
            True if both JSON and Markdown files exist
        """
        json_path = self.json_dir / f"{post_id}_{slug}.json"
        markdown_path = self.posts_dir / f"{post_id}_{slug}.md"
        return json_path.exists() and markdown_path.exists()
    
    def save_post(self, post: Dict) -> None:
        """
        Save a post in both JSON and Markdown formats.
        
        Args:
            post: Post dictionary from WordPress API
        """
        post_id = post['id']
        slug = post.get('slug', f"post-{post_id}")
        
        # Prepare post data for JSON
        post_data = {
            'id': post_id,
            'title': post.get('title', {}).get('rendered', ''),
            'slug': slug,
            'date': post.get('date', ''),
            'modified': post.get('modified', ''),
            'status': post.get('status', ''),
            'link': post.get('link', ''),
            'content': post.get('content', {}).get('rendered', ''),
            'excerpt': post.get('excerpt', {}).get('rendered', ''),
            'author': post.get('author', ''),
            'featured_media': post.get('featured_media', 0),
            'categories': post.get('categories', []),
            'tags': post.get('tags', []),
            'format': post.get('format', 'standard'),
        }
        
        # Add embedded data if available
        if '_embedded' in post:
            post_data['_embedded'] = post['_embedded']
        
        # Save JSON
        json_path = self.json_dir / f"{post_id}_{slug}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(post_data, f, indent=2, ensure_ascii=False)
        
        # Convert to Markdown
        markdown_content = self._post_to_markdown(post_data)
        
        # Save Markdown
        markdown_path = self.posts_dir / f"{post_id}_{slug}.md"
        with open(markdown_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
    
    def _post_to_markdown(self, post_data: Dict) -> str:
        """
        Convert post data to Markdown format.
        
        Args:
            post_data: Post dictionary
            
        Returns:
            Markdown string
        """
        lines = []
        
        # Front matter
        lines.append("---")
        lines.append(f"id: {post_data['id']}")
        lines.append(f"title: {json.dumps(post_data['title'], ensure_ascii=False)}")
        lines.append(f"slug: {post_data['slug']}")
        lines.append(f"date: {post_data['date']}")
        lines.append(f"modified: {post_data['modified']}")
        lines.append(f"link: {post_data['link']}")
        lines.append(f"author: {post_data['author']}")
        lines.append(f"categories: {json.dumps(post_data['categories'])}")
        lines.append(f"tags: {json.dumps(post_data['tags'])}")
        lines.append("---")
        lines.append("")
        
        # Title
        lines.append(f"# {post_data['title']}")
        lines.append("")
        
        # Excerpt if available
        if post_data.get('excerpt'):
            excerpt_md = self.html_to_markdown(post_data['excerpt'])
            if excerpt_md.strip():
                lines.append(f"*{excerpt_md.strip()}*")
                lines.append("")
        
        # Content
        content_md = self.html_to_markdown(post_data['content'])
        lines.append(content_md)
        
        return "\n".join(lines)
    
    def download_all(self, skip_existing: bool = True) -> None:
        """
        Download all posts and media.
        
        Args:
            skip_existing: If True, skip posts that have already been downloaded
        """
        posts = self.get_all_posts()
        
        print(f"\nProcessing {len(posts)} posts...")
        
        skipped = 0
        processed = 0
        
        for i, post in enumerate(posts, 1):
            post_id = post['id']
            slug = post.get('slug', f"post-{post_id}")
            title = post.get('title', {}).get('rendered', f"Post {post_id}")
            
            # Check if post already exists
            if skip_existing and self.post_exists(post_id, slug):
                skipped += 1
                print(f"[{i}/{len(posts)}] Skipping (already exists): {title}")
                continue
            
            processed += 1
            print(f"[{i}/{len(posts)}] Processing: {title}")
            
            # Save post
            self.save_post(post)
            
            # Download media
            media_urls = self.extract_media_urls(post)
            if media_urls:
                for url in media_urls:
                    self.download_media(url)
        
        print(f"\nArchive complete! Posts saved to {self.output_dir}")
        if skip_existing:
            print(f"  Processed: {processed} posts, Skipped: {skipped} posts (already existed)")


def load_config(config_path: Path) -> Dict:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to config file
        
    Returns:
        Dictionary with configuration values
    """
    if not config_path.exists():
        return {}
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f) or {}
    
    return config


def main():
    """Main entry point."""
    # Default config file path (in project root)
    default_config_path = Path(__file__).parent.parent / 'config.yaml'
    
    parser = argparse.ArgumentParser(
        description="Download and archive WordPress blog posts"
    )
    parser.add_argument(
        'url',
        nargs='?',
        default=None,
        help='Base URL of the WordPress site (e.g., https://example.com). '
             'If not provided, will be read from config file.'
    )
    parser.add_argument(
        '-c', '--config',
        type=Path,
        default=default_config_path,
        help=f'Path to config file (default: {default_config_path})'
    )
    parser.add_argument(
        '-o', '--output',
        type=Path,
        default=None,
        help='Output directory for archived posts (overrides config file)'
    )
    parser.add_argument(
        '-u', '--username',
        help='WordPress username for authentication (overrides config file)'
    )
    parser.add_argument(
        '-p', '--password',
        help='WordPress application password for authentication (overrides config file)'
    )
    parser.add_argument(
        '--rate-limit',
        type=float,
        default=None,
        help='Delay between API requests in seconds (overrides config file)'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force re-download of all posts, even if they already exist'
    )
    
    args = parser.parse_args()
    
    # Load config from file
    config = load_config(args.config)
    wordpress_config = config.get('wordpress', {})
    settings_config = config.get('settings', {})
    
    # Get values: command line args override config file
    base_url = args.url or wordpress_config.get('url')
    if not base_url:
        print("Error: WordPress URL is required. Provide it as an argument or in the config file.", file=sys.stderr)
        sys.exit(1)
    
    username = args.username or wordpress_config.get('username') or None
    password = args.password or wordpress_config.get('password') or None
    
    # Empty strings should be treated as None
    if username == "":
        username = None
    if password == "":
        password = None
    
    output_dir = args.output or Path(settings_config.get('output_dir', 'archive/wordpress'))
    rate_limit = args.rate_limit or settings_config.get('rate_limit', 0.5)
    
    downloader = WordPressDownloader(
        base_url=base_url,
        output_dir=output_dir,
        username=username,
        password=password,
        rate_limit_delay=rate_limit,
    )
    
    try:
        downloader.download_all(skip_existing=not args.force)
    except KeyboardInterrupt:
        print("\nDownload interrupted by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

