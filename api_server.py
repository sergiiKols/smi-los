"""
API server for web dashboard
FastAPI backend for Next.js frontend
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import ArticleDatabase
from scheduler import ContentScheduler
import config

app = FastAPI(title="Content Search API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database and scheduler
db = ArticleDatabase()
scheduler = ContentScheduler()

# Pydantic models
class Settings(BaseModel):
    search_hour: int
    search_minute: int
    blog_post_hour: int
    blog_post_minute: int
    facebook_post_hour: int
    facebook_post_minute: int
    instagram_post_hour: int
    instagram_post_minute: int
    max_articles_per_day: int
    min_article_score: float

class ActionResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

# Routes

@app.get("/")
async def root():
    return {"message": "Content Search API", "status": "running"}

@app.get("/api/stats")
async def get_stats():
    """Get dashboard statistics"""
    try:
        # Query database for stats
        import sqlite3
        conn = sqlite3.connect(config.DATABASE_PATH)
        cursor = conn.cursor()
        
        # Total articles
        cursor.execute("SELECT COUNT(*) FROM articles")
        total_articles = cursor.fetchone()[0]
        
        # Pending articles
        cursor.execute("SELECT COUNT(*) FROM articles WHERE status = 'pending'")
        pending_articles = cursor.fetchone()[0]
        
        # Published articles
        cursor.execute("SELECT COUNT(*) FROM articles WHERE status = 'published'")
        published_articles = cursor.fetchone()[0]
        
        # Average score
        cursor.execute("SELECT AVG(ai_score) FROM articles WHERE ai_score > 0")
        result = cursor.fetchone()
        avg_score = result[0] if result[0] else 0
        
        conn.close()
        
        return {
            "total_articles": total_articles,
            "pending_articles": pending_articles,
            "published_articles": published_articles,
            "avg_score": round(avg_score, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/articles")
async def get_articles(status: Optional[str] = None, limit: Optional[int] = None):
    """Get articles with optional filtering"""
    try:
        import sqlite3
        conn = sqlite3.connect(config.DATABASE_PATH)
        cursor = conn.cursor()
        
        query = "SELECT * FROM articles"
        params = []
        
        if status and status != 'all':
            query += " WHERE status = ?"
            params.append(status)
        
        query += " ORDER BY ai_score DESC, found_date DESC"
        
        if limit:
            query += f" LIMIT {limit}"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        articles = []
        for row in rows:
            articles.append({
                "id": row[0],
                "title": row[1],
                "url": row[2],
                "content": row[3],
                "source": row[4],
                "keywords": eval(row[5]) if row[5] else [],
                "ai_score": row[6],
                "relevance_score": row[7],
                "found_date": row[8],
                "status": row[9],
            })
        
        return {"articles": articles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/logs")
async def get_logs(limit: int = 10):
    """Get activity logs"""
    try:
        import sqlite3
        conn = sqlite3.connect(config.DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, platform as action, post_id as message, published_date as timestamp, status
            FROM publications
            ORDER BY published_date DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        logs = []
        for row in rows:
            logs.append({
                "id": row[0],
                "action": row[1],
                "message": f"Опубликовано в {row[1]}: {row[2]}",
                "timestamp": row[3],
                "status": "success" if row[4] == "success" else "error"
            })
        
        return {"logs": logs}
    except Exception as e:
        return {"logs": []}

@app.post("/api/articles/{article_id}/approve")
async def approve_article(article_id: int):
    """Approve an article for publication"""
    try:
        db.update_article_status(article_id, 'approved')
        return ActionResponse(
            success=True,
            message="Статья одобрена для публикации"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/articles/{article_id}/reject")
async def reject_article(article_id: int):
    """Reject an article"""
    try:
        db.update_article_status(article_id, 'rejected')
        return ActionResponse(
            success=True,
            message="Статья отклонена"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/settings")
async def get_settings():
    """Get current settings"""
    return Settings(
        search_hour=config.SEARCH_HOUR,
        search_minute=config.SEARCH_MINUTE,
        blog_post_hour=config.BLOG_POST_HOUR,
        blog_post_minute=config.BLOG_POST_MINUTE,
        facebook_post_hour=config.FACEBOOK_POST_HOUR,
        facebook_post_minute=config.FACEBOOK_POST_MINUTE,
        instagram_post_hour=config.INSTAGRAM_POST_HOUR,
        instagram_post_minute=config.INSTAGRAM_POST_MINUTE,
        max_articles_per_day=config.MAX_ARTICLES_PER_DAY,
        min_article_score=config.MIN_ARTICLE_SCORE
    )

@app.post("/api/settings")
async def update_settings(settings: Settings):
    """Update settings"""
    try:
        # Update config file
        import os
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        
        # Read current .env
        lines = []
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                lines = f.readlines()
        
        # Update values
        settings_map = {
            'SEARCH_HOUR': str(settings.search_hour),
            'SEARCH_MINUTE': str(settings.search_minute),
            'BLOG_POST_HOUR': str(settings.blog_post_hour),
            'BLOG_POST_MINUTE': str(settings.blog_post_minute),
            'FACEBOOK_POST_HOUR': str(settings.facebook_post_hour),
            'FACEBOOK_POST_MINUTE': str(settings.facebook_post_minute),
            'INSTAGRAM_POST_HOUR': str(settings.instagram_post_hour),
            'INSTAGRAM_POST_MINUTE': str(settings.instagram_post_minute),
            'MAX_ARTICLES_PER_DAY': str(settings.max_articles_per_day),
            'MIN_ARTICLE_SCORE': str(settings.min_article_score),
        }
        
        # Write back
        new_lines = []
        for line in lines:
            updated = False
            for key, value in settings_map.items():
                if line.startswith(f"{key}="):
                    new_lines.append(f"{key}={value}\n")
                    updated = True
                    break
            if not updated:
                new_lines.append(line)
        
        with open(env_path, 'w') as f:
            f.writelines(new_lines)
        
        return ActionResponse(
            success=True,
            message="Настройки обновлены"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/search")
async def trigger_search():
    """Manually trigger article search"""
    try:
        scheduler.search_and_collect_articles()
        return ActionResponse(
            success=True,
            message="Поиск статей запущен"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/publish")
async def trigger_publish():
    """Manually trigger blog publication"""
    try:
        scheduler.publish_to_blog()
        return ActionResponse(
            success=True,
            message="Публикация в блог запущена"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/settings")
async def trigger_settings():
    """Open settings page"""
    return ActionResponse(
        success=True,
        message="Перенаправление на страницу настроек"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3001)
