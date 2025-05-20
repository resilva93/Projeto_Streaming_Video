import { createApp } from 'vue'
import App from './app.vue'
import './assets/tailwind.css'  
import router from './router'
import axios from 'axios'

// Configuração global do Axios
axios.defaults.baseURL = 'http://localhost:8080/api';  

const app = createApp(App);

// Registra o Vue Router
app.use(router);

// Monta a aplicação no DOM
app.mount('#app');  