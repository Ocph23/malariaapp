import { inject, type App } from 'vue';
import { toastService, type ToastService } from '@/services/ToastService';

const ToastSymbol = Symbol('toast');

export const useToast = (): ToastService => {
  const toast = inject(ToastSymbol);
  if (!toast) {
    throw new Error('Toast plugin not installed');
  }
  return toast as ToastService;
};

export const toastPlugin = {
  install(app: App) {
    app.provide(ToastSymbol, toastService);
    app.config.globalProperties.$toast = toastService;
  }
};

declare module '@vue/runtime-core' {
  export interface ComponentCustomProperties {
    $toast: ToastService;
  }
}