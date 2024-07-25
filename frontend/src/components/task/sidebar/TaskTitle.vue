<template>
  <div class="sidebar-item">
    <h2 className="sidebar-title">Task Title</h2>
    <TaskTextInput label="Title" placeholder="Task Title" v-model="title" inputId="titleInput" />
  </div>
</template>

<script setup>
import TaskTextInput from '../essentials/TaskTextInput.vue'
import { ref, watch } from 'vue'
import { useTaskStore } from '@/stores/taskStore'

const task = useTaskStore()
const title = ref(task.title)

watch(title, (newValue) => {
  task.changeTitle(newValue)
})
</script>

<style scoped>
.sidebar-title {
  font-size: 20px;
  font-weight: normal;
  margin-bottom: 20px;
  color: #fff;
}

.sidebar-item {
  margin-top: 10px;
  margin-right: 0.7rem;
  width: 87%;
}
</style>
