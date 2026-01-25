import { type App, inject } from 'vue'
import { loadingService, type LoadingService } from '@/services/LoadingService'

const LoadingSymbol = Symbol('loading')

export const useLoading = (): LoadingService => {
  const loading = inject(LoadingSymbol)
  if (!loading) {
    throw new Error('Loading plugin not installed')
  }
  return loading as LoadingService
}

export const loadingPlugin = {
  install(app: App) {
    app.provide(LoadingSymbol, loadingService)
    app.config.globalProperties.$loading = loadingService
  }
}

declare module '@vue/runtime-core' {
  export interface ComponentCustomProperties {
    $loading: LoadingService
  }
}