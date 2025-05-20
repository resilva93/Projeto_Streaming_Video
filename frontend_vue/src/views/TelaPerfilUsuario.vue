<template>
  <div id="app" class="flex flex-col min-h-screen bg-[#F4FAF9] text-[#2D0F32]">
    <!-- Menu Superior -->
    <div class="w-full bg-[#CFF1EC] shadow-md">
      <MenuSuperior />
    </div>

    <!-- Conteúdo principal -->
    <main class="flex flex-col items-center flex-grow py-10 px-4 w-full">
      <h1 class="title">👤 Perfil do Usuário</h1>

      <div v-if="mensagem" class="mensagem">{{ mensagem }}</div>

      <form @submit.prevent="salvarAlteracoes" class="form-container">
        <label for="login">Login:</label>
        <input v-model="usuario.login" id="login" type="text" class="input" required />

        <label for="senhaAtual">Senha Atual:</label>
        <input v-model="usuario.senha_atual" id="senhaAtual" type="password" class="input" required />

        <label for="novaSenha">Nova Senha:</label>
        <input v-model="usuario.nova_senha" id="novaSenha" type="password" class="input" required />

        <button type="submit" class="btn-salvar">Salvar Alterações</button>
      </form>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import MenuSuperior from '@/components/MenuSuperior.vue'

const usuario = ref({
  login: '',
  senha_atual: '',
  nova_senha: ''
})

const mensagem = ref('')

const salvarAlteracoes = async () => {
  try {
    console.log('Payload enviado:', JSON.stringify(usuario.value))

    await axios.put(
      'http://localhost:8080/api/usuarios/perfil/trocar-senha',
      JSON.stringify(usuario.value),
      {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    )

    mensagem.value = 'Informações atualizadas com sucesso!'
  } catch (error) {
    console.error('Erro ao atualizar perfil:', error)

    if (error.response) {
      const status = error.response.status
      if (status === 400) {
        mensagem.value = '⚠️ Senha atual incorreta.'
      } else if (status === 404) {
        mensagem.value = '⚠️ Usuário não encontrado.'
      } else {
        mensagem.value = 'Erro inesperado ao atualizar perfil.'
      }
    } else {
      mensagem.value = 'Erro de conexão com o servidor.'
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

* {
  font-family: 'bold';
  box-sizing: border-box;
}

.title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 2rem;
  color: #2D0F32;
  text-align: center;
}

.mensagem {
  background-color: #f3e8ff;
  border: 1px solid #d3adf7;
  padding: 12px 20px;
  border-radius: 8px;
  color: #6A0DAD;
  font-weight: 600;
  margin-bottom: 20px;
  max-width: 500px;
  text-align: center;
}

.form-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
  max-width: 500px;
  background: #ffffff;
  padding: 30px;
  border-radius: 16px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.05);
}

label {
  font-weight: 600;
  color: #2D0F32;
}

.input {
  padding: 12px;
  border: 2px solid #570a67;
  border-radius: 8px;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.3s;
}

.input:focus {
  border-color: #2D0F32;
  box-shadow: 0 0 0 2px rgba(45, 15, 50, 0.2);
}

.btn-salvar {
  background-color: #2D0F32;
  color: white;
  padding: 12px;
  border-radius: 10px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s;
  margin-top: 10px;
  border: none;
}

.btn-salvar:hover {
  background-color: #570a67;
}
</style>
