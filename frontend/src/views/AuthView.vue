<template>
  <div class="container min-vh-100 d-flex align-items-center justify-content-center">
    <div class="card p-4 shadow-lg" style="max-width: 400px; width: 100%;">
      <h2 class="text-center mb-4">{{ isLogin ? 'Вход' : 'Регистрация' }}</h2>
      <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
        {{ error }}
        <button type="button" class="btn-close" @click="error = ''"></button>
      </div>
      <form @submit.prevent="submitForm">
        <div class="mb-3">
          <label for="email" class="form-label"><i class="bi bi-envelope me-2"></i>Email</label>
          <input v-model="email" type="email" class="form-control" id="email" required placeholder="Введите email"/>
        </div>
        <div class="mb-3">
          <label for="password" class="form-label"><i class="bi bi-lock me-2"></i>Пароль</label>
          <input v-model="password" type="password" class="form-control" id="password" required
                 placeholder="Введите пароль"/>
        </div>
        <button type="submit" class="btn btn-primary w-100">
          <i class="bi bi-box-arrow-in-right me-2"></i>{{ isLogin ? 'Войти' : 'Зарегистрироваться' }}
        </button>
      </form>
      <p class="mt-3 text-center">
        <a href="#" @click.prevent="toggleMode" class="text-primary">
          {{ isLogin ? 'Нет аккаунта? Зарегистрируйтесь' : 'Уже есть аккаунт? Войдите' }}
        </a>
      </p>
    </div>
  </div>
</template>

<script setup>
import {ref} from 'vue'
import {useRouter} from 'vue-router'
import axios from 'axios'

const isLogin = ref(true)
const email = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()

const BASE_URL = 'https://resume-fullproject.onrender.com/auth'

const toggleMode = () => {
  isLogin.value = !isLogin.value
  error.value = ''
}

const submitForm = async () => {
  try {
    const endpoint = isLogin.value ? '/login' : '/register'
    const response = await axios.post(`${BASE_URL}${endpoint}`, {email: email.value, password: password.value})
    if (isLogin.value) {
      localStorage.setItem('jwt', response.data.access_token)
      router.push('/resumes')
    } else {
      error.value = 'Регистрация прошла успешно! Пожалуйста, войдите.'
      toggleMode()
    }
  } catch (error) {
    error.value = error.response?.data?.detail || 'Неизвестная ошибка'
  }
}
</script>