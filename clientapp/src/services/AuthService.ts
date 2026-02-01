import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import type { HeaderRequest, LoginRequest, RegisterRequest } from '@/models/request'
import type { AuthResponse } from '@/models/response'

const AuthService = {
  login: async (loginRequest: LoginRequest): Promise<AuthResponse> => {
    try {
      const url = '/auth/login'
      const result = await axios.post(url, loginRequest)
      if (result) {
        const auth = useAuthStore()
        await auth.setAuthResponse(result.data)
        return result.data as unknown as AuthResponse
      }
      throw new Error('Anda tidak memiliki akses')
    } catch (err: unknown | Error) {
      const error = err as Error
      return Promise.reject(error.message || err)
    }
  },
  register: async (registerRequest: RegisterRequest): Promise<AuthResponse> => {
    try {
      const url = '/auth/register'
      const result = await axios.post(url, registerRequest)
      if (result) {
        const auth = useAuthStore()
        await auth.setAuthResponse(result.data)
        return result.data as AuthResponse
      }
      throw new Error('Anda tidak memiliki akses')
    } catch (err: unknown | Error) {
      const error = err as Error
      return Promise.reject(error.message || err)
    }
  },
  getHeader: (): HeaderRequest => {
    const auth = useAuthStore()
    const token = auth.getToken()
    return {
      headers: {
        Authorization: 'bearer ' + token,
      },
    } as HeaderRequest
  },

  isLogin: async (): Promise<boolean> => {
    const auth = useAuthStore()
    return auth.isLogin()
  },

  logout: async (): Promise<void> => {
    const auth = useAuthStore()
    auth.logout()
  },
}

export default AuthService
