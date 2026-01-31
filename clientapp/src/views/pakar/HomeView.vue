<script setup lang="ts">
import PageTitle from '@/components/PageTitle.vue';
import TheWelcome from '../../components/TheWelcome.vue'
import PakarLayout from '@/components/layouts/PakarLayout.vue';

import('preline').then(() => {
  console.log("preline ok");
});

</script>

<template>
  <PakarLayout>
    <PageTitle title="Home"></PageTitle>
    <TheWelcome />
  </PakarLayout>
</template>
