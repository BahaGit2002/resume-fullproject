<template>
  <div class="modal fade show d-block" tabindex="-1" style="background: rgba(0,0,0,0.5);">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content shadow-lg">
        <div class="modal-header">
          <h5 class="modal-title">
            <i class="bi bi-file-earmark-plus me-2"></i>{{ resume ? 'Редактировать резюме' : 'Добавить резюме' }}
          </h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>
        <div class="modal-body">
          <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
            {{ error }}
            <button type="button" class="btn-close" @click="error = ''"></button>
          </div>
          <form @submit.prevent="saveResume">
            <div class="mb-3">
              <label for="title" class="form-label">Название</label>
              <input v-model="form.title" type="text" class="form-control" id="title" required
                     placeholder="Введите название"/>
            </div>
            <div class="mb-3">
              <label for="content" class="form-label">Содержание</label>
              <textarea v-model="form.content" class="form-control" id="content" rows="6" required
                        placeholder="Введите текст резюме"></textarea>
            </div>
            <button type="submit" class="btn btn-primary me-2">
              <i class="bi bi-save me-2"></i>Сохранить
            </button>
            <button type="button" class="btn btn-secondary" @click="$emit('close')">
              <i class="bi bi-x-circle me-2"></i>Отмена
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, watch} from 'vue'
import {defineProps, defineEmits} from 'vue'
import axios from 'axios'

const props = defineProps({
  resume: Object
})

const emit = defineEmits(['close', 'saved'])

const form = ref({
  title: '',
  content: ''
})

const error = ref('')

watch(() => props.resume, (newResume) => {
  if (newResume) {
    form.value.title = newResume.title
    form.value.content = newResume.content
  }
}, {immediate: true})

const BASE_URL = 'http://localhost:8000'
const token = localStorage.getItem('jwt')

const saveResume = async () => {
  try {
    if (props.resume) {
      await axios.put(`${BASE_URL}/resumes/${props.resume.id}`, form.value, {headers: {Authorization: `Bearer ${token}`}})
    } else {
      await axios.post(`${BASE_URL}/resumes`, form.value, {headers: {Authorization: `Bearer ${token}`}})
    }
    emit('saved')
    emit('close')
    error.value = ''
  } catch (error) {
    error.value = 'Ошибка при сохранении резюме'
  }
}
</script>