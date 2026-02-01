<template>
  <!-- ========== HEADER ========== -->
  <header
    class="sticky top-0 inset-x-0 flex flex-wrap md:justify-start md:flex-nowrap z-48 w-full bg-white border-b border-gray-200 text-sm py-2.5 lg:ps-65 dark:bg-neutral-800 dark:border-neutral-700"
  >
    <nav class="px-4 sm:px-6 flex basis-full items-center w-full mx-auto">
      <div class="me-5 lg:me-0 lg:hidden">
        <!-- Logo -->
        <a
          class="flex-none rounded-md text-xl inline-block font-semibold focus:outline-hidden focus:opacity-80"
          href="#"
          aria-label="Preline"
        >
          <img src="../../assets/images/LogoHilab.png" class="w-28 h-auto" alt="Logo" />
        </a>
        <!-- End Logo -->

        <div class="lg:hidden ms-1"></div>
      </div>

      <div class="w-full flex items-center justify-end ms-auto gap-x-1 md:gap-x-3">
        <div class="flex flex-row items-center justify-end gap-1">
          <!-- Dropdown -->
          <div class="hs-dropdown [--placement:bottom-right] relative inline-flex">
            <button
              id="hs-dropdown-account"
              type="button"
              class="cursor-pointer inline-flex justify-center items-center gap-x-2 text-sm font-semibold rounded-full border border-transparent text-gray-800 focus:outline-hidden disabled:opacity-50 disabled:pointer-events-none dark:text-white"
              aria-haspopup="menu"
              aria-expanded="false"
              aria-label="Dropdown"
            >
              {{ getUserName() }}
            </button>

            <div
              class="hs-dropdown-menu transition-[opacity,margin] duration hs-dropdown-open:opacity-100 opacity-0 hidden min-w-60 bg-white shadow-md rounded-lg mt-2 dark:bg-neutral-800 dark:border dark:border-neutral-700 dark:divide-neutral-700 after:h-4 after:absolute after:-bottom-4 after:start-0 after:w-full before:h-4 before:absolute before:-top-4 before:start-0 before:w-full"
              role="menu"
              aria-orientation="vertical"
              aria-labelledby="hs-dropdown-account"
            >
              <div class="py-3 px-5 bg-gray-100 rounded-t-lg dark:bg-neutral-700">
                <p class="text-sm text-gray-500 dark:text-neutral-500">Signed in as</p>
                <p class="text-sm font-medium text-gray-800 dark:text-neutral-200"></p>
              </div>
              <div class="p-1.5 space-y-0.5">
                <a
                  class="flex items-center gap-x-3.5 py-2 px-3 rounded-lg text-sm text-gray-800 hover:bg-gray-100 focus:outline-hidden focus:bg-gray-100 dark:text-neutral-400 dark:hover:bg-neutral-700 dark:hover:text-neutral-300 dark:focus:bg-neutral-700 dark:focus:text-neutral-300"
                  @click="logout"
                >
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
                    <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
                    <circle cx="9" cy="7" r="4" />
                    <path d="M22 21v-2a4 4 0 0 0-3-3.87" />
                    <path d="M16 3.13a4 4 0 0 1 0 7.75" />
                  </svg>
                  Logout
                </a>
              </div>
            </div>
          </div>
          <!-- End Dropdown -->
        </div>
      </div>
    </nav>
  </header>
  <!-- ========== END HEADER ========== -->

  <!-- ========== MAIN CONTENT ========== -->
  <div class="-mt-px">
    <!-- Breadcrumb -->
    <div
      class="sticky top-0 inset-x-0 z-20 bg-white border-y border-gray-200 px-4 sm:px-6 lg:px-8 lg:hidden dark:bg-neutral-800 dark:border-neutral-700"
    >
      <div class="flex items-center py-2">
        <!-- Navigation Toggle -->
        <button
          type="button"
          class="size-8 flex justify-center items-center gap-x-2 border border-gray-200 text-gray-800 hover:text-gray-500 rounded-lg focus:outline-hidden focus:text-gray-500 disabled:opacity-50 disabled:pointer-events-none dark:border-neutral-700 dark:text-neutral-200 dark:hover:text-neutral-500 dark:focus:text-neutral-500"
          aria-haspopup="dialog"
          aria-expanded="false"
          aria-controls="hs-application-sidebar"
          aria-label="Toggle navigation"
          data-hs-overlay="#hs-application-sidebar"
        >
          <span class="sr-only">Toggle Navigation</span>
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
            <rect width="18" height="18" x="3" y="3" rx="2" />
            <path d="M15 3v18" />
            <path d="m8 9 3 3-3 3" />
          </svg>
        </button>
        <!-- End Navigation Toggle -->

        <!-- Breadcrumb -->
        <ol class="ms-3 flex items-center whitespace-nowrap">
          <li
            v-for="path in breadcrumb"
            :key="path"
            class="flex items-center text-sm text-gray-800 dark:text-neutral-400"
          >
            {{ path }}
            <svg
              class="shrink-0 mx-3 overflow-visible size-2.5 text-gray-400 dark:text-neutral-500"
              width="16"
              height="16"
              viewBox="0 0 16 16"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M5 1L10.6869 7.16086C10.8637 7.35239 10.8637 7.64761 10.6869 7.83914L5 14"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
              />
            </svg>
          </li>
        </ol>
        <!-- End Breadcrumb -->
      </div>
    </div>
    <!-- End Breadcrumb -->
  </div>

  <!-- Sidebar -->
  <div
    id="hs-application-sidebar"
    class="hs-overlay [--auto-close:lg] hs-overlay-open:translate-x-0 -translate-x-full transition-all duration-300 transform w-65 h-full hidden fixed inset-y-0 start-0 z-60 bg-white border-e border-gray-200 lg:block lg:translate-x-0 lg:end-auto lg:bottom-0 dark:bg-neutral-800 dark:border-neutral-700"
    role="dialog"
    tabindex="-1"
    aria-label="Sidebar"
  >
    <div class="relative flex flex-col h-full max-h-full">
      <div class="px-6 pt-4 flex items-center">
        <!-- Logo -->
        <a
          class="flex-none rounded-xl text-xl inline-block font-semibold focus:outline-hidden focus:opacity-80"
          href="#"
          aria-label="Preline"
        >
        </a>
        <!-- End Logo -->

        <div class="hidden lg:block ms-2"></div>
      </div>

      <!-- Content -->
      <div
        class="p-2 h-full overflow-y-auto [&::-webkit-scrollbar]:w-2 [&::-webkit-scrollbar-thumb]:rounded-full [&::-webkit-scrollbar-track]:bg-gray-100 [&::-webkit-scrollbar-thumb]:bg-gray-300 dark:[&::-webkit-scrollbar-track]:bg-neutral-700 dark:[&::-webkit-scrollbar-thumb]:bg-neutral-500"
      >
        <img src="../../assets/images/LogoHilab.png" class="h-auto" alt="Logo" />
        <nav
          class="hs-accordion-group p-3 w-full flex flex-col flex-wrap"
          data-hs-accordion-always-open
        >
          <ul>
            <li v-for="menu in menus" :key="menu.name" class="mt-1">
              <a
                v-if="!menu.children"
                :class="
                  isActive(menu.routeName) ? 'bg-green-600 text-white' : 'bg-gray-100 text-gray-800'
                "
                class="cursor-pointer flex items-center gap-x-3.5 py-2 px-2.5 bg-gray-100 text-sm text-gray-800 rounded-lg hover:bg-gray-300 focus:outline-hidden focus:bg-gray-100 dark:bg-neutral-700 dark:hover:bg-neutral-700 dark:focus:bg-neutral-700 dark:text-white"
                @click="selectMenu(menu.routeName)"
              >
                <component
                  v-if="menu.Icon"
                  :is="menu.Icon"
                  class="h-5 w-5 text-gray-600"
                  :class="isActive(menu.routeName) ? 'text-white' : 'text-gray-600'"
                />
                {{ menu.name }}
              </a>
              <div v-else class="hs-accordion" :id="menu.name + '-accordion'">
                <button
                  type="button"
                  class="hs-accordion-toggle w-full text-start flex items-center gap-x-3.5 py-2 px-2.5 text-sm text-gray-800 rounded-lg hover:bg-gray-100 focus:outline-hidden focus:bg-gray-100 dark:bg-neutral-800 dark:hover:bg-neutral-700 dark:focus:bg-neutral-700 dark:text-neutral-200"
                  aria-expanded="true"
                  :aria-controls="menu.name + '-accordion-child'"
                >
                  <component v-if="menu.Icon" :is="menu.Icon" class="h-5 w-5 text-gray-600" />
                  {{ menu.name }}

                  <svg
                    class="hs-accordion-active:block ms-auto hidden size-4"
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
                    <path d="m18 15-6-6-6 6" />
                  </svg>

                  <svg
                    class="hs-accordion-active:hidden ms-auto block size-4"
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
                    <path d="m6 9 6 6 6-6" />
                  </svg>
                </button>
                <div
                  :id="menu.name + '-accordion-child'"
                  class="hs-accordion-content w-full overflow-hidden transition-[height] duration-300 hidden"
                  role="region"
                  :aria-labelledby="menu.name + '-accordion'"
                >
                  <ul class="hs-accordion-group ps-8 pt-1 space-y-1" data-hs-accordion-always-open>
                    <li v-for="child in menu.children" :key="child.name">
                      <a
                        class="flex items-center gap-x-3.5 py-2 px-2.5 text-sm text-gray-800 rounded-lg hover:bg-gray-100 focus:outline-hidden focus:bg-gray-100 dark:bg-neutral-800 dark:hover:bg-neutral-700 dark:focus:bg-neutral-700 dark:text-neutral-200"
                        @click="selectMenu(child.routeName, child.name)"
                      >
                        <component
                          v-if="child.Icon"
                          :is="menu.Icon"
                          class="h-5 w-5 text-gray-600"
                        />
                        {{ child.name }}
                      </a>
                    </li>
                  </ul>
                </div>
              </div>
            </li>
          </ul>
        </nav>
      </div>
      <!-- End Content -->
    </div>
  </div>
  <!-- End Sidebar -->

  <!-- Content -->
  <div class="w-full lg:ps-64">
    <div class="p-4 sm:p-6 space-y-4 sm:space-y-6 md:px-8 lg:px-10 lg:py-6">
      <slot></slot>
    </div>
  </div>
  <!-- End Content -->
  <!-- ========== END MAIN CONTENT ========== -->
</template>
<script setup lang="ts">
import AuthService from '@/services/AuthService'
import { useAuthStore } from '@/stores/auth'
import { type FunctionalComponent, type HTMLAttributes, type VNodeProps } from 'vue'
import { useRoute, useRouter } from 'vue-router'
const router = useRouter()
const route = useRoute()
const breadcrumb = route.fullPath.split('/')
const userStore = useAuthStore()
const user = userStore.getUser()

const isActive = (name: string) => route.name === name

interface Menu {
  name: string
  routeName: string
  children: Menu[] | null
  Icon: FunctionalComponent<HTMLAttributes & VNodeProps>
}

defineProps<{ menus: Menu[] }>()

const getUserName = () => {
  return user?.username || user?.email || 'Guest'
}

const selectMenu = (menuName: string) => {
  router.push({ name: menuName })
}

const logout = async () => {
  await AuthService.logout()
  router.push({ name: 'login' })

  console.log(router.currentRoute)
}
</script>

<style scoped></style>
