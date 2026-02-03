'use client'

import { useEffect, useState } from 'react'
import { FileText, CheckCircle, Clock, TrendingUp } from 'lucide-react'

interface Stats {
  total_articles: number
  pending_articles: number
  published_articles: number
  avg_score: number
}

export default function DashboardStats() {
  const [stats, setStats] = useState<Stats>({
    total_articles: 0,
    pending_articles: 0,
    published_articles: 0,
    avg_score: 0,
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      const response = await fetch('/api/stats')
      const data = await response.json()
      setStats(data)
    } catch (error) {
      console.error('Error fetching stats:', error)
    } finally {
      setLoading(false)
    }
  }

  const statCards = [
    {
      title: 'Всего статей',
      value: stats.total_articles,
      icon: <FileText className="h-6 w-6" />,
      color: 'bg-blue-500',
    },
    {
      title: 'В ожидании',
      value: stats.pending_articles,
      icon: <Clock className="h-6 w-6" />,
      color: 'bg-yellow-500',
    },
    {
      title: 'Опубликовано',
      value: stats.published_articles,
      icon: <CheckCircle className="h-6 w-6" />,
      color: 'bg-green-500',
    },
    {
      title: 'Средний балл',
      value: stats.avg_score.toFixed(1),
      icon: <TrendingUp className="h-6 w-6" />,
      color: 'bg-purple-500',
    },
  ]

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="card animate-pulse">
            <div className="h-20 bg-gray-200 dark:bg-gray-700 rounded"></div>
          </div>
        ))}
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {statCards.map((stat, index) => (
        <div key={index} className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                {stat.title}
              </p>
              <p className="mt-2 text-3xl font-bold text-gray-900 dark:text-white">
                {stat.value}
              </p>
            </div>
            <div className={`p-3 rounded-lg ${stat.color} text-white`}>
              {stat.icon}
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
