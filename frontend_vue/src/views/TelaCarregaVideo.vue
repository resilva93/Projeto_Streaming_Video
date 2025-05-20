<template>
  <div id="app" class="flex flex-col min-h-screen bg-[#F4FAF9] text-[#004D40]">
    <!-- Menu Superior -->
    <div class="w-full bg-[#CFF1EC] shadow-md">
      <MenuSuperior />
    </div>

    <!-- Conteúdo principal -->
    <main class="flex flex-col items-center flex-grow py-10">
      <h1 class="title text-center">📤 Envie seu vídeo para a galeria</h1>

      <!-- Formulário de Upload -->
      <form
        @submit.prevent="submitForm"
        class="w-full max-w-xl mx-auto bg-white rounded-2xl shadow-md p-8 mb-20 flex flex-col items-center space-y-6"
      >
        <input v-model="titulo" type="text" placeholder="Título" class="input-sm" required />
        <input v-model="descricao" type="text" placeholder="Descrição" class="input-sm" required />
        <input v-model="categoria" type="text" placeholder="Categoria" class="input-sm" />
        <input
          type="file"
          @change="handleFileUpload"
          accept="video/*"
          class="input-sm cursor-pointer"
          required
        />

        <!-- Botão centralizado -->
        <div class="w-full flex justify-center">
          <button type="submit" :disabled="isUploading" class="btn w-1/2">
            {{ isUploading ? 'Enviando...' : 'Enviar Vídeo' }}
          </button>
        </div>

        <!-- Mensagem e progresso -->
        <div v-if="mensagem" class="text-sm text-center font-medium text-[#2D0F32]">{{ mensagem }}</div>
        <div v-if="isUploading" class="w-full bg-gray-200 rounded-full h-2.5">
          <div
            class="bg-[#2D0F32] h-2.5 rounded-full"
            :style="{ width: progress + '%' }"
          ></div>
        </div>
      </form>

      <!-- Lista de Vídeos -->
      <div class="grid-container w-full mt-6">
        <div class="video-grid">
          <div
            class="video-card"
            v-for="video in videosPaginados"
            :key="video.id"
            @click="selecionarVideoDireto(video)"
          >
            <Clapperboard class="icon-xl" />
            <h3>{{ video.titulo }}</h3>
            <p>{{ video.artista }}</p>
          </div>
        </div>

        <!-- Paginação -->
        <div class="pagination-controls mt-6 flex gap-4">
          <button class="btn" :disabled="paginaAtual === 1" @click="paginaAnterior">Anterior</button>
          <span>Página {{ paginaAtual }} de {{ totalPaginas }}</span>
          <button class="btn" :disabled="paginaAtual === totalPaginas" @click="proximaPagina">Próxima</button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Clapperboard } from 'lucide-vue-next'
import axios from 'axios'
import MenuSuperior from '@/components/MenuSuperior.vue'

const API_URL = 'http://localhost:8080'

const titulo = ref('')
const descricao = ref('')
const categoria = ref('')
const file = ref(null)
const mensagem = ref('')
const isUploading = ref(false)
const progress = ref(0)

const videos = ref([])
const paginaAtual = ref(1)
const itensPorPagina = 5
const loading = ref(false)

const totalPaginas = computed(() => {
  return Math.ceil(videos.value.length / itensPorPagina)
})

const videosPaginados = computed(() => {
  const inicio = (paginaAtual.value - 1) * itensPorPagina
  return videos.value.slice(inicio, inicio + itensPorPagina)
})

const handleFileUpload = (e) => {
  file.value = e.target.files[0]
}

const submitForm = async () => {
  if (!file.value) {
    mensagem.value = 'Por favor, selecione um arquivo.'
    return
  }

  const formData = new FormData()
  formData.append('titulo', titulo.value)
  formData.append('descricao', descricao.value)
  formData.append('categoria', categoria.value)
  formData.append('file', file.value)

  isUploading.value = true
  mensagem.value = ''
  progress.value = 0

  try {
    await axios.post(`${API_URL}/api/videos/upload`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (e) => {
        if (e.lengthComputable) {
          progress.value = Math.round((e.loaded * 100) / e.total)
        }
      }
    })

    mensagem.value = 'Vídeo enviado com sucesso!'
    titulo.value = ''
    descricao.value = ''
    categoria.value = ''
    file.value = null
    await fetchVideos()
    paginaAtual.value = 1
  } catch (error) {
    console.error('Erro ao enviar vídeo:', error)
    mensagem.value = 'Erro no envio do vídeo.'
  } finally {
    isUploading.value = false
  }
}

const fetchVideos = async () => {
  loading.value = true
  try {
    const response = await axios.get(`${API_URL}/api/videos/`)
    videos.value = [...response.data].sort((a, b) => a.titulo.localeCompare(b.titulo))
  } catch (error) {
    console.error('Erro ao carregar vídeos:', error)
  } finally {
    loading.value = false
  }
}

const selecionarVideoDireto = (video) => {
  alert(`Vídeo selecionado: ${video.titulo}`)
}

const proximaPagina = () => {
  if (paginaAtual.value < totalPaginas.value) paginaAtual.value++
}
const paginaAnterior = () => {
  if (paginaAtual.value > 1) paginaAtual.value--
}

onMounted(fetchVideos)
</script>

<style scoped>
.title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 2rem;
  color: #2D0F32;
}

.input-sm {
  width: 50%;
  padding: 0.75rem;
  border: 2px solid #570a67;
  border-radius: 8px;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.3s, box-shadow 0.3s;
  margin-bottom: 1rem;
}
.input-sm:focus {
  border-color: #2D0F32;
  box-shadow: 0 0 0 2px rgba(45, 15, 50, 0.2);
}

.btn {
  background-color: #2D0F32;
  color: white;
  padding: 8px 16px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 500;
  transition: 0.3s;
}
.btn:hover {
  background-color: #570a67;
}
.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.grid-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.video-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 30px;
  max-width: 1100px;
  margin-bottom: 40px;
}
.video-card {
  background-color: #570a67;
  border-radius: 16px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  color: #FFFFFF;
  transition: background-color 0.3s;
}
.video-card:hover {
  background-color: #2D0F32;
}

.pagination-controls {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  font-weight: bold;
  color: #2D0F32;
}
.loading-spinner {
  color: #2D0F32;
  font-weight: bold;
}
</style>
