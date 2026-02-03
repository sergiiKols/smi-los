'use client'

import { signOut } from 'next-auth/react'
import { LogOut } from 'lucide-react'

export default function LogoutButton() {
  const handleLogout = () => {
    signOut({ callbackUrl: '/login' })
  }

  return (
    <button
      onClick={handleLogout}
      className="flex items-center space-x-2 text-gray-700 dark:text-gray-300 hover:text-red-600 dark:hover:text-red-400 transition-colors"
      title="Выйти"
    >
      <LogOut className="h-5 w-5" />
      <span>Выход</span>
    </button>
  )
}
