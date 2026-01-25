<script setup lang="ts">
import AdminLayout from '@/components/layouts/AdminLayout.vue';
import TheWelcome from '../components/TheWelcome.vue'

import('preline').then(() => {
  console.log("preline ok");
});

</script>

<template>
  <AdminLayout>
    <TheWelcome />
  </AdminLayout>
</template>
