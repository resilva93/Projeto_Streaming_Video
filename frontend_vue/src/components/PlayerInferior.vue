<template>
  <footer class="player-bar fixed bottom-0 left-0 w-full z-50">
    <div class="media-controls" v-if="videoAtual">
      <!-- Título -->
      <div class="player-title">
        <h2>{{ videoAtual.titulo }}</h2>
      </div>

      <!-- Botões de navegação -->
      <div class="control-buttons">
        <button @click="emit('anterior')">⏮️</button>
        <button @click="emit('proximo')">⏭️</button>
        <button @click="entrarTelaCheia">📺</button>
      </div>

      <!-- Vídeo -->
      <div class="inline-video-player">
        <video
          ref="videoPlayer"
          :src="getVideoUrl(videoAtual.url)"
          autoplay
          controls
          @ended="emit('proximo')"
          class="video-element"
        ></video>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'

const props = defineProps(['videoAtual', 'getVideoUrl'])
const emit = defineEmits(['proximo', 'anterior'])

const videoPlayer = ref(null)

watch(() => props.videoAtual, async () => {
  if (videoPlayer.value) {
    await nextTick()
    try {
      await videoPlayer.value.play()
    } catch (err) {
      console.warn('Autoplay bloqueado:', err)
    }
  }
})

const entrarTelaCheia = () => {
  const player = videoPlayer.value
  if (player && player.requestFullscreen) {
    player.requestFullscreen()
  }
}
</script>

<style scoped>
.player-bar {
  background-color: #23005A;
  padding: 20px;
  border-top: 1px solid #FFDD33;
  box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.05);
}
.media-controls {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
}
.player-title h2 {
  font-size: 16px;
  font-weight: 600;
}
.control-buttons button {
  font-size: 22px;
  background: none;
  border: none;
  cursor: pointer;
  color: 	#23005A;
}
.control-buttons button:hover {
  color: #004D40;
}
.inline-video-player {
  width: 360px;
  height: 200px;
}
.video-element {
  width: 100%;
  height: 100%;
  border-radius: 10px;
}
</style>
