<template>
  <div class="task-button">
    <button
      type="button"
      id="createButton"
      class="btn btn-primary btn-info"
      @click="openCreateModal"
    >
      <img
        class="drone"
        src="../../../assets/black-silhouette-drone-against-white-background_1023514-2334-removebg-preview.png"
        alt=""
      />Create Drone
    </button>
    <button
      type="button"
      class="btn btn-primary btn-info btn-create"
      :class="{ disabled: isDisabled === true }"
      @click="openCreateTaskModal"
    >
      <i class="fa fas fa-tasks"></i><b class="margin-b"></b
      ><span class="create-task">Create Task</span>
    </button>
    <button
      type="button"
      id="updateButton"
      class="btn btn-primary btn-info btn-create"
      :class="{ disabled: isDisabled === true }"
      @click="openUpdateModal"
    >
      <img
        class="drone"
        src="../../../assets/black-silhouette-drone-against-white-background_1023514-2334-removebg-preview.png"
        alt=""
      />Update Drone
    </button>
    <button
      type="button"
      class="btn btn-primary btn-info btn-create"
      @click="deleteDrone"
      :class="{ disabled: isDisabled === true }"
    >
      <img
        class="drone"
        src="../../../assets/black-silhouette-drone-against-white-background_1023514-2334-removebg-preview.png"
        alt=""
      />Delete Drone
    </button>
    <button
      type="button"
      class="btn btn-primary btn-info btn-create"
      :class="{ disabled: isDisabled === true }"
      @click="seeAssignedTasks"
    >
      <i class="fa fas fa-tasks"></i><b class="margin-b"></b
      ><span class="create-task">Assigned Tasks</span>
    </button>
    <button
      type="button"
      class="btn btn-primary btn-info btn-create"
      :class="{ disabled: isDisabled === true }"
      @click="seeExecutingTasks"
    >
      <i class="fa fas fa-tasks"></i><b class="margin-b"></b
      ><span class="create-task">Executing Tasks</span>
    </button>
    <div class="modals">
      <DroneCreateView :isOpenProp="isOpenCreate" @update:isOpenProp="isOpenCreate = $event">
      </DroneCreateView>
      <DroneUpdateView
        :selectedDroneId="selectedDroneId"
        :isOpenProp="isOpenUpdate"
        @update:isOpenProp="isOpenUpdate = $event"
      >
      </DroneUpdateView>
      <DroneCreateTaskView
        :selectedDroneId="selectedDroneId"
        :isOpenProp="isOpenCreateTask"
        @update:isOpenProp="isOpenCreateTask = $event"
      ></DroneCreateTaskView>
    </div>
  </div>
  <div>
    <ToastComponent ref="toastRef" />
  </div>
</template>

<style scoped>
.task-button {
  margin-top: 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  column-gap: 10px;
  margin-bottom: 40px;
}

.task-button .fa {
  margin-right: 40px;
}

.task-button .btn {
  text-align: center;
  padding: 10px 25px 10px 25px;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 10px;
  border-radius: 30px;
  width: 100%;
  border: 2px solid #fff;
  background: #fff;
  color: #000;
  --bs-btn-disabled-color: white;
  --bs-btn-disabled-bg: darkgray;
  --bs-btn-disabled-border-color: darkgray;
}

.task-button .btn:focus {
  box-shadow: none !important;
}

.task-button .btn:hover {
  border: 2px solid #000 !important;
  background: #000000 !important;
  color: #fff;
  transition: 0.6s;
}

#drone-info {
  padding-right: 10.5vw;
}

.create-task {
  margin-right: 8px;
}

.drone {
  width: 2vw;
  height: 3vh;
  margin-right: 10px;
}

.btn:hover .drone {
  filter: invert(100%);
}

.margin-b {
  margin-right: 18px;
}

.modals {
  margin-top: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>

<script setup>
import 'bootstrap/dist/js/bootstrap.bundle.js'
import 'bootstrap/dist/css/bootstrap.min.css'
import DroneCreateView from '../DroneCreateView.vue'
import DroneUpdateView from '../DroneUpdateView.vue'
import DroneCreateTaskView from '../DroneCreateTaskView.vue'
import ToastComponent from '../../ToastComponent.vue'
import { defineProps, toRefs, ref, watch } from 'vue'
import { useSocketStore } from '../../../stores/socketStore.js'
import { useRoute } from 'vue-router'

let toastRef = ref(null)
const socketStore = useSocketStore()
const route = useRoute()

const props = defineProps({
  selectedDroneId: {
    type: Number,
    default: null
  }
})

const { selectedDroneId } = toRefs(props)
const isDisabled = ref(true)
watch(selectedDroneId, (newValue) => {
  isDisabled.value = newValue === null
})

const isOpenCreate = ref(false)
const openCreateModal = () => {
  isOpenCreate.value = true
}

const isOpenUpdate = ref(false)
const openUpdateModal = () => {
  isOpenUpdate.value = true
}

const isOpenCreateTask = ref(false)
const openCreateTaskModal = () => {
  isOpenCreateTask.value = true
}

const seeAssignedTasks = () => {
  route.push({ name: 'assigned-tasks', params: { selectedDroneId } })
}

const seeExecutingTasks = () => {
  route.push({ name: 'executing-tasks', params: { selectedDroneId } })
}

const getCsrfToken = async () => {
  try {
    const response = await fetch('http://localhost:5000/csrf-token', {
      credentials: 'include'
    })
    if (!response.ok) {
      throw new Error('Failed to fetch CSRF token')
    }
    const data = await response.json()
    return data.csrf_token
  } catch (error) {
    console.error('Error fetching CSRF token:', error)
    return null
  }
}

const deleteDrone = async () => {
  try {
    const csrfToken = await getCsrfToken()
    const response = await fetch(`http://localhost:5000/api/drones/${selectedDroneId.value}`, {
      headers: {
        'Access-Control-Allow-Credentials': true,
        'X-CSRFToken': csrfToken
      },
      credentials: 'include',
      method: 'DELETE'
    })
    const data = await response.json()

    if (response.status >= 400) {
      toastRef.value.showMessage({
        messages: data.message,
        type: 'error'
      })
      throw new Error('Network response was not ok')
    }

    toastRef.value.showMessage({
      messages: `Drone ${selectedDroneId.value} is successfully deleted`,
      type: 'success'
    })
    socketStore.filterDrones()
  } catch (error) {
    console.error(error)
  }
}
</script>
