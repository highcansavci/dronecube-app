<template>
  <div>
    <ModalView :isOpenProp="isOpenProp" @update:isOpenProp="$emit('update:isOpenProp', $event)">
      <div class="create-drone">
        <div class="modal-header">
          <h3>Register Drone</h3>
        </div>
        <form id="regForm" class="requires-validation" novalidate>
          <div class="form-group">
            <h4>Drone Name</h4>
            <input class="form-control" type="text" name="name" required v-model="drone.name" />
          </div>
          <div class="form-group">
            <h4>Drone Position</h4>
            <div class="col-md-12 drone-position">
              <div class="col-md-4 drone-position-item">
                <h5>Latitude</h5>
                <input
                  class="form-control"
                  type="number"
                  name="latitude"
                  required
                  v-model.number="drone.latitude"
                  @input="validateInput('latitude', -90, 90)"
                />
              </div>
              <div class="col-md-4 drone-position-item">
                <h5>Longitude</h5>
                <input
                  class="form-control"
                  type="number"
                  name="longitude"
                  required
                  v-model.number="drone.longitude"
                  @input="validateInput('longitude', -180, 180)"
                />
              </div>
              <div class="col-md-4 drone-position-item">
                <h5>Altitude</h5>
                <input
                  class="form-control"
                  type="number"
                  name="altitude"
                  required
                  v-model.number="drone.altitude"
                  @input="validateInput('altitude', -99999, 99999)"
                />
              </div>
            </div>
          </div>
          <div class="form-group">
            <h4>Drone Home Position</h4>
            <div class="col-md-12 drone-position">
              <div class="col-md-4 drone-position-item">
                <h5>Latitude</h5>
                <input
                  class="form-control"
                  type="number"
                  name="home_latitude"
                  required
                  v-model.number="drone.home_latitude"
                  @input="validateInput('home_latitude', -90, 90)"
                />
              </div>
              <div class="col-md-4 drone-position-item">
                <h5>Longitude</h5>
                <input
                  class="form-control"
                  type="number"
                  name="home_longitude"
                  required
                  v-model.number="drone.home_longitude"
                  @input="validateInput('home_longitude', -180, 180)"
                />
              </div>
              <div class="col-md-4 drone-position-item">
                <h5>Altitude</h5>
                <input
                  class="form-control"
                  type="number"
                  name="home_altitude"
                  required
                  v-model.number="drone.home_altitude"
                  @input="validateInput('home_altitude', -99999, 99999)"
                />
              </div>
            </div>
          </div>
          <div class="form-group">
            <h4>Drone Velocity</h4>
            <div class="col-md-12 drone-position">
              <div class="col-md-4 drone-position-item">
                <h5>X Velocity</h5>
                <input
                  class="form-control"
                  type="number"
                  name="velocity_x"
                  required
                  v-model.number="drone.velocity_x"
                  @input="validateInput('velocity_x', -99999, 99999)"
                />
              </div>
              <div class="col-md-4 drone-position-item">
                <h5>Y Velocity</h5>
                <input
                  class="form-control"
                  type="number"
                  name="velocity_y"
                  required
                  v-model.number="drone.velocity_y"
                  @input="validateInput('velocity_y', -99999, 99999)"
                />
              </div>
              <div class="col-md-4 drone-position-item">
                <h5>Z Velocity</h5>
                <input
                  class="form-control"
                  type="number"
                  name="velocity_z"
                  required
                  v-model.number="drone.velocity_z"
                  @input="validateInput('velocity_z', -99999, 99999)"
                />
              </div>
            </div>
          </div>
          <div class="form-group">
            <h4>Drone Connection Status</h4>
            <div class="radio-group">
              <label class="radio-label">
                <input
                  type="radio"
                  name="connected"
                  value="Connected"
                  v-model="drone.connected"
                  :checked="true"
                />
                <span class="custom-radio"></span>
                Connected
              </label>
              <label class="radio-label">
                <input
                  type="radio"
                  name="connected"
                  value="Not Connected"
                  v-model="drone.connected"
                />
                <span class="custom-radio"></span>
                Not Connected
              </label>
            </div>
          </div>
        </form>
        <div class="modal-footer form-button-mt3">
          <button
            type="submit"
            id="submit-task"
            class="btn btn-primary btn-submit"
            @click.stop.prevent="createDrone"
            :disabled="!isValidForm"
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
import { toRefs, defineProps, reactive, computed, ref } from 'vue'
import ModalView from '../ModalView.vue'
import ToastComponent from '../../components/ToastComponent.vue'
import 'bootstrap/dist/js/bootstrap.bundle.js'
import 'bootstrap/dist/css/bootstrap.min.css'
import { useSocketStore } from '../../stores/socketStore.js'
import Cookies from 'js-cookie'

