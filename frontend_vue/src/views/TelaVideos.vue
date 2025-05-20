<template>
  <div id="app" class="flex flex-col min-h-screen bg-[#F4FAF9] text-[#004D40]">
    <!-- Menu Superior -->
    <div class="w-full bg-[#CFF1EC] shadow-md">
      <MenuSuperior />
    </div>

    <!-- Conteúdo principal -->
    <main class="flex flex-col items-center flex-grow py-10 w-full px-4">
      <h1 class="title">🎬 Galeria de Vídeos</h1>

      <!-- Campo de busca -->
      <div class="w-full flex justify-center mb-10">
        <input
          v-model="termoBusca"
          type="text"
          placeholder="🔎 Pesquisar por título..."
          class="input-sm"
          @input="buscarVideos"
        />
      </div>

      <div v-if="loading" class="loading-spinner">Carregando vídeos...</div>

      <div v-else class="grid-container">
        <!-- Vídeos Locais -->
        <div class="video-grid">
          <div
            class="video-card"
            v-for="video in videosPaginados"
            :key="video.id"
            @click="selecionarVideoDireto(video)"
          >
            <Clapperboard class="icon-xl" />
            <h3>{{ video.titulo }}</h3>
            <p>{{ video.descricao }}</p>
          </div>
        </div>

        <!-- Resultados do YouTube -->
        <div v-if="resultadosYoutube.length > 0" class="youtube-section w-full mt-12">
          <h2 class="title mb-6">📺 Resultados da API do YouTube</h2>
          <div class="video-grid">
            <div
              class="video-card youtube-card"
              v-for="yt in resultadosYoutube"
              :key="yt.id.videoId"
              @click="abrirYoutube(yt.id.videoId)"
            >
              <img :src="yt.snippet.thumbnails.medium.url" alt="Miniatura" class="rounded-md mb-2" />
              <h3>{{ yt.snippet.title }}</h3>
              <p class="text-sm">{{ yt.snippet.channelTitle }}</p>
            </div>
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

    <!-- Player Inferior -->
    <PlayerInferior
      ref="playerRef"
      :videoAtual="videoAtual"
      :getVideoUrl="getVideoUrl"
      :togglePlayPause="togglePlayPause"
      :proximaVideo="proximaVideo"
      :videoAnterior="videoAnterior"
      :pararVideo="pararVideo"
      :atualizarVolume="atualizarVolume"
      :atualizarProgresso="atualizarProgresso"
      :isPlaying="isPlaying"
      :volume="volume"
      @update:volume="volume = $event"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useRoute } from 'vue-router'
import { Clapperboard } from 'lucide-vue-next'
import axios from 'axios'

import MenuSuperior from '@/components/MenuSuperior.vue'
import PlayerInferior from '@/components/PlayerInferior.vue'

const API_URL = 'http://localhost:8080'
const route = useRoute()

const todasVideos = ref([])
const termoBusca = ref('')
const videosFiltrados = ref([])
const resultadosYoutube = ref([])
const loading = ref(true)

const videoAtual = ref(null)
const isPlaying = ref(false)
const volume = ref(0.5)
const audioPlayer = ref(null)

const itensPorPagina = 25
const paginaAtual = ref(1)

const buscarVideos = async () => {
  const termo = termoBusca.value.toLowerCase().trim()
  if (!termo) {
    videosFiltrados.value = [...todasVideos.value]
    resultadosYoutube.value = []
  } else {
    videosFiltrados.value = todasVideos.value.filter(video =>
      (video.titulo || '').toLowerCase().includes(termo) ||
      (video.descricao || '').toLowerCase().includes(termo)
    )

    try {
      const resp = await axios.get(`${API_URL}/api/videos/apiexterna_consulta`, {
        params: { txtPesquisa: termo }
      })
      resultadosYoutube.value = resp.data.items || []
    } catch (error) {
      console.error("Erro ao consultar YouTube:", error)
      resultadosYoutube.value = []
    }
  }

  videosFiltrados.value.sort((a, b) => (a.titulo || '').localeCompare(b.titulo || ''))
  paginaAtual.value = 1
}

const totalPaginas = computed(() => {
  return Math.ceil(videosFiltrados.value.length / itensPorPagina)
})

const videosPaginados = computed(() => {
  const inicio = (paginaAtual.value - 1) * itensPorPagina
  return videosFiltrados.value.slice(inicio, inicio + itensPorPagina)
})

const fetchTodosVideos = async () => {
  try {
    const response = await axios.get(`${API_URL}/api/videos`)
    todasVideos.value = response.data.sort((a, b) =>
      (a.titulo || '').localeCompare(b.titulo || '')
    )
    videosFiltrados.value = [...todasVideos.value]
  } catch (error) {
    console.error('Erro ao carregar vídeos locais:', error)
  }
}

const selecionarVideoDireto = (video) => {
  videoAtual.value = video
  nextTick(() => {
    isPlaying.value = true
  })
}

const abrirYoutube = (videoId) => {
  window.open(`https://www.youtube.com/watch?v=${videoId}`, '_blank')
}

const getVideoUrl = (url) => encodeURI(`${API_URL}${url}`)

const togglePlayPause = () => {
  if (!audioPlayer.value) return
  if (audioPlayer.value.paused) {
    audioPlayer.value.play()
    isPlaying.value = true
  } else {
    audioPlayer.value.pause()
    isPlaying.value = false
  }
}

const atualizarVolume = () => {
  if (audioPlayer.value) {
    audioPlayer.value.volume = volume.value
  }
}

const proximaPagina = () => {
  if (paginaAtual.value < totalPaginas.value) paginaAtual.value++
}

const paginaAnterior = () => {
  if (paginaAtual.value > 1) paginaAtual.value--
}

watch(termoBusca, buscarVideos)

onMounted(async () => {
  await fetchTodosVideos()
  buscarVideos()
  loading.value = false
})
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
}
.input-sm:focus {
  border-color: #2D0F32;
  box-shadow: 0 0 0 2px rgba(45, 15, 50, 0.2);
}

.grid-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
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

.youtube-card {
  background-color: #CFF1EC;
  color: #004D40;
}
.youtube-card:hover {
  background-color: #B2DFDB;
}

.pagination-controls {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  font-weight: bold;
  color: #2D0F32;
  margin-bottom: 2rem;
}

.loading-spinner {
  color: #2D0F32;
  font-weight: bold;
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
</style>
