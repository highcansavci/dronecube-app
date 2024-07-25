<template>
  <div class="wrapper">
    <div className="card-container">
      <DroneCard
        class="drone-card"
        v-for="drone in paginatedData"
        :key="drone.id"
        :drone="drone"
        :selectedDroneId="selectedDroneId"
        @select="handleDroneSelect(drone.id)"
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

.drone-card {
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
import DroneCard from './drone/essentials/DroneCard.vue'
import PaginationComponent from './drone/essentials/PaginationComponent.vue'
import { useSocketStore } from '@/stores/socketStore'
import eventBus from '../stores/eventBus.js'

const pageSize = 12
const currentPage = ref(1)
const droneData = ref([])
const isVisible = ref(true)
const socketStore = useSocketStore()

watch(
  () => eventBus.drones,
  () => {
    filterData()
  },
  { deep: true }
)

const filterData = async () => {
  droneData.value = socketStore.drones
  isVisible.value = droneData.value.length > 0
  selectedDroneId.value = null
}

onMounted(filterData)

const totalPages = computed(() => Math.ceil(droneData.value.length / pageSize))

const paginatedData = computed(() => {
  const startIndex = (currentPage.value - 1) * pageSize
  const endIndex = startIndex + pageSize
  return droneData.value.slice(startIndex, endIndex)
})

const handlePageChange = (page) => {
  currentPage.value = page
}

const selectedDroneId = ref(null)
const emit = defineEmits(['select'])

const handleDroneSelect = (droneId) => {
  if (selectedDroneId.value === droneId) {
    selectedDroneId.value = null
  } else {
    selectedDroneId.value = droneId
  }
  emit('select', selectedDroneId.value)
}
</script>
