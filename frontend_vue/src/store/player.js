// src/store/player.js
import { reactive } from 'vue'

export const player = reactive({
  currentSong: null,
  currentSongName: null,
  isPlaying: false,
  volume: 0.5,

  togglePlay(songUrl, songName) {
    if (this.currentSong === songUrl) {
      this.isPlaying = !this.isPlaying
    } else {
      this.currentSong = songUrl
      this.currentSongName = songName
      this.isPlaying = true
    }
  }
})
