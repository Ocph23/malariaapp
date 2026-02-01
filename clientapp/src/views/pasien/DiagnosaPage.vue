<template>
  <PasienLayout>
    <PageTitle title="Diagnosa Penyakit"></PageTitle>
    <div>
      <div class="text-xl">Diagnosa Penyakit</div>
      <div class="text-md">Jawab Semua Pertanyaan <span class="text-red-500">*</span></div>
    </div>
    <div class="w-full md:w-[50%]">
      <form @submit.prevent="submit">
        <JawabanItem
          v-for="gejala in data.gejalas"
          :key="gejala.kode"
          :kode="gejala.kode"
          :pertanyaan="gejala.pertanyaan"
          :error="gejala.error"
          v-model="gejala.jawaban"
        />

        <div class="flex justify-end gap-2 mx-4 mt-4">
          <button
            type="submit"
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            Diagnosa
          </button>
        </div>
      </form>
    </div>
  </PasienLayout>
</template>

<script setup lang="ts">
import PasienLayout from '@/components/layouts/PasienLayout.vue'
import PageTitle from '@/components/PageTitle.vue'
import JawabanItem from '@/components/JawabanItem.vue'
import { reactive } from 'vue'
import GejalaService from '@/services/GejalaService'
import z from 'zod'
import HelperService from '@/services/HelperService'
import { useLoading } from '@/plugins/loading'

const loadingService = useLoading()

interface DiagnosaItem {
  kode: string
  pertanyaan: string
  jawaban: string
  error?: string
}

const diagnosaItemSchema = z.object({
  jawaban: z.string().min(1, 'Jawaban tidak boleh kosong'),
})

const data = reactive({ gejalas: [] as DiagnosaItem[] })
const load = async () => {
  try {
    GejalaService.get().then((response) => {
      data.gejalas = response
        .sort((a, b) => a.kode.localeCompare(b.kode))
        .map(
          (gejala) =>
            ({
              kode: gejala.kode,
              pertanyaan: `Apakah Anda mengalami ${gejala.nama}?`,
              jawaban: '',
              error: '',
            }) as DiagnosaItem,
        )
    })
  } catch (error) {
    console.error('Error loading options:', error)
    return []
  }
}

const submit = async () => {
  const loader = loadingService.spinner('Diagnosa ...', { fullscreen: true })
  try {
    let isValid = true
    data.gejalas.forEach((item) => {
      item.error = ''
      const result = diagnosaItemSchema.safeParse(item)
      if (!result.success) {
        const err = HelperService.mapZodErrors(result.error)
        item.error = err.jawaban
        isValid = false
      }
    })
    if (isValid) {
      setTimeout(() => {
        loader.remove()
      }, 5000)
    } else loader.remove()
  } catch (error) {
    console.error('Validation Error:', error)
    loader.remove()
  }
}

load()
</script>
