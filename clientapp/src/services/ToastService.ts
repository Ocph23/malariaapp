export type ToastType = 'success' | 'error' | 'warning' | 'info' | 'custom';

export interface ToastConfig {
  title: string;
  message: string;
  type: ToastType;
  duration?: number;
  position?: ToastPosition;
  icon?: string;
  onClose?: () => void;
}

export type ToastPosition =
  | 'top-left'
  | 'top-center'
  | 'top-right'
  | 'bottom-left'
  | 'bottom-center'
  | 'bottom-right';

export interface ToastInstance {
  id: string;
  element: HTMLElement;
  config: ToastConfig;
  remove: () => void;
}

export class ToastService {
  private container: HTMLElement | null = null;
  private toastCount = 0;
  private readonly defaultDuration = 5000;

  private getIcon(type: ToastType): string {
    const icons: Record<ToastType, string> = {
      success: '<i class="fas fa-check-circle text-green-500"></i>',
      error: '<i class="fas fa-exclamation-circle text-red-500"></i>',
      warning: '<i class="fas fa-exclamation-triangle text-yellow-500"></i>',
      info: '<i class="fas fa-info-circle text-blue-500"></i>',
      custom: '<i class="fas fa-bell text-purple-500"></i>'
    };
    return icons[type];
  }

  private getBorderColor(type: ToastType): string {
    const colors: Record<ToastType, string> = {
      success: 'border-green-200',
      error: 'border-red-200',
      warning: 'border-yellow-200',
      info: 'border-blue-200',
      custom: 'border-purple-200'
    };
    return colors[type];
  }

  private getBackgroundColor(type: ToastType): string {
    const colors: Record<ToastType, string> = {
      success: 'bg-green-500',
      error: 'bg-red-500',
      warning: 'bg-yellow-500',
      info: 'bg-blue-500',
      custom: 'bg-purple-500'
    };
    return colors[type];
  }

  private createContainer(position: ToastPosition = 'top-right'): HTMLElement {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = `fixed z-[9999] flex flex-col gap-3 ${this.getPositionClasses(position)}`;
    document.body.appendChild(container);
    return container;
  }

  private getPositionClasses(position: ToastPosition): string {
    const positions: Record<ToastPosition, string> = {
      'top-left': 'top-4 left-4',
      'top-center': 'top-4 left-1/2 transform -translate-x-1/2',
      'top-right': 'top-4 right-4',
      'bottom-left': 'bottom-4 left-4',
      'bottom-center': 'bottom-4 left-1/2 transform -translate-x-1/2',
      'bottom-right': 'bottom-4 right-4'
    };
    return positions[position];
  }

  public show(config: ToastConfig): ToastInstance {
    if (!this.container) {
      this.container = this.createContainer(config.position);
    }

    const toastId = `toast-${Date.now()}-${++this.toastCount}`;
    const duration = config.duration || this.defaultDuration;

    const toastElement = document.createElement('div');
    toastElement.id = toastId;
    toastElement.className = `
      max-w-sm w-full ${this.getBackgroundColor(config.type)}
      ${this.getBorderColor(config.type)} border rounded-xl shadow-lg
      transform transition-all duration-300 ease-in-out
      animate-toast-in
    `;
    toastElement.setAttribute('role', 'alert');

    const icon = config.icon || this.getIcon(config.type);

    toastElement.innerHTML = `
      <div class="flex items-start p-4">
        <div class="flex-shrink-0 text-xl">
          ${icon}
        </div>
        <div class="ml-3 flex-1">
          <h3 class="font-semibold text-white">${config.title}</h3>
          <p class="mt-1 text-sm text-white">${config.message}</p>
        </div>
        <button
          type="button"
          class="ml-4 -mt-1 -mr-2 p-2 text-gray-400 hover:text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-300"
          aria-label="Close"
        >
          <i class="fas fa-times"></i>
        </button>
      </div>
    `;

    // Add close button event listener
    const closeButton = toastElement.querySelector('button');
    closeButton?.addEventListener('click', () => {
      this.removeToast(toastElement);
      config.onClose?.();
    });

    this.container.appendChild(toastElement);

    // Auto remove
    if (duration > 0) {
      setTimeout(() => {
        this.removeToast(toastElement);
        config.onClose?.();
      }, duration);
    }

    const toastInstance: ToastInstance = {
      id: toastId,
      element: toastElement,
      config,
      remove: () => this.removeToast(toastElement)
    };

    return toastInstance;
  }

  private removeToast(toastElement: HTMLElement): void {
    toastElement.classList.remove('animate-toast-in');
    toastElement.classList.add('animate-toast-out');

    setTimeout(() => {
      if (toastElement.parentNode) {
        toastElement.parentNode.removeChild(toastElement);
      }
    }, 300);
  }

  // Convenience methods
  public success(message: string, title: string = 'Success'): ToastInstance {
    return this.show({
      title,
      message,
      type: 'success',
      duration: 3000
    });
  }

  public error(message: string, title: string = 'Error'): ToastInstance {
    return this.show({
      title,
      message,
      type: 'error',
      duration: 5000
    });
  }

  public warning(message: string, title: string = 'Warning'): ToastInstance {
    return this.show({
      title,
      message,
      type: 'warning',
      duration: 4000
    });
  }

  public info(message: string, title: string = 'Info'): ToastInstance {
    return this.show({
      title,
      message,
      type: 'info',
      duration: 3000
    });
  }

  public clearAll(): void {
    if (this.container) {
      this.container.innerHTML = '';
    }
  }
}

export const toastService = new ToastService();
