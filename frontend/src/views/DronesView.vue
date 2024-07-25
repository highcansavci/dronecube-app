<template>
  <div class="page-background">
    <DroneSidebar :selectedDroneId="selectedDroneId" />
    <NavbarComponent />
    <DronesComponent @select="handleDroneSelect" />
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
import DroneSidebar from '../components/drone/sidebar/DroneSidebar.vue'
import NavbarComponent from '../components/NavbarComponent.vue'
import ToastComponent from '../components/ToastComponent.vue'
import DronesComponent from '../components/DronesComponent.vue'
import { ref } from 'vue'

const selectedDroneId = ref(null)

const handleDroneSelect = (droneId) => {
  selectedDroneId.value = droneId
}
</script>
