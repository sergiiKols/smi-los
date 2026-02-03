'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { 
  LayoutDashboard, 
  FileText, 
  Settings, 
  TrendingUp,
  Clock,
  CheckCircle,
  XCircle,
  AlertCircle
} from 'lucide-react'
import DashboardStats from '@/components/DashboardStats'
import RecentArticles from '@/components/RecentArticles'
import ActivityLog from '@/components/ActivityLog'

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Navbar */}
      <nav className="bg-white dark:bg-gray-800 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <TrendingUp className="h-8 w-8 text-primary-600" />
              <span className="ml-2 text-xl font-bold text-gray-900 dark:text-white">
                Content Dashboard
              </span>
            </div>
            <div className="flex items-center space-x-4">
              <Link 
                href="/" 
                className="flex items-center space-x-2 text-gray-700 dark:text-gray-300 hover:text-primary-600"
              >
                <LayoutDashboard className="h-5 w-5" />
                <span>Dashboard</span>
              </Link>
              <Link 
                href="/articles" 
                className="flex items-center space-x-2 text-gray-700 dark:text-gray-300 hover:text-primary-600"
              >
                <FileText className="h-5 w-5" />
                <span>Статьи</span>
              </Link>
              <Link 
                href="/settings" 
                className="flex items-center space-x-2 text-gray-700 dark:text-gray-300 hover:text-primary-600"
              >
                <Settings className="h-5 w-5" />
                <span>Настройки</span>
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Панель управления
          </h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">
            Система автоматического поиска и публикации контента для energo-audit.by
          </p>
        </div>

        {/* Stats */}
        <DashboardStats />

        {/* Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
          {/* Recent Articles */}
          <RecentArticles />

          {/* Activity Log */}
          <ActivityLog />
        </div>

        {/* Quick Actions */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
          <QuickAction
            icon={<FileText className="h-6 w-6" />}
            title="Найти статьи"
            description="Запустить поиск новых статей"
            action="search"
          />
          <QuickAction
            icon={<CheckCircle className="h-6 w-6" />}
            title="Опубликовать"
            description="Опубликовать одобренные статьи"
            action="publish"
          />
          <QuickAction
            icon={<Settings className="h-6 w-6" />}
            title="Настройки"
            description="Изменить параметры системы"
            action="settings"
          />
        </div>
      </main>
    </div>
  )
}

function QuickAction({ 
  icon, 
  title, 
  description, 
  action 
}: { 
  icon: React.ReactNode
  title: string
  description: string
  action: string 
}) {
  const [loading, setLoading] = useState(false)

  const handleAction = async () => {
    setLoading(true)
    try {
      const response = await fetch(`/api/${action}`, { method: 'POST' })
      const data = await response.json()
      alert(data.message || 'Действие выполнено')
    } catch (error) {
      alert('Ошибка выполнения действия')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card hover:shadow-lg transition-shadow cursor-pointer" onClick={handleAction}>
      <div className="flex items-start space-x-4">
        <div className="p-3 bg-primary-100 dark:bg-primary-900 rounded-lg text-primary-600 dark:text-primary-300">
          {icon}
        </div>
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            {title}
          </h3>
          <p className="mt-1 text-sm text-gray-600 dark:text-gray-400">
            {description}
          </p>
        </div>
      </div>
      {loading && (
        <div className="mt-4 text-center">
          <div className="inline-block animate-spin rounded-full h-6 w-6 border-b-2 border-primary-600"></div>
        </div>
      )}
    </div>
  )
}