const props = defineProps({
  isOpenProp: {
    type: Boolean
  }
})

const { isOpenProp } = toRefs(props)
const emit = defineEmits(['update:isOpenProp'])
const socketStore = useSocketStore()
const drone = reactive({
  name: '',
  latitude: null,
  longitude: null,
  altitude: null,
  home_latitude: null,
  home_longitude: null,
  home_altitude: null,
  velocity_x: null,
  velocity_y: null,
  velocity_z: null,
  connected: null
})
let toastRef = ref(null)

socketStore.initialize(Cookies.get('user_id'))

const closeModal = () => {
  emit('update:isOpenProp', false)
}

const validateInput = (field, min, max) => {
  if (drone[field] < min) drone[field] = min
  if (drone[field] > max) drone[field] = max
}

const isValidForm = computed(() => {
  return (
    drone.name !== '' &&
    drone.latitude !== null &&
    drone.longitude !== null &&
    drone.altitude !== null &&
    drone.home_latitude !== null &&
    drone.home_longitude !== null &&
    drone.home_altitude !== null &&
    drone.velocity_x !== null &&
    drone.velocity_y !== null &&
    drone.velocity_z !== null &&
    drone.connected !== null
  )
})

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

const createDrone = async () => {
  try {
    const csrfToken = await getCsrfToken()
    const formData = new FormData()
    formData.append('name', drone.name)
    formData.append('latitude', drone.latitude)
    formData.append('longitude', drone.longitude)
    formData.append('altitude', drone.altitude)
    formData.append('home_latitude', drone.home_latitude)
    formData.append('home_longitude', drone.home_longitude)
    formData.append('home_altitude', drone.home_altitude)
    formData.append('velocity_x', drone.velocity_x)
    formData.append('velocity_y', drone.velocity_y)
    formData.append('velocity_z', drone.velocity_z)
    formData.append('connected', drone.connected)
    const response = await fetch('http://localhost:5000/api/drones', {
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
      messages: `${data.name} is successfully created`,
      type: 'success'
    })
    socketStore.filterDrones()
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

.create-drone #regForm {
  background-color: #1c1c1e;
  margin: 0 auto;
  padding: 40px;
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  color: #ffffff;
  max-width: 600px;
}

.create-drone .modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #333;
  padding-bottom: 10px;
  margin-bottom: 20px;
}

.create-drone .modal-header h3 {
  font-size: 1.5rem; /* Reduced from 1.75rem */
  margin: 0;
}

.create-drone .btn-close {
  background: none;
  border: none;
  color: #fff;
  font-size: 1.25rem; /* Reduced from 1.5rem */
  cursor: pointer;
}

.create-drone h4 {
  font-size: 1rem; /* Reduced from 1.25rem */
  margin-bottom: 10px;
}

.create-drone h5 {
  font-size: 0.875rem; /* Reduced from 1rem */
  margin-bottom: 5px;
}

.create-drone input,
.create-drone select,
.create-drone .form-control {
  padding: 10px;
  font-size: 0.75rem; /* Reduced from 0.875rem */
  border: 1px solid #444;
  border-radius: 8px;
  background-color: #2c2c2e;
  color: #fff;
}

.create-drone input::placeholder {
  color: #aaa;
}

.create-drone .form-group {
  margin-bottom: 20px;
}

.create-drone .drone-position {
  display: flex;
  gap: 15px;
  margin-bottom: 25px;
}

.create-drone .drone-position-item {
  display: flex;
  flex-direction: column;
  width: 31%;
  gap: 5px;
}

.create-drone .modal-footer {
  display: flex;
  justify-content: space-between;
  padding: 20px 15px; /* Increased padding */
  border-top: 1px solid #333;
  margin-top: 20px; /* Margin top added */
}

.create-drone .btn-submit,
.create-drone .btn-secondary {
  background-color: #007bff;
  border-color: #007bff;
  font-size: 1rem; /* Increase font size */
  padding: 12px 24px; /* Increase padding */
  transition:
    background-color 0.3s,
    border-color 0.3s;
}

.create-drone .btn-submit:hover,
.create-drone .btn-secondary:hover {
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
