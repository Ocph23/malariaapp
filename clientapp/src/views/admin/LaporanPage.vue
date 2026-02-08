<template>
  <AdminLayout>
    <div class="flex flex-col">
      <PageTitle title="Laporan"></PageTitle>
      <div class="flex justify-end items-end gap-2 pb-5">
        <div>
          <label for="nama" class="block text-sm mb-2 dark:text-white">Mulai Tanggal</label>
          <div class="relative">
            <input type="date" v-model="modelCari.mulai"
              class="py-2.5 sm:py-3 px-4 block w-full border-gray-200 rounded-lg sm:text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-neutral-400 dark:placeholder-neutral-500 dark:focus:ring-neutral-600"
              aria-describedby="nama-error" />
          </div>
          <!-- <p v-if="errors.password" class="text-xs text-red-600 mt-2" id="nama-error">
            {{ errors.nama }}
          </p> -->
        </div>
        <div>
          <label for="nama" class="block text-sm mb-2 dark:text-white">Hingga Tanggal</label>
          <div class="relative">
            <input type="date" v-model="modelCari.hingga"
              class="py-2.5 sm:py-3 px-4 block w-full border-gray-200 rounded-lg sm:text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-neutral-400 dark:placeholder-neutral-500 dark:focus:ring-neutral-600"
              aria-describedby="nama-error" />
          </div>
          <!-- <p v-if="errors.password" class="text-xs text-red-600 mt-2" id="nama-error">
            {{ errors.nama }}
          </p> -->
        </div>
        <button @click="search"
          class="py-3 px-3 inline-flex items-center gap-x-2 text-sm font-medium rounded-lg bg-emerald-500 border border-primary-line text-primary-foreground hover:bg-primary-hover focus:outline-hidden focus:bg-primary-focus disabled:opacity-50 disabled:pointer-events-none">
          Cari
        </button>
      </div>
      <div class="-m-1.5 overflow-x-auto">
        <div class="p-1.5 min-w-full inline-block align-middle">
          <div class="overflow-hidden">
            <table class="min-w-full divide-y divide-gray-200 dark:divide-neutral-700">
              <thead>
                <tr>
                  <th scope="col"
                    class="px-6 py-3 text-start text-xs font-medium text-gray-500 uppercase dark:text-neutral-500">
                    Tanggal Diagnosa
                  </th>
                  <th scope="col"
                    class="px-6 py-3 text-start text-xs font-medium text-gray-500 uppercase dark:text-neutral-500">Name
                    Pasien
                  </th>
                  <th scope="col"
                    class="px-6 py-3 text-start text-xs font-medium text-gray-500 uppercase dark:text-neutral-500">JK
                  </th>
                  <th scope="col"
                    class="px-6 py-3 text-start text-xs font-medium text-gray-500 uppercase dark:text-neutral-500">
                    Hasil Diagnosa</th>
                  <th scope="col"
                    class="px-6 py-3 text-end text-xs font-medium text-gray-500 uppercase dark:text-neutral-500">Action
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in data" :key="item.id"
                  class="odd:bg-white even:bg-gray-100 dark:odd:bg-neutral-900 dark:even:bg-neutral-800">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-800 dark:text-neutral-200">{{
                    item.tanggal_diagnosa }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200">{{
                    item.pasien.nama }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200">{{
                    item.pasien.jenis_kelamin }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200">
                    {{ item.penyakit.kode }}-{{ item.penyakit.nama }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-end text-sm font-medium">
                    <button type="button" @click="showDetail(item)">
                      <InformationCircleIcon class="size-5 hover:size-6 cursor-pointer text-blue-600">
                      </InformationCircleIcon>
                    </button>

                  </td>
                </tr>


              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <div id="detailModal"
      class="hs-overlay hidden size-full fixed top-0 start-0 z-80 overflow-x-hidden overflow-y-auto pointer-events-none"
      role="dialog" tabindex="-1" aria-labelledby="detailModal-label">
      <div
        class="hs-overlay-open:mt-7 hs-overlay-open:opacity-100 hs-overlay-open:duration-500 mt-0 opacity-0 ease-out transition-all sm:max-w-lg sm:w-full m-3 sm:mx-auto min-h-[calc(100%-56px)] flex items-center">
        <div
          class="bg-gray-100 w-full flex flex-col bg-overlay border border-overlay-line shadow-2xs rounded-xl pointer-events-auto">
          <div class="flex justify-between items-center py-3 px-4 border-b border-gray-300">
            <h3 id="detailModal-label" class="font-semibold text-foreground">Detail Diagnosa</h3>
            <button type="button"
              class="size-8 inline-flex justify-center items-center gap-x-2 rounded-full bg-surface border border-surface-line text-surface-foreground hover:bg-surface-hover focus:outline-hidden focus:bg-surface-focus disabled:opacity-50 disabled:pointer-events-none"
              aria-label="Close" data-hs-overlay="#detailModal">
              <span class="sr-only">Close</span>
              <svg class="shrink-0 size-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M18 6 6 18"></path>
                <path d="m6 6 12 12"></path>
              </svg>
            </button>
          </div>
          <form>
            <div class="p-4 overflow-y-auto">
              <div class="space-y-4 p-5">
                <div class="grid">
                  <PageTitle :size="'xs'" class="mb-5" title="Data Pasien"></PageTitle>
                  <div class="flex flex-col md:flex-row mb-2 justify-between">
                    <label class="block text-sm dark:text-white">Nama Pasien</label>
                    <div class="text-sm text-gray-800 dark:text-neutral-200">
                      {{ selectedRiwayat?.pasien.nama }}
                    </div>
                  </div>
                  <div class="flex flex-col md:flex-row mb-2 justify-between">
                    <label class="block text-sm dark:text-white">Jenis Kelamin</label>
                    <div class="text-sm text-gray-800 dark:text-neutral-200">
                      {{ selectedRiwayat?.pasien.jenis_kelamin }}
                    </div>
                  </div>
                  <div class="flex flex-col md:flex-row mb-2 justify-between">
                    <label class="block text-sm dark:text-white">Umur</label>
                    <div class="text-sm text-gray-800 dark:text-neutral-200">

                      {{ HelperService.hitungUmur(selectedRiwayat?.pasien.tanggal_lahir) }}
                    </div>
                  </div>
                  <div class="flex flex-col md:flex-row mb-2 justify-between">
                    <label class="block text-sm dark:text-white">Alamat</label>
                    <div class="text-sm text-gray-800 dark:text-neutral-200">
                      {{ selectedRiwayat?.pasien.alamat }}
                    </div>
                  </div>
                  <PageTitle :size="'xs'" class="my-5" title="Diagnosa"></PageTitle>
                  <div class="flex flex-col md:flex-row mb-2 justify-between">
                    <label class="block text-sm dark:text-white">Penyakit</label>
                    <div class="text-sm text-gray-800 dark:text-neutral-200">
                      {{ selectedRiwayat?.penyakit.kode }} - {{ selectedRiwayat?.penyakit.nama }}
                    </div>

                  </div>
                  <div class="flex flex-col md:flex-row mb-2 justify-between">
                    <label class="block text-sm dark:text-white">Gejala</label>
                  </div>
                  <div class="flex flex-col md:flex-row mb-2 ">
                    <div class="ml-5 text-sm text-gray-800 dark:text-neutral-200">
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
            <div
              class="flex justify-end items-center gap-x-2 py-3 px-4 border-t border-gray-200 dark:border-neutral-800">
              <button type="button"
                class="py-2 px-3 inline-flex items-center gap-x-2 text-sm font-medium rounded-lg bg-layer border border-layer-line text-layer-foreground shadow-2xs hover:bg-layer-hover focus:outline-hidden focus:bg-layer-focus disabled:opacity-50 disabled:pointer-events-none"
                data-hs-overlay="#detailModal">
                Close
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

  </AdminLayout>
</template>

<script setup lang="ts">
import AdminLayout from '@/components/layouts/AdminLayout.vue';

import { useToast } from '@/plugins/toast';

import { useLoading } from '@/plugins/loading';
import { InformationCircleIcon, XCircleIcon } from '@heroicons/vue/24/outline';
import PageTitle from '@/components/PageTitle.vue';
import { reactive, ref } from 'vue';
import z from 'zod';
import HelperService from '@/services/HelperService';
import DiagnosaService from '@/services/DiagnosaService';
import type { RiwayatDiagnosa } from '@/models';
import HSOverlay from '@preline/overlay';
const loadingService = useLoading();
const toast = useToast();


const modelCari = reactive({
  mulai: '',
  hingga: '',
});


const data = ref<Array<RiwayatDiagnosa>>([]);

const cariSchema = z
  .object({
    mulai: z.coerce.date(),
    hingga: z.coerce.date(),
  })
  .refine((data) => data.hingga >= data.mulai, {
    message: 'Tanggal akhir harus setelah tanggal mulai',
    path: ['hingga'],
  })

const errors = ref<Record<string, string>>({});
const cetak = (item: unknown) => {
  // Logic untuk mencetak laporan berdasarkan item
};

const search = () => {
  try {
    errors.value = {};
    cariSchema.parse(modelCari);

    console.log(modelCari);
    DiagnosaService.search(modelCari).then((response) => {
      console.log(response);
      data.value = response;
      toast.success('Laporan berhasil diambil');
    }).catch((error: unknown) => {
      toast.error('Gagal mengambil laporan');
    });

  } catch (err: unknown) {
    if (err instanceof z.ZodError) {
      errors.value = HelperService.mapZodErrors(err);
      console.log(errors);
    }
  }
};

const selectedRiwayat = ref<RiwayatDiagnosa | null>(null);
const showDetail = (riwayat: RiwayatDiagnosa) => {
  selectedRiwayat.value = riwayat;
  HSOverlay.open('#detailModal')
}

</script>

<style scoped></style>
