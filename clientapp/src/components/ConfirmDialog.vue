<template>
  <div :id="id"
    class=" flex justify-between items-center hs-overlay hidden size-full fixed top-0 start-0 z-[80] overflow-x-hidden overflow-y-auto">
    <div class=" hs-overlay-open:opacity-100 opacity-0 transition-all sm:max-w-md sm:w-full m-3 sm:mx-auto">
      <div class="bg-white border rounded-xl shadow-sm">
        <!-- Header -->
        <div class="px-4 py-3 border-b border-gray-200">
          <h3 class="font-bold text-gray-800">
            {{ title }}
          </h3>
        </div>

        <!-- Body -->
        <div class="p-4">
          <p class="text-gray-600">
            {{ message }}
          </p>
        </div>

        <!-- Footer -->
        <div class="flex justify-end gap-2 px-4 py-3 ">
          <button class="px-3 py-2 bg-gray-200 rounded" :data-hs-overlay="`#${id}`">
            {{ cancelText }}
          </button>

          <button class="px-3 py-2 bg-red-600 text-white rounded" @click="onConfirm">
            {{ confirmText }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { HSOverlay } from 'preline'

const props = defineProps({
  id: { type: String, required: true },
  title: { type: String, default: 'Konfirmasi' },
  message: { type: String, default: 'Apakah Anda yakin?' },
  confirmText: { type: String, default: 'Ya' },
  cancelText: { type: String, default: 'Batal' }
})

const emit = defineEmits(['confirm'])

const onConfirm = () => {
  emit('confirm')
  HSOverlay.close(`#${props.id}`)
}
</script>
