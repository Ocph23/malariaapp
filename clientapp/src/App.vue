<script setup lang="ts">
import { RouterView, useRouter } from 'vue-router'

import 'preline';
import axios, { AxiosError, type AxiosResponse } from 'axios';
import { useAuthStore } from './stores/auth';
import type { ResponseRequest } from './models/request';
import { toastService } from './services/ToastService';
import AuthService from './services/AuthService';


const router = useRouter()

axios.defaults.baseURL = import.meta.env.VITE_API_URL;
const auth = useAuthStore();
const token = auth.getToken();
if (auth && token) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
}

axios.interceptors.response.use(function (response) {
  // Optional: Do something with response data
  return response
}, function (err) {
  try {
    const axiosError = err as AxiosError;
    const axiosResponse = axiosError.response as AxiosResponse;
    const response: ResponseRequest = err.response.data as ResponseRequest;
    let errorMessage;
    if (axiosResponse.status == 401) {
      toastService.error(response.message, "Error")
      setTimeout(() => {
        AuthService.logout()
        router.push('/login')
      }, 2000)
      return
    }
    if (axiosResponse.status == 404) {
      toastService.error(response.error as string, "Error")
      return
    }
    if (axiosResponse.status == 503 || axiosResponse.status == 500) {
      toastService.error(axiosResponse.statusText, "Error")
    }

    if (response.message)
      errorMessage = response.message

    throw new Error(errorMessage)
  } catch (error: unknown) {
    const err = error as Error;
    toastService.error(err.message, "Error")
  }
  return Promise.reject(err)
});















</script>

<template>
  <!-- Global Toast Container -->
  <div id="toast-container" class="hs-toast-container fixed top-5 right-5 z-[9999] space-y-3"></div>
  <RouterView />
</template>

<style scoped>
/* header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
} */
</style>
