<template>
  <div>
    <ModalView :isOpenProp="isOpenProp" @update:isOpenProp="$emit('update:isOpenProp', $event)">
      <div class="create-task">
        <div class="modal-header">
          <h3>Create Task</h3>
        </div>
        <form id="regForm" class="requires-validation" novalidate>
          <div class="form-group">
            <h4>Task Title</h4>
            <input class="form-control" type="text" name="name" required v-model="task.title" />
          </div>
          <div class="form-group">
            <h4>Task Position</h4>
            <div class="col-md-12 task-position">
              <div class="col-md-4 task-position-item">
                <h5>Latitude</h5>
                <input
                  class="form-control"
                  type="number"
                  name="latitude"
                  required
                  v-model.number="task.latitude"
                  @input="validateInput('latitude', -90, 90)"
                />
              </div>
              <div class="col-md-4 task-position-item">
                <h5>Longitude</h5>
                <input
                  class="form-control"
                  type="number"
                  name="longitude"
                  required
                  v-model.number="task.longitude"
                  @input="validateInput('longitude', -180, 180)"
                />
              </div>
              <div class="col-md-4 task-position-item">
                <h5>Altitude</h5>
                <input
                  class="form-control"
                  type="number"
                  name="altitude"
                  required
                  v-model.number="task.altitude"
                  @input="validateInput('altitude', -99999, 99999)"
                />
              </div>
            </div>
          </div>
          <div class="form-group">
            <h4>Task Interval</h4>
            <div class="col-md-12 task-position">
              <div class="col-md-6 task-position-item-md6">
                <h5>Start Date</h5>
                <input
                  class="form-control"
                  type="datetime-local"
                  name="start_date"
                  v-model="task.start_date"
                  required
                  @blur="validateDates"
                />
                <small v-if="startDateError" class="text-danger">{{ startDateError }}</small>
              </div>
              <div class="col-md-6 task-position-item-md6">
                <h5>End Date</h5>
                <input
                  class="form-control"
                  type="datetime-local"
                  name="end_date"
                  v-model="task.end_date"
                  required
                  @blur="validateDates"
                />
                <small v-if="endDateError" class="text-danger">{{ endDateError }}</small>
              </div>
            </div>
          </div>
          <div class="form-group">
            <h4>Task Completion Status</h4>
            <div class="radio-group">
              <label class="radio-label">
                <input type="radio" name="completed" value="Completed" v-model="task.completed" />
                <span class="custom-radio"></span>
                Completed
              </label>
              <label class="radio-label">
                <input
                  type="radio"
                  name="completed"
                  value="Not Completed"
                  v-model="task.completed"
                />
                <span class="custom-radio"></span>
                Not Completed
              </label>
            </div>
          </div>
        </form>
        <div class="modal-footer form-button-mt3">
          <button
            type="submit"
            id="submit-task"
            class="btn btn-primary btn-submit"
            @click.stop.prevent="createTask"
            :disabled="!isFormValid"
          >
            Create
          </button>
          <button id="close-task" type="button" class="btn btn-secondary" @click="closeModal">
            Close
          </button>
        </div>
      </div>
    </ModalView>
  </div>
  <div>
    <ToastComponent ref="toastRef" />
  </div>
</template>

<script setup>
import { toRefs, defineProps, reactive, ref, computed } from 'vue'
import ModalView from '../ModalView.vue'
import ToastComponent from '../../components/ToastComponent.vue'
import 'bootstrap/dist/js/bootstrap.bundle.js'
import 'bootstrap/dist/css/bootstrap.min.css'
import { useSocketStore } from '../../stores/socketStore.js'
import Cookies from 'js-cookie'

const props = defineProps({
  isOpenProp: {
    type: Boolean
  },
  selectedDroneId: {
    type: Number,
    default: null
  }
})

const { isOpenProp, selectedDroneId } = toRefs(props)
const emit = defineEmits(['update:isOpenProp'])
const socketStore = useSocketStore()
socketStore.initialize(Cookies.get('user_id'))

const task = reactive({
  title: '',
  latitude: null,
  longitude: null,
  altitude: null,
  start_date: null,
  end_date: null,
  completed: null
})
let toastRef = ref(null)
const startDateError = ref('')
const endDateError = ref('')

const closeModal = () => {
  emit('update:isOpenProp', false)
}

const validateDates = () => {
  const now = new Date().toISOString()
  startDateError.value = ''
  endDateError.value = ''

  if (task.start_date <= now) {
    startDateError.value = 'Start date must be in the future.'
  }

  if (task.end_date <= now) {
    endDateError.value = 'End date must be in the future.'
  }

  if (task.start_date && task.end_date && task.start_date >= task.end_date) {
    endDateError.value = 'End date must be after the start date.'
  }
}

