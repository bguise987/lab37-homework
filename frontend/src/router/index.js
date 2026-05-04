import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import LoginView from '../views/LoginView.vue'
import SelectCompanyView from '../views/SelectCompanyView.vue'
import DashboardView from '../views/DashboardView.vue'
import RecipeView from '../views/RecipeView.vue'
import RecipeEditView from '../views/RecipeEditView.vue'

const routes = [
  { path: '/login', component: LoginView },
  { path: '/select-company', component: SelectCompanyView, meta: { requiresAuth: true } },
  { path: '/', component: DashboardView, meta: { requiresAuth: true, requiresCompany: true } },
  { path: '/recipes/new', component: RecipeEditView, meta: { requiresAuth: true, requiresCompany: true } },
  { path: '/recipes/:id', component: RecipeView, meta: { requiresAuth: true, requiresCompany: true } },
  { path: '/recipes/:id/edit', component: RecipeEditView, meta: { requiresAuth: true, requiresCompany: true } },
  { path: '/:pathMatch(.*)*', redirect: '/' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.token) return '/login'
  if (to.meta.requiresCompany && !auth.selectedCompanyId) return '/select-company'
  if (to.path === '/login' && auth.token) {
    return auth.selectedCompanyId ? '/' : '/select-company'
  }
})

export default router
