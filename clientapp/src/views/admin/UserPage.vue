<template>
  <AdminLayout>
    <div class="flex flex-col">
      <div class="-m-1.5 overflow-x-auto">
        <div class="p-1.5 min-w-full inline-block align-middle">
          <div class="flex justify-end pb-5">

            <PlusSmallIcon @click="addModal" class="size-8 bg-teal-500 rounded-full p-1 text-white"></PlusSmallIcon>
          </div>
          <div class="overflow-hidden">
            <table class="min-w-full divide-y divide-gray-200 dark:divide-neutral-700">
              <thead>
                <tr>
                  <th scope="col"
                    class="px-6 py-3 text-start text-xs font-medium text-gray-500 uppercase dark:text-neutral-500">User
                    Name
                  </th>
                  <th scope="col"
                    class="px-6 py-3 text-start text-xs font-medium text-gray-500 uppercase dark:text-neutral-500">Email
                  </th>
                  <th scope="col"
                    class="px-6 py-3 text-start text-xs font-medium text-gray-500 uppercase dark:text-neutral-500">Role
                  </th>
                  <th scope="col"
                    class="px-6 py-3 text-start text-xs font-medium text-gray-500 uppercase dark:text-neutral-500">
                    Status</th>
                  <th scope="col"
                    class="px-6 py-3 text-end text-xs font-medium text-gray-500 uppercase dark:text-neutral-500">Action
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in data.users" :key="item.id"
                  class="odd:bg-white even:bg-gray-100 dark:odd:bg-neutral-900 dark:even:bg-neutral-800">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-800 dark:text-neutral-200">
                    {{ item.username }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200">
                    {{ item.email }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200">
                    {{ item.role }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200">
                    {{ item.is_active }}</td>

                  <td class="px-6 py-4 whitespace-nowrap text-end text-sm font-medium">
                    <!-- <button type="button" @click="edit(item)">
                      <PencilSquareIcon class="size-5 hover:size-6 cursor-pointer text-amber-600"></PencilSquareIcon>
                    </button> -->
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

    <div id="userModal"
      class="hs-overlay hidden size-full fixed top-0 start-0 z-80 overflow-x-hidden overflow-y-auto pointer-events-none"
      role="dialog" tabindex="-1" aria-labelledby="userModal-label">
      <div
        class="hs-overlay-open:mt-7 hs-overlay-open:opacity-100 hs-overlay-open:duration-500 mt-0 opacity-0 ease-out transition-all sm:max-w-lg sm:w-full m-3 sm:mx-auto min-h-[calc(100%-56px)] flex items-center">
        <div
          class="bg-gray-100 w-full flex flex-col bg-overlay border border-overlay-line shadow-2xs rounded-xl pointer-events-auto">
          <div class="flex justify-between items-center py-3 px-4 border-b border-gray-300">
            <h3 id="userModal-label" class="font-semibold text-foreground">
              Tambah User
            </h3>
            <button type="button"
              class="size-8 inline-flex justify-center items-center gap-x-2 rounded-full bg-surface border border-surface-line text-surface-foreground hover:bg-surface-hover focus:outline-hidden focus:bg-surface-focus disabled:opacity-50 disabled:pointer-events-none"
              aria-label="Close" data-hs-overlay="#userModal">
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
                    <label for="username" class="block text-sm mb-2 dark:text-white">UserName</label>
                    <div class="relative">
                      <input v-model="user.username"
                        class="py-2.5 sm:py-3 px-4 block w-full border-gray-200 rounded-lg sm:text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-neutral-400 dark:placeholder-neutral-500 dark:focus:ring-neutral-600"
                        aria-describedby="username-error">
                    </div>
                    <p v-if="errors.username" class="text-xs text-red-600 mt-2" id="email-error">
                      {{ errors.username }}
                    </p>
                  </div>
                  <div>
                    <label for="email" class="block text-sm mb-2 dark:text-white">Email</label>
                    <div class="relative">
                      <input v-model="user.email"
                        class="py-2.5 sm:py-3 px-4 block w-full border-gray-200 rounded-lg sm:text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-neutral-400 dark:placeholder-neutral-500 dark:focus:ring-neutral-600"
                        required aria-describedby="email-error">
                    </div>
                    <p v-if="errors.password" class="text-xs text-red-600 mt-2" id="email-error">
                      {{ errors.email }}
                    </p>
                  </div>
                  <div>
                    <label for="email" class="block text-sm mb-2 dark:text-white">Role</label>
                    <div class="relative">
                      <select v-model="user.role"
                        class="py-3 px-4 pe-9 block w-full bg-layer border-layer-line rounded-lg text-sm text-foreground focus:border-primary-focus focus:ring-primary-focus disabled:opacity-50 disabled:pointer-events-none">
                        <option selected>Open this select menu</option>
                        <option value="admin">Admin</option>
                        <option value="pakar">Pakar</option>
                      </select>
                    </div>
                    <p v-if="errors.role" class="text-xs text-red-600 mt-2" id="email-error">
                      {{ errors.role }}
                    </p>
                  </div>

                </div>

              </div>
            </div>
            <div
              class="flex justify-end items-center gap-x-2 py-3 px-4 border-t border-gray-200 dark:border-neutral-800">
              <button type="button"
                class="py-2 px-3 inline-flex items-center gap-x-2 text-sm font-medium rounded-lg bg-layer border border-layer-line text-layer-foreground shadow-2xs hover:bg-layer-hover focus:outline-hidden focus:bg-layer-focus disabled:opacity-50 disabled:pointer-events-none"
                data-hs-overlay="#userModal">
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

  </AdminLayout>

</template>

<script setup lang="ts">
import AdminLayout from '@/components/layouts/AdminLayout.vue';
import { useToast } from '@/plugins/toast';
import { useLoading } from '@/plugins/loading';
import UserService from '@/services/UserService';
import { reactive, ref } from 'vue';
import type { User } from '@/models';
import { PlusSmallIcon, XCircleIcon } from '@heroicons/vue/24/outline';
const loadingService = useLoading();
const toast = useToast();


import { HSOverlay } from "preline"
import z from 'zod';
import HelperService from '@/services/HelperService';
import ConfirmDialog from '@/components/ConfirmDialog.vue';


const addModal = () => {
  HSOverlay.open("#userModal")
}




// buka

// tutup

const data = reactive({ users: [] as User[] })


const user = reactive({
  username: '',
  email: '',
  role: '',
  is_active: true
} as User)


const userSchema = z.object({
  username: z.string().nonempty(),
  email: z.email(),
  role: z.string().nonempty(),
  is_active: z.boolean()
});


const load = () => {
  const loader = loadingService.spinner('Loading data...', { fullscreen: true });
  UserService.get().then(response => {
    data.users = response;
    loader.remove();
  }).catch(error => {
    console.log(error);
    loader.remove();
  });
}

const errors = ref<Record<string, string>>({})


const handleSubmit = async () => {
  const result = userSchema.safeParse(user);
  console.log(result);
  if (result.success) {
    UserService.post(user as User).then(response => {
      data.users.push(response);
      toast.success('Data saved successfully!');
      HSOverlay.close("#userModal")
      console.log(response);
    }).catch(error => {
      console.log(error);
    });

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
    UserService.delete(deleteId.value).then(() => {
      data.users = data.users.filter(item => item.id !== deleteId.value);
      loader.remove();
      toast.success('Data deleted successfully!');
    }).catch(error => {
      console.log(error);
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
