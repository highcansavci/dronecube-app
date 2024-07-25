<template>
  <div class="wrapper">
    <div className="card-container">
      <TaskCard
        class="task-card"
        v-for="task in paginatedData"
        :key="task.id"
        :task="task"
        :selectedTaskId="selectedTaskId"
        @select="handleTaskSelect(task.id)"
      />
    </div>
    <PaginationComponent
      v-show="isVisible"
      class="pagination"
      :totalPages="totalPages"
      :currentPage="currentPage"
      @pageChange="handlePageChange"
    />
  </div>
</template>

<style scoped>
.wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.card-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
  max-width: 100%; /* Adjust the width as needed */
}

.card-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
  max-width: 100%; /* Adjust the width as needed */
  margin-top: 3rem;
  margin-left: 17rem;
}

.task-card {
  flex: 1 1 calc(20% - 20px); /* 20% width minus the gap */
  max-width: calc(20% - 20px);
  box-sizing: border-box;
}

.pagination {
  display: flex;
  justify-content: center;
  gap: 10px;
  width: 100%;
  margin-top: 20px;
  margin-left: 17rem;
  background-color: transparent;
}
</style>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import TaskCard from './task/essentials/TaskCard.vue'
import PaginationComponent from './task/essentials/PaginationComponent.vue'
import { useSocketStore } from '@/stores/socketStore'
import eventBus from '../stores/eventBus.js'

const pageSize = 12
const currentPage = ref(1)
const taskData = ref([])
const isVisible = ref(true)
const socketStore = useSocketStore()

watch(
  () => eventBus.tasks,
  () => {
    filterData()
  },
  { deep: true }
)

const filterData = async () => {
  taskData.value = socketStore.tasks
  isVisible.value = taskData.value.length > 0
  selectedTaskId.value = null
}

onMounted(filterData)

const totalPages = computed(() => Math.ceil(taskData.value.length / pageSize))

const paginatedData = computed(() => {
  const startIndex = (currentPage.value - 1) * pageSize
  const endIndex = startIndex + pageSize
  return taskData.value.slice(startIndex, endIndex)
})

const handlePageChange = (page) => {
  currentPage.value = page
}

const selectedTaskId = ref(null)
const emit = defineEmits(['select'])

const handleTaskSelect = (taskId) => {
  if (selectedTaskId.value === taskId) {
    selectedTaskId.value = null
  } else {
    selectedTaskId.value = taskId
  }
  emit('select', selectedTaskId.value)
}
</script>
