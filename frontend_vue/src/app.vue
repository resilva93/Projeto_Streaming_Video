<template>
  <div id="app">
    <router-view />

    <!-- Player de Videos Global Invisível -->
    <audio
      ref="audioPlayer"
      v-if="player.currentSong"
      :src="player.currentSong"
      @ended="player.isPlaying = false"
      hidden
    ></audio>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { player } from '@/store/player'

const audioPlayer = ref(null)

// Sempre que o currentSong mudar
watch(() => player.currentSong, async (newSong) => {
  if (newSong && audioPlayer.value) {
    try {
      await audioPlayer.value.play()
      player.isPlaying = true
    } catch (error) {
      console.error('Erro ao tentar reproduzir o vídeo:', error)
    }
  }
})

// Quando clicar em "Pause" ou "Play"
watch(() => player.isPlaying, (isPlaying) => {
  if (audioPlayer.value) {
    if (isPlaying) {
      audioPlayer.value.play()
    } else {
      audioPlayer.value.pause()
    }
  }
})
</script>

<style scoped>
.global-player {
  position: fixed;
  bottom: 0;
  left: 250px;
  right: 0;
  height: 80px;
  background: #e6f0fa;
  border-top: 1px solid #ccc;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 30px;
  z-index: 1000;
}

.player-info {
  font-size: 16px;
  font-weight: bold;
}

.player-controls {
  display: flex;
  align-items: center;
  gap: 20px;
}

.icon-btn {
  width: 28px;
  height: 28px;
  cursor: pointer;
  transition: transform 0.2s;
}

.icon-btn:hover {
  transform: scale(1.2);
}

.player-volume input {
  width: 100px;
}
</style>