const isFormValid = computed(() => {
  return (
    task.name !== '' &&
    task.latitude !== null &&
    task.longitude !== null &&
    task.altitude !== null &&
    !startDateError.value &&
    !endDateError.value &&
    task.start_date &&
    task.end_date &&
    task.completed !== null
  )
})

const validateInput = (field, min, max) => {
  if (task[field] < min) task[field] = min
  if (task[field] > max) task[field] = max
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

const createTask = async () => {
  try {
    const csrfToken = await getCsrfToken()
    const formData = new FormData()
    formData.append('assigned_drone_id', selectedDroneId.value)
    formData.append('title', task.title)
    formData.append('latitude', task.latitude)
    formData.append('longitude', task.longitude)
    formData.append('altitude', task.altitude)
    formData.append('start_date', task.start_date)
    formData.append('end_date', task.end_date)
    formData.append('completed', task.completed)
    const response = await fetch(`http://localhost:5000/api/tasks`, {
      method: 'POST',
      headers: {
        'Access-Control-Allow-Credentials': true,
        'X-CSRFToken': csrfToken
      },
      credentials: 'include',
      body: formData
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
      messages: `${data.title} task is successfully created on ${selectedDroneId.value}`,
      type: 'success'
    })
    socketStore.filterTasks()
  } catch (error) {
    console.error(error)
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

html,
body {
  box-sizing: border-box;
  padding: 0;
  margin: 0;
  background: linear-gradient(to right, #000000, gray);
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: fixed;
  font-family: 'Roboto', sans-serif;
  position: absolute;
  top: 0;
}

.create-task #regForm {
  background-color: #1c1c1e;
  margin: 0 auto;
  padding: 40px;
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  color: #ffffff;
  max-width: 600px;
}

.create-task .modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #333;
  padding-bottom: 10px;
  margin-bottom: 20px;
}

.create-task .modal-header h3 {
  font-size: 1.5rem; /* Reduced from 1.75rem */
  margin: 0;
}

.create-task .btn-close {
  background: none;
  border: none;
  color: #fff;
  font-size: 1.25rem; /* Reduced from 1.5rem */
  cursor: pointer;
}

.create-task h4 {
  font-size: 1rem; /* Reduced from 1.25rem */
  margin-bottom: 10px;
}

.create-task h5 {
  font-size: 0.875rem; /* Reduced from 1rem */
  margin-bottom: 5px;
}

.create-task input,
.create-task select,
.create-task .form-control {
  padding: 10px;
  font-size: 0.75rem; /* Reduced from 0.875rem */
  border: 1px solid #444;
  border-radius: 8px;
  background-color: #2c2c2e;
  color: #fff;
}

.create-task input::placeholder {
  color: #aaa;
}

.create-task .form-group {
  margin-bottom: 20px;
}

.create-task .task-position {
  display: flex;
  gap: 15px;
  margin-bottom: 25px;
}

.create-task .task-position-item {
  display: flex;
  flex-direction: column;
  width: 31%;
  gap: 5px;
}

.create-task .task-position-item-md6 {
  display: flex;
  flex-direction: column;
  width: 48%;
  gap: 8px;
}

.create-task .modal-footer {
  display: flex;
  justify-content: space-between;
  padding: 20px 15px; /* Increased padding */
  border-top: 1px solid #333;
  margin-top: 20px; /* Margin top added */
}

.create-task .btn-submit,
.create-task .btn-secondary {
  background-color: #007bff;
  border-color: #007bff;
  font-size: 1rem; /* Increase font size */
  padding: 12px 24px; /* Increase padding */
  transition:
    background-color 0.3s,
    border-color 0.3s;
}

.create-task .btn-submit:hover,
.create-task .btn-secondary:hover {
  background-color: #0056b3;
  border-color: #0056b3;
}

.radio-group {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1rem;
  cursor: pointer;
  position: relative;
  padding-left: 35px;
  user-select: none;
  transition: color 0.3s;
}

.radio-label input[type='radio'] {
  position: absolute;
  opacity: 0;
}

.radio-label .custom-radio {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background-color: transparent;
  border: 2px solid #007bff;
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  transition:
    border-color 0.3s,
    background-color 0.3s;
}

.radio-label input[type='radio']:checked + .custom-radio {
  background-color: #007bff;
}

.radio-label .custom-radio::after {
  content: '';
  width: 10px;
  height: 10px;
  background-color: white;
  border-radius: 50%;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  opacity: 0;
  transition: opacity 0.3s;
}

.radio-label input[type='radio']:checked + .custom-radio::after {
  opacity: 1;
}

.radio-label:hover {
  color: #007bff;
}
</style>
