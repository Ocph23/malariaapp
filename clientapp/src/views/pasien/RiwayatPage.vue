<template>
  <PasienLayout>
    <div class="flex flex-col no-print">
      <div class="-m-1.5 overflow-x-auto">
        <div class="p-1.5 min-w-full inline-block align-middle">
          <PageTitle title="Riwayat Diagnosa"></PageTitle>
          <div class="overflow-hidden mt-5">
            <table class="min-w-full divide-y divide-gray-200 dark:divide-neutral-700">
              <thead>
                <tr>
                  <th scope="col"
                    class="px-6 py-3 text-start text-xs font-medium text-gray-500 uppercase dark:text-neutral-500">
                    Tanggal Diagnosa
                  </th>
                  <th scope="col"
                    class="px-6 py-3 text-start text-xs font-medium text-gray-500 uppercase dark:text-neutral-500">
                    Penyakit
                  </th>
                  <th scope="col"
                    class="px-6 py-3 text-start text-xs font-medium text-gray-500 uppercase dark:text-neutral-500">
                    Gejala
                  </th>
                  <th scope="col"
                    class="px-6 py-3 text-end text-xs font-medium text-gray-500 uppercase dark:text-neutral-500">
                    Action
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in data.diagnosas" :key="item.id"
                  class="odd:bg-white even:bg-gray-100 dark:odd:bg-neutral-900 dark:even:bg-neutral-800">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-800 dark:text-neutral-200">
                    {{ new Date(item.tanggal_diagnosa).toLocaleDateString() }} {{ new
                      Date(item.tanggal_diagnosa).toLocaleTimeString() }}

                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200">
                    {{ item.penyakit.kode }} - {{ item.penyakit.nama }}
                  </td>
                  <td class="px-6 py-4 whitespace-pre-wrap text-sm text-gray-800 dark:text-neutral-200">
                    <span v-for="gejala in item.gejala" :key="gejala.id">{{ gejala.nama }}, </span>
                  </td>
                  <td class="w-24 px-6 py-4 font-medium gap-2 text-end">
                    <button type="button" @click="print(item)">
                      <PrinterIcon class="size-5 hover:size-6 cursor-pointer text-blue-600">
                      </PrinterIcon>
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

    <PrintDiagnosaPage v-if="isPrint" ref="printDiagnosaRef"></PrintDiagnosaPage>

    <ConfirmDialog id="deleteConfirm" @confirm="deletex"></ConfirmDialog>
  </PasienLayout>
</template>

<script setup lang="ts">
import { useToast } from '@/plugins/toast'
import { useLoading } from '@/plugins/loading'
import { reactive, ref } from 'vue'
import type { RiwayatDiagnosa } from '@/models'
import { PrinterIcon, XCircleIcon } from '@heroicons/vue/24/outline'
const loadingService = useLoading()
const toast = useToast()

import { HSOverlay } from 'preline'
import ConfirmDialog from '@/components/ConfirmDialog.vue'
import PageTitle from '@/components/PageTitle.vue'
import PasienLayout from '@/components/layouts/PasienLayout.vue'
import PasienService from '@/services/PasienService'
import DiagnosaService from '@/services/DiagnosaService'
import PrintDiagnosaPage from './PrintDiagnosaPage.vue'

const data = reactive({ diagnosas: [] as RiwayatDiagnosa[] })
const printDiagnosaRef = ref<InstanceType<typeof PrintDiagnosaPage> | null>(null)

const isPrint = ref(false)

const load = () => {
  const loader = loadingService.spinner('Loading data...', { fullscreen: true })
  PasienService.riwayat()
    .then((response) => {
      data.diagnosas = response
      loader.remove()
    })
    .catch((error) => {
      console.log(error)
      loader.remove()
    })
}



const deleteId = ref<number>(0)

const confirmDelete = (id: number) => {
  deleteId.value = id
  HSOverlay.open('#deleteConfirm')
}

const deletex = async () => {
  try {
    const loader = loadingService.spinner('Delete data...', { fullscreen: true })
    DiagnosaService.delete(deleteId.value)
      .then(() => {
        data.diagnosas = data.diagnosas.filter((item) => item.id !== deleteId.value)
        loader.remove()
        toast.success('Data deleted successfully!')
      })
      .catch(() => {
        loader.remove()
      })
  } catch (error: unknown) {
    const err = error as Error
    toast.error('Failed to save data', err.message)
  }
}

const print = (riwayatDiagnosa: RiwayatDiagnosa) => {
  printDiagnosaRef.value?.setRiwayat(riwayatDiagnosa)
  setTimeout(() => {
    isPrint.value = true

  }, 500)
}

load()
</script>

<style scoped></style>
