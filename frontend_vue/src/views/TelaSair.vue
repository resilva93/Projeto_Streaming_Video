<template>
  <div id="app" class="flex flex-col min-h-screen bg-[#F4FAF9] text-[#004D40]">
    <!-- Menu Superior -->
    <div class="w-full bg-[#CFF1EC] shadow-md">
      <MenuSuperior />
    </div>

    <!-- Conteúdo principal -->
    <main class="flex flex-col items-center flex-grow py-10 w-full px-4">
      <h1 class="title">👋 Sessão encerrada</h1>

      <p class="mensagem-despedida">
        Sua sessão foi finalizada com sucesso.<br />
        Esperamos ver você novamente em breve!
      </p>

      <router-link to="/login">
        <button class="btn mt-6">Fazer Login</button>
      </router-link>
    </main>

    <!-- Player inferior (opcional: remova se não quiser exibir nessa tela) -->
    <PlayerInferior
      ref="playerRef"
      :videoAtual="null"
      :getVideoUrl="() => ''"
      @proximo="() => {}"
      @anterior="() => {}"
    />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import MenuSuperior from '@/components/MenuSuperior.vue'
import PlayerInferior from '@/components/PlayerInferior.vue'

// Limpa dados de sessão ou token no logout
onMounted(() => {
  localStorage.removeItem('token')
  sessionStorage.clear()
})
</script>

<style scoped>
.title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 2rem;
  color: #2D0F32;
  text-align: center;
}

.mensagem-despedida {
  font-size: 16px;
  color: #1A1A1A;
  text-align: center;
  line-height: 1.6;
}

.btn {
  background-color: #2D0F32;
  color: white;
  padding: 12px 24px;
  font-weight: bold;
  font-size: 16px;
  border-radius: 10px;
  cursor: pointer;
  transition: background-color 0.3s;
}
.btn:hover {
  background-color: #570a67;
}
</style>
