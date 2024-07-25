<template>
  <div class="page-background">
    <ExecutingTaskSidebar :selectedDroneId="selectedDroneId" :selectedTaskIds="selectedTaskIds" />
    <NavbarComponent />
    <ExecutingTasksComponent @select="handleTaskSelect" />
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
import ExecutingTaskSidebar from '../components/task/sidebar/ExecutingTaskSidebar.vue'
import NavbarComponent from '../components/NavbarComponent.vue'
import ToastComponent from '../components/ToastComponent.vue'
import ExecutingTasksComponent from '../components/ExecutingTasksComponent.vue'
import { useRoute } from 'vue-router'
import { ref } from 'vue'

const route = useRoute()
const selectedTaskId = ref([])
const selectedDroneId = ref(route.params.droneId)

const handleTaskSelect = (taskIds) => {
  selectedTaskId.value = taskIds
}
</script>
