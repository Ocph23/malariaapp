<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div class="w-full flex flex-col ">
    <label :for="name" class="block text-sm mb-1 dark:text-white">
      {{ label }}
    </label>

    <div class="relative">
      <input :id="name" :name="name" :type="type" :value="modelValue" @input="onInput" :required="required"
        :aria-invalid="!!error" :aria-describedby="error ? `${name}-error` : undefined" :class="[
          baseClass,
          error && errorClass
        ]" />

      <!-- icon error -->
      <div v-if="error" class="absolute inset-y-0 end-0 pointer-events-none pe-3 flex items-center">
        <svg class="size-5 text-red-500" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
          <path
            d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8 4a.905.905 0 0 0-.9.995l.35 3.507a.552.552 0 0 0 1.1 0l.35-3.507A.905.905 0 0 0 8 4zm.002 6a1 1 0 1 0 0 2 1 1 0 0 0 0-2z" />
        </svg>
      </div>
    </div>

    <p v-if="error" class="text-xs text-red-600 mt-2" :id="`${name}-error`">
      {{ error }}
    </p>
  </div>
</template>

<script setup lang="ts">
interface InputProps {
  name: string
  label: string
  type?: string
  modelValue?: string | number
  error?: string
  required?: boolean
}

const props = withDefaults(defineProps<InputProps>(), {
  type: 'text',
  required: false
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()

const onInput = (e: Event) => {
  emit('update:modelValue', (e.target as HTMLInputElement).value)
}

const baseClass =
  'py-2.5 sm:py-3 px-4 block w-[calc(100%-1rem)] rounded-lg sm:text-sm border focus:ring-1 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:text-neutral-400'

const errorClass =
  'border-red-500 focus:border-red-500 focus:ring-red-500'
</script>
