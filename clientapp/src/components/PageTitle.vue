<template>
  <div :class="getSizeClass(props.size)"
    class="w-full font-bold decoration-amber-500 underline underline-offset-8 decoration-3 uppercase">
    {{ props.title }}
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{ title: string, size?: 'xs' | 'sm' | 'md' | 'lg' }>()
const getSizeClass = (size: string | undefined) => {
  switch (size) {
    case 'xs':
      return 'text-sm'
    case 'sm':
      return 'text-lg md:text-xl'
    case 'lg':
      return 'text-3xl md:text-4xl'
    case 'md':
    default:
      return 'text-xl md:text-2xl'
  }
}
</script>

<style scoped></style>
