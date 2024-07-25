<template>
  <div class="sidebar-item">
    <h2 className="sidebar-title">Drone Home Position</h2>
    <h3 className="middle-title">Latitude</h3>
    <DroneNumberInput
      label="Home Latitude"
      minPlaceholder="Minimum"
      maxPlaceholder="Maximum"
      v-model:minValue="homeLatitudeMin"
      v-model:maxValue="homeLatitudeMax"
      inputIdMin="homeLatitudeMinInput"
      inputIdMax="homeLatitudeMaxInput"
      :min="-90"
      :max="90"
    />
    <h3 className="middle-title">Longitude</h3>
    <DroneNumberInput
      label="Home Longitude"
      minPlaceholder="Minimum"
      maxPlaceholder="Maximum"
      v-model:minValue="homeLongitudeMin"
      v-model:maxValue="homeLongitudeMax"
      inputIdMin="homeLongitudeMinInput"
      inputIdMax="homeLongitudeMaxInput"
      :min="-180"
      :max="180"
    />
    <h3 className="middle-title">Altitude</h3>
    <DroneNumberInput
      label="Home Altitude"
      minPlaceholder="Minimum"
      maxPlaceholder="Maximum"
      v-model:minValue="homeAltitudeMin"
      v-model:maxValue="homeAltitudeMax"
      inputIdMin="homeAltitudeMinInput"
      inputIdMax="homeAltitudeMaxInput"
      :min="-99999"
      :max="99999"
    />
  </div>
</template>

<script setup>
import DroneNumberInput from '../essentials/DroneNumberInput.vue'
import { ref, watch } from 'vue'
import { useDroneStore } from '@/stores/droneStore'

const drone = useDroneStore()
const homeLatitudeMin = ref(drone.homeLatitudeMin)
const homeLongitudeMin = ref(drone.homeLongitudeMin)
const homeAltitudeMin = ref(drone.homeAltitudeMin)
const homeLatitudeMax = ref(drone.homeLatitudeMax)
const homeLongitudeMax = ref(drone.homeLongitudeMax)
const homeAltitudeMax = ref(drone.homeAltitudeMax)

watch(homeLatitudeMin, (newValue) => {
  drone.changeHomeLatitudeMin(newValue)
})

watch(homeLongitudeMin, (newValue) => {
  drone.changeHomeLongitudeMin(newValue)
})

watch(homeAltitudeMin, (newValue) => {
  drone.changeHomeAltitudeMin(newValue)
})

watch(homeLatitudeMax, (newValue) => {
  drone.changeHomeLatitudeMax(newValue)
})

watch(homeLongitudeMax, (newValue) => {
  drone.changeHomeLongitudeMax(newValue)
})

watch(homeAltitudeMax, (newValue) => {
  drone.changeHomeAltitudeMax(newValue)
})
</script>

<style scoped>
.sidebar-item {
  margin: 10px 0;
  width: 90%;
}

.sidebar-title {
  color: #fff;
  font-size: 22px;
  font-weight: normal;
  margin-bottom: 20px;
}

.middle-title {
  color: #fff;
  font-size: 19px;
  font-weight: normal;
  margin-bottom: 15px;
}

.minmax {
  display: flex;
  flex-direction: column;
  column-gap: 10px;
}

@media (min-width: 768px) {
  .minmax {
    flex-direction: row;
    flex-wrap: wrap;
  }
}
</style>
