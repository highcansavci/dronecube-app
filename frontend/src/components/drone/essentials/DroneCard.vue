<template>
  <div className="drone-card" :class="{ selected: isSelected }" @click="toggleSelection">
    <div v-if="drone.connected" className="card-header">
      <img className="drone-img" :src="droneConnectedIcon" alt="" />
    </div>
    <div v-else className="card-header">
      <img className="drone-img" :src="droneDisconnectedIcon" alt="" />
    </div>
    <h2>{{ drone.name }}</h2>
    <div className="drone-details">
      <p><strong>Location:</strong></p>
      <ul>
        <li>Latitude: {{ drone.latitude }}</li>
        <li>Longitude: {{ drone.longitude }}</li>
        <li>Altitude: {{ drone.altitude }}</li>
      </ul>
      <p><strong>Home Location:</strong></p>
      <ul>
        <li>Home Latitude: {{ drone.home_latitude }}</li>
        <li>Home Longitude: {{ drone.home_longitude }}</li>
        <li>Home Altitude: {{ drone.home_altitude }}</li>
      </ul>
      <p><strong>Velocity:</strong></p>
      <ul>
        <li>X: {{ drone.velocity_x }}</li>
        <li>Y: {{ drone.velocity_y }}</li>
        <li>Z: {{ drone.velocity_z }}</li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.drone-card {
  background: linear-gradient(0deg, rgba(40, 44, 52, 1) 0%, rgba(17, 0, 32, 0.5) 100%);
  padding: 20px;
  margin: 20px;
  border-radius: 10px;
  box-shadow: 0 7px 20px 5px #00000088;
  font-family: 'Montserrat', sans-serif;
  overflow: hidden;
  width: 450px;
  transition:
    background 0.3s,
    color 0.3s;
}

.card-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

.drone-img {
  max-width: 10vw; /* Increased size */
  margin-right: 20px;
}

.drone-card h2 {
  margin-bottom: 10px;
  font-size: 24px;
  color: #a89ec9;
}

.drone-details p {
  margin: 8px 0 4px;
  color: #a89ec9;
  font-size: 12px;
}

.drone-details ul {
  font-size: 12px;
  margin-top: 10px;
  color: #282c34;
  list-style-type: none;
  padding: 0;
  margin: 0;
  background: #dcdcdc;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.drone-details li {
  padding: 10px 15px; /* Reduced padding */
  border-bottom: 1px solid #ddd;
  transition:
    background 0.3s,
    color 0.3s;
}

.drone-details li:last-child {
  border-bottom: none;
}

.drone-details li:hover {
  background: #f0f0f0;
  color: #333;
}

.selected {
  background-color: #ccdfe7;
}

.drone-card:hover {
  background-color: #afadad;
}

.drone-card:not(.selected):hover {
  background-color: #afadad;
}

.drone-card:not(.selected) {
  background-color: linear-gradient(0deg, rgba(40, 44, 52, 1) 0%, rgba(17, 0, 32, 0.5) 100%);
}
</style>

<script setup>
import droneConnectedIcon from '@/assets/imageedit_3_2653131340.png'
import droneDisconnectedIcon from '@/assets/imageedit_6_6707006329.png'
import { toRefs, ref, watch } from 'vue'

const props = defineProps({
  drone: {
    type: Object,
    required: true,
    default: () => ({
      name: '',
      latitude: 0,
      longitude: 0,
      altitude: 0,
      home_latitude: 0,
      home_longitude: 0,
      home_altitude: 0,
      velocity_x: 0,
      velocity_y: 0,
      velocity_z: 0,
      connected: false
    })
  },
  selectedDroneId: {
    type: Number,
    default: null
  }
})

const emits = defineEmits(['select'])
const isSelected = ref(false)
const { drone, selectedDroneId } = toRefs(props)

// Watch for changes in selectedDroneId prop
watch(selectedDroneId, (newValue) => {
  isSelected.value = newValue === drone.value.id
})

const toggleSelection = () => {
  isSelected.value = selectedDroneId.value === drone.value.id
  if (isSelected.value) {
    emits('select', drone.value.id)
  } else {
    emits('select', null)
  }
}
</script>
