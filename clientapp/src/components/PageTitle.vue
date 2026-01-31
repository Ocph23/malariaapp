<template>
  <div class="w-full text-2xl font-bold  decoration-amber-500 underline underline-offset-8 decoration-3 uppercase">
    {{ props.title }}
  </div>
</template>

<script setup lang="ts">

const props = defineProps<{ title: string }>();

</script>

<style scoped></style>
