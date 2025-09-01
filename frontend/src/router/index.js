import { createRouter, createWebHashHistory } from 'vue-router'
import AuthView from "@/views/AuthView.vue";
import ResumesView from "@/views/ResumesView.vue";

const router = createRouter({
    history: createWebHashHistory(import.meta.env.BASE_URL),
    routes: [
        { path: '/', name: 'auth', component: AuthView },
        { path: '/resumes', name: 'resumes', component: ResumesView, meta: { requiresAuth: true } }
    ]
})

router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('jwt')
    if (to.matched.some(record => record.meta.requiresAuth) && !token) {
        next('/')
    } else {
        next()
    }
})

export default router