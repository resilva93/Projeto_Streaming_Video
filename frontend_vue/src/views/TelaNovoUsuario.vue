<template>
  <div id="app" class="flex flex-col min-h-screen bg-[#F4FAF9] text-[#004D40]">
    <!-- Menu Superior -->
    <div class="w-full bg-[#CFF1EC] shadow-md">
      <MenuSuperior />
    </div>

    <!-- Conteúdo principal -->
    <main class="flex flex-col items-center flex-grow py-10 w-full px-4">
      <div class="w-full max-w-md bg-white rounded-2xl shadow-lg p-8">
        <h1 class="title text-center">📝 Criar Conta</h1>

        <form @submit.prevent="criarUsuario" class="space-y-5">
          <div>
            <label for="nome_usuario" class="sr-only">Nome</label>
            <input
              id="nome_usuario"
              v-model="nome_usuario"
              type="text"
              placeholder="Nome completo"
              class="input"
              required
            />
          </div>

          <div>
            <label for="login" class="sr-only">Login</label>
            <input
              id="login"
              v-model="login"
              type="text"
              placeholder="Login"
              class="input"
              autocomplete="username"
              required
            />
          </div>

          <div>
            <label for="senha" class="sr-only">Senha</label>
            <input
              id="senha"
              v-model="senha"
              type="password"
              placeholder="Senha"
              class="input"
              autocomplete="new-password"
              required
            />
          </div>

          <button type="submit" class="btn" :disabled="carregando">
            {{ carregando ? 'Criando...' : 'Criar Conta' }}
          </button>
        </form>

        <p class="text-sm text-center text-gray-600 mt-4">
          Já tem uma conta?
          <router-link to="/login" class="text-[#2BBBAD] hover:underline font-semibold">
            Fazer login
          </router-link>
        </p>

        <div
          v-if="mensagem"
          class="mensagem-alerta mt-4"
          :class="sucesso ? 'sucesso' : 'erro'"
        >
          {{ mensagem }}
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import MenuSuperior from '@/components/MenuSuperior.vue'

const nome_usuario = ref('')
const login = ref('')
const senha = ref('')
const mensagem = ref('')
const sucesso = ref(false)
const carregando = ref(false)
const router = useRouter()

const API = 'http://localhost:8080/api/usuarios/criar'

const criarUsuario = async () => {
  carregando.value = true
  mensagem.value = ''
  sucesso.value = false

  try {
    const payload = {
      nome_usuario: nome_usuario.value,
      login: login.value,
      senha: senha.value
    }

    const response = await axios.post(API, payload)

    if (response.status === 200 || response.status === 201) {
      sucesso.value = true
      mensagem.value = 'Conta criada com sucesso! ✅'
      setTimeout(() => router.push('/login'), 1500)
    }
  } catch (err) {
    if (err.response?.data?.detail) {
      mensagem.value = err.response.data.detail
    } else {
      mensagem.value = 'Erro ao criar usuário ❌'
    }
  } finally {
    carregando.value = false
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

* {
  font-family: 'bold';
}

.title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 2rem;
  color: #2D0F32;
}

.input {
  width: 50%;
  padding: 0.75rem;
  border: 2px solid #570a67;
  border-radius: 8px;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.3s, box-shadow 0.3s;
  margin-bottom: 1rem;
}

.input:focus {
  outline: none;
  border-color: #2D0F32;
  box-shadow: 0 0 0 2px rgba(45, 15, 50, 0.2);
}

.btn {
  width: 100%;
  background-color: #2D0F32;
  color: white;
  padding: 12px;
  font-weight: bold;
  font-size: 16px;
  border-radius: 10px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn:hover {
  background-color: #570a67;
}

.btn:disabled {
  background-color: #b2dfdb;
  cursor: not-allowed;
}

.mensagem-alerta {
  padding: 10px 15px;
  border-radius: 8px;
  text-align: center;
  font-weight: 500;
}

.mensagem-alerta.sucesso {
  background-color: #E8F6F3;
  color: #145a86;
}

.mensagem-alerta.erro {
  background-color: #fdecea;
  color: #b00020;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
</style>
