<template>
  <PakarLayout>
    <div class="flex flex-col">
      <div class="-m-1.5 overflow-x-auto">
        <div class="p-1.5 min-w-full inline-block align-middle">
          <PageTitle title="Data Penyakit"></PageTitle>
          <div class="flex justify-end pb-5">
            <PlusSmallIcon
              @click="addModal"
              class="size-8 bg-teal-500 rounded-full p-1 text-white"
            ></PlusSmallIcon>
          </div>
          <div class="overflow-hidden">
            <table class="min-w-full divide-y divide-gray-200 dark:divide-neutral-700">
              <thead>
                <tr>
                  <th
                    scope="col"
                    class="px-6 py-3 text-start text-xs font-medium text-gray-500 uppercase dark:text-neutral-500"
                  >
                    Kode
                  </th>
                  <th
                    scope="col"
                    class="px-6 py-3 text-start text-xs font-medium text-gray-500 uppercase dark:text-neutral-500"
                  >
                    Nama Penyakit
                  </th>
                  <th
                    scope="col"
                    class="px-6 py-3 text-start text-xs font-medium text-gray-500 uppercase dark:text-neutral-500"
                  >
                    Status Aktif
                  </th>
                  <th
                    scope="col"
                    class="px-6 py-3 text-end text-xs font-medium text-gray-500 uppercase dark:text-neutral-500"
                  >
                    Action
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="item in data.penyakits"
                  :key="item.id"
                  class="odd:bg-white even:bg-gray-100 dark:odd:bg-neutral-900 dark:even:bg-neutral-800"
                >
                  <td
                    class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-800 dark:text-neutral-200"
                  >
                    {{ item.kode }}
                  </td>
                  <td
                    class="px-6 py-4 whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200"
                  >
                    {{ item.nama }}
                  </td>
                  <td
                    class="px-6 py-4 whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200"
                  >
                    {{ item.nama }}
                  </td>
                  <td
                    class="px-6 py-4 whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200"
                  >
                    {{ item.nama }}
                  </td>
                  <td class="px-6 py-4 text-sm text-gray-800 dark:text-neutral-200">
                    {{ item.solusi }}
                  </td>
                  <td class="px-6 py-4 font-medium flex justify-end gap-2">
                    <button type="button" @click="detail(item)">
                      <ListBulletIcon
                        class="size-5 hover:size-6 cursor-pointer text-blue-600"
                      ></ListBulletIcon>
                    </button>
                    <button type="button" @click="edit(item)">
                      <PencilSquareIcon
                        class="size-5 hover:size-6 cursor-pointer text-amber-600"
                      ></PencilSquareIcon>
                    </button>
                    <button type="button" @click="confirmDelete(item.id)">
                      <XCircleIcon
                        class="size-5 hover:size-6 cursor-pointer text-red-600"
                      ></XCircleIcon>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <div
      id="penyakitModal"
      class="hs-overlay hidden size-full fixed top-0 start-0 z-80 overflow-x-hidden overflow-y-auto pointer-events-none"
      role="dialog"
      tabindex="-1"
      aria-labelledby="penyakitModal-label"
    >
      <div
        class="hs-overlay-open:mt-7 hs-overlay-open:opacity-100 hs-overlay-open:duration-500 mt-0 opacity-0 ease-out transition-all sm:max-w-lg sm:w-full m-3 sm:mx-auto min-h-[calc(100%-56px)] flex items-center"
      >
        <div
          class="bg-gray-100 w-full flex flex-col bg-overlay border border-overlay-line shadow-2xs rounded-xl pointer-events-auto"
        >
          <div class="flex justify-between items-center py-3 px-4 border-b border-gray-300">
            <h3 id="penyakitModal-label" class="font-semibold text-foreground">Tambah Penyakit</h3>
            <button
              type="button"
              class="size-8 inline-flex justify-center items-center gap-x-2 rounded-full bg-surface border border-surface-line text-surface-foreground hover:bg-surface-hover focus:outline-hidden focus:bg-surface-focus disabled:opacity-50 disabled:pointer-events-none"
              aria-label="Close"
              data-hs-overlay="#penyakitModal"
            >
              <span class="sr-only">Close</span>
              <svg
                class="shrink-0 size-4"
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
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
                    <label for="penyakitname" class="block text-sm mb-2 dark:text-white"
                      >Kode</label
                    >
                    <div class="relative">
                      <input
                        v-model="penyakit.kode"
                        class="py-2.5 sm:py-3 px-4 block w-full border-gray-200 rounded-lg sm:text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-neutral-400 dark:placeholder-neutral-500 dark:focus:ring-neutral-600"
                        aria-describedby="penyakitname-error"
                      />
                    </div>
                    <p v-if="errors.kode" class="text-xs text-red-600 mt-2" id="email-error">
                      {{ errors.kode }}
                    </p>
                  </div>
                  <div>
                    <label for="nama" class="block text-sm mb-2 dark:text-white"
                      >Nama Penyakit</label
                    >
                    <div class="relative">
                      <input
                        v-model="penyakit.nama"
                        class="py-2.5 sm:py-3 px-4 block w-full border-gray-200 rounded-lg sm:text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-neutral-400 dark:placeholder-neutral-500 dark:focus:ring-neutral-600"
                        aria-describedby="nama-error"
                      />
                    </div>
                    <p v-if="errors.nama" class="text-xs text-red-600 mt-2" id="nama-error">
                      {{ errors.nama }}
                    </p>
                  </div>
                  <div>
                    <label for="bobot" class="block text-sm mb-2 dark:text-white">Bobot</label>
                    <div class="relative">
                      <input
                        type="number"
                        v-model="penyakit.bobot"
                        min="0"
                        step="0.1"
                        class="py-2.5 sm:py-3 px-4 block w-full border-gray-200 rounded-lg sm:text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-neutral-400 dark:placeholder-neutral-500 dark:focus:ring-neutral-600"
                        aria-describedby="bobot-error"
                      />
                    </div>
                    <p v-if="errors.bobot" class="text-xs text-red-600 mt-2" id="bobot-error">
                      {{ errors.bobot }}
                    </p>
                  </div>
                  <div>
                    <label for="solusi" class="block text-sm mb-2 dark:text-white">Solusi</label>
                    <div class="relative">
                      <textarea
                        v-model="penyakit.solusi"
                        class="py-2.5 sm:py-3 px-4 block w-full border-gray-200 rounded-lg sm:text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-neutral-400 dark:placeholder-neutral-500 dark:focus:ring-neutral-600"
                        aria-describedby="solusi-error"
                      ></textarea>
                    </div>
                    <p v-if="errors.solusi" class="text-xs text-red-600 mt-2" id="solusi-error">
                      {{ errors.solusi }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
            <div
              class="flex justify-end items-center gap-x-2 py-3 px-4 border-t border-gray-200 dark:border-neutral-800"
            >
              <button
                type="button"
                class="py-2 px-3 inline-flex items-center gap-x-2 text-sm font-medium rounded-lg bg-layer border border-layer-line text-layer-foreground shadow-2xs hover:bg-layer-hover focus:outline-hidden focus:bg-layer-focus disabled:opacity-50 disabled:pointer-events-none"
                data-hs-overlay="#penyakitModal"
              >
                Close
              </button>
              <button
                type="submit"
                class="py-2 px-3 inline-flex items-center gap-x-2 text-sm font-medium rounded-lg bg-primary border border-primary-line text-primary-foreground hover:bg-primary-hover focus:outline-hidden focus:bg-primary-focus disabled:opacity-50 disabled:pointer-events-none"
              >
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
import { useToast } from '@/plugins/toast'
import { useLoading } from '@/plugins/loading'
import PenyakitService from '@/services/PenyakitService'
import { reactive, ref } from 'vue'
import type { Penyakit } from '@/models'
import {
  ListBulletIcon,
  PencilSquareIcon,
  PlusSmallIcon,
  XCircleIcon,
} from '@heroicons/vue/24/outline'
import { HSOverlay } from 'preline'
import z from 'zod'
import HelperService from '@/services/HelperService'
import ConfirmDialog from '@/components/ConfirmDialog.vue'
import PakarLayout from '@/components/layouts/PakarLayout.vue'
import { useRouter } from 'vue-router'
import PageTitle from '@/components/PageTitle.vue'

const loadingService = useLoading()
const toast = useToast()
const router = useRouter()

const addModal = () => {
  penyakit.id = 0
  penyakit.kode = ''
  penyakit.bobot = 0
  penyakit.solusi = ''
  penyakit.nama = ''
  HSOverlay.open('#penyakitModal')
}

// buka

// tutup

const data = reactive({ penyakits: [] as Penyakit[] })

const penyakit = reactive({
  id: 0,
  kode: '',
  nama: '',
  bobot: 0,
  solusi: '',
} as Penyakit)

const penyakitSchema = z.object({
  kode: z.string().nonempty(),
  nama: z.string().nonempty(),
  bobot: z.number().min(0.1),
  solusi: z.string().nullable(),
})

const load = () => {
  const loader = loadingService.spinner('Loading data...', { fullscreen: true })
  PenyakitService.get()
    .then((response) => {
      data.penyakits = response
      loader.remove()
    })
    .catch((error) => {
      console.log(error)
      loader.remove()
    })
}

const errors = ref<Record<string, string>>({})

const detail = (oldPenyakit: Penyakit) => {
  router.push('/pakar/penyakit/' + oldPenyakit.id)
}

const edit = (oldPenyakit: Penyakit) => {
  penyakit.kode = oldPenyakit.kode
  penyakit.nama = oldPenyakit.nama
  penyakit.bobot = oldPenyakit.bobot
  penyakit.solusi = oldPenyakit.solusi
  penyakit.id = oldPenyakit.id
  HSOverlay.open('#penyakitModal')
}

const handleSubmit = async () => {
  const result = penyakitSchema.safeParse(penyakit)
  const loader = loadingService.spinner('Saving data...', { fullscreen: true })
  if (result.success) {
    if (penyakit.id > 0) {
      PenyakitService.put(penyakit.id, penyakit)
        .then(() => {
          const row = data.penyakits.find((item) => item.id === penyakit.id)
          if (row) {
            row.kode = penyakit.kode
            row.nama = penyakit.nama
            row.bobot = penyakit.bobot
            row.solusi = penyakit.solusi
          }
          toast.success('Data saved successfully!')
          HSOverlay.close('#penyakitModal')
          loader.remove()
        })
        .catch((error) => {
          console.log(error)
          loader.remove()
        })
    } else {
      PenyakitService.post(penyakit as Penyakit)
        .then((response) => {
          data.penyakits.push(response)
          toast.success('Data saved successfully!')
          HSOverlay.close('#penyakitModal')
          loader.remove()
        })
        .catch((error) => {
          console.log(error)
          loader.remove()
        })
    }
  } else {
    errors.value = HelperService.mapZodErrors(result.error)
    console.log(errors.value)
    loader.remove()
  }
}

const deleteId = ref<number>(0)

const confirmDelete = (id: number) => {
  deleteId.value = id
  HSOverlay.open('#deleteConfirm')
}

const deletex = async () => {
  try {
    const loader = loadingService.spinner('Delete data...', { fullscreen: true })
    PenyakitService.delete(deleteId.value)
      .then(() => {
        data.penyakits = data.penyakits.filter((item) => item.id !== deleteId.value)
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

load()
</script>

<style scoped></style>
