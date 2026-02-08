<template>
  <div class="w-full only-print">
    <div class="me-5 lg:me-0 lg:hidden"><!-- Logo --><a
        class="flex-none rounded-md text-xl inline-block font-semibold focus:outline-hidden focus:opacity-80" href="#"
        aria-label="Preline"><img src="/LogoHilab.png" class="w-32 h-auto" alt="Logo"></a><!-- End Logo -->
      <div class="lg:hidden ms-1"></div>
    </div>

    <div class="w-full flex justify-center">
      <PageTitle :size="'md'" class="my-10" title="hasil diagnosa"></PageTitle>
    </div>
    <div>
      <div class="space-y-4">
        <div class="grid">
          <PageTitle :size="'xs'" class="mb-5" title="Data Pasien"></PageTitle>
          <div class="flex  mb-2">
            <label class="block text-sm dark:text-white">Nama Pasien</label>
            <div class="text-sm text-gray-800 dark:text-neutral-200">
              {{ selectedRiwayat?.pasien?.nama }}
            </div>
          </div>
          <div class="flex  mb-2">
            <label class="block text-sm dark:text-white">Jenis Kelamin</label>
            <div class="text-sm text-gray-800 dark:text-neutral-200">
              {{ selectedRiwayat?.pasien?.jenis_kelamin }}
            </div>
          </div>
          <div class="flex  mb-2">
            <label class="block text-sm dark:text-white">Umur</label>
            <div class="text-sm text-gray-800 dark:text-neutral-200">
              {{ HelperService.hitungUmur(selectedRiwayat?.pasien?.tanggal_lahir) }}
            </div>
          </div>
          <div class="flex  mb-2">
            <label class="block text-sm dark:text-white">Alamat</label>
            <div class="text-sm text-gray-800 dark:text-neutral-200">
              {{ selectedRiwayat?.pasien?.alamat }}
            </div>
          </div>
          <PageTitle :size="'xs'" class="my-5" title="Diagnosa"></PageTitle>
          <div class="flex  mb-2">
            <label class="block text-sm dark:text-white">Penyakit</label>
            <div class="text-sm text-gray-800 dark:text-neutral-200">
              {{ selectedRiwayat?.penyakit?.kode }} - {{ selectedRiwayat?.penyakit?.nama }}
            </div>

          </div>
          <div class="flex mb-2">
            <label class="block text-sm dark:text-white">Gejala</label>
            <div class="text-sm text-gray-800 dark:text-neutral-200">
              <ul class="list-disc list-inside">
                <li v-for="gejala in selectedRiwayat?.gejala" :key="gejala.id">
                  {{ gejala.kode }} - {{ gejala.nama }}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import PageTitle from '@/components/PageTitle.vue';
import type { RiwayatDiagnosa } from '@/models';
import HelperService from '@/services/HelperService';
import { ref } from 'vue';

const selectedRiwayat = ref<RiwayatDiagnosa | null>(null);

defineExpose({
  setRiwayat
})

const isPrint = ref(false);

function setRiwayat(riwayat: RiwayatDiagnosa): void {
  selectedRiwayat.value = riwayat;
  isPrint.value = true;
  setTimeout(() => {
    window.print()
  }, 500);
}

</script>

<style scoped>
label {
  min-width: 150px;
}
</style>
