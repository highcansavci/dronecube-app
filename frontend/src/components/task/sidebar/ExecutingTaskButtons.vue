<template>
  <div class="task-button">
    <button
      type="button"
      id="addExecutingTaskButton"
      class="btn btn-primary btn-info"
      :class="{ disabled: isDisabled === true }"
      @click="addExecutingTask"
    >
      <i class="fa fas fa-tasks"></i><b class="margin-b"></b
      ><span class="execute-task">Add Executing Tasks</span>
    </button>
    <button
      type="button"
      id="removeExecutingTaskButton"
      class="btn btn-primary btn-info btn-create"
      :class="{ disabled: isDisabled === true }"
      @click="removeExecutingTask"
    >
      <i class="fa fas fa-tasks"></i><b class="margin-b"></b
      ><span class="execute-task">Remove Executing Tasks</span>
    </button>
    <button
      type="button"
      id="executeTaskButton"
      class="btn btn-primary btn-info btn-create"
      :class="{ disabled: isDisabled === true }"
      @click="executeTask"
    >
      <i class="fa fas fa-tasks"></i><b class="margin-b"></b
      ><span class="execute-task">Execute Tasks</span>
    </button>
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

.assign-task {
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
import ToastComponent from '../../ToastComponent.vue'
import { defineProps, toRefs, ref, watch } from 'vue'
import { useSocketStore } from '../../../stores/socketStore.js'

let toastRef = ref(null)
const socketStore = useSocketStore()

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
const isDisabled = ref(true)
watch(
  selectedTaskIds,
  (newValue) => {
    isDisabled.value = newValue.length > 0
  },
  { deep: true }
)

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

const addExecutingTask = async () => {
  try {
    const csrfToken = await getCsrfToken()
    const response = await fetch(
      `http://localhost:5000/api/drones/${selectedDroneId.value}/tasks/bulk_execute`,
      {
        headers: {
          'Access-Control-Allow-Credentials': true,
          'X-CSRFToken': csrfToken
        },
        credentials: 'include',
        body: { task_ids: selectedTaskIds.value },
        method: 'POST'
      }
    )
    const data = await response.json()

    if (response.status >= 400) {
      toastRef.value.showMessage({
        messages: data.message,
        type: 'error'
      })
      throw new Error('Network response was not ok')
    }

    toastRef.value.showMessage({
      messages: `Tasks will be executed via drone with drone id ${selectedDroneId.value}`,
      type: 'success'
    })
    socketStore.filterExecutingTasks(selectedDroneId.value)
  } catch (error) {
    console.error(error)
  }
}

const removeExecutingTask = async () => {
  try {
    const csrfToken = await getCsrfToken()
    const response = await fetch(
      `http://localhost:5000/api/drones/${selectedDroneId.value}/tasks/bulk_cancel_execution`,
      {
        headers: {
          'Access-Control-Allow-Credentials': true,
          'X-CSRFToken': csrfToken
        },
        credentials: 'include',
        body: { task_ids: selectedTaskIds.value },
        method: 'POST'
      }
    )
    const data = await response.json()

    if (response.status >= 400) {
      toastRef.value.showMessage({
        messages: data.message,
        type: 'error'
      })
      throw new Error('Network response was not ok')
    }

    toastRef.value.showMessage({
      messages: `Execution of tasks are cancelled in drone with drone id ${selectedDroneId.value}`,
      type: 'success'
    })
    socketStore.filterExecutingTasks(selectedDroneId.value)
  } catch (error) {
    console.error(error)
  }
}

const executeTask = async () => {
  try {
    if (selectedTaskIds.value.length == 0) {
      return
    }
    const csrfToken = await getCsrfToken()
    const response = await fetch(
      `http://localhost:5000/api/drones/${selectedDroneId.value}/tasks/${selectedTaskIds.value[0].id}/execute`,
      {
        headers: {
          'Access-Control-Allow-Credentials': true,
          'X-CSRFToken': csrfToken
        },
        credentials: 'include',
        method: 'GET'
      }
    )
    const data = await response.json()

    if (response.status >= 400) {
      toastRef.value.showMessage({
        messages: data.message,
        type: 'error'
      })
      throw new Error('Network response was not ok')
    }

    toastRef.value.showMessage({
      messages: `Execution of task with task id ${selectedTaskIds.value[0].id} has started via drone with drone id ${selectedDroneId.value}`,
      type: 'success'
    })
    socketStore.filterExecutingTasks(selectedDroneId.value)
  } catch (error) {
    console.error(error)
  }
}
</script>
