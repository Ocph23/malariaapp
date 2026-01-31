<template>
  <LayoutBase :menus="menus">
    <slot></slot>
  </LayoutBase>
</template>
<script setup lang="ts">
import { HomeIcon, UsersIcon } from '@heroicons/vue/24/outline';
import { ref } from 'vue';
import LayoutBase from './LayoutBase.vue';
import { MapIcon } from '@heroicons/vue/24/solid';

const menus = ref([
  { name: 'Home', routeName: 'admin.home', children: null, Icon: HomeIcon },
  { name: 'Users', routeName: 'admin.user', children: null, Icon: UsersIcon },
  { name: 'Laporan', routeName: 'admin.laporan', children: null, Icon: MapIcon },
]);


</script>

<style scoped></style>
