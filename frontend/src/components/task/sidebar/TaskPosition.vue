<template>
  <div class="sidebar-item">
    <h2 className="sidebar-title">Task Position</h2>
    <h3 className="middle-title">Latitude</h3>
    <TaskNumberInput
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
    <TaskNumberInput
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
    <TaskNumberInput
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
import TaskNumberInput from '../essentials/TaskNumberInput.vue'
import { ref, watch } from 'vue'
import { useTaskStore } from '@/stores/taskStore'

const task = useTaskStore()
const latitudeMin = ref(task.latitudeMin)
const longitudeMin = ref(task.longitudeMin)
const altitudeMin = ref(task.altitudeMin)
const latitudeMax = ref(task.latitudeMax)
const longitudeMax = ref(task.longitudeMax)
const altitudeMax = ref(task.altitudeMax)

watch(latitudeMin, (newValue) => {
  task.changeLatitudeMin(newValue)
})

watch(longitudeMin, (newValue) => {
  task.changeLongitudeMin(newValue)
})

watch(altitudeMin, (newValue) => {
  task.changeAltitudeMin(newValue)
})

watch(latitudeMax, (newValue) => {
  task.changeLatitudeMax(newValue)
})

watch(longitudeMax, (newValue) => {
  task.changeLongitudeMax(newValue)
})

watch(altitudeMax, (newValue) => {
  task.changeAltitudeMax(newValue)
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
