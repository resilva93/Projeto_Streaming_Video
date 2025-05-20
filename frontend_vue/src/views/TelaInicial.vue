<template>
  <div id="app" class="flex flex-col min-h-screen bg-[#F4FAF9] text-[#004D40]">
    <!-- Menu Superior-->
    <div class="w-full bg-[#CFF1EC] shadow-md">
      <MenuSuperior />
    </div>

    <!-- Conteúdo principal -->
    <main class="flex flex-col items-center flex-grow py-10 w-full px-4">
      <h1 class="title">🎬 Bem-vindo(a) à sua galeria de vídeos!</h1>

      <div v-if="loading" class="loading-spinner">Carregando vídeos...</div>

      <div v-else class="grid-container">
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

    <!-- Player inferior -->
    <PlayerInferior
      ref="playerRef"
      :videoAtual="videoAtual"
      :getVideoUrl="getVideoUrl"
      @proximo="proximaVideo"
      @anterior="videoAnterior"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, defineExpose } from 'vue'
import { Clapperboard } from 'lucide-vue-next'
import axios from 'axios'

import MenuSuperior from '@/components/MenuSuperior.vue'
import PlayerInferior from '@/components/PlayerInferior.vue'

const API_URL = 'http://localhost:8080'
const videos = ref([])
const loading = ref(true)
const videoAtual = ref(null)
const videoPlayer = ref(null)

defineExpose({ videoPlayer })

const itensPorPagina = 25
const paginaAtual = ref(1)

const totalPaginas = computed(() => {
  return Math.ceil(videos.value.length / itensPorPagina)
})

const videosPaginados = computed(() => {
  const inicio = (paginaAtual.value - 1) * itensPorPagina
  const fim = inicio + itensPorPagina
  return videos.value.slice(inicio, fim)
})

const fetchVideos = async () => {
  try {
    const response = await axios.get(`${API_URL}/api/videos/`)
    videos.value = [...response.data].sort((a, b) =>
      a.titulo.localeCompare(b.titulo)
    )
  } catch (error) {
    console.error('Erro ao carregar vídeos:', error)
  } finally {
    loading.value = false
  }
}

const selecionarVideoDireto = (video) => {
  videoAtual.value = video
  nextTick(() => {
    const player = videoPlayer.value?.videoPlayer
    if (player) {
      player.load()
      player.play().catch(err => {
        console.warn('Autoplay bloqueado:', err)
      })
    }
  })
}

const getVideoUrl = (url) => `${API_URL}${url}`.replace(/ /g, '%20')

const proximaVideo = () => {
  const index = videos.value.findIndex(v => v.id === videoAtual.value?.id)
  if (index !== -1 && index + 1 < videos.value.length) {
    videoAtual.value = videos.value[index + 1]
  }
}

const videoAnterior = () => {
  const index = videos.value.findIndex(v => v.id === videoAtual.value?.id)
  if (index > 0) {
    videoAtual.value = videos.value[index - 1]
  }
}

const proximaPagina = () => {
  if (paginaAtual.value < totalPaginas.value) {
    paginaAtual.value++
  }
}

const paginaAnterior = () => {
  if (paginaAtual.value > 1) {
    paginaAtual.value--
  }
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
.input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
  outline: none;
}
.input:focus {
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
