<template>
  <header class="top-menu">
    <nav class="menu-nav">
      <router-link to="/" class="menu-item">Início</router-link>
      <router-link to="/upload" class="menu-item">Upload de Vídeos</router-link>
      <router-link to="/videos" class="menu-item">Todos os Vídeos</router-link>
      <router-link to="/playlists" class="menu-item">Criar Playlist</router-link>
      <router-link to="/gerenciar-playlists" class="menu-item">Minhas Playlists</router-link>
      <router-link to="/usuario" class="menu-item">Usuário</router-link>
      <router-link to="/sair" class="menu-item">Sair</router-link>
    </nav>
  </header>
</template>

<style scoped>
.top-menu {
  background-color:	#23005A;
  padding: 15px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}
.menu-nav {
  display: flex;
  justify-content: center;
  gap: 30px;
}
.menu-item {
  color: #FFDD33;
  font-weight: 600;
  font-size: 1rem;
  text-decoration: none;
  transition: color 0.3s;
}
.menu-item:hover {
  color: #2BBBAD;
}
</style>
