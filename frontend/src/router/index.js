import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import MapWithLogin from '../views/MapWithLogin.vue'
import ForgotPasswordRequest from '../views/ForgotPasswordRequest.vue'
import ForgotPasswordToken from '../views/ForgotPasswordToken.vue'
import DronesView from '../views/DronesView.vue'
import TasksView from '../views/TasksView.vue'
import AssignedTasksView from '../views/AssignedTasksView.vue'
import ExecutingTasksView from '../views/ExecutingTasksView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login-register',
      name: 'login-register',
      component: LoginView
    },
    {
      path: '/reset-password',
      name: 'reset-password',
      component: ForgotPasswordRequest
    },
    {
      path: '/reset-password/:token/:userId',
      name: 'reset-password-token',
      component: ForgotPasswordToken,
      props: true
    },
    {
      path: '/home',
      name: 'home-login',
      component: MapWithLogin
    },
    {
      path: '/drones',
      name: 'drones',
      component: DronesView
    },
    {
      path: '/tasks',
      name: 'tasks',
      component: TasksView
    },
    {
      path: '/drones/:droneId/assigned-tasks',
      name: 'assigned-tasks',
      component: AssignedTasksView
    },
    {
      path: '/drones/:droneId/executing-tasks',
      name: 'executing-tasks',
      component: ExecutingTasksView
    }
  ]
})

export default router
