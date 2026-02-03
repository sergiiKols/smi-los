"""
WordPress publishing module
"""
import requests
from requests.auth import HTTPBasicAuth
from typing import Dict, Optional
import logging
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WordPressPublisher:
    def __init__(self):
        self.base_url = config.WORDPRESS_URL.rstrip('/')
        self.api_url = f"{self.base_url}/wp-json/wp/v2"
        self.username = config.WORDPRESS_USERNAME
        self.password = config.WORDPRESS_PASSWORD
        self.auth = HTTPBasicAuth(self.username, self.password)
    
    def create_post(self, post_data: Dict) -> Optional[str]:
        """
        Create a new WordPress post
        
        Args:
            post_data: Dictionary containing:
                - title: Post title
                - content: Post content (HTML)
                - excerpt: Post excerpt
                - status: 'publish', 'draft', or 'pending'
                - tags: List of tag names
                - categories: List of category IDs
        
        Returns:
            Post ID if successful, None otherwise
        """
        endpoint = f"{self.api_url}/posts"
        
        # Prepare post payload
        payload = {
            'title': post_data.get('title', ''),
            'content': post_data.get('content', ''),
            'excerpt': post_data.get('excerpt', ''),
            'status': post_data.get('status', 'draft'),
        }
        
        # Handle tags
        if post_data.get('tags'):
            tag_ids = self._get_or_create_tags(post_data['tags'])
            payload['tags'] = tag_ids
        
        # Handle categories
        if post_data.get('categories'):
            payload['categories'] = post_data['categories']
        
        try:
            response = requests.post(
                endpoint,
                json=payload,
                auth=self.auth,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code in [200, 201]:
                post_id = response.json().get('id')
                logger.info(f"Successfully created WordPress post: {post_id}")
                return str(post_id)
            else:
                logger.error(f"Failed to create post: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating WordPress post: {e}")
            return None
    
    def _get_or_create_tags(self, tag_names: list) -> list:
        """Get or create tags and return their IDs"""
        tag_ids = []
        
        for tag_name in tag_names:
            # Check if tag exists
            search_url = f"{self.api_url}/tags?search={tag_name}"
            
            try:
                response = requests.get(search_url, auth=self.auth)
                
                if response.status_code == 200:
                    tags = response.json()
                    
                    if tags:
                        # Tag exists
                        tag_ids.append(tags[0]['id'])
                    else:
                        # Create new tag
                        create_url = f"{self.api_url}/tags"
                        create_response = requests.post(
                            create_url,
                            json={'name': tag_name},
                            auth=self.auth
                        )
                        
                        if create_response.status_code in [200, 201]:
                            tag_ids.append(create_response.json()['id'])
                        
            except Exception as e:
                logger.error(f"Error handling tag '{tag_name}': {e}")
                continue
        
        return tag_ids
    
    def update_post(self, post_id: str, post_data: Dict) -> bool:
        """Update an existing WordPress post"""
        endpoint = f"{self.api_url}/posts/{post_id}"
        
        try:
            response = requests.post(
                endpoint,
                json=post_data,
                auth=self.auth,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                logger.info(f"Successfully updated WordPress post: {post_id}")
                return True
            else:
                logger.error(f"Failed to update post: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error updating WordPress post: {e}")
            return False
    
    def format_blog_post(self, blog_data: Dict) -> str:
        """Format blog post content as HTML"""
        html = f"""
        <div class="blog-post">
            <div class="intro">
                {self._text_to_html(blog_data.get('intro', ''))}
            </div>
            
            <div class="body">
                {self._text_to_html(blog_data.get('body', ''))}
            </div>
            
            <div class="conclusion">
                {self._text_to_html(blog_data.get('conclusion', ''))}
            </div>
            
            <div class="cta">
                <p><strong>Свяжитесь с нами для профессиональной консультации!</strong></p>
                <p>Наши услуги: энергоаудит, тепловизионное обследование, испытания систем вентиляции.</p>
            </div>
        </div>
        """
        return html
    
    def _text_to_html(self, text: str) -> str:
        """Convert plain text to HTML paragraphs"""
        if not text:
            return ""
        
        paragraphs = text.split('\n\n')
        html_paragraphs = [f"<p>{p.strip()}</p>" for p in paragraphs if p.strip()]
        return '\n'.join(html_paragraphs)
