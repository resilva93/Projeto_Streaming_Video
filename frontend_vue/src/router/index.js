import { createRouter, createWebHistory } from 'vue-router'

import TelaLogin from '@/views/TelaLogin.vue'
import TelaInicial from '@/views/TelaInicial.vue'
import TelaVideos from '@/views/TelaVideos.vue'
import TelaPlaylist from '@/views/TelaPlaylist.vue'
import TelaGerenciaPlaylists from '@/views/TelaGerenciaPlaylists.vue'
import TelaCarregaVideo from '@/views/TelaCarregaVideo.vue'
import TelaPlaylistDetalhe from '@/views/TelaPlaylistDetalhe.vue'
import TelaPerfilUsuario from '@/views/TelaPerfilUsuario.vue'
import TelaSair from '@/views/TelaSair.vue'
import TelaNovoUsuario from '@/views/TelaNovoUsuario.vue'


const routes = [
  {
    path: '/login',
    name: 'Login',
    component: TelaLogin,
  },
  {
    path: '/',
    name: 'Inicio',
    component: TelaInicial,
  },
    {
    path: '/criar-usuario',
    name: 'Novo Usuario',
    component: TelaNovoUsuario,
  },
  {
    path: '/videos',
    name: 'Todos Os Videos',
    component: TelaVideos,
  },
  {
    path: '/usuario',
    name: 'Perfil Usuario',
    component: TelaPerfilUsuario,
  },
  {
    path: '/gerenciar-playlists',
    name: 'GerenciarPlaylists',
    component: TelaGerenciaPlaylists,
  },
  {
    path: '/upload',
    name: 'Upload Videos',
    component: TelaCarregaVideo,
  },
  {
    path: '/playlists',
    name: 'Minhas Playlists',
    component: TelaPlaylist,
  },
    {
    path: '/sair',
    name: 'Sair',
    component: TelaSair,
  },
  {
    path: '/playlist/:id',
    name: 'PlaylistDetalhe',
    component: TelaPlaylistDetalhe,
    props: true, 
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
