#!/usr/bin/env python3
"""
Blogger Takeout Archive Processor

Extracts and processes blog posts from Google Blogger Takeout archive.
Converts Blogger posts to match WordPress archive format (JSON + Markdown).
"""

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse, unquote
from xml.etree import ElementTree as ET

from bs4 import BeautifulSoup
import html2text


class BloggerProcessor:
    """Processes Blogger takeout archive and converts to WordPress format."""
    
    def __init__(self, takeout_zip: Path, output_dir: Path):
        """
        Initialize the Blogger processor.
        
        Args:
            takeout_zip: Path to Blogger takeout ZIP file
            output_dir: Directory to save processed posts
        """
        self.takeout_zip = Path(takeout_zip)
        self.output_dir = Path(output_dir)
        
        # Create output directories
        self.posts_dir = self.output_dir / "posts"
        self.json_dir = self.output_dir / "json"
        self.media_dir = self.output_dir / "media"
        
        for dir_path in [self.posts_dir, self.json_dir, self.media_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # HTML to Markdown converter
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = False
        self.html_converter.body_width = 0
    
    def extract_feed(self, blog_name: str = "Probably Overthinking It") -> ET.Element:
        """
        Extract and parse the Atom feed from the takeout archive.
        
        Args:
            blog_name: Name of the blog to extract
            
        Returns:
            Parsed XML root element
        """
        feed_path = f"Takeout/Blogger/Blogs/{blog_name}/feed.atom"
        
        print(f"Extracting feed from {self.takeout_zip}...")
        with zipfile.ZipFile(self.takeout_zip, 'r') as zip_ref:
            if feed_path not in zip_ref.namelist():
                raise FileNotFoundError(f"Feed not found: {feed_path}")
            
            feed_content = zip_ref.read(feed_path)
        
        print(f"Parsing Atom feed ({len(feed_content)} bytes)...")
        root = ET.fromstring(feed_content)
        return root
    
    def parse_entry(self, entry: ET.Element) -> Dict:
        """
        Parse a single Atom entry (blog post) into a structured dictionary.
        
        Args:
            entry: XML element representing a blog post entry
            
        Returns:
            Dictionary with post data
        """
        # Extract basic fields
        post_data = {}
        
        # Title
        title_elem = entry.find('{http://www.w3.org/2005/Atom}title')
        post_data['title'] = title_elem.text if title_elem is not None else ''
        
        # ID (Blogger post ID)
        id_elem = entry.find('{http://www.w3.org/2005/Atom}id')
        post_data['id'] = id_elem.text if id_elem is not None else ''
        
        # Extract Blogger post ID from tag:blogger.com,1999:blog-xxx.post-yyy
        blogger_id = None
        if post_data['id']:
            match = re.search(r'post-(\d+)', post_data['id'])
            if match:
                blogger_id = match.group(1)
        
        # Published date
        published_elem = entry.find('{http://www.w3.org/2005/Atom}published')
        post_data['date'] = published_elem.text if published_elem is not None else ''
        
        # Updated date
        updated_elem = entry.find('{http://www.w3.org/2005/Atom}updated')
        post_data['modified'] = updated_elem.text if updated_elem is not None else post_data['date']
        
        # Link (permalink)
        link_elem = entry.find('{http://www.w3.org/2005/Atom}link[@rel="alternate"]')
        post_data['link'] = link_elem.get('href') if link_elem is not None else ''
        
        # Content
        content_elem = entry.find('{http://www.w3.org/2005/Atom}content')
        if content_elem is not None:
            # Handle both text content and CDATA sections
            post_data['content'] = content_elem.text or ''
        else:
            post_data['content'] = ''
        
        # Labels (tags/categories in Blogger)
        labels = []
        for category in entry.findall('{http://www.w3.org/2005/Atom}category'):
            term = category.get('term')
            if term:
                labels.append(term)
        post_data['labels'] = labels
        
        # Author
        author_elem = entry.find('{http://www.w3.org/2005/Atom}author')
        if author_elem is not None:
            name_elem = author_elem.find('{http://www.w3.org/2005/Atom}name')
            post_data['author'] = name_elem.text if name_elem is not None else ''
        else:
            post_data['author'] = ''
        
        # Generate slug from title
        slug = self._title_to_slug(post_data['title'])
        post_data['slug'] = slug
        
        # Store Blogger ID for reference
        post_data['blogger_id'] = blogger_id
        
        return post_data
    
    def _title_to_slug(self, title: str) -> str:
        """Convert title to URL-friendly slug."""
        if not title:
            return 'untitled'
        
        # Convert to lowercase and replace spaces with hyphens
        slug = title.lower()
        slug = re.sub(r'[^\w\s-]', '', slug)  # Remove special chars
        slug = re.sub(r'[-\s]+', '-', slug)  # Replace spaces/hyphens with single hyphen
        slug = slug.strip('-')  # Remove leading/trailing hyphens
        
        return slug[:100]  # Limit length
    
    def extract_media_urls(self, content: str) -> List[str]:
        """
        Extract media URLs from HTML content.
        
        Args:
            content: HTML content string
            
        Returns:
            List of media URLs
        """
        media_urls = []
        if not content:
            return media_urls
        
        soup = BeautifulSoup(content, 'html.parser')
        
        for img in soup.find_all('img'):
            src = img.get('src')
            if src and not src.startswith('data:'):
                # Convert relative URLs to absolute if needed
                if not src.startswith('http'):
                    # Blogger images are usually absolute, but handle relative just in case
                    continue
                media_urls.append(src)
        
        return media_urls
    
    def save_post(self, post_data: Dict) -> None:
        """
        Save a post in both JSON and Markdown formats (matching WordPress format).
        
        Args:
            post_data: Post dictionary
        """
        # Use Blogger ID or slug for filename
        if post_data.get('blogger_id'):
            file_id = post_data['blogger_id']
        else:
            file_id = post_data.get('slug', 'untitled')
        
        # Prepare JSON data (matching WordPress schema)
        json_data = {
            'id': post_data.get('blogger_id', ''),
            'title': post_data.get('title', ''),
            'slug': post_data.get('slug', ''),
            'date': post_data.get('date', ''),
            'modified': post_data.get('modified', ''),
            'status': 'publish',  # Blogger posts are published
            'link': post_data.get('link', ''),
            'content': post_data.get('content', ''),
            'excerpt': '',  # Blogger doesn't have separate excerpts
            'author': post_data.get('author', ''),
            'featured_media': 0,
            'categories': [],  # Will map from labels
            'tags': post_data.get('labels', []),  # Blogger labels become tags
            'format': 'standard',
            'source': 'blogger',  # Mark as Blogger source
            'blogger_id': post_data.get('blogger_id', ''),
        }
        
        # Save JSON
        json_path = self.json_dir / f"{file_id}_{post_data['slug']}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        # Convert to Markdown
        markdown_content = self._post_to_markdown(json_data)
        
        # Save Markdown
        markdown_path = self.posts_dir / f"{file_id}_{post_data['slug']}.md"
        with open(markdown_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
    
    def _post_to_markdown(self, post_data: Dict) -> str:
        """
        Convert post data to Markdown format (matching WordPress format).
        
        Args:
            post_data: Post dictionary
            
        Returns:
            Markdown string
        """
        lines = []
        
        # Front matter
        lines.append("---")
        lines.append(f"id: {post_data.get('id', '')}")
        lines.append(f"title: {json.dumps(post_data.get('title', ''), ensure_ascii=False)}")
        lines.append(f"slug: {post_data.get('slug', '')}")
        lines.append(f"date: {post_data.get('date', '')}")
        lines.append(f"modified: {post_data.get('modified', '')}")
        lines.append(f"link: {post_data.get('link', '')}")
        lines.append(f"author: {post_data.get('author', '')}")
        lines.append(f"tags: {json.dumps(post_data.get('tags', []))}")
        lines.append(f"source: blogger")
        if post_data.get('blogger_id'):
            lines.append(f"blogger_id: {post_data.get('blogger_id', '')}")
        lines.append("---")
        lines.append("")
        
        # Title
        lines.append(f"# {post_data.get('title', '')}")
        lines.append("")
        
        # Content (handle None values)
        content = post_data.get('content') or ''
        if content:
            content_md = self.html_converter.handle(content)
            lines.append(content_md)
        
        return "\n".join(lines)
    
    def process_all(self, blog_name: str = "Probably Overthinking It", skip_existing: bool = True) -> None:
        """
        Process all posts from the Blogger takeout archive.
        
        Args:
            blog_name: Name of the blog to process
            skip_existing: If True, skip posts that already exist
        """
        # Extract and parse feed
        root = self.extract_feed(blog_name)
        
        # Find all entries (filter for actual posts, not comments)
        all_entries = root.findall('{http://www.w3.org/2005/Atom}entry')
        entries = []
        for entry in all_entries:
            # Check if this is a post (not a comment)
            blogger_type = entry.find('{http://schemas.google.com/blogger/2018}type')
            if blogger_type is None or blogger_type.text == 'POST':
                entries.append(entry)
        
        print(f"Found {len(entries)} posts in feed (filtered from {len(all_entries)} total entries)")
        
        processed = 0
        skipped = 0
        
        for i, entry in enumerate(entries, 1):
            post_data = self.parse_entry(entry)
            title = post_data.get('title', f"Post {i}")
            
            # Check if already exists
            if skip_existing:
                file_id = post_data.get('blogger_id', post_data.get('slug', 'untitled'))
                json_path = self.json_dir / f"{file_id}_{post_data['slug']}.json"
                markdown_path = self.posts_dir / f"{file_id}_{post_data['slug']}.md"
                
                if json_path.exists() and markdown_path.exists():
                    skipped += 1
                    print(f"[{i}/{len(entries)}] Skipping (already exists): {title}")
                    continue
            
            processed += 1
            print(f"[{i}/{len(entries)}] Processing: {title}")
            
            # Save post
            self.save_post(post_data)
            
            # Extract and note media URLs (we'll download them separately if needed)
            media_urls = self.extract_media_urls(post_data.get('content', ''))
            if media_urls:
                # Store media URLs in a separate file for later download
                media_list_path = self.media_dir / f"{post_data.get('blogger_id', post_data['slug'])}_media.json"
                with open(media_list_path, 'w', encoding='utf-8') as f:
                    json.dump(media_urls, f, indent=2)
        
        print(f"\nProcessing complete!")
        print(f"  Processed: {processed} posts")
        if skip_existing:
            print(f"  Skipped: {skipped} posts (already existed)")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Process Blogger takeout archive and convert to WordPress format"
    )
    parser.add_argument(
        'takeout_zip',
        type=Path,
        help='Path to Blogger takeout ZIP file'
    )
    parser.add_argument(
        '-o', '--output',
        type=Path,
        default=Path('archive/blogger'),
        help='Output directory for processed posts (default: archive/blogger)'
    )
    parser.add_argument(
        '--blog-name',
        default='Probably Overthinking It',
        help='Name of the blog to process (default: Probably Overthinking It)'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force re-processing of all posts, even if they already exist'
    )
    
    args = parser.parse_args()
    
    processor = BloggerProcessor(
        takeout_zip=args.takeout_zip,
        output_dir=args.output
    )
    
    try:
        processor.process_all(
            blog_name=args.blog_name,
            skip_existing=not args.force
        )
    except KeyboardInterrupt:
        print("\nProcessing interrupted by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

