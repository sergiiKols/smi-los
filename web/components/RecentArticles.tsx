'use client'

import { useEffect, useState } from 'react'
import { ExternalLink, Star } from 'lucide-react'

interface Article {
  id: number
  title: string
  ai_score: number
  status: string
  found_date: string
}

export default function RecentArticles() {
  const [articles, setArticles] = useState<Article[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchArticles()
  }, [])

  const fetchArticles = async () => {
    try {
      const response = await fetch('/api/articles?limit=5')
      const data = await response.json()
      setArticles(data.articles || [])
    } catch (error) {
      console.error('Error fetching articles:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="card">
        <h2 className="text-xl font-bold mb-4">Последние статьи</h2>
        <div className="space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="animate-pulse">
              <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4 mb-2"></div>
              <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-1/2"></div>
            </div>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold text-gray-900 dark:text-white">
          Последние статьи
        </h2>
        <a 
          href="/articles" 
          className="text-sm text-primary-600 hover:text-primary-700 flex items-center"
        >
          Все статьи
          <ExternalLink className="h-4 w-4 ml-1" />
        </a>
      </div>

      <div className="space-y-4">
        {articles.length === 0 ? (
          <p className="text-gray-500 dark:text-gray-400 text-center py-8">
            Статьи не найдены. Запустите поиск.
          </p>
        ) : (
          articles.map((article) => (
            <div 
              key={article.id}
              className="border-l-4 border-primary-500 pl-4 py-2 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h3 className="font-medium text-gray-900 dark:text-white line-clamp-2">
                    {article.title}
                  </h3>
                  <div className="flex items-center mt-2 space-x-4 text-sm text-gray-500 dark:text-gray-400">
                    <span className="flex items-center">
                      <Star className="h-4 w-4 mr-1 text-yellow-500" />
                      {article.ai_score.toFixed(1)}
                    </span>
                    <span className={`px-2 py-1 rounded text-xs font-medium ${
                      article.status === 'published' 
                        ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                        : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
                    }`}>
                      {article.status === 'published' ? 'Опубликовано' : 'В ожидании'}
                    </span>
                    <span>{new Date(article.found_date).toLocaleDateString('ru-RU')}</span>
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
