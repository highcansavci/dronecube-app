<template>
  <div class="sidebar-item">
    <h2 className="sidebar-title">Drone Name</h2>
    <DroneTextInput label="Name" placeholder="Drone Name" v-model="name" inputId="nameInput" />
  </div>
</template>

<script setup>
import DroneTextInput from '../essentials/DroneTextInput.vue'
import { ref, watch } from 'vue'
import { useDroneStore } from '@/stores/droneStore'

const drone = useDroneStore()
const name = ref(drone.name)

watch(name, (newValue) => {
  drone.changeName(newValue)
})
</script>

<style scoped>
.sidebar-title {
  font-size: 20px;
  font-weight: normal;
  margin-bottom: 20px;
  color: #fff;
}

.sidebar-item {
  margin-top: 10px;
  margin-right: 0.7rem;
  width: 87%;
}
</style>
