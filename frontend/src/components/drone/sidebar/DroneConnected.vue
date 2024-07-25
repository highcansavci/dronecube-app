<template>
  <div class="sidebar-item">
    <h2 class="sidebar-title">Drone Connection Status</h2>
    <DroneRadioInput
      v-model="selectedOption"
      name="connected"
      value="All"
      title="All"
      :checked="true"
    />
    <DroneRadioInput
      v-model="selectedOption"
      name="connected"
      value="Connected"
      title="Connected"
    />
    <DroneRadioInput
      v-model="selectedOption"
      name="connected"
      value="Not Connected"
      title="Not Connected"
    />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import DroneRadioInput from '../essentials/DroneRadioInput.vue'
import { useDroneStore } from '@/stores/droneStore'

const drone = useDroneStore()
const selectedOption = ref(drone.connected)

watch(selectedOption, (newValue) => {
  drone.changeConnected(newValue)
})
</script>

<style scoped>
.sidebar-item {
  margin: 10px 0;
  width: 90%;
}

.sidebar-title {
  font-size: 19px;
  font-weight: normal;
  color: #fff;
  margin-bottom: 20px;
}
</style>
