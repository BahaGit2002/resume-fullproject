<template>
  <div class="container py-5">
    <h1 class="mb-4 display-6"><i class="bi bi-file-earmark-person me-2"></i>Мои резюме</h1>
    <button @click="showAddForm = true" class="btn btn-success mb-4">
      <i class="bi bi-plus-circle me-2"></i>Добавить резюме
    </button>

    <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
      {{ error }}
      <button type="button" class="btn-close" @click="error = ''"></button>
    </div>

    <!-- Модальное окно для добавления резюме -->
    <ResumeForm v-if="showAddForm" @close="showAddForm = false" @saved="fetchResumes" />

    <!-- Модальное окно для редактирования резюме -->
    <ResumeForm v-if="showEditForm" :resume="selectedResume" @close="showEditForm = false" @saved="handleEditSaved" />

    <!-- Модальное окно для просмотра резюме -->
    <div v-if="showViewModal" class="modal fade show d-block" tabindex="-1" style="background: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable">
        <div class="modal-content shadow-lg">
          <div class="modal-header">
            <h5 class="modal-title">{{ selectedResume.title }}</h5>
            <button type="button" class="btn-close" @click="closeView"></button>
          </div>
          <div class="modal-body">
            <p class="mb-4" style="white-space: pre-wrap; max-height: 300px; overflow-y: auto;">{{ displayedContent }}</p>
            <div class="d-flex gap-2 mb-3">
              <button @click="improveResume" class="btn btn-primary">
                <i class="bi bi-stars me-2"></i>Улучшить
              </button>
              <button @click="editResume" class="btn btn-warning">
                <i class="bi bi-pencil-square me-2"></i>Редактировать
              </button>
              <button @click="deleteResume" class="btn btn-danger">
                <i class="bi bi-trash me-2"></i>Удалить
              </button>
            </div>
            <!-- Таблица истории улучшений -->
            <div v-if="history.length > 0" class="mt-4">
              <h5>История улучшений</h5>
              <table class="table table-striped table-bordered">
                <thead>
                <tr>
                  <th style="width: 10%;">Версия</th>
                  <th style="width: 70%;">Содержимое</th>
                  <th style="width: 20%;">Дата</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="entry in history" :key="entry.version">
                  <td>{{ entry.version }}</td>
                  <td style="white-space: pre-wrap; word-break: break-word;">{{ entry.content }}</td>
                  <td>{{ new Date(entry.created_at).toLocaleString('ru-RU') }}</td>
                </tr>
                </tbody>
              </table>
            </div>
            <div v-else class="text-muted">История улучшений отсутствует</div>
          </div>
          <div class="modal-footer">
            <button @click="closeView" class="btn btn-secondary">
              <i class="bi bi-x-circle me-2"></i>Закрыть
            </button>
          </div>
        </div>
      </div>
    </div>

    <ul class="list-group">
      <li v-for="resume in resumes" :key="resume.id" class="list-group-item d-flex justify-content-between align-items-center">
        <span><i class="bi bi-file-earmark-text me-2"></i>{{ resume.title }}</span>
        <button @click="viewResume(resume)" class="btn btn-primary btn-sm">
          <i class="bi bi-eye me-2"></i>Просмотреть
        </button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import ResumeForm from '../components/ResumeForm.vue'

const resumes = ref([])
const selectedResume = ref(null)
const displayedContent = ref('')
const showAddForm = ref(false)
const showEditForm = ref(false)
const showViewModal = ref(false)
const error = ref('')
const history = ref([])

const BASE_URL = 'https://resume-fullproject.onrender.com'
const token = localStorage.getItem('jwt')

const fetchResumes = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/resumes`, { headers: { Authorization: `Bearer ${token}` } })
    resumes.value = response.data
    error.value = ''
  } catch (error) {
    error.value = 'Ошибка при получении списка резюме'
  }
}

const viewResume = async (resume) => {
  try {
    const response = await axios.get(`${BASE_URL}/resumes/${resume.id}`, { headers: { Authorization: `Bearer ${token}` } })
    selectedResume.value = response.data
    displayedContent.value = response.data.content
    await fetchHistory(resume.id)
    showViewModal.value = true
    error.value = ''
  } catch (error) {
    error.value = 'Ошибка при просмотре резюме'
  }
}

const fetchHistory = async (resumeId) => {
  try {
    const response = await axios.get(`${BASE_URL}/resumes/${resumeId}/history`, { headers: { Authorization: `Bearer ${token}` } })
    history.value = response.data
    error.value = ''
  } catch (error) {
    error.value = 'Ошибка при получении истории улучшений'
    history.value = []
  }
}

const improveResume = async () => {
  try {
    if (!selectedResume.value || !selectedResume.value.content) {
      error.value = 'Нет данных для улучшения резюме'
      return
    }
    const response = await axios.post(
        `${BASE_URL}/resumes/${selectedResume.value.id}/improve`,
        { content: selectedResume.value.content },
        { headers: { Authorization: `Bearer ${token}` } }
    )
    displayedContent.value = response.data.improved_content
    selectedResume.value.content = response.data.improved_content
    await fetchHistory(selectedResume.value.id)
    error.value = ''
  } catch (error) {
    error.value = 'Ошибка при улучшении резюме: ' + (error.response?.data?.detail || error.message)
  }
}

const editResume = () => {
  showViewModal.value = false
  showEditForm.value = true
}

const handleEditSaved = async () => {
  await fetchResumes()
  if (selectedResume.value) {
    await viewResume({ id: selectedResume.value.id })
  }
}

const deleteResume = async () => {
  if (confirm('Вы уверены, что хотите удалить резюме?')) {
    try {
      await axios.delete(`${BASE_URL}/resumes/${selectedResume.value.id}`, { headers: { Authorization: `Bearer ${token}` } })
      showViewModal.value = false
      selectedResume.value = null
      history.value = []
      fetchResumes()
      error.value = ''
    } catch (error) {
      error.value = 'Ошибка при удалении резюме'
    }
  }
}

const closeView = () => {
  showViewModal.value = false
  selectedResume.value = null
  displayedContent.value = ''
  history.value = []
  error.value = ''
}

onMounted(fetchResumes)
</script>