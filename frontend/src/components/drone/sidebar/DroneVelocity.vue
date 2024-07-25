<template>
  <div class="sidebar-item">
    <h2 className="sidebar-title">Drone Velocity</h2>
    <h3 className="middle-title">Velocity X</h3>
    <DroneNumberInput
      label="Velocity X"
      minPlaceholder="Minimum"
      maxPlaceholder="Maximum"
      v-model:minValue="velocityXMin"
      v-model:maxValue="velocityXMax"
      inputIdMin="velocityXMinInput"
      inputIdMax="velocityXMaxInput"
      :min="-99999"
      :max="99999"
    />
    <h3 className="middle-title">Velocity Y</h3>
    <DroneNumberInput
      label="Velocity Y"
      minPlaceholder="Minimum"
      maxPlaceholder="Maximum"
      v-model:minValue="velocityYMin"
      v-model:maxValue="velocityYMax"
      inputIdMin="velocityYMinInput"
      inputIdMax="velocityYMaxInput"
      :min="-99999"
      :max="99999"
    />
    <h3 className="middle-title">Velocity Z</h3>
    <DroneNumberInput
      label="Velocity Z"
      minPlaceholder="Minimum"
      maxPlaceholder="Maximum"
      v-model:minValue="velocityZMin"
      v-model:maxValue="velocityZMax"
      inputIdMin="velocityZMinInput"
      inputIdMax="velocityZMaxInput"
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
const velocityXMin = ref(drone.velocityXMin)
const velocityYMin = ref(drone.velocityYMin)
const velocityZMin = ref(drone.velocityZMin)
const velocityXMax = ref(drone.velocityXMax)
const velocityYMax = ref(drone.velocityYMax)
const velocityZMax = ref(drone.velocityZMax)

watch(velocityXMin, (newValue) => {
  drone.changeVelocityXMin(newValue)
})

watch(velocityYMin, (newValue) => {
  drone.changeVelocityYMin(newValue)
})

watch(velocityZMin, (newValue) => {
  drone.changeVelocityZMin(newValue)
})

watch(velocityXMax, (newValue) => {
  drone.changeVelocityXMax(newValue)
})

watch(velocityYMax, (newValue) => {
  drone.changeVelocityYMax(newValue)
})

watch(velocityZMax, (newValue) => {
  drone.changeVelocityZMax(newValue)
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
