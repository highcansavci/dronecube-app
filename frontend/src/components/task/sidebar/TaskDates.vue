<template>
  <div class="sidebar-item">
    <h2 className="sidebar-title">Task Dates</h2>
    <h3 className="middle-title">Start Date</h3>
    <TaskDateInput
      label="Start Date"
      minPlaceholder="Minimum"
      maxPlaceholder="Maximum"
      v-model:minValue="startDateMin"
      v-model:maxValue="startDateMax"
      inputIdMin="startDateMinInput"
      inputIdMax="startDateMaxInput"
      :min="minDate"
      :max="maxDate"
    />
    <h3 className="middle-title">End Date</h3>
    <TaskDateInput
      label="End Date"
      minPlaceholder="Minimum"
      maxPlaceholder="Maximum"
      v-model:minValue="endDateMin"
      v-model:maxValue="endDateMax"
      inputIdMin="endDateMinInput"
      inputIdMax="endDateMaxInput"
      :min="minDate"
      :max="maxDate"
    />
  </div>
</template>

<script setup>
import TaskDateInput from '../essentials/TaskDateInput.vue'
import { ref, watch } from 'vue'
import { useTaskStore } from '@/stores/taskStore'

const task = useTaskStore()
const startDateMin = ref(new Date(task.startDateMin))
const endDateMin = ref(new Date(task.endDateMin))
const startDateMax = ref(new Date(task.startDateMax))
const endDateMax = ref(new Date(task.endDateMax))

const minDate = ref(new Date(1900, 0, 1))
const maxDate = ref(new Date(2100, 11, 31))

watch(startDateMin, (newValue) => {
  task.changeStartDateMin(new Date(newValue))
})

watch(endDateMin, (newValue) => {
  task.changeEndDateMin(new Date(newValue))
})

watch(startDateMax, (newValue) => {
  task.changeStartDateMax(new Date(newValue))
})

watch(endDateMax, (newValue) => {
  task.changeEndDateMax(new Date(newValue))
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
