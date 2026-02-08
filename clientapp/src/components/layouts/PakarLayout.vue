<template>
  <LayoutBase :menus="menus">
    <slot></slot>
  </LayoutBase>
</template>
<script setup lang="ts">
import { BugAntIcon, EyeDropperIcon, HomeIcon, ShieldExclamationIcon } from '@heroicons/vue/24/outline';
import { ref } from 'vue';
import LayoutBase from './LayoutBase.vue';


const menus = ref([
  { name: 'Home', routeName: 'pakar.home', children: null, Icon: HomeIcon },
  { name: 'Gejala', routeName: 'pakar.gejala', children: null, Icon: ShieldExclamationIcon },
  { name: 'Penyakit', routeName: 'pakar.penyakit', children: null, Icon: BugAntIcon },
]);


</script>

<style scoped></style>
