import './assets/main.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { toastPlugin } from './plugins/toast'
import { loadingPlugin } from './plugins/loading'
import 'preline'

const app = createApp(App)
app.use(router)
app.use(toastPlugin)
app.use(loadingPlugin)
app.use(createPinia())

app.mount('#app')

// document.addEventListener('DOMContentLoaded', () => {
//   import('preline').then(() => {
//     console.log('Preline UI initialized after DOM loaded')
//   })
// })
