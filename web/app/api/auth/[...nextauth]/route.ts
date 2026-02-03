import NextAuth from "next-auth"
import CredentialsProvider from "next-auth/providers/credentials"
import type { NextAuthOptions } from "next-auth"

export const authOptions: NextAuthOptions = {
  providers: [
    CredentialsProvider({
      name: 'Credentials',
      credentials: {
        username: { label: "Логин", type: "text", placeholder: "admin" },
        password: { label: "Пароль", type: "password" }
      },
      async authorize(credentials) {
        // Получаем логин и пароль из переменных окружения
        const validUsername = process.env.ADMIN_USERNAME || 'admin'
        const validPassword = process.env.ADMIN_PASSWORD || 'admin123'

        if (
          credentials?.username === validUsername &&
          credentials?.password === validPassword
        ) {
          // Возвращаем пользователя при успешной аутентификации
          return {
            id: '1',
            name: credentials.username,
            email: credentials.username + '@admin.local',
          }
        }
        
        // Возвращаем null при неудачной аутентификации
        return null
      }
    })
  ],
  pages: {
    signIn: '/login',
  },
  session: {
    strategy: 'jwt',
    maxAge: 30 * 24 * 60 * 60, // 30 дней
  },
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id
      }
      return token
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.id = token.id as string
      }
      return session
    },
  },
  secret: process.env.NEXTAUTH_SECRET,
}

const handler = NextAuth(authOptions)

export { handler as GET, handler as POST }
