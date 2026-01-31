<template>
  <PakarLayout>
    <div class="flex flex-col">
      <div class="-m-1.5 overflow-x-auto">
        <div class="p-1.5 min-w-full inline-block align-middle">
          <PageTitle title="data Gejala"></PageTitle>
          <div class="flex justify-end pb-5">
            <PlusSmallIcon @click="addModal" class="size-8 bg-teal-500 rounded-full p-1 text-white"></PlusSmallIcon>
          </div>
          <div class="overflow-hidden">
            <table class="min-w-full divide-y divide-gray-200 dark:divide-neutral-700">
              <thead>
                <tr>
                  <th scope="col"
                    class="px-6 py-3 text-start text-xs font-medium text-gray-500 uppercase dark:text-neutral-500">
                    Kode
                  </th>
                  <th scope="col"
                    class="px-6 py-3 text-start text-xs font-medium text-gray-500 uppercase dark:text-neutral-500">Nama
                    Gejala
                  </th>
                  <th scope="col"
                    class="px-6 py-3 text-start text-xs font-medium text-gray-500 uppercase dark:text-neutral-500">
                    Status Aktif</th>
                  <th scope="col"
                    class="px-6 py-3 text-end text-xs font-medium text-gray-500 uppercase dark:text-neutral-500">Action
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in data.gejalas" :key="item.id"
                  class="odd:bg-white even:bg-gray-100 dark:odd:bg-neutral-900 dark:even:bg-neutral-800">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-800 dark:text-neutral-200">
                    {{ item.kode }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200">
                    {{ item.nama }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200">
                    <input type="checkbox" :checked="item.is_active">
                  </td>
                  <td class=" px-6 py-4  font-medium flex justify-end gap-2">
                    <button type="button" @click="edit(item)">
                      <PencilSquareIcon class="size-5 hover:size-6 cursor-pointer text-amber-600"></PencilSquareIcon>
                    </button>
                    <button type="button" @click="confirmDelete(item.id)">
                      <XCircleIcon class="size-5 hover:size-6 cursor-pointer text-red-600"></XCircleIcon>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <div id="gejalaModal"
      class="hs-overlay hidden size-full fixed top-0 start-0 z-80 overflow-x-hidden overflow-y-auto pointer-events-none"
      role="dialog" tabindex="-1" aria-labelledby="gejalaModal-label">
      <div
        class="hs-overlay-open:mt-7 hs-overlay-open:opacity-100 hs-overlay-open:duration-500 mt-0 opacity-0 ease-out transition-all sm:max-w-lg sm:w-full m-3 sm:mx-auto min-h-[calc(100%-56px)] flex items-center">
        <div
          class="bg-gray-100 w-full flex flex-col bg-overlay border border-overlay-line shadow-2xs rounded-xl pointer-events-auto">
          <div class="flex justify-between items-center py-3 px-4 border-b border-gray-300">
            <h3 id="gejalaModal-label" class="font-semibold text-foreground">
              Tambah Gejala
            </h3>
            <button type="button"
              class="size-8 inline-flex justify-center items-center gap-x-2 rounded-full bg-surface border border-surface-line text-surface-foreground hover:bg-surface-hover focus:outline-hidden focus:bg-surface-focus disabled:opacity-50 disabled:pointer-events-none"
              aria-label="Close" data-hs-overlay="#gejalaModal">
              <span class="sr-only">Close</span>
              <svg class="shrink-0 size-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M18 6 6 18"></path>
                <path d="m6 6 12 12"></path>
              </svg>
            </button>
          </div>
          <form @submit.prevent="handleSubmit">
            <div class="p-4 overflow-y-auto">
              <div class="space-y-4 p-5">
                <div class="grid gap-y-4">
                  <!-- Form Group -->
                  <div>
                    <label for="gejalaname" class="block text-sm mb-2 dark:text-white">Kode</label>
                    <div class="relative">
                      <input v-model="gejala.kode"
                        class="py-2.5 sm:py-3 px-4 block w-full border-gray-200 rounded-lg sm:text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-neutral-400 dark:placeholder-neutral-500 dark:focus:ring-neutral-600"
                        aria-describedby="gejalaname-error">
                    </div>
                    <p v-if="errors.kode" class="text-xs text-red-600 mt-2" id="email-error">
                      {{ errors.kode }}
                    </p>
                  </div>
                  <div>
                    <label for="nama" class="block text-sm mb-2 dark:text-white">Nama Gejala</label>
                    <div class="relative">
                      <input v-model="gejala.nama"
                        class="py-2.5 sm:py-3 px-4 block w-full border-gray-200 rounded-lg sm:text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-neutral-400 dark:placeholder-neutral-500 dark:focus:ring-neutral-600"
                        aria-describedby="nama-error">
                    </div>
                    <p v-if="errors.password" class="text-xs text-red-600 mt-2" id="nama-error">
                      {{ errors.nama }}
                    </p>
                  </div>
                  <div class="flex">
                    <label for="is_active" class="block text-sm mb-2 dark:text-white">Aktif</label>
                    <input type="checkbox" v-model="gejala.is_active"
                      class="w-4 h-4 py-2.5 mx-4 sm:py-3 px-4 block  border-gray-200 rounded-lg sm:text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-neutral-400 dark:placeholder-neutral-500 dark:focus:ring-neutral-600"
                      required aria-describedby="nama-error">
                    <p v-if="errors.is_active" class="text-xs text-red-600 mt-2" id="is_active-error">
                      {{ errors.is_active }}
                    </p>
                  </div>

                </div>

              </div>
            </div>
            <div
              class="flex justify-end items-center gap-x-2 py-3 px-4 border-t border-gray-200 dark:border-neutral-800">
              <button type="button"
                class="py-2 px-3 inline-flex items-center gap-x-2 text-sm font-medium rounded-lg bg-layer border border-layer-line text-layer-foreground shadow-2xs hover:bg-layer-hover focus:outline-hidden focus:bg-layer-focus disabled:opacity-50 disabled:pointer-events-none"
                data-hs-overlay="#gejalaModal">
                Close
              </button>
              <button type="submit"
                class="py-2 px-3 inline-flex items-center gap-x-2 text-sm font-medium rounded-lg bg-primary border border-primary-line text-primary-foreground hover:bg-primary-hover focus:outline-hidden focus:bg-primary-focus disabled:opacity-50 disabled:pointer-events-none">
                Save changes
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <ConfirmDialog id="deleteConfirm" @confirm="deletex"></ConfirmDialog>

  </PakarLayout>

</template>

<script setup lang="ts">
import { useToast } from '@/plugins/toast';
import { useLoading } from '@/plugins/loading';
import GejalaService from '@/services/GejalaService';
import { reactive, ref } from 'vue';
import type { Gejala } from '@/models';
import { PencilSquareIcon, PlusSmallIcon, XCircleIcon } from '@heroicons/vue/24/outline';
const loadingService = useLoading();
const toast = useToast();


import { HSOverlay } from "preline"
import z from 'zod';
import HelperService from '@/services/HelperService';
import ConfirmDialog from '@/components/ConfirmDialog.vue';
import PakarLayout from '@/components/layouts/PakarLayout.vue';
import PageTitle from '@/components/PageTitle.vue';


const addModal = () => {
  gejala.id = 0;
  gejala.kode = '';
  gejala.nama = '';
  gejala.is_active = true;
  HSOverlay.open("#gejalaModal")
}




// buka

// tutup

const data = reactive({ gejalas: [] as Gejala[] })

const gejala = reactive({
  id: 0,
  kode: '',
  nama: '',
  is_active: true,
} as Gejala)


const gejalaSchema = z.object({
  kode: z.string().nonempty(),
  nama: z.string().nonempty(),
  is_active: z.boolean()
});


const load = () => {
  const loader = loadingService.spinner('Loading data...', { fullscreen: true });
  GejalaService.get().then(response => {
    data.gejalas = response;
    loader.remove();
  }).catch(error => {
    console.log(error);
    loader.remove();
  });
}

const errors = ref<Record<string, string>>({})


const edit = (oldGejala: Gejala) => {
  gejala.is_active = oldGejala.is_active;
  gejala.kode = oldGejala.kode;
  gejala.nama = oldGejala.nama;
  gejala.id = oldGejala.id;
  HSOverlay.open("#gejalaModal")
}


const handleSubmit = async () => {


  const result = gejalaSchema.safeParse(gejala);
  console.log(result);
  if (result.success) {
    const loader = loadingService.spinner('Saving data...', { fullscreen: true });

    if (gejala.id > 0) {
      GejalaService.put(gejala.id, gejala).then(() => {

        const row = data.gejalas.find(item => item.id === gejala.id);
        if (row) {
          row.kode = gejala.kode;
          row.nama = gejala.nama;
          row.is_active = gejala.is_active;
        }


        toast.success('Data saved successfully!');
        HSOverlay.close("#gejalaModal")
        loader.remove();
      }).catch(error => {
        console.log(error);
      });
    } else {
      GejalaService.post(gejala as Gejala).then(response => {
        data.gejalas.push(response);
        toast.success('Data saved successfully!');
        HSOverlay.close("#gejalaModal")
        loader.remove();
      }).catch(error => {
        console.log(error);
      });
    }



  } else {
    errors.value = HelperService.mapZodErrors(result.error);
    console.log(errors.value);
  }
}



const deleteId = ref<number>(0);

const confirmDelete = (id: number) => {
  deleteId.value = id;
  HSOverlay.open("#deleteConfirm")
}


const deletex = async () => {
  try {

    const loader = loadingService.spinner('Delete data...', { fullscreen: true });
    GejalaService.delete(deleteId.value).then(() => {
      data.gejalas = data.gejalas.filter(item => item.id !== deleteId.value);
      loader.remove();
      toast.success('Data deleted successfully!');
    }).catch(() => {
      loader.remove();
    });
  } catch (error: unknown) {
    const err = error as Error
    toast.error('Failed to save data', err.message);
  }
};


load();
</script>

<style scoped></style>
