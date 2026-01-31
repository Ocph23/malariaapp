<template>
  <div class="p-4 md:p-7 grid grid-cols-1 md:grid-cols-2 items-center gap-5 w-full justify-center">
    <div class="md:h-screen flex flex-col justify-center items-center gap-2 mb-5">
      <img src="../../assets/images/LogoHilab.png" class="h-auto w-[70%]" alt="Logo">
    </div>
    <div
      class="md:h-auto w-full  lg:w-[70%] bg-white border border-gray-200 rounded-xl shadow-2xs dark:bg-neutral-900 dark:border-neutral-700">
      <slot></slot>
    </div>

  </div>
</template>

<script setup lang="ts">

</script>

<style scoped></style>
