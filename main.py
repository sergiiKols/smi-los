#!/usr/bin/env python3
"""
Main entry point for the content search and publishing system
"""
import argparse
import sys
import os
from pathlib import Path
import logging
from scheduler import ContentScheduler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def ensure_directories():
    """Ensure required directories exist"""
    directories = ['data', 'logs']
    for dir_name in directories:
        Path(dir_name).mkdir(exist_ok=True)

def main():
    parser = argparse.ArgumentParser(
        description='Content Search and Publishing System for energo-audit.by'
    )
    
    parser.add_argument(
        '--mode',
        choices=['scheduler', 'search', 'publish-blog', 'publish-social', 'test'],
        default='scheduler',
        help='Operation mode'
    )
    
    parser.add_argument(
        '--test-keyword',
        type=str,
        help='Test search with a specific keyword'
    )
    
    args = parser.parse_args()
    
    # Ensure directories exist
    ensure_directories()
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        logger.warning("No .env file found. Using .env.example as template.")
        logger.warning("Please copy .env.example to .env and configure your API keys.")
        
        if args.mode != 'test':
            logger.error("Cannot run without proper configuration. Exiting.")
            sys.exit(1)
    
    # Initialize scheduler
    scheduler = ContentScheduler()
    
    if args.mode == 'scheduler':
        # Run full scheduler
        logger.info("Starting scheduler mode...")
        scheduler.run()
    
    elif args.mode == 'search':
        # Run search only
        logger.info("Running article search...")
        scheduler.search_and_collect_articles()
        logger.info("Search completed.")
    
    elif args.mode == 'publish-blog':
        # Run blog publication only
        logger.info("Running blog publication...")
        scheduler.publish_to_blog()
        logger.info("Blog publication completed.")
    
    elif args.mode == 'publish-social':
        # Run social media publication only
        logger.info("Running social media publication...")
        scheduler.publish_to_facebook()
        scheduler.publish_to_instagram()
        logger.info("Social media publication completed.")
    
    elif args.mode == 'test':
        # Test mode
        logger.info("Running in test mode...")
        
        if args.test_keyword:
            from gemini_search import GeminiSearchEngine
            gemini = GeminiSearchEngine()
            
            logger.info(f"Testing search for keyword: {args.test_keyword}")
            results = gemini.search_articles(args.test_keyword, num_results=3)
            
            logger.info(f"Found {len(results)} results:")
            for i, article in enumerate(results, 1):
                logger.info(f"\n{i}. {article.get('title', 'No title')}")
                logger.info(f"   Description: {article.get('description', 'No description')[:100]}...")
        else:
            logger.info("System check:")
            logger.info(f"  - Database: {os.path.exists('data/articles.db')}")
            logger.info(f"  - Config loaded: Yes")
            logger.info("Run with --test-keyword to test search functionality")

if __name__ == '__main__':
    main()
