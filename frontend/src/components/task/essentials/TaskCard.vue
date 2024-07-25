<template>
  <div class="task-card" :class="{ selected: isSelected }" @click="toggleSelection">
    <div v-if="task.completed" class="card-header">
      <img class="task-img" :src="taskCompletedIcon" alt="" />
    </div>
    <div v-else-if="task.executing_drone_id" class="card-header">
      <img class="task-img" :src="taskExecutingIcon" alt="" />
    </div>
    <div v-else-if="task.assigned_drone_id" class="card-header">
      <img class="task-img" :src="taskOnHoldIcon" alt="" />
    </div>
    <div v-else class="card-header">
      <img class="task-img" :src="taskAvailableIcon" alt="" />
    </div>
    <h2>{{ task.title }}</h2>
    <div class="task-details">
      <p><strong>Location:</strong></p>
      <ul>
        <li>Latitude: {{ task.latitude }}</li>
        <li>Longitude: {{ task.longitude }}</li>
        <li>Altitude: {{ task.altitude }}</li>
      </ul>
      <p><strong>Date:</strong></p>
      <ul>
        <li>Creation Date: {{ formatDate(task.creation_date) }}</li>
        <li>Start Date: {{ formatDate(task.start_date) }}</li>
        <li>End Date: {{ formatDate(task.end_date) }}</li>
      </ul>
      <p><strong>Assigned Drone:</strong></p>
      <ul>
        <li>ID: {{ task.assigned_drone_id }}</li>
        <li>Name: {{ task.assigned_drone_name }}</li>
        <li>Status: {{ convertConnected(task.assigned_drone_connected) }}</li>
      </ul>
      <p><strong>Executing Drone:</strong></p>
      <ul>
        <li>ID: {{ task.executing_drone_id }}</li>
        <li>Name: {{ task.executing_drone_name }}</li>
        <li>Status: {{ convertConnected(task.executing_drone_connected) }}</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import dayjs from 'dayjs'
import taskCompletedIcon from '@/assets/task_completed-removebg-preview.png'
import taskExecutingIcon from '@/assets/task_executing-removebg-preview.png'
import taskAvailableIcon from '@/assets/task_not_completed-removebg-preview.png'
import taskOnHoldIcon from '@/assets/task_on_hold-removebg-preview.png'
import { toRefs, ref, watch } from 'vue'

const props = defineProps({
  task: {
    type: Object,
    required: true,
    default: () => ({
      title: '',
      latitude: 0,
      longitude: 0,
      altitude: 0,
      creation_date: null,
      start_date: null,
      end_date: null,
      assigned_drone_id: 0,
      assigned_drone_name: '',
      assigned_drone_connected: false,
      executing_drone_id: 0,
      executing_drone_name: '',
      executing_drone_connected: false,
      completed: false
    })
  },
  selectedTaskId: {
    type: Number,
    default: null
  }
})

const emits = defineEmits(['select'])
const isSelected = ref(false)
const { task, selectedTaskId } = toRefs(props)

watch(selectedTaskId, (newValue) => {
  isSelected.value = newValue === task.value.id
})

const toggleSelection = () => {
  isSelected.value = selectedTaskId.value === task.value.id
  if (isSelected.value) {
    emits('select', task.value.id)
  } else {
    emits('select', null)
  }
}

const formatDate = (date) => {
  return dayjs(date).format('MMMM D, YYYY h:mm A')
}

const convertConnected = (connected) => {
  switch (connected) {
    case null:
      return ''
    case true:
      return 'Connected'
    case false:
      return 'Not Connected'
    default:
      return ''
  }
}
</script>

<style scoped>
.task-card {
  background: linear-gradient(0deg, rgba(40, 44, 52, 1) 0%, rgba(17, 0, 32, 0.5) 100%);
  padding: 20px;
  margin: 20px;
  border-radius: 10px;
  box-shadow: 0 7px 20px 5px #00000088;
  font-family: 'Montserrat', sans-serif;
  width: 450px;
  overflow: hidden;
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

.task-img {
  max-width: 10vw;
  margin-right: 20px;
}

.task-card h2 {
  margin-bottom: 10px;
  font-size: 24px;
  color: #a89ec9;
}

.task-details p {
  margin: 8px 0 4px;
  color: #a89ec9;
  font-size: 12px;
}

.task-details ul {
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

.task-details li {
  padding: 10px 15px;
  border-bottom: 1px solid #ddd;
  transition:
    background 0.3s,
    color 0.3s;
}

.task-details li:last-child {
  border-bottom: none;
}

.task-details li:hover {
  background: #f0f0f0;
  color: #333;
}

.selected {
  background-color: #ccdfe7;
}

.task-card:hover {
  background-color: #afadad;
}

.task-card:not(.selected):hover {
  background-color: #afadad;
}

.task-card:not(.selected) {
  background-color: linear-gradient(0deg, rgba(40, 44, 52, 1) 0%, rgba(17, 0, 32, 0.5) 100%);
}
</style>
