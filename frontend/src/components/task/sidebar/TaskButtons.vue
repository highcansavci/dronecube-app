<template>
  <div class="task-button">
    <button
      type="button"
      id="createButton"
      class="btn btn-primary btn-info"
      @click="openCreateModal"
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
      <i class="fa fas fa-tasks"></i><b class="margin-b"></b
      ><span class="create-task">Update Task</span>
    </button>
    <button
      type="button"
      class="btn btn-primary btn-info btn-create"
      @click="deleteTask"
      :class="{ disabled: isDisabled === true }"
    >
      <i class="fa fas fa-tasks"></i><b class="margin-b"></b
      ><span class="create-task">Delete Task</span>
    </button>
    <div class="modals">
      <TaskCreateView :isOpenProp="isOpenCreate" @update:isOpenProp="isOpenCreate = $event">
      </TaskCreateView>
      <TaskUpdateView
        :selectedTaskId="selectedTaskId"
        :isOpenProp="isOpenUpdate"
        @update:isOpenProp="isOpenUpdate = $event"
      >
      </TaskUpdateView>
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
import TaskCreateView from '../TaskCreateView.vue'
import TaskUpdateView from '../TaskUpdateView.vue'
import ToastComponent from '../../ToastComponent.vue'
import { defineProps, toRefs, ref, watch } from 'vue'
import { useSocketStore } from '../../../stores/socketStore.js'

let toastRef = ref(null)
const socketStore = useSocketStore()

const props = defineProps({
  selectedTaskId: {
    type: Number,
    default: null
  }
})

const { selectedTaskId } = toRefs(props)
const isDisabled = ref(true)
watch(selectedTaskId, (newValue) => {
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

const deleteTask = async () => {
  try {
    const csrfToken = await getCsrfToken()
    const response = await fetch(`http://localhost:5000/api/tasks/${selectedTaskId.value}`, {
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
      messages: `Task ${selectedTaskId.value} is successfully deleted`,
      type: 'success'
    })
    socketStore.filterTasks()
  } catch (error) {
    console.error(error)
  }
}
</script>
