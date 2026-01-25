import type { IStaticMethods } from "preline/dist";

declare global {
  interface Window {
    // Optional third-party libraries
    _;
    $: typeof import("jquery");
    jQuery: typeof import("jquery");
    DataTable;
    Dropzone;
    VanillaCalendarPro;

    // Preline UI
    HSStaticMethods: IStaticMethods;
  }
}


declare module 'preline' {
  export interface ToastOptions {
    position?: 'top-left' | 'top-center' | 'top-right' | 'bottom-left' | 'bottom-center' | 'bottom-right';
    duration?: number;
    style?: {
      backgroundColor?: string;
      color?: string;
      borderRadius?: string;
      [key: string]: string | undefined;
    };
  }

  export interface HSStaticMethods {
    autoInit(): void;
    toast(message: string, options?: ToastOptions): void;
    // Add other methods as needed
  }

  export const HSStaticMethods: HSStaticMethods;
}

// Extend Window interface
declare global {
  interface Window {
    HSStaticMethods?: import('preline').HSStaticMethods;
  }
}

export { };