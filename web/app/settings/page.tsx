'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { ArrowLeft, Save, RefreshCw } from 'lucide-react'
import { toast } from 'react-toastify'

interface Settings {
  search_hour: number
  search_minute: number
  blog_post_hour: number
  blog_post_minute: number
  facebook_post_hour: number
  facebook_post_minute: number
  instagram_post_hour: number
  instagram_post_minute: number
  max_articles_per_day: number
  min_article_score: number
}

export default function SettingsPage() {
  const [settings, setSettings] = useState<Settings>({
    search_hour: 9,
    search_minute: 0,
    blog_post_hour: 10,
    blog_post_minute: 0,
    facebook_post_hour: 12,
    facebook_post_minute: 0,
    instagram_post_hour: 14,
    instagram_post_minute: 0,
    max_articles_per_day: 5,
    min_article_score: 7.0,
  })
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    fetchSettings()
  }, [])

  const fetchSettings = async () => {
    try {
      const response = await fetch('/api/settings')
      const data = await response.json()
      setSettings(data)
    } catch (error) {
      toast.error('Ошибка загрузки настроек')
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async () => {
    setSaving(true)
    try {
      const response = await fetch('/api/settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(settings)
      })
      
      if (response.ok) {
        toast.success('Настройки сохранены')
      } else {
        toast.error('Ошибка сохранения настроек')
      }
    } catch (error) {
      toast.error('Ошибка сохранения настроек')
    } finally {
      setSaving(false)
    }
  }

  const handleChange = (field: keyof Settings, value: number) => {
    setSettings({ ...settings, [field]: value })
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
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
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Настройки системы
          </h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">
            Настройка расписания и параметров работы системы
          </p>
        </div>

        <div className="space-y-6">
          {/* Schedule Settings */}
          <div className="card">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-6">
              Расписание задач
            </h2>

            <div className="space-y-6">
              {/* Search Schedule */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Поиск статей
                </label>
                <div className="flex items-center space-x-4">
                  <input
                    type="number"
                    min="0"
                    max="23"
                    value={settings.search_hour}
                    onChange={(e) => handleChange('search_hour', parseInt(e.target.value))}
                    className="input w-20"
                  />
                  <span className="text-gray-700 dark:text-gray-300">:</span>
                  <input
                    type="number"
                    min="0"
                    max="59"
                    value={settings.search_minute}
                    onChange={(e) => handleChange('search_minute', parseInt(e.target.value))}
                    className="input w-20"
                  />
                  <span className="text-gray-500 dark:text-gray-400 text-sm">
                    ({settings.search_hour.toString().padStart(2, '0')}:{settings.search_minute.toString().padStart(2, '0')})
                  </span>
                </div>
              </div>

              {/* Blog Post Schedule */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Публикация в блог
                </label>
                <div className="flex items-center space-x-4">
                  <input
                    type="number"
                    min="0"
                    max="23"
                    value={settings.blog_post_hour}
                    onChange={(e) => handleChange('blog_post_hour', parseInt(e.target.value))}
                    className="input w-20"
                  />
                  <span className="text-gray-700 dark:text-gray-300">:</span>
                  <input
                    type="number"
                    min="0"
                    max="59"
                    value={settings.blog_post_minute}
                    onChange={(e) => handleChange('blog_post_minute', parseInt(e.target.value))}
                    className="input w-20"
                  />
                  <span className="text-gray-500 dark:text-gray-400 text-sm">
                    ({settings.blog_post_hour.toString().padStart(2, '0')}:{settings.blog_post_minute.toString().padStart(2, '0')})
                  </span>
                </div>
              </div>

              {/* Facebook Schedule */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Публикация в Facebook
                </label>
                <div className="flex items-center space-x-4">
                  <input
                    type="number"
                    min="0"
                    max="23"
                    value={settings.facebook_post_hour}
                    onChange={(e) => handleChange('facebook_post_hour', parseInt(e.target.value))}
                    className="input w-20"
                  />
                  <span className="text-gray-700 dark:text-gray-300">:</span>
                  <input
                    type="number"
                    min="0"
                    max="59"
                    value={settings.facebook_post_minute}
                    onChange={(e) => handleChange('facebook_post_minute', parseInt(e.target.value))}
                    className="input w-20"
                  />
                  <span className="text-gray-500 dark:text-gray-400 text-sm">
                    ({settings.facebook_post_hour.toString().padStart(2, '0')}:{settings.facebook_post_minute.toString().padStart(2, '0')})
                  </span>
                </div>
              </div>

              {/* Instagram Schedule */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Публикация в Instagram
                </label>
                <div className="flex items-center space-x-4">
                  <input
                    type="number"
                    min="0"
                    max="23"
                    value={settings.instagram_post_hour}
                    onChange={(e) => handleChange('instagram_post_hour', parseInt(e.target.value))}
                    className="input w-20"
                  />
                  <span className="text-gray-700 dark:text-gray-300">:</span>
                  <input
                    type="number"
                    min="0"
                    max="59"
                    value={settings.instagram_post_minute}
                    onChange={(e) => handleChange('instagram_post_minute', parseInt(e.target.value))}
                    className="input w-20"
                  />
                  <span className="text-gray-500 dark:text-gray-400 text-sm">
                    ({settings.instagram_post_hour.toString().padStart(2, '0')}:{settings.instagram_post_minute.toString().padStart(2, '0')})
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Content Settings */}
          <div className="card">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-6">
              Параметры контента
            </h2>

            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Максимум статей в день
                </label>
                <input
                  type="number"
                  min="1"
                  max="20"
                  value={settings.max_articles_per_day}
                  onChange={(e) => handleChange('max_articles_per_day', parseInt(e.target.value))}
                  className="input w-32"
                />
                <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
                  Максимальное количество статей для публикации в день
                </p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Минимальный балл статьи
                </label>
                <input
                  type="number"
                  min="0"
                  max="10"
                  step="0.1"
                  value={settings.min_article_score}
                  onChange={(e) => handleChange('min_article_score', parseFloat(e.target.value))}
                  className="input w-32"
                />
                <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
                  Минимальный балл AI для одобрения статьи (0-10)
                </p>
              </div>
            </div>
          </div>

          {/* Save Button */}
          <div className="flex justify-end space-x-4">
            <button
              onClick={fetchSettings}
              className="btn btn-secondary flex items-center space-x-2"
              disabled={saving}
            >
              <RefreshCw className="h-4 w-4" />
              <span>Сбросить</span>
            </button>
            <button
              onClick={handleSave}
              className="btn btn-primary flex items-center space-x-2"
              disabled={saving}
            >
              {saving ? (
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              ) : (
                <Save className="h-4 w-4" />
              )}
              <span>{saving ? 'Сохранение...' : 'Сохранить'}</span>
            </button>
          </div>
        </div>
      </main>
    </div>
  )
}
