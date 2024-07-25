<template>
  <div class="sidebar-item">
    <h2 class="sidebar-title">Task Completion Status</h2>
    <TaskRadioInput
      v-model="selectedOption"
      name="completed"
      value="All"
      title="All"
      :checked="true"
    />
    <TaskRadioInput v-model="selectedOption" name="completed" value="Completed" title="Completed" />
    <TaskRadioInput
      v-model="selectedOption"
      name="completed"
      value="Not Completed"
      title="Not Completed"
    />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import TaskRadioInput from '../essentials/TaskRadioInput.vue'
import { useTaskStore } from '@/stores/taskStore'

const task = useTaskStore()
const selectedOption = ref(task.completed)

watch(selectedOption, (newValue) => {
  task.changeCompleted(newValue)
})
</script>

<style scoped>
.sidebar-item {
  margin: 10px 0;
  width: 90%;
}

.sidebar-title {
  font-size: 19px;
  font-weight: normal;
  color: #fff;
  margin-bottom: 20px;
}
</style>
