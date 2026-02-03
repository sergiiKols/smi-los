'use client'

import { useEffect, useState } from 'react'
import { Activity, CheckCircle, Search, Share2, AlertCircle } from 'lucide-react'

interface LogEntry {
  id: number
  action: string
  message: string
  timestamp: string
  status: 'success' | 'error' | 'info'
}

export default function ActivityLog() {
  const [logs, setLogs] = useState<LogEntry[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchLogs()
  }, [])

  const fetchLogs = async () => {
    try {
      const response = await fetch('/api/logs?limit=10')
      const data = await response.json()
      setLogs(data.logs || [])
    } catch (error) {
      console.error('Error fetching logs:', error)
    } finally {
      setLoading(false)
    }
  }

  const getIcon = (action: string) => {
    switch (action) {
      case 'search':
        return <Search className="h-4 w-4" />
      case 'publish':
        return <CheckCircle className="h-4 w-4" />
      case 'share':
        return <Share2 className="h-4 w-4" />
      default:
        return <Activity className="h-4 w-4" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'success':
        return 'text-green-600 dark:text-green-400'
      case 'error':
        return 'text-red-600 dark:text-red-400'
      default:
        return 'text-blue-600 dark:text-blue-400'
    }
  }

  if (loading) {
    return (
      <div className="card">
        <h2 className="text-xl font-bold mb-4">Лог активности</h2>
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="animate-pulse flex space-x-3">
              <div className="h-8 w-8 bg-gray-200 dark:bg-gray-700 rounded-full"></div>
              <div className="flex-1">
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4 mb-2"></div>
                <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-1/2"></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="card">
      <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
        Лог активности
      </h2>

      <div className="space-y-3">
        {logs.length === 0 ? (
          <p className="text-gray-500 dark:text-gray-400 text-center py-8">
            Нет записей активности
          </p>
        ) : (
          logs.map((log) => (
            <div key={log.id} className="flex items-start space-x-3">
              <div className={`p-2 rounded-full ${getStatusColor(log.status)} bg-opacity-10`}>
                {getIcon(log.action)}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm text-gray-900 dark:text-white">
                  {log.message}
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                  {new Date(log.timestamp).toLocaleString('ru-RU')}
                </p>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
