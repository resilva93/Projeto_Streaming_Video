<template>
  <div id="app" class="flex flex-col min-h-screen bg-[#F4FAF9] text-[#004D40]">
    <!-- Menu Superior-->
    <div class="w-full bg-[#CFF1EC] shadow-md">
      <MenuSuperior />
    </div>

    <!-- Conteúdo principal -->
    <main class="flex flex-col items-center flex-grow py-10 w-full px-4">
      <h1 class="title">🎵 Playlist {{ playlistId }}</h1>

      <div v-if="loading" class="loading-spinner">Carregando playlist...</div>

      <div v-else class="grid-container">
        <h2 class="subtitle">🎶 Vídeos na Playlist</h2>

        <div v-if="videosNaPlaylist.length === 0" class="empty-message">
          Nenhum vídeo adicionado ainda 🎵
        </div>

        <div class="video-grid">
          <div v-for="(video, index) in videosNaPlaylist" :key="video.id" class="video-card">
            <h3>{{ video.titulo }}</h3>
            <p>{{ video.artista }}</p>
            <button @click="selecionarVideo(index)" class="btn">▶️ Tocar</button>
            <button @click="removerVideo(video.id)" class="btn-remove">Remover</button>
          </div>
        </div>

        <h2 class="subtitle">➕ Adicionar novos vídeos</h2>
        <div class="video-grid">
          <div v-for="video in todasVideos" :key="video.id" class="video-card">
            <h3>{{ video.titulo }}</h3>
            <p>{{ video.artista }}</p>
            <button @click="adicionarVideo(video.id)" class="btn-add">Adicionar</button>
          </div>
        </div>
      </div>
    </main>

    <!-- Player inferior -->
    <PlayerInferior
      ref="playerRef"
      :videoAtual="videoAtual"
      :getVideoUrl="getAudioUrl"
      @proximo="proximoVideo"
      @anterior="videoAnterior"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import MenuSuperior from '@/components/MenuSuperior.vue'
import PlayerInferior from '@/components/PlayerInferior.vue'

const API_URL = 'http://localhost:8080'
const route = useRoute()
const playlistId = route.params.id
const videosNaPlaylist = ref([])
const todasVideos = ref([])
const loading = ref(true)

const videoAtual = ref(null)
const videoAtualIndex = ref(0)
const playerRef = ref(null)

const fetchVideosDaPlaylist = async () => {
  try {
    const response = await axios.get(`${API_URL}/api/playlists/${playlistId}/videos`)
    videosNaPlaylist.value = response.data
  } catch (error) {
    console.error('Erro ao carregar vídeos da playlist:', error)
  }
}

const fetchTodosVideos = async () => {
  try {
    const response = await axios.get(`${API_URL}/api/videos`)
    todasVideos.value = response.data
  } catch (error) {
    console.error('Erro ao carregar todos vídeos:', error)
  }
}

const adicionarVideo = async (videoId) => {
  try {
    await axios.post(`${API_URL}/api/playlists/${playlistId}/add-video/${videoId}`)
    alert('Música adicionada!')
    fetchVideosDaPlaylist()
  } catch (error) {
    console.error('Erro ao adicionar vídeo:', error)
  }
}

const removerVideo = async (videoId) => {
  if (confirm('Remover vídeo da playlist?')) {
    try {
      await axios.delete(`${API_URL}/api/playlists/${playlistId}/remove-video/${videoId}`)
      alert('Vídeo removido!')
      fetchVideosDaPlaylist()
    } catch (error) {
      console.error('Erro ao remover vídeo:', error)
    }
  }
}

const selecionarVideo = (index) => {
  videoAtualIndex.value = index
  videoAtual.value = videosNaPlaylist.value[index]
  nextTick(() => {
    const player = playerRef.value?.videoPlayer
    if (player) {
      player.load()
      player.play().catch(err => console.warn('Autoplay bloqueado:', err))
    }
  })
}

const getAudioUrl = (url) => `${API_URL}${url}`.replace(/ /g, '%20')

const proximoVideo = () => {
  if (videosNaPlaylist.value.length === 0) return
  videoAtualIndex.value = (videoAtualIndex.value + 1) % videosNaPlaylist.value.length
  selecionarVideo(videoAtualIndex.value)
}

const videoAnterior = () => {
  if (videosNaPlaylist.value.length === 0) return
  videoAtualIndex.value = (videoAtualIndex.value - 1 + videosNaPlaylist.value.length) % videosNaPlaylist.value.length
  selecionarVideo(videoAtualIndex.value)
}

onMounted(async () => {
  await fetchVideosDaPlaylist()
  await fetchTodosVideos()
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
.subtitle {
  font-size: 20px;
  font-weight: 600;
  margin-top: 2rem;
  color: #004D40;
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
.btn,
.btn-add,
.btn-remove {
  background-color: #2D0F32;
  color: white;
  padding: 8px 16px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 500;
  transition: 0.3s;
  margin-top: 10px;
}
.btn-add {
  background-color: #00b894;
}
.btn-remove {
  background-color: #ff4d4d;
}
.loading-spinner {
  color: #2D0F32;
  font-weight: bold;
}
.empty-message {
  font-size: 18px;
  color: #888;
  margin-bottom: 20px;
}
</style>
