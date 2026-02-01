<template>
  <AuthLayout>
    <div class="p-4 sm:p-7">
      <div class="mt-5">
        <!-- Form -->
        <form @submit.prevent="handleSubmit">
          <div class="flex flex-col gap-4">
            <!-- Form Group -->
            <h1 class="block text-2xl font-bold text-gray-800 dark:text-white">Sign in</h1>
            <div>
              <Input
                name="email"
                type="email"
                label="Username / Email"
                v-model="user.username"
                :error="errors.username"
              ></Input>
            </div>
            <!-- End Form Group -->

            <!-- Form Group -->
            <div>
              <Input
                name="password"
                type="password"
                label="Password"
                v-model="user.password"
                :error="errors.password"
              ></Input>
              <div class="flex flex-wrap justify-between items-center gap-2 mt-2">
                <a
                  class="inline-flex items-center gap-x-1 text-sm text-blue-600 decoration-2 hover:underline focus:outline-hidden focus:underline font-medium dark:text-blue-500"
                  href="../examples/html/recover-account.html"
                  >Forgot password?</a
                >
              </div>
            </div>
            <!-- End Form Group -->

            <!-- Checkbox -->
            <div class="flex items-center">
              <div class="flex">
                <input
                  id="remember-me"
                  name="remember-me"
                  type="checkbox"
                  class="shrink-0 mt-0.5 border-gray-200 rounded-sm text-blue-600 focus:ring-blue-500 dark:bg-neutral-800 dark:border-neutral-700 dark:checked:bg-blue-500 dark:checked:border-blue-500 dark:focus:ring-offset-gray-800"
                />
              </div>
              <div class="ms-3">
                <label for="remember-me" class="text-sm dark:text-white">Remember me</label>
              </div>
            </div>
            <!-- End Checkbox -->

            <button
              type="submit"
              class="w-full py-3 px-4 inline-flex justify-center items-center gap-x-2 text-sm font-medium rounded-lg border border-transparent bg-blue-600 text-white hover:bg-blue-700 focus:outline-hidden focus:bg-blue-700 disabled:opacity-50 disabled:pointer-events-none"
            >
              Sign in
            </button>
          </div>
          <p class="mt-2 text-sm text-gray-600 dark:text-neutral-400">
            Don't have an account yet?
            <a
              class="text-blue-600 decoration-2 hover:underline focus:outline-hidden focus:underline font-medium dark:text-blue-500"
              href="/auth/register"
            >
              Sign up here
            </a>
          </p>
        </form>
        <!-- End Form -->
      </div>
    </div>
  </AuthLayout>
</template>

<script setup lang="ts">
import Input from '@/components/Input.vue'
import AuthLayout from '@/components/layouts/AuthLayout.vue'
import { useLoading } from '@/plugins/loading'
import AuthService from '@/services/AuthService'
import HelperService from '@/services/HelperService'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import z from 'zod'

const router = useRouter()

const errors = ref<Record<string, string>>({})

const loginSchema = z.object({
  username: z.email({ message: 'Invalid email' }),
  password: z.string().min(1),
})

const loadingService = useLoading()

const user = {
  username: '',
  password: '',
}

const handleSubmit = async () => {
  const loader = loadingService.spinner('Login...', { fullscreen: true })
  const validateResult = loginSchema.safeParse(user)
  if (validateResult.success) {
    const result = await AuthService.login(user)
    if (result.user.role === 'admin') {
      router.push({ name: 'home' })
    }

    if (result.user.role === 'pakar') {
      router.push({ name: 'pakar.home' })
    }

    if (result.user.role === 'pasien') {
      router.push({ name: 'pasien.home' })
    }

    loader.remove()
  } else {
    errors.value = HelperService.mapZodErrors(validateResult.error)
    loader.remove()
  }
}
</script>

<style scoped></style>
