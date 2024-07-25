<template>
  <section class="sidebar">
    <TaskTitle />
    <TaskPosition />
    <TaskDates />
    <TaskCompleted />
    <TaskButtons :selectedTaskId="selectedTaskId" />
  </section>
</template>

<script setup>
import { defineProps, toRefs, watch } from 'vue'
import TaskTitle from './TaskTitle.vue'
import TaskPosition from './TaskPosition.vue'
import TaskDates from './TaskDates.vue'
import TaskCompleted from './TaskCompleted.vue'
import TaskButtons from './TaskButtons.vue'
import { useTaskStore } from '@/stores/taskStore'
import { useSocketStore } from '@/stores/socketStore'
import Cookies from 'js-cookie'

const props = defineProps({
  selectedTaskId: {
    type: Number,
    default: null
  }
})

const { selectedTaskId } = toRefs(props)
const taskStore = useTaskStore()
const socketStore = useSocketStore()

socketStore.initialize(Cookies.get('user_id'))

watch(
  () => taskStore.title,
  () => {
    socketStore.filterTasks()
  }
)

watch(
  () => taskStore.latitudeMin,
  () => {
    socketStore.filterTasks()
  }
)

watch(
  () => taskStore.longitudeMin,
  () => {
    socketStore.filterTasks()
  }
)

watch(
  () => taskStore.altitudeMin,
  () => {
    socketStore.filterTasks()
  }
)

watch(
  () => taskStore.latitudeMax,
  () => {
    socketStore.filterTasks()
  }
)

watch(
  () => taskStore.longitudeMax,
  () => {
    socketStore.filterTasks()
  }
)

watch(
  () => taskStore.altitudeMax,
  () => {
    socketStore.filterTasks()
  }
)

watch(
  () => taskStore.startDateMin,
  () => {
    socketStore.filterTasks()
  }
)

watch(
  () => taskStore.startDateMax,
  () => {
    socketStore.filterTasks()
  }
)

watch(
  () => taskStore.endDateMin,
  () => {
    socketStore.filterTasks()
  }
)

watch(
  () => taskStore.endDateMax,
  () => {
    socketStore.filterTasks()
  }
)

watch(
  () => taskStore.completed,
  () => {
    socketStore.filterTasks()
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
