<template>
  <div class="p-6 max-w-4xl mx-auto">
    <h1 class="text-2xl font-bold mb-6 text-gray-800">Preline Toast with TypeScript</h1>

    <!-- Toast Container (Auto created by service) -->

    <!-- Demo Controls -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Basic Toasts -->
      <div class="space-y-4">
        <h2 class="text-lg font-semibold text-gray-700">Basic Toasts</h2>

        <div class="space-y-3">
          <button @click="showSuccess"
            class="w-full bg-green-500 hover:bg-green-600 text-white px-4 py-3 rounded-lg transition-colors">
            Success Toast
          </button>

          <button @click="showError"
            class="w-full bg-red-500 hover:bg-red-600 text-white px-4 py-3 rounded-lg transition-colors">
            Error Toast
          </button>

          <button @click="showWarning"
            class="w-full bg-yellow-500 hover:bg-yellow-600 text-white px-4 py-3 rounded-lg transition-colors">
            Warning Toast
          </button>

          <button @click="showInfo"
            class="w-full bg-blue-500 hover:bg-blue-600 text-white px-4 py-3 rounded-lg transition-colors">
            Info Toast
          </button>
        </div>
      </div>

      <!-- Advanced Toasts -->
      <div class="space-y-4">
        <h2 class="text-lg font-semibold text-gray-700">Advanced Toasts</h2>

        <div class="space-y-3">
          <button @click="showCustomToast"
            class="w-full bg-purple-500 hover:bg-purple-600 text-white px-4 py-3 rounded-lg transition-colors">
            Custom Toast
          </button>

          <button @click="showToastWithCallback"
            class="w-full bg-indigo-500 hover:bg-indigo-600 text-white px-4 py-3 rounded-lg transition-colors">
            Toast with Callback
          </button>

          <button @click="showPersistentToast"
            class="w-full bg-pink-500 hover:bg-pink-600 text-white px-4 py-3 rounded-lg transition-colors">
            Persistent Toast
          </button>

          <button @click="clearAllToasts"
            class="w-full bg-gray-500 hover:bg-gray-600 text-white px-4 py-3 rounded-lg transition-colors">
            Clear All Toasts
          </button>
        </div>
      </div>

      <!-- Position Demo -->
      <div class="md:col-span-2 space-y-4">
        <h2 class="text-lg font-semibold text-gray-700">Toast Positions</h2>

        <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
          <button v-for="position in toastPositions" :key="position" @click="showPositionedToast(position)"
            class="bg-gray-200 hover:bg-gray-300 text-gray-800 px-4 py-2 rounded transition-colors">
            {{ position }}
          </button>
        </div>
      </div>
    </div>

    <!-- Toast Controls -->
    <div v-if="activeToasts.length > 0" class="mt-8 p-4 bg-gray-50 rounded-lg">
      <h3 class="font-semibold text-gray-700 mb-3">Active Toasts ({{ activeToasts.length }})</h3>
      <div class="space-y-2">
        <div v-for="toast in activeToasts" :key="toast.id"
          class="flex items-center justify-between p-3 bg-white rounded border">
          <div>
            <span class="font-medium">{{ toast.config.title }}</span>
            <span class="text-sm text-gray-500 ml-2">{{ toast.config.type }}</span>
          </div>
          <button @click="removeToast(toast.id)" class="text-red-500 hover:text-red-700">
            Remove
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { toastService, type ToastInstance, type ToastPosition } from '@/services/ToastService';

// Reactive state
const activeToasts = ref<ToastInstance[]>([]);
const toastPositions: ToastPosition[] = [
  'top-left', 'top-center', 'top-right',
  'bottom-left', 'bottom-center', 'bottom-right'
];

// Toast methods
const showSuccess = () => {
  const toast = toastService.success('Operation completed successfully!');
  activeToasts.value.push(toast);
};

const showError = () => {
  const toast = toastService.error('Failed to save data. Please try again.');
  activeToasts.value.push(toast);
};

const showWarning = () => {
  const toast = toastService.warning('Please review your input before submitting.');
  activeToasts.value.push(toast);
};

const showInfo = () => {
  const toast = toastService.info('New update available. Check the changelog.');
  activeToasts.value.push(toast);
};

const showCustomToast = () => {
  const toast = toastService.show({
    title: 'Custom Notification',
    message: 'This is a custom toast with special styling',
    type: 'custom',
    duration: 4000,
    icon: '<i class="fas fa-star text-yellow-500"></i>',
    position: 'top-center'
  });
  activeToasts.value.push(toast);
};

const showToastWithCallback = () => {
  const toast = toastService.show({
    title: 'Action Required',
    message: 'Click to perform an action',
    type: 'info',
    duration: 0, // No auto-close
    onClose: () => {
      console.log('Toast was closed');
      showSuccess();
    }
  });
  activeToasts.value.push(toast);
};

const showPersistentToast = () => {
  const toast = toastService.show({
    title: 'Important Notice',
    message: 'This toast will not auto-close. Click X to dismiss.',
    type: 'warning',
    duration: 0 // No auto-close
  });
  activeToasts.value.push(toast);
};

const showPositionedToast = (position: ToastPosition) => {
  const toast = toastService.show({
    title: `${position} Toast`,
    message: `This toast is positioned at ${position}`,
    type: 'info',
    position,
    duration: 3000
  });
  activeToasts.value.push(toast);
};

const removeToast = (toastId: string) => {
  const index = activeToasts.value.findIndex(t => t.id === toastId);
  if (index !== -1) {
    activeToasts.value.splice(index, 1);
  }
};

const clearAllToasts = () => {
  toastService.clearAll();
  activeToasts.value = [];
};

// Lifecycle
onMounted(() => {
  // Initialize Preline if needed
  if (window.HSStaticMethods) {
    window.HSStaticMethods.autoInit();
  }
});
</script>

<style scoped>
/* Custom animations */
@keyframes toastIn {
  from {
    opacity: 0;
    transform: translateY(-20px) scale(0.95);
  }

  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes toastOut {
  from {
    opacity: 1;
    transform: translateY(0) scale(1);
  }

  to {
    opacity: 0;
    transform: translateY(-20px) scale(0.95);
  }
}

.animate-toast-in {
  animation: toastIn 0.3s ease-out;
}

.animate-toast-out {
  animation: toastOut 0.3s ease-in;
}
</style>