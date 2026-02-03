"""
Social media publishing module for Facebook and Instagram
"""
import requests
from typing import Dict, Optional
import logging
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FacebookPublisher:
    def __init__(self):
        self.access_token = config.FACEBOOK_ACCESS_TOKEN
        self.page_id = config.FACEBOOK_PAGE_ID
        self.api_version = 'v18.0'
        self.base_url = f'https://graph.facebook.com/{self.api_version}'
    
    def create_post(self, message: str, link: Optional[str] = None) -> Optional[str]:
        """
        Create a Facebook page post
        
        Args:
            message: Post text
            link: Optional link to share
        
        Returns:
            Post ID if successful, None otherwise
        """
        endpoint = f"{self.base_url}/{self.page_id}/feed"
        
        payload = {
            'message': message,
            'access_token': self.access_token
        }
        
        if link:
            payload['link'] = link
        
        try:
            response = requests.post(endpoint, data=payload)
            
            if response.status_code == 200:
                post_id = response.json().get('id')
                logger.info(f"Successfully created Facebook post: {post_id}")
                return post_id
            else:
                logger.error(f"Failed to create Facebook post: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating Facebook post: {e}")
            return None
    
    def create_photo_post(self, message: str, image_url: str) -> Optional[str]:
        """Create a Facebook post with an image"""
        endpoint = f"{self.base_url}/{self.page_id}/photos"
        
        payload = {
            'message': message,
            'url': image_url,
            'access_token': self.access_token
        }
        
        try:
            response = requests.post(endpoint, data=payload)
            
            if response.status_code == 200:
                post_id = response.json().get('id')
                logger.info(f"Successfully created Facebook photo post: {post_id}")
                return post_id
            else:
                logger.error(f"Failed to create photo post: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating Facebook photo post: {e}")
            return None
    
    def format_post_message(self, article: Dict, blog_url: Optional[str] = None) -> str:
        """Format article for Facebook post"""
        title = article.get('title', '')
        description = article.get('description', '')[:200]
        
        message = f"""📢 {title}

{description}...

Читайте полную статью на нашем сайте! 👇
"""
        
        if blog_url:
            message += f"\n{blog_url}"
        
        message += "\n\n#энергоаудит #тепловизия #вентиляция #теплопотери #энергоэффективность"
        
        return message


class InstagramPublisher:
    def __init__(self):
        self.access_token = config.INSTAGRAM_ACCESS_TOKEN
        self.account_id = config.INSTAGRAM_BUSINESS_ACCOUNT_ID
        self.api_version = 'v18.0'
        self.base_url = f'https://graph.facebook.com/{self.api_version}'
    
    def create_post(self, image_url: str, caption: str) -> Optional[str]:
        """
        Create an Instagram post
        Note: Instagram requires images for posts
        
        Args:
            image_url: URL of the image to post
            caption: Post caption
        
        Returns:
            Media ID if successful, None otherwise
        """
        # Step 1: Create media container
        container_endpoint = f"{self.base_url}/{self.account_id}/media"
        
        container_payload = {
            'image_url': image_url,
            'caption': caption,
            'access_token': self.access_token
        }
        
        try:
            # Create container
            container_response = requests.post(container_endpoint, data=container_payload)
            
            if container_response.status_code != 200:
                logger.error(f"Failed to create Instagram container: {container_response.text}")
                return None
            
            container_id = container_response.json().get('id')
            
            # Step 2: Publish media
            publish_endpoint = f"{self.base_url}/{self.account_id}/media_publish"
            publish_payload = {
                'creation_id': container_id,
                'access_token': self.access_token
            }
            
            publish_response = requests.post(publish_endpoint, data=publish_payload)
            
            if publish_response.status_code == 200:
                media_id = publish_response.json().get('id')
                logger.info(f"Successfully created Instagram post: {media_id}")
                return media_id
            else:
                logger.error(f"Failed to publish Instagram media: {publish_response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating Instagram post: {e}")
            return None
    
    def format_post_caption(self, article: Dict) -> str:
        """Format article for Instagram caption"""
        title = article.get('title', '')
        description = article.get('description', '')[:150]
        
        caption = f"""{title}

{description}...

Больше информации на нашем сайте energo-audit.by

#энергоаудит #тепловизия #вентиляция #теплопотери #энергоэффективность #дом #ремонт #стройка #беларусь
"""
        
        return caption
    
    def create_carousel_post(self, image_urls: list, caption: str) -> Optional[str]:
        """Create an Instagram carousel post with multiple images"""
        # Note: This is a simplified version
        # Real implementation would require creating multiple media containers
        logger.info("Carousel posts require additional implementation")
        return None


class SocialMediaManager:
    def __init__(self):
        self.facebook = FacebookPublisher()
        self.instagram = InstagramPublisher()
    
    def publish_to_all(self, article: Dict, blog_url: Optional[str] = None, 
                      image_url: Optional[str] = None) -> Dict[str, Optional[str]]:
        """
        Publish article to all social media platforms
        
        Returns:
            Dictionary with platform names and post IDs
        """
        results = {}
        
        # Publish to Facebook
        fb_message = self.facebook.format_post_message(article, blog_url)
        
        if image_url:
            fb_post_id = self.facebook.create_photo_post(fb_message, image_url)
        else:
            fb_post_id = self.facebook.create_post(fb_message, blog_url)
        
        results['facebook'] = fb_post_id
        
        # Publish to Instagram (requires image)
        if image_url:
            ig_caption = self.instagram.format_post_caption(article)
            ig_post_id = self.instagram.create_post(image_url, ig_caption)
            results['instagram'] = ig_post_id
        else:
            logger.warning("Instagram post skipped: image required")
            results['instagram'] = None
        
        return results
