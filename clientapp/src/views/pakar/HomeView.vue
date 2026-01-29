<script setup lang="ts">
import TheWelcome from '../../components/TheWelcome.vue'
import PakarLayout from '@/components/layouts/PakarLayout.vue';

import('preline').then(() => {
  console.log("preline ok");
});

</script>

<template>
  <PakarLayout>
    <TheWelcome />
  </PakarLayout>
</template>
