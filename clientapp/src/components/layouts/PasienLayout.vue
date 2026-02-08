<template>
  <LayoutBase :menus="menus">
    <slot></slot>
  </LayoutBase>
</template>
<script setup lang="ts">
import { EyeDropperIcon, HomeIcon, UserCircleIcon } from '@heroicons/vue/24/outline';
import { ref } from 'vue';
import LayoutBase from './LayoutBase.vue';
import { ClockIcon } from '@heroicons/vue/24/solid';


const menus = ref([
  { name: 'Home', routeName: 'pasien.home', children: null, Icon: HomeIcon },
  { name: 'Diagnosa', routeName: 'pasien.diagnosa', children: null, Icon: EyeDropperIcon },
  { name: 'Riwayat', routeName: 'pasien.riwayat', children: null, Icon: ClockIcon },
]);


</script>

<style scoped></style>
