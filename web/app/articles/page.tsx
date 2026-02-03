'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { 
  ArrowLeft, 
  Star, 
  ExternalLink, 
  CheckCircle, 
  XCircle,
  Eye,
  Trash2
} from 'lucide-react'
import { toast } from 'react-toastify'

interface Article {
  id: number
  title: string
  content: string
  url: string
  source: string
  ai_score: number
  relevance_score: number
  status: string
  found_date: string
  keywords: string[]
}

export default function ArticlesPage() {
  const [articles, setArticles] = useState<Article[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<'all' | 'pending' | 'published'>('all')
  const [selectedArticle, setSelectedArticle] = useState<Article | null>(null)

  useEffect(() => {
    fetchArticles()
  }, [filter])

  const fetchArticles = async () => {
    setLoading(true)
    try {
      const response = await fetch(`/api/articles?status=${filter}`)
      const data = await response.json()
      setArticles(data.articles || [])
    } catch (error) {
      toast.error('Ошибка загрузки статей')
    } finally {
      setLoading(false)
    }
  }

  const handleApprove = async (articleId: number) => {
    try {
      const response = await fetch(`/api/articles/${articleId}/approve`, {
        method: 'POST'
      })
      if (response.ok) {
        toast.success('Статья одобрена')
        fetchArticles()
      }
    } catch (error) {
      toast.error('Ошибка одобрения статьи')
    }
  }

  const handleReject = async (articleId: number) => {
    try {
      const response = await fetch(`/api/articles/${articleId}/reject`, {
        method: 'POST'
      })
      if (response.ok) {
        toast.success('Статья отклонена')
        fetchArticles()
      }
    } catch (error) {
      toast.error('Ошибка отклонения статьи')
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Navbar */}
      <nav className="bg-white dark:bg-gray-800 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Link href="/" className="flex items-center text-gray-700 dark:text-gray-300 hover:text-primary-600">
                <ArrowLeft className="h-5 w-5 mr-2" />
                Назад к Dashboard
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Управление статьями
          </h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">
            Просмотр, одобрение и редактирование найденных статей
          </p>
        </div>

        {/* Filters */}
        <div className="flex space-x-4 mb-6">
          <button
            onClick={() => setFilter('all')}
            className={`btn ${filter === 'all' ? 'btn-primary' : 'btn-secondary'}`}
          >
            Все ({articles.length})
          </button>
          <button
            onClick={() => setFilter('pending')}
            className={`btn ${filter === 'pending' ? 'btn-primary' : 'btn-secondary'}`}
          >
            В ожидании
          </button>
          <button
            onClick={() => setFilter('published')}
            className={`btn ${filter === 'published' ? 'btn-primary' : 'btn-secondary'}`}
          >
            Опубликовано
          </button>
        </div>

        {/* Articles List */}
        {loading ? (
          <div className="grid gap-6">
            {[1, 2, 3].map((i) => (
              <div key={i} className="card animate-pulse">
                <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-3/4 mb-4"></div>
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-full mb-2"></div>
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-2/3"></div>
              </div>
            ))}
          </div>
        ) : articles.length === 0 ? (
          <div className="card text-center py-12">
            <p className="text-gray-500 dark:text-gray-400">
              Статьи не найдены
            </p>
          </div>
        ) : (
          <div className="grid gap-6">
            {articles.map((article) => (
              <div key={article.id} className="card hover:shadow-lg transition-shadow">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                      {article.title}
                    </h3>
                    <p className="text-gray-600 dark:text-gray-400 mb-4 line-clamp-3">
                      {article.content}
                    </p>
                    
                    <div className="flex flex-wrap items-center gap-4 text-sm">
                      <span className="flex items-center text-yellow-600">
                        <Star className="h-4 w-4 mr-1" />
                        Балл: {article.ai_score.toFixed(1)}
                      </span>
                      <span className="text-gray-500 dark:text-gray-400">
                        Релевантность: {article.relevance_score.toFixed(1)}
                      </span>
                      <span className="text-gray-500 dark:text-gray-400">
                        {new Date(article.found_date).toLocaleDateString('ru-RU')}
                      </span>
                      <span className={`px-2 py-1 rounded text-xs font-medium ${
                        article.status === 'published'
                          ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                          : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
                      }`}>
                        {article.status === 'published' ? 'Опубликовано' : 'В ожидании'}
                      </span>
                    </div>

                    {article.keywords && article.keywords.length > 0 && (
                      <div className="mt-3 flex flex-wrap gap-2">
                        {article.keywords.map((keyword, idx) => (
                          <span
                            key={idx}
                            className="px-2 py-1 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded text-xs"
                          >
                            {keyword}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>

                {/* Actions */}
                <div className="mt-4 flex items-center space-x-3 pt-4 border-t border-gray-200 dark:border-gray-700">
                  <button
                    onClick={() => setSelectedArticle(article)}
                    className="btn btn-secondary flex items-center space-x-2"
                  >
                    <Eye className="h-4 w-4" />
                    <span>Просмотр</span>
                  </button>
                  
                  {article.status === 'pending' && (
                    <>
                      <button
                        onClick={() => handleApprove(article.id)}
                        className="btn btn-primary flex items-center space-x-2"
                      >
                        <CheckCircle className="h-4 w-4" />
                        <span>Одобрить</span>
                      </button>
                      <button
                        onClick={() => handleReject(article.id)}
                        className="btn btn-danger flex items-center space-x-2"
                      >
                        <XCircle className="h-4 w-4" />
                        <span>Отклонить</span>
                      </button>
                    </>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </main>

      {/* Article Detail Modal */}
      {selectedArticle && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white dark:bg-gray-800 rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto p-6">
            <div className="flex items-start justify-between mb-4">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                {selectedArticle.title}
              </h2>
              <button
                onClick={() => setSelectedArticle(null)}
                className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
              >
                <XCircle className="h-6 w-6" />
              </button>
            </div>
            
            <div className="prose dark:prose-invert max-w-none">
              <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
                {selectedArticle.content}
              </p>
            </div>

            <div className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="font-medium">Источник:</span> {selectedArticle.source}
                </div>
                <div>
                  <span className="font-medium">Балл AI:</span> {selectedArticle.ai_score.toFixed(1)}
                </div>
                <div>
                  <span className="font-medium">Релевантность:</span> {selectedArticle.relevance_score.toFixed(1)}
                </div>
                <div>
                  <span className="font-medium">Дата:</span> {new Date(selectedArticle.found_date).toLocaleString('ru-RU')}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
