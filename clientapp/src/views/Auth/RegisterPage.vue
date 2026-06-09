<template>
  <AuthLayout>
    <div class="p-4 sm:p-7 gap-5 w-full">
      <div class="mt-5">
        <!-- Form -->
        <form @submit.prevent="handleSubmit">
          <div class="flex flex-col gap-4">
            <!-- Form Group -->
            <h1 class="block text-2xl font-bold text-gray-800 dark:text-white">Register</h1>
            <div class="w-full">
              <Input name="nama" label="Nama" type="text" v-model="form.nama" :error="errors.nama" required></Input>
            </div>
            <div class="columns-2 flex justify-start ">
              <Input name="tanggal_lahir" label="Tanggal Lahir" type="date" v-model="form.tanggal_lahir"
                required></Input>
              <ComboBox name="jenis_kelamin" label="Jenis Kelamin" v-model="form.jenis_kelamin"
                :options="[{ label: 'Laki-laki', value: 'laki-laki' }, { label: 'Perempuan', value: 'perempuan' }]"
                :error="errors.jenis_kelamin">
              </ComboBox>
            </div>
            <div>
              <Input name="nomor_telepon" label="Telepon" type="text" v-model="form.nomor_telepon"
                :error="errors.nomor_telepon"></Input>
            </div>

            <div>
              <Input name="alamat" label="alamat" type="text" v-model="form.alamat" :error="errors.alamat"></Input>
            </div>

            <div>
              <Input name="email" label="Email" type="email" v-model="form.email" required
                :error="errors.email"></Input>
            </div>
            <div class="columns-2 flex justify-start">
              <Input name="password" label="Password" type="password" v-model="form.password" required
                :error="errors.password"></Input>
              <Input name="confirm" label="Confirm Password" type="password" v-model="form.confirmPassword" required
                :error="errors.confirmPassword"></Input>
            </div>


            <!-- Checkbox -->
            <div class="flex items-center">
              <div class="flex">
                <input id="remember-me" name="remember-me" type="checkbox" @change="terms = !terms"
                  class="shrink-0 mt-0.5 border-gray-200 rounded-sm text-blue-600 focus:ring-blue-500 dark:bg-neutral-800 dark:border-neutral-700 dark:checked:bg-blue-500 dark:checked:border-blue-500 dark:focus:ring-offset-gray-800">
              </div>
              <div class="ms-3">
                <label for="remember-me" class="text-sm dark:text-white">I accept the <a
                    class="text-blue-600 decoration-2 hover:underline focus:outline-hidden focus:underline font-medium dark:text-blue-500"
                    href="#">Terms and Conditions</a></label>
              </div>
            </div>
            <!-- End Checkbox -->
            <button type="submit" :disabled="terms"
              class="w-[calc(100%-1rem)] py-3 px-4 inline-flex justify-center items-center gap-x-2 text-sm font-medium rounded-lg border border-transparent bg-blue-600 text-white hover:bg-blue-700 focus:outline-hidden focus:bg-blue-700 disabled:opacity-50 disabled:pointer-events-none">Sign
              up</button>
            <p class="mt-2 text-sm text-gray-600 dark:text-neutral-400">
              Have an account ?
              <a class="text-blue-600 decoration-2 hover:underline focus:outline-hidden focus:underline font-medium dark:text-blue-500"
                href="/auth/login">
                Login up here
              </a>
            </p>
          </div>

        </form>
        <!-- End Form -->
      </div>
    </div>
  </AuthLayout>
</template>

<script setup lang="ts">
import ComboBox from '@/components/ComboBox.vue';
import Input from '@/components/Input.vue';
import AuthLayout from '@/components/layouts/AuthLayout.vue';
import type { RegisterRequest } from '@/models/request';
import { useLoading } from '@/plugins/loading';
import AuthService from '@/services/AuthService';
import HelperService from '@/services/HelperService';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import z from 'zod';

const router = useRouter();

const loadingService = useLoading();


const registerSchema = z
  .object({
    nama: z.string().min(1, 'Nama wajib diisi'),
    tanggal_lahir: z.string().min(1, 'Tanggal lahir wajib diisi'),
    jenis_kelamin: z.string().min(1, 'Jenis kelamin wajib diisi'),
    nomor_telepon: z.string().min(1, 'Nomor telepon wajib diisi'),
    alamat: z.string().min(1, 'Alamat wajib diisi'),
    email: z.string().email('Email tidak valid'),
    password: z.string().min(6, 'Password minimal 6 karakter'),
    confirmPassword: z.string().min(6, 'Konfirmasi password wajib'),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: 'Password dan konfirmasi password tidak sama',
    path: ['confirmPassword'], // ❗ error diarahkan ke field ini
  })



const form = {
  nama: '',
  username: '',
  tanggal_lahir: new Date().toISOString().split('T')[0],
  jenis_kelamin: '',
  nomor_telepon: '',
  alamat: '',
  email: '',
  password: '',
  confirmPassword: '',
};


//remove confirmPassowrd



const terms = ref(true);


const errors = ref<Record<string, string>>({})


const handleSubmit = async () => {
  console.log("submit");


  const loader = loadingService.spinner('Login...', { fullscreen: true });
  const validateResult = registerSchema.safeParse(form);
  const register = {
    ...form,
    confirmPassword: ''
  } as RegisterRequest;

  if (validateResult.success) {
    register.username = register.nama;
    AuthService.register(register).then(() => {
      router.push({ name: 'pasien.home' });
      loader.remove();
    }).catch(() => {
      loader.remove();
    });
  } else {
    errors.value = HelperService.mapZodErrors(validateResult.error);
    loader.remove();
  }


};
</script>

<style scoped></style>
