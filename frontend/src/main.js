import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Toast from 'vue-toastification'
import { library, dom } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { fab } from '@fortawesome/free-brands-svg-icons'
import { far } from '@fortawesome/free-regular-svg-icons'
import { createPinia } from 'pinia'

library.add(fas, far, fab)
dom.watch()

const app = createApp(App)
const pinia = createPinia()

app.use(router)
app.use(Toast, {}).component('font-awesome-icon', FontAwesomeIcon)
app.use(pinia)
app.mount('#app')
