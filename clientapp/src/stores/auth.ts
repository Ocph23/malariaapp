import type { User } from '@/models'
import { defineStore, acceptHMRUpdate } from 'pinia'



interface ToolStore {
  token: string | null
  user: User
}

export const useAuthStore = defineStore('user', {
  state: () => {
    return {} as ToolStore
  },

  actions: {
    getToken() {
      if (!this.token) {
        this.token = localStorage.getItem('token');
      }
      return this.token;
    },

    getUser(): User | null {
      if (!this.user || Object.keys(this.user).length === 0) {
        const userData = localStorage.getItem('user');
        if (userData) {
          this.user = JSON.parse(userData);
        } else {
          return null;
        }
      }
      return this.user;
    },
    setAuthResponse(authResponse: { token: string, role: string, user: User }): Promise<void> {

      localStorage.setItem('token', authResponse.token);
      localStorage.setItem('user', JSON.stringify(authResponse.user));
      this.token = authResponse.token;
      this.user = authResponse.user;
      return Promise.resolve();
    },


    isLogin(): boolean {
      const token = localStorage.getItem('token');
      return token != null;
    },

    logout() {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      this.token = null;
    }
  },
})


if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useAuthStore, import.meta.hot));
}
