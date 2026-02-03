"""
Scheduler module for automated daily tasks
"""
import schedule
import time
import logging
from datetime import datetime
from typing import Callable
import config
from database import ArticleDatabase
from gemini_search import GeminiSearchEngine
from wordpress_publisher import WordPressPublisher
from social_media_publisher import SocialMediaManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ContentScheduler:
    def __init__(self):
        self.db = ArticleDatabase()
        self.gemini = GeminiSearchEngine()
        self.wp_publisher = WordPressPublisher()
        self.social_media = SocialMediaManager()
        
    def search_and_collect_articles(self):
        """Daily task: Search for articles and store in database"""
        logger.info("Starting daily article search...")
        
        total_found = 0
        
        for keyword in config.KEYWORDS:
            logger.info(f"Searching for keyword: {keyword}")
            
            try:
                articles = self.gemini.search_articles(keyword, num_results=5)
                
                for article in articles:
                    # Analyze article
                    analysis = self.gemini.analyze_article(article)
                    
                    # Prepare article data
                    article_data = {
                        'title': article.get('title', ''),
                        'url': article.get('source_type', ''),
                        'content': article.get('description', ''),
                        'source': 'Gemini Search',
                        'keywords': [keyword],
                        'ai_score': analysis['scores']['overall'],
                        'relevance_score': analysis['scores']['relevance'],
                        'analysis': analysis
                    }
                    
                    # Save to database
                    article_id = self.db.add_article(article_data)
                    
                    if article_id > 0:
                        total_found += 1
                        logger.info(f"Added article: {article_data['title']} (Score: {article_data['ai_score']})")
                    elif article_id == -1:
                        logger.info(f"Article already exists: {article_data['title']}")
                
                # Record search history
                self.db.add_search_history(keyword, len(articles))
                
                # Small delay to avoid rate limiting
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Error searching for keyword '{keyword}': {e}")
                continue
        
        logger.info(f"Daily search completed. Found {total_found} new articles.")
    
    def publish_to_blog(self):
        """Daily task: Publish best articles to WordPress blog"""
        logger.info("Starting blog publication task...")
        
        # Get top articles
        articles = self.db.get_pending_articles(limit=config.MAX_ARTICLES_PER_DAY)
        
        if not articles:
            logger.info("No articles to publish today.")
            return
        
        published_count = 0
        
        for article in articles:
            try:
                # Generate blog post
                blog_post = self.gemini.generate_blog_post(article)
                
                # Format content
                content_html = self.wp_publisher.format_blog_post(blog_post)
                
                # Prepare WordPress post
                post_data = {
                    'title': blog_post['title'],
                    'content': content_html,
                    'excerpt': blog_post['meta_description'],
                    'status': 'draft',  # Change to 'publish' for auto-publish
                    'tags': blog_post.get('tags', [])
                }
                
                # Publish to WordPress
                post_id = self.wp_publisher.create_post(post_data)
                
                if post_id:
                    # Update article status
                    self.db.update_article_status(article['id'], 'published')
                    
                    # Record publication
                    self.db.add_publication(article['id'], 'wordpress', post_id)
                    
                    published_count += 1
                    logger.info(f"Published to blog: {blog_post['title']}")
                    
                    # Store blog URL for social media
                    article['blog_url'] = f"{config.WORDPRESS_URL}/?p={post_id}"
                else:
                    logger.error(f"Failed to publish article: {article['title']}")
                
                time.sleep(5)  # Delay between posts
                
            except Exception as e:
                logger.error(f"Error publishing article {article['id']}: {e}")
                continue
        
        logger.info(f"Blog publication completed. Published {published_count} articles.")
    
    def publish_to_facebook(self):
        """Daily task: Publish to Facebook"""
        logger.info("Starting Facebook publication task...")
        
        # Get recently published articles
        articles = self.db.get_pending_articles(limit=1)
        
        if not articles:
            logger.info("No articles to publish to Facebook.")
            return
        
        for article in articles:
            try:
                # Get blog URL if published
                blog_url = article.get('blog_url', config.WORDPRESS_URL)
                
                # Publish to Facebook
                fb_post_id = self.social_media.facebook.create_post(
                    self.social_media.facebook.format_post_message(article, blog_url),
                    blog_url
                )
                
                if fb_post_id:
                    self.db.add_publication(article['id'], 'facebook', fb_post_id)
                    logger.info(f"Published to Facebook: {article['title']}")
                
            except Exception as e:
                logger.error(f"Error publishing to Facebook: {e}")
    
    def publish_to_instagram(self):
        """Daily task: Publish to Instagram"""
        logger.info("Starting Instagram publication task...")
        
        # Note: Instagram requires images
        logger.info("Instagram publication requires images - implement image generation or selection")
        # Implement image handling logic here
    
    def setup_schedule(self):
        """Setup all scheduled tasks"""
        # Daily article search
        schedule.every().day.at(f"{config.SEARCH_HOUR:02d}:{config.SEARCH_MINUTE:02d}").do(
            self.search_and_collect_articles
        )
        
        # Daily blog publication
        schedule.every().day.at(f"{config.BLOG_POST_HOUR:02d}:{config.BLOG_POST_MINUTE:02d}").do(
            self.publish_to_blog
        )
        
        # Daily Facebook publication
        schedule.every().day.at(f"{config.FACEBOOK_POST_HOUR:02d}:{config.FACEBOOK_POST_MINUTE:02d}").do(
            self.publish_to_facebook
        )
        
        # Daily Instagram publication
        schedule.every().day.at(f"{config.INSTAGRAM_POST_HOUR:02d}:{config.INSTAGRAM_POST_MINUTE:02d}").do(
            self.publish_to_instagram
        )
        
        logger.info("Schedule setup completed:")
        logger.info(f"  - Article search: {config.SEARCH_HOUR:02d}:{config.SEARCH_MINUTE:02d}")
        logger.info(f"  - Blog publication: {config.BLOG_POST_HOUR:02d}:{config.BLOG_POST_MINUTE:02d}")
        logger.info(f"  - Facebook publication: {config.FACEBOOK_POST_HOUR:02d}:{config.FACEBOOK_POST_MINUTE:02d}")
        logger.info(f"  - Instagram publication: {config.INSTAGRAM_POST_HOUR:02d}:{config.INSTAGRAM_POST_MINUTE:02d}")
    
    def run(self):
        """Start the scheduler"""
        self.setup_schedule()
        
        logger.info("Scheduler started. Press Ctrl+C to stop.")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user.")


def run_scheduler():
    """Main function to run the scheduler"""
    scheduler = ContentScheduler()
    scheduler.run()


if __name__ == '__main__':
    run_scheduler()
