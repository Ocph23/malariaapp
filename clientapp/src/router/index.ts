import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

import LoginPage from '@/views/Auth/LoginPage.vue'
import RegisterPage from '@/views/Auth/RegisterPage.vue'
import { useAuthStore } from '@/stores/auth'
import LaporanPage from '@/views/admin/LaporanPage.vue'
import UserPage from '@/views/admin/UserPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/pasien',
      name: 'pasien',
      children: [
        {
          path: '',
          name: 'pasien.home',
          component: () => import('../views/pasien/HomePage.vue'),
        },
        {
          path: 'diagnosa',
          name: 'pasien.diagnosa',
          component: () => import('../views/pasien/DiagnosaPage.vue'),
        },
        {
          path: 'riwayat',
          name: 'pasien.riwayat',
          component: () => import('../views/pasien/RiwayatPage.vue'),
        },
      ],
    },

    {
      path: '/admin',
      name: 'admin',
      children: [
        {
          path: '',
          name: 'admin.home',
          component: HomeView,
        },
        {
          path: 'user',
          name: 'admin.user',
          component: UserPage,
        },
        {
          path: 'laporan',
          name: 'admin.laporan',
          component: LaporanPage,
        },
      ],
    },
    {
      path: '/pakar',
      name: 'pakar',
      children: [
        {
          path: '',
          name: 'pakar.home',
          component: () => import('../views/pakar/HomeView.vue'),
        },
        {
          path: 'gejala',
          name: 'pakar.gejala',
          component: () => import('../views/pakar/GejalaPage.vue'),
        },
        {
          path: 'penyakit',
          name: 'pakar.penyakit',
          component: () => import('../views/pakar/PenyakitPage.vue'),
        },
        {
          path: 'penyakit/:id',
          name: 'pakar.penyakit.aturan',
          component: () => import('../views/pakar/AturanPenyakitPage.vue'),
        },
      ],
    },
    {
      path: '/auth',
      name: 'auth',
      children: [
        {
          path: 'login',
          name: 'login',
          component: LoginPage,
        },
        {
          path: 'register',
          name: 'register',
          component: RegisterPage,
        },
      ],
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
  ],
})

router.beforeEach(async (to) => {
  // redirect to login page if not logged in and trying to access a restricted page

  const publicPages = ['/auth/login', '/auth/register', '/about']
  const authRequired = !publicPages.includes(to.path)
  const auth = useAuthStore()
  const token = auth.getToken()
  if (authRequired && !token) {
    return '/auth/login'
  }
  if (to.path === '/') {
    const user = auth.getUser()
    if (user && user.role === 'admin') {
      return '/admin'
    }
    if (user && user.role === 'pakar') {
      return '/pakar'
    }
    return '/pasien'
  }
})

router.afterEach(async (to, from, failure) => {
  if (!failure) setTimeout(() => window.HSStaticMethods.autoInit(), 100)
})

export default router
