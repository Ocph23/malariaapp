export interface LoadingConfig {
  message?: string;
  type?: 'spinner' | 'dots' | 'bar';
  color?: string;
  overlay?: boolean;
  fullscreen?: boolean;
  showPercentage?: boolean;
  showCancel?: boolean;
  onCancel?: () => void;
}

export interface LoadingInstance {
  id: string;
  element: HTMLElement;
  config: LoadingConfig;
  progress: number;
  remove: () => void;
  updateProgress: (progress: number) => void;
  updateMessage: (message: string) => void;
}

export class LoadingService {
  private instances: Map<string, LoadingInstance> = new Map();
  private container: HTMLElement | null = null;

  private createSpinner(color: string = '#3b82f6'): string {
    return `
      <svg class="w-8 h-8 animate-spin" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="${color}" stroke-width="4" fill="none"/>
        <path class="opacity-75" fill="${color}" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
      </svg>
    `
  }

  private createDots(color: string = '#3b82f6'): string {
    return `
      <div class="flex space-x-1">
        <div class="w-2 h-2 rounded-full bg-${color}-500 animate-bounce"></div>
        <div class="w-2 h-2 rounded-full bg-${color}-500 animate-bounce" style="animation-delay: -0.2s"></div>
        <div class="w-2 h-2 rounded-full bg-${color}-500 animate-bounce" style="animation-delay: -0.4s"></div>
      </div>
    `
  }

  private createProgressBar(color: string = '#3b82f6'): string {
    return `
      <div class="w-24 h-2 bg-gray-200 rounded-full overflow-hidden">
        <div class="h-full bg-${color}-500 animate-progress"></div>
      </div>
    `
  }

  public show(config: LoadingConfig = {}): LoadingInstance {
    const id = `loading-${Date.now()}`

    const defaultConfig: LoadingConfig = {
      message: 'Loading...',
      type: 'spinner',
      overlay: true,
      fullscreen: false,
      showPercentage: false,
      showCancel: false,
      ...config
    }

    const element = this.createElement(id, defaultConfig)

    if (defaultConfig.fullscreen) {
      document.body.appendChild(element)
    } else {
      if (!this.container) {
        this.container = this.createContainer()
      }
      this.container.appendChild(element)
    }

    const instance: LoadingInstance = {
      id,
      element,
      config: defaultConfig,
      progress: 0,
      remove: () => this.hide(id),
      updateProgress: (progress: number) => this.updateProgress(id, progress),
      updateMessage: (message: string) => this.updateMessage(id, message)
    }

    this.instances.set(id, instance)
    return instance
  }

  private createElement(id: string, config: LoadingConfig): HTMLElement {
    const element = document.createElement('div')
    element.id = id

    const overlay = config.overlay ? 'bg-black/50' : ''
    const fullscreen = config.fullscreen ? 'fixed inset-0' : 'absolute'

    element.className = `${fullscreen} z-50 flex items-center justify-center ${overlay}`

    let loaderHTML = ''
    if (config.type === 'spinner') {
      loaderHTML = this.createSpinner(config.color)
    } else if (config.type === 'dots') {
      loaderHTML = this.createDots(config.color)
    } else if (config.type === 'bar') {
      loaderHTML = this.createProgressBar(config.color)
    }

    element.innerHTML = `
      <div class="bg-white rounded-lg shadow-lg p-6 min-w-[300px] z-[9000]">
        <div class="flex flex-col items-center space-y-4">
          ${loaderHTML}
          <div class="text-center">
            <p class="text-gray-700">${config.message}</p>
            ${config.showPercentage ? `
              <div class="mt-2">
                <div class="text-lg font-bold" id="${id}-percentage">0%</div>
                <div class="w-full bg-gray-200 rounded-full h-2 mt-2">
                  <div id="${id}-progress" class="bg-blue-500 h-2 rounded-full" style="width: 0%"></div>
                </div>
              </div>
            ` : ''}
          </div>
          ${config.showCancel ? `
            <button
              id="${id}-cancel"
              class="mt-2 px-4 py-1 text-sm text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded"
            >
              Cancel
            </button>
          ` : ''}
        </div>
      </div>
    `

    if (config.showCancel) {
      const cancelBtn = element.querySelector(`#${id}-cancel`)
      cancelBtn?.addEventListener('click', () => {
        config.onCancel?.()
        this.hide(id)
      })
    }

    return element
  }

  private createContainer(): HTMLElement {
    const container = document.createElement('div')
    container.id = 'loading-container'
    container.className = 'fixed inset-0 z-40 pointer-events-none'
    document.body.appendChild(container)
    return container
  }

  public updateProgress(id: string, progress: number): void {
    const instance = this.instances.get(id)
    if (!instance) return

    const clampedProgress = Math.min(100, Math.max(0, progress))
    instance.progress = clampedProgress

    const percentElement = document.getElementById(`${id}-percentage`)
    const progressElement = document.getElementById(`${id}-progress`)

    if (percentElement) {
      percentElement.textContent = `${Math.round(clampedProgress)}%`
    }

    if (progressElement) {
      progressElement.style.width = `${clampedProgress}%`
    }
  }

  public updateMessage(id: string, message: string): void {
    const instance = this.instances.get(id)
    if (!instance) return

    const messageElement = instance.element.querySelector('p')
    if (messageElement) {
      messageElement.textContent = message
    }
  }

  public hide(id: string): void {
    const instance = this.instances.get(id)
    if (!instance) return

    if (instance.element.parentNode) {
      instance.element.parentNode.removeChild(instance.element)
    }

    this.instances.delete(id)

    if (this.instances.size === 0 && this.container) {
      this.container.remove()
      this.container = null
    }
  }

  public hideAll(): void {
    this.instances.forEach(instance => {
      setTimeout(() => {
        this.hide(instance.id)
      }, 500);
    })
  }

  // Convenience methods
  public spinner(message?: string, config?: Partial<LoadingConfig>): LoadingInstance {
    return this.show({
      message,
      type: 'spinner',
      ...config
    })
  }

  public progress(message?: string, config?: Partial<LoadingConfig>): LoadingInstance {
    return this.show({
      message,
      type: 'bar',
      showPercentage: true,
      ...config
    })
  }

  public dots(message?: string, config?: Partial<LoadingConfig>): LoadingInstance {
    return this.show({
      message,
      type: 'dots',
      ...config
    })
  }

  public fullscreen(message?: string, config?: Partial<LoadingConfig>): LoadingInstance {
    return this.show({
      message,
      fullscreen: true,
      overlay: true,
      ...config
    })
  }
}

export const loadingService = new LoadingService()
