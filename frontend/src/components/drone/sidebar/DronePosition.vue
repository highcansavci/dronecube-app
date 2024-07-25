<template>
  <div class="sidebar-item">
    <h2 className="sidebar-title">Drone Position</h2>
    <h3 className="middle-title">Latitude</h3>
    <DroneNumberInput
      label="Latitude"
      minPlaceholder="Minimum"
      maxPlaceholder="Maximum"
      v-model:minValue="latitudeMin"
      v-model:maxValue="latitudeMax"
      inputIdMin="latitudeMinInput"
      inputIdMax="latitudeMaxInput"
      :min="-90"
      :max="90"
    />
    <h3 className="middle-title">Longitude</h3>
    <DroneNumberInput
      label="Longitude"
      minPlaceholder="Minimum"
      maxPlaceholder="Maximum"
      v-model:minValue="longitudeMin"
      v-model:maxValue="longitudeMax"
      inputIdMin="longitudeMinInput"
      inputIdMax="longitudeMaxInput"
      :min="-180"
      :max="180"
    />
    <h3 className="middle-title">Altitude</h3>
    <DroneNumberInput
      label="Altitude"
      minPlaceholder="Minimum"
      maxPlaceholder="Maximum"
      v-model:minValue="altitudeMin"
      v-model:maxValue="altitudeMax"
      inputIdMin="altitudeMinInput"
      inputIdMax="altitudeMaxInput"
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
const latitudeMin = ref(drone.latitudeMin)
const longitudeMin = ref(drone.longitudeMin)
const altitudeMin = ref(drone.altitudeMin)
const latitudeMax = ref(drone.latitudeMax)
const longitudeMax = ref(drone.longitudeMax)
const altitudeMax = ref(drone.altitudeMax)

watch(latitudeMin, (newValue) => {
  drone.changeLatitudeMin(newValue)
})

watch(longitudeMin, (newValue) => {
  drone.changeLongitudeMin(newValue)
})

watch(altitudeMin, (newValue) => {
  drone.changeAltitudeMin(newValue)
})

watch(latitudeMax, (newValue) => {
  drone.changeLatitudeMax(newValue)
})

watch(longitudeMax, (newValue) => {
  drone.changeLongitudeMax(newValue)
})

watch(altitudeMax, (newValue) => {
  drone.changeAltitudeMax(newValue)
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
  column-gap: 6px;
}

@media (min-width: 768px) {
  .minmax {
    flex-direction: row;
    flex-wrap: wrap;
  }
}
</style>
