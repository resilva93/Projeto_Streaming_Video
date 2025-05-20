<template>
  <div id="app" class="flex flex-col min-h-screen bg-[#F4FAF9] text-[#004D40]">
    <!-- Menu Superior -->
    <div class="w-full bg-[#CFF1EC] shadow-md">
      <MenuSuperior />
    </div>

    <!-- Conteúdo principal -->
    <main class="flex flex-col items-center flex-grow py-10 w-full px-4">
      <h1 class="title">🎬 Minhas Playlists</h1>

      <!-- Campo de busca -->
      <div class="w-full flex justify-center mb-6">
        <input
          v-model="termoBusca"
          type="text"
          placeholder="🔎 Pesquisar por título..."
          class="input-sm"
        />
      </div>

      <div v-if="mensagem" class="mensagem">{{ mensagem }}</div>
      <div v-if="loading" class="loading-spinner">Carregando playlists...</div>

      <div v-else class="grid-container">
        <div class="playlist-grid">
          <div
            v-for="playlist in playlistsPaginadas"
            :key="playlist.id"
            class="playlist-card"
          >
            <h2 class="playlist-title">{{ playlist.nome }}</h2>
            <p class="playlist-desc">{{ playlist.descricao }}</p>
            <p class="playlist-info">🎥 {{ playlist.videos?.length || 0 }} vídeo(s)</p>

            <div class="miniaturas">
              <div
                v-for="video in playlist.videos?.slice(0, 3)"
                :key="video.id"
                class="miniatura-card"
              >
                <img :src="video.thumbUrl || '/placeholder.jpg'" class="miniatura-img" />
                <p class="miniatura-title">{{ video.titulo.slice(0, 20) }}</p>
              </div>
            </div>

            <div class="actions">
              <button class="btn" @click="verVideos(playlist.id)">Ver Vídeos</button>
              <button class="btn editar" @click="editarPlaylist(playlist.id)">Editar</button>
              <button class="btn excluir" @click="excluirPlaylist(playlist.id)">Excluir</button>
            </div>
          </div>
        </div>

        <!-- Paginação -->
        <div class="pagination-controls mt-6">
          <button class="btn" :disabled="paginaAtual === 1" @click="paginaAnterior">Anterior</button>
          <span class="mx-4">Página {{ paginaAtual }} de {{ totalPaginas }}</span>
          <button class="btn" :disabled="paginaAtual === totalPaginas" @click="proximaPagina">Próxima</button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import MenuSuperior from '@/components/MenuSuperior.vue'

const API_URL = 'http://localhost:8080'

const playlists = ref([])
const playlistsFiltradas = ref([])
const termoBusca = ref('')
const loading = ref(true)
const mensagem = ref('')
const paginaAtual = ref(1)
const itensPorPagina = 10
const router = useRouter()

const fetchPlaylists = async () => {
  try {
    const response = await axios.get(`${API_URL}/api/playlists`)
    playlists.value = response.data.sort((a, b) =>
      (a.nome || '').localeCompare(b.nome || '')
    )
    filtrarPlaylists()
  } catch (error) {
    console.error('Erro ao carregar playlists:', error)
  } finally {
    loading.value = false
  }
}

const filtrarPlaylists = () => {
  const termo = termoBusca.value.toLowerCase().trim()
  if (!termo) {
    playlistsFiltradas.value = [...playlists.value]
  } else {
    playlistsFiltradas.value = playlists.value.filter(playlist =>
      (playlist.nome || '').toLowerCase().includes(termo)
    )
  }
  playlistsFiltradas.value.sort((a, b) =>
    (a.nome || '').localeCompare(b.nome || '')
  )
  paginaAtual.value = 1
}

const totalPaginas = computed(() => {
  return Math.ceil(playlistsFiltradas.value.length / itensPorPagina)
})

const playlistsPaginadas = computed(() => {
  const inicio = (paginaAtual.value - 1) * itensPorPagina
  return playlistsFiltradas.value.slice(inicio, inicio + itensPorPagina)
})

const paginaAnterior = () => {
  if (paginaAtual.value > 1) paginaAtual.value--
}

const proximaPagina = () => {
  if (paginaAtual.value < totalPaginas.value) paginaAtual.value++
}

const excluirPlaylist = async (playlistId) => {
  if (confirm('Tem certeza que deseja excluir essa playlist?')) {
    try {
      await axios.delete(`${API_URL}/api/playlists/${playlistId}`)
      mensagem.value = 'Playlist excluída com sucesso!'
      await fetchPlaylists()
    } catch (error) {
      console.error('Erro ao excluir playlist:', error)
    }
  }
}

const verVideos = (playlistId) => {
  router.push(`/playlist/${playlistId}`)
}

const editarPlaylist = (playlistId) => {
  router.push(`/editar-playlist/${playlistId}`)
}

onMounted(fetchPlaylists)
watch(termoBusca, filtrarPlaylists)
</script>

<style scoped>
.title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 2rem;
  color: #2D0F32;
  text-align: center;
}

.input-sm {
  width: 50%;
  padding: 0.75rem;
  border: 2px solid #570a67;
  border-radius: 10px;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.input-sm:focus {
  border-color: #2D0F32;
  box-shadow: 0 0 0 2px rgba(45, 15, 50, 0.2);
}

.mensagem {
  background-color: #f3e8ff;
  border: 1px solid #d3adf7;
  padding: 12px 20px;
  border-radius: 8px;
  color: #6A0DAD;
  font-weight: 600;
  margin-bottom: 20px;
  width: 100%;
  max-width: 800px;
  text-align: center;
}

.grid-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
}

.playlist-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 30px;
  max-width: 1100px;
  margin-bottom: 40px;
  width: 100%;
}

.playlist-card {
  background-color: #570a67;
  border-radius: 16px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
  color: #FFFFFF;
  transition: background-color 0.3s;
}

.playlist-card:hover {
  background-color: #2D0F32;
}

.playlist-title {
  font-size: 20px;
  font-weight: 700;
}

.playlist-desc {
  font-size: 14px;
  margin: 10px 0;
}

.playlist-info {
  font-size: 13px;
  color: #E0BBE4;
  margin-bottom: 10px;
}

.miniaturas {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin-top: 10px;
  flex-wrap: wrap;
}

.miniatura-card {
  width: 80px;
  text-align: center;
}

.miniatura-img {
  width: 80px;
  height: 45px;
  object-fit: cover;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.miniatura-title {
  font-size: 12px;
  color: #E0BBE4;
  margin-top: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.actions {
  margin-top: 15px;
  display: flex;
  justify-content: center;
  gap: 10px;
  flex-wrap: wrap;
}

.btn {
  background-color: #2D0F32;
  color: white;
  padding: 8px 14px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 500;
  transition: 0.3s;
}
.btn:hover {
  background-color: #570a67;
}
.btn.excluir {
  background-color: #D32F2F;
}
.btn.excluir:hover {
  background-color: #B71C1C;
}
.btn.editar {
  background-color: #5E35B1;
}
.btn.editar:hover {
  background-color: #7E57C2;
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;
  color: #2D0F32;
  margin-top: 20px;
  gap: 20px;
}

.loading-spinner {
  color: #2D0F32;
  font-weight: bold;
}
</style>
