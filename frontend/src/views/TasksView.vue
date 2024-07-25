<template>
  <div class="page-background">
    <TaskSidebar :selectedTaskId="selectedTaskId" />
    <NavbarComponent />
    <TasksComponent @select="handleTaskSelect" />
    <ToastComponent />
  </div>
</template>

<style scoped>
.page-background {
  background: linear-gradient(to right, #000000, gray);
  background-size: cover; /* Ensures the background image covers the entire container */
  background-position: center; /* Centers the background image */
  background-repeat: no-repeat; /* Prevents the background image from repeating */
  background-attachment: fixed;
  min-height: 100vh;
  width: 100vw; /* Ensure it covers the full viewport width */
  overflow-x: hidden;
}
</style>

<script setup>
import TaskSidebar from '../components/task/sidebar/TaskSidebar.vue'
import NavbarComponent from '../components/NavbarComponent.vue'
import ToastComponent from '../components/ToastComponent.vue'
import TasksComponent from '../components/TasksComponent.vue'
import { ref } from 'vue'

const selectedTaskId = ref(null)

const handleTaskSelect = (taskId) => {
  selectedTaskId.value = taskId
}
</script>
