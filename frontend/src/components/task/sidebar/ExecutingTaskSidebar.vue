<template>
  <section class="sidebar">
    <TaskTitle />
    <TaskPosition />
    <TaskDates />
    <TaskCompleted />
    <ExecutingTaskButtons :selectedDroneId="selectedDroneId" :selectedTaskIds="selectedTaskIds" />
  </section>
</template>

<script setup>
import { defineProps, toRefs, watch } from 'vue'
import TaskTitle from './TaskTitle.vue'
import TaskPosition from './TaskPosition.vue'
import TaskDates from './TaskDates.vue'
import TaskCompleted from './TaskCompleted.vue'
import ExecutingTaskButtons from './ExecutingTaskButtons.vue'
import { useTaskStore } from '@/stores/taskStore'
import { useSocketStore } from '@/stores/socketStore'
import Cookies from 'js-cookie'

const props = defineProps({
  selectedDroneId: {
    type: Number,
    default: null
  },
  selectedTaskIds: {
    type: Object,
    default: null
  }
})

const { selectedDroneId, selectedTaskIds } = toRefs(props)
const taskStore = useTaskStore()
const socketStore = useSocketStore()

socketStore.initialize(Cookies.get('user_id'))

watch(
  () => taskStore.title,
  () => {
    socketStore.filterExecutingTasks(selectedDroneId.value)
  }
)

watch(
  () => taskStore.latitudeMin,
  () => {
    socketStore.filterExecutingTasks(selectedDroneId.value)
  }
)

watch(
  () => taskStore.longitudeMin,
  () => {
    socketStore.filterExecutingTasks(selectedDroneId.value)
  }
)

watch(
  () => taskStore.altitudeMin,
  () => {
    socketStore.filterExecutingTasks(selectedDroneId.value)
  }
)

watch(
  () => taskStore.latitudeMax,
  () => {
    socketStore.filterExecutingTasks(selectedDroneId.value)
  }
)

watch(
  () => taskStore.longitudeMax,
  () => {
    socketStore.filterExecutingTasks(selectedDroneId.value)
  }
)

watch(
  () => taskStore.altitudeMax,
  () => {
    socketStore.filterExecutingTasks(selectedDroneId.value)
  }
)

watch(
  () => taskStore.startDateMin,
  () => {
    socketStore.filterExecutingTasks(selectedDroneId.value)
  }
)

watch(
  () => taskStore.startDateMax,
  () => {
    socketStore.filterExecutingTasks(selectedDroneId.value)
  }
)

watch(
  () => taskStore.endDateMin,
  () => {
    socketStore.filterExecutingTasks(selectedDroneId.value)
  }
)

watch(
  () => taskStore.endDateMax,
  () => {
    socketStore.filterExecutingTasks(selectedDroneId.value)
  }
)

watch(
  () => taskStore.completed,
  () => {
    socketStore.filterExecutingTasks(selectedDroneId.value)
  }
)
</script>

<style scoped>
.sidebar {
  width: 15%;
  position: fixed;
  height: 100%;
  border-right: 2px solid #e5e5e5;
  z-index: 3;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 3.4rem;
  overflow-y: auto;
  opacity: 0.2;
  background-color: rgba(34, 34, 34, 0.8);
}

.sidebar:hover {
  opacity: 1;
}
</style>
