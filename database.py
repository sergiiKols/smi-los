"""
Database module for storing and managing articles
"""
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import config

class ArticleDatabase:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or config.DATABASE_PATH
        self._init_database()
    
    def _init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Articles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                url TEXT UNIQUE,
                content TEXT,
                source TEXT,
                keywords TEXT,
                ai_score REAL,
                relevance_score REAL,
                found_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'pending',
                analysis TEXT
            )
        ''')
        
        # Publications table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS publications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                article_id INTEGER,
                platform TEXT,
                post_id TEXT,
                published_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'success',
                FOREIGN KEY (article_id) REFERENCES articles (id)
            )
        ''')
        
        # Search history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT,
                search_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                results_count INTEGER
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_article(self, article: Dict) -> int:
        """Add a new article to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO articles (title, url, content, source, keywords, ai_score, relevance_score, analysis)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                article.get('title'),
                article.get('url'),
                article.get('content'),
                article.get('source'),
                json.dumps(article.get('keywords', [])),
                article.get('ai_score'),
                article.get('relevance_score'),
                json.dumps(article.get('analysis', {}))
            ))
            conn.commit()
            article_id = cursor.lastrowid
            return article_id
        except sqlite3.IntegrityError:
            # Article already exists
            return -1
        finally:
            conn.close()
    
    def get_pending_articles(self, limit: int = None) -> List[Dict]:
        """Get articles pending for publication"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = '''
            SELECT id, title, url, content, source, keywords, ai_score, relevance_score, analysis
            FROM articles
            WHERE status = 'pending' AND ai_score >= ?
            ORDER BY ai_score DESC, relevance_score DESC
        '''
        
        if limit:
            query += f' LIMIT {limit}'
        
        cursor.execute(query, (config.MIN_ARTICLE_SCORE,))
        rows = cursor.fetchall()
        conn.close()
        
        articles = []
        for row in rows:
            articles.append({
                'id': row[0],
                'title': row[1],
                'url': row[2],
                'content': row[3],
                'source': row[4],
                'keywords': json.loads(row[5]) if row[5] else [],
                'ai_score': row[6],
                'relevance_score': row[7],
                'analysis': json.loads(row[8]) if row[8] else {}
            })
        
        return articles
    
    def update_article_status(self, article_id: int, status: str):
        """Update article status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE articles SET status = ? WHERE id = ?', (status, article_id))
        conn.commit()
        conn.close()
    
    def add_publication(self, article_id: int, platform: str, post_id: str, status: str = 'success'):
        """Record a publication"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO publications (article_id, platform, post_id, status)
            VALUES (?, ?, ?, ?)
        ''', (article_id, platform, post_id, status))
        conn.commit()
        conn.close()
    
    def add_search_history(self, keyword: str, results_count: int):
        """Record a search operation"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO search_history (keyword, results_count)
            VALUES (?, ?)
        ''', (keyword, results_count))
        conn.commit()
        conn.close()
    
    def get_article_by_url(self, url: str) -> Optional[Dict]:
        """Get article by URL"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articles WHERE url = ?', (url,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'title': row[1],
                'url': row[2],
                'content': row[3],
                'source': row[4],
                'keywords': json.loads(row[5]) if row[5] else [],
                'ai_score': row[6],
                'relevance_score': row[7]
            }
        return None
