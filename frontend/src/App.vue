<template>
  <div>
    <nav v-if="$route.meta.requiresAuth" class="navbar navbar-expand-lg navbar-light bg-light shadow-sm">
      <div class="container">
        <a class="navbar-brand" href="#">Резюме</a>
        <button class="btn btn-outline-danger ms-auto" @click="logout">
          <i class="bi bi-box-arrow-right"></i> Выйти
        </button>
      </div>
    </nav>
    <div class="container py-4">
      <RouterView/>
    </div>
  </div>
</template>

<script setup>
import {useRouter} from 'vue-router'

const router = useRouter()

const logout = () => {
  localStorage.removeItem('jwt')
  router.push('/')
}
</script>