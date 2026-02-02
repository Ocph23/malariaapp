<template>
  <div class="flex flex-col items-start gap-1 mt-6">
    <div class flex>
      <span class="mr-2 rounded-md p-1 bg-blue-300">{{ kode }}</span>
      <label>{{ pertanyaan }}</label>
    </div>
    <div class="w-full">
      <label :for="name" class="block text-sm mb-1 dark:text-white">
        {{ label }}
      </label>

      <div class="relative">
        <select
          :id="name"
          :name="name"
          :value="modelValue"
          @change="onChange"
          :required="required"
          :aria-invalid="!!error"
          :aria-describedby="error ? `${name}-error` : undefined"
          :class="[baseClass, error && errorClass]"
        >
          <option value="" disabled>
            {{ placeholder }}
          </option>

          <option v-for="option in options" :key="option.value" :value="option.value">
            {{ option.label }}
          </option>
        </select>

        <!-- error icon -->
        <div
          v-if="error"
          class="absolute inset-y-0 end-0 pointer-events-none pe-3 flex items-center"
        >
          <svg
            class="size-5 text-red-500"
            viewBox="0 0 16 16"
            fill="currentColor"
            aria-hidden="true"
          >
            <path
              d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8 4a.905.905 0 0 0-.9.995l.35 3.507a.552.552 0 0 0 1.1 0l.35-3.507A.905.905 0 0 0 8 4zm.002 6a1 1 0 1 0 0 2 1 1 0 0 0 0-2z"
            />
          </svg>
        </div>
      </div>

      <p v-if="error" class="text-xs text-red-600 mt-2" :id="`${name}-error`">
        {{ error }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
interface SelectOption {
  label: string
  value: string | number
}

interface JawabanItemProps {
  kode: string
  pertanyaan: string
  name?: string
  label?: string
  modelValue?: string | number
  placeholder?: string
  error?: string
  required?: boolean
}

withDefaults(defineProps<JawabanItemProps>(), {})

const options: SelectOption[] = [
  { label: 'Ya', value: 'ya' },
  { label: 'Tidak', value: 'tidak' },
]

const emit = defineEmits<{
  (e: 'update:modelValue', value: string | number): void
}>()

const onChange = (e: Event) => {
  const value = (e.target as HTMLSelectElement).value
  emit('update:modelValue', value)
}

const baseClass =
  'py-2.5 sm:py-3 px-4 block w-[calc(100%-1rem)] rounded-lg sm:text-sm border focus:ring-1 dark:bg-neutral-900 dark:text-neutral-400'

const errorClass = 'border-red-500 focus:border-red-500 focus:ring-red-500'
</script>

<style scoped>
/* Add your custom styles here */
</style>
