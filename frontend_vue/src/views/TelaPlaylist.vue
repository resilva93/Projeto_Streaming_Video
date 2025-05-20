<template>
  <div id="app" class="flex flex-col min-h-screen bg-[#F4FAF9] text-[#004D40]">
    <!-- Menu Superior -->
    <div class="w-full bg-[#CFF1EC] shadow-md">
      <MenuSuperior />
    </div>

    <!-- Conteúdo principal -->
    <main class="flex flex-col items-center flex-grow py-10 w-full px-4">
      <h1 class="title">🎬 Criar Nova Playlist</h1>

    <!-- Inputs -->
      <div class="w-full md:w-1/2 mx-auto flex flex-col gap-4 mb-8">
        <input
          v-model="nomePlaylist"
          placeholder="Nome da Playlist"
          class="input-sm"
        />
        <input
          v-model="descricao"
          placeholder="Descrição da Playlist"
          class="input-sm"
        />
      </div>

      <!-- Lista de vídeos com paginação -->
      <div class="grid-container">
        <div class="video-grid">
          <div
            v-for="video in videosPaginados"
            :key="video.id"
            class="video-card"
            :class="{ 'selecionado': videosSelecionados.includes(video.id) }"
            @click="toggleVideoSelecionado(video.id)"
          >
            <div class="flex gap-4 items-start">
              <input
                type="checkbox"
                :checked="videosSelecionados.includes(video.id)"
                @click.stop="toggleVideoSelecionado(video.id)"
              />
              <div>
                <h3 class="font-bold text-lg">{{ video.titulo }}</h3>
                <p class="text-sm text-[#eee]">{{ video.descricao }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Controles de paginação -->
        <div class="pagination-controls mt-6">
          <button class="btn" :disabled="paginaAtual === 1" @click="paginaAnterior">Anterior</button>
          <span class="px-4">Página {{ paginaAtual }} de {{ totalPaginas }}</span>
          <button class="btn" :disabled="paginaAtual === totalPaginas" @click="proximaPagina">Próxima</button>
        </div>
      </div>

      <!-- Botão -->
      <button @click="criarPlaylist" class="btn mt-8">Criar Playlist</button>

      <!-- Mensagem -->
      <div v-if="mensagem" class="mensagem-alerta mt-4">
        {{ mensagem }}
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import MenuSuperior from '@/components/MenuSuperior.vue'

const API_URL = 'http://localhost:8080'

const videos = ref([])
const videosSelecionados = ref([])
const nomePlaylist = ref('')
const descricao = ref('')
const mensagem = ref('')
const paginaAtual = ref(1)
const itensPorPagina = 25
const router = useRouter()

const fetchVideos = async () => {
  try {
    const response = await axios.get(`${API_URL}/api/videos`)
    videos.value = response.data
  } catch (error) {
    console.error('Erro ao buscar vídeos:', error)
  }
}

const videosPaginados = computed(() => {
  const inicio = (paginaAtual.value - 1) * itensPorPagina
  return videos.value.slice(inicio, inicio + itensPorPagina)
})

const totalPaginas = computed(() => {
  return Math.ceil(videos.value.length / itensPorPagina)
})

const proximaPagina = () => {
  if (paginaAtual.value < totalPaginas.value) paginaAtual.value++
}

const paginaAnterior = () => {
  if (paginaAtual.value > 1) paginaAtual.value--
}

const toggleVideoSelecionado = (id) => {
  const index = videosSelecionados.value.indexOf(id)
  if (index > -1) {
    videosSelecionados.value.splice(index, 1)
  } else {
    videosSelecionados.value.push(id)
  }
}

const criarPlaylist = async () => {
  try {
    const payload = {
      nome_playlist: nomePlaylist.value?.trim(),
      descricao: descricao.value?.trim() || '',
      videos_ids: videosSelecionados.value
        .filter(id => id !== null && id !== undefined)
        .map(id => parseInt(id))
    }

    console.log('Payload enviado:', JSON.stringify(payload, null, 2))

    await axios.post(`${API_URL}/api/playlists/`, payload)
    mensagem.value = 'Playlist criada com sucesso! 🎉'

    setTimeout(() => {
      router.push('/manage-playlists')
    }, 1500)
  } catch (error) {
    console.error('Erro ao criar playlist:', error)
    if (error.response?.data?.detail) {
      console.error('Detalhe da API:', error.response.data.detail)
    }
    mensagem.value = 'Erro ao criar a playlist. Verifique os campos.'
  }
}

onMounted(fetchVideos)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

* {
  font-family: bold;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.title {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 2rem;
  color: #2D0F32;
}

.input-sm {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #570a67;
  border-radius: 8px;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.3s, box-shadow 0.3s;
  margin-bottom: 1rem;
  max-width: 400px;
}
.input-sm:focus {
  border-color: #2D0F32;
  box-shadow: 0 0 0 2px rgba(45, 15, 50, 0.2);
}

.grid-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.video-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 20px;
  max-width: 1200px;
}

.video-card {
  background-color: #570a67;
  border-radius: 16px;
  padding: 16px;
  color: white;
  text-align: left;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
  transition: background-color 0.3s, border-color 0.3s;
  margin-bottom: 1rem;
  cursor: pointer;
  border: 2px solid transparent;
}

.video-card:hover {
  background-color: #2D0F32;
}

.video-card.selecionado {
  background-color: #2D0F32;
  border-color: #00bfa5;
}

.btn {
  background-color: #2D0F32;
  color: white;
  padding: 12px 24px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s;
}
.btn:hover {
  background-color: #570a67;
}

.pagination-controls {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  font-weight: bold;
  color: #2D0F32;
  margin-bottom: 4rem;
}

.mensagem-alerta {
  font-weight: bold;
  color: #145a86;
  background: #e6f0fa;
  padding: 10px 20px;
  border-radius: 8px;
  text-align: center;
}
</style>
