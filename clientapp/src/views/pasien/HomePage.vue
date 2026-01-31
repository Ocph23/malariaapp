<script setup lang="ts">
import PageTitle from '@/components/PageTitle.vue';
import TheWelcome from '../../components/TheWelcome.vue'
import PakarLayout from '@/components/layouts/PakarLayout.vue';
import PasienLayout from '@/components/layouts/PasienLayout.vue';

import('preline').then(() => {
  console.log("preline ok");
});

</script>

<template>
  <PasienLayout>
    <PageTitle title="Home"></PageTitle>

    <div class="w-full text-center px-6">

      <!-- Title -->
      <h1 class="text-4xl md:text-5xl font-extrabold text-gray-800 leading-tight">
        Deteksi Dini Penyakit Malaria
        <span class="block text-emerald-600 mt-2">
          Secara Cepat dan Akurat
        </span>
      </h1>

      <!-- Description -->
      <p class="mt-6 text-lg text-gray-600 leading-relaxed">
        Aplikasi ini membantu mendeteksi kemungkinan penyakit malaria
        berdasarkan gejala yang dialami pasien menggunakan
        <span class="font-semibold text-gray-700">metode sistem pakar</span>.
      </p>

      <!-- CTA Buttons -->
      <div class="mt-10 flex flex-col sm:flex-row gap-4 justify-center">
        <a href="/pasien/diagnosa"
          class="inline-flex items-center justify-center gap-2 px-8 py-3 text-white bg-emerald-600 hover:bg-emerald-700 rounded-xl text-lg font-semibold shadow-lg transition">
          🔍 Mulai Deteksi
        </a>

        <a href="https://malaria.kemkes.go.id/" target="_blank"
          class="inline-flex items-center justify-center gap-2 px-8 py-3 text-emerald-700 border-2 border-emerald-600 hover:bg-emerald-50 rounded-xl text-lg font-semibold transition">
          📘 Pelajari Tentang Malaria
        </a>
      </div>

      <!-- Footer Note -->
      <p class="mt-12 text-sm text-gray-500">
        *Hasil deteksi bersifat pendukung dan tidak menggantikan diagnosis dokter
      </p>

    </div>
  </PasienLayout>
</template>


<script setup lang="ts">





</script>
