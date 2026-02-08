<template>
  <div class="p-4 md:p-7 grid grid-cols-1 md:grid-cols-2 items-center gap-5 w-full justify-center">
    <div class="md:h-screen flex flex-col justify-center items-center gap-2 mb-5">
      <img src="../../assets/images/LogoHilab.png" class="h-auto w-[50%]" alt="Logo">
      <div class="w-full text-center px-6 ">

        <!-- Title -->
        <h1 class="text-xl md:text-4xl mt-5 font-extrabold text-gray-800 leading-tight">
          Deteksi Dini Penyakit Malaria
          <span class="block text-emerald-600 mt-2">
            Secara Cepat dan Akurat
          </span>
        </h1>

        <!-- Description -->
        <p class="mt-6 md:text-lg text-gray-600 leading-relaxed">
          Aplikasi ini membantu mendeteksi kemungkinan penyakit malaria
          berdasarkan gejala yang dialami pasien menggunakan
          <span class="font-semibold text-gray-700">metode sistem pakar</span>.
        </p>

        <!-- CTA Buttons -->
        <div class="mt-10 flex flex-col sm:flex-row gap-4 justify-center">

          <a href="https://malaria.kemkes.go.id/" target="_blank"
            class="inline-flex items-center justify-center gap-2 px-8 py-3 text-emerald-700 border-2 border-emerald-600 hover:bg-emerald-50 rounded-xl text-lg font-semibold transition">
            📘 Pelajari Tentang Malaria
          </a>
        </div>
      </div>

    </div>
    <div
      class="md:h-auto w-full  lg:w-[70%] bg-white border border-gray-200 rounded-xl shadow-2xs dark:bg-neutral-900 dark:border-neutral-700">
      <slot></slot>
    </div>

  </div>
</template>

<script setup lang="ts">

</script>

<style scoped></style>
