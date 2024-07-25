import { ref, watch } from 'vue'
import { defineStore } from 'pinia'
import Cookies from 'js-cookie'

// Helper functions for local storage
function saveState(key, state) {
  localStorage.setItem(key, JSON.stringify(state))
}

function loadState(key, defaultValue) {
  const storedValue = localStorage.getItem(key)
  return storedValue ? JSON.parse(storedValue) : defaultValue
}

export const useDroneStore = defineStore('drone', () => {
  const name = ref(loadState('drone_name', ''))
  const latitudeMin = ref(loadState('drone_latitudeMin', -90))
  const longitudeMin = ref(loadState('drone_longitudeMin', -180))
  const altitudeMin = ref(loadState('drone_altitudeMin', -99999))
  const latitudeMax = ref(loadState('drone_latitudeMax', 90))
  const longitudeMax = ref(loadState('drone_longitudeMax', 180))
  const altitudeMax = ref(loadState('drone_altitudeMax', 99999))
  const homeLatitudeMin = ref(loadState('drone_homeLatitudeMin', -90))
  const homeLongitudeMin = ref(loadState('drone_homeLongitudeMin', -180))
  const homeAltitudeMin = ref(loadState('drone_homeAltitudeMin', -99999))
  const homeLatitudeMax = ref(loadState('drone_homeLatitudeMax', 90))
  const homeLongitudeMax = ref(loadState('drone_homeLongitudeMax', 180))
  const homeAltitudeMax = ref(loadState('drone_homeAltitudeMax', 99999))
  const velocityXMin = ref(loadState('drone_velocityXMin', -99999))
  const velocityYMin = ref(loadState('drone_velocityYMin', -99999))
  const velocityZMin = ref(loadState('drone_velocityZMin', -99999))
  const velocityXMax = ref(loadState('drone_velocityXMax', 99999))
  const velocityYMax = ref(loadState('drone_velocityYMax', 99999))
  const velocityZMax = ref(loadState('drone_velocityZMax', 99999))
  const connected = ref(loadState('drone_connected', 'All'))

  // Watchers to save state to local storage
  watch(name, (newValue) => saveState('drone_name', newValue))
  watch(latitudeMin, (newValue) => saveState('drone_latitudeMin', newValue))
  watch(longitudeMin, (newValue) => saveState('drone_longitudeMin', newValue))
  watch(altitudeMin, (newValue) => saveState('drone_altitudeMin', newValue))
  watch(latitudeMax, (newValue) => saveState('drone_latitudeMax', newValue))
  watch(longitudeMax, (newValue) => saveState('drone_longitudeMax', newValue))
  watch(altitudeMax, (newValue) => saveState('drone_altitudeMax', newValue))
  watch(homeLatitudeMin, (newValue) => saveState('drone_homeLatitudeMin', newValue))
  watch(homeLongitudeMin, (newValue) => saveState('drone_homeLongitudeMin', newValue))
  watch(homeAltitudeMin, (newValue) => saveState('drone_homeAltitudeMin', newValue))
  watch(homeLatitudeMax, (newValue) => saveState('drone_homeLatitudeMax', newValue))
  watch(homeLongitudeMax, (newValue) => saveState('drone_homeLongitudeMax', newValue))
  watch(homeAltitudeMax, (newValue) => saveState('drone_homeAltitudeMax', newValue))
  watch(velocityXMin, (newValue) => saveState('drone_velocityXMin', newValue))
  watch(velocityYMin, (newValue) => saveState('drone_velocityYMin', newValue))
  watch(velocityZMin, (newValue) => saveState('drone_velocityZMin', newValue))
  watch(velocityXMax, (newValue) => saveState('drone_velocityXMax', newValue))
  watch(velocityYMax, (newValue) => saveState('drone_velocityYMax', newValue))
  watch(velocityZMax, (newValue) => saveState('drone_velocityZMax', newValue))
  watch(connected, (newValue) => saveState('drone_connected', newValue))

  // Change functions
  function changeName(newValue) {
    name.value = newValue
  }

  function changeLatitudeMin(newValue) {
    latitudeMin.value = newValue
  }

  function changeLongitudeMin(newValue) {
    longitudeMin.value = newValue
  }

  function changeAltitudeMin(newValue) {
    altitudeMin.value = newValue
  }

  function changeLatitudeMax(newValue) {
    latitudeMax.value = newValue
  }

  function changeLongitudeMax(newValue) {
    longitudeMax.value = newValue
  }

  function changeAltitudeMax(newValue) {
    altitudeMax.value = newValue
  }

  function changeHomeLatitudeMin(newValue) {
    homeLatitudeMin.value = newValue
  }

  function changeHomeLongitudeMin(newValue) {
    homeLongitudeMin.value = newValue
  }

  function changeHomeAltitudeMin(newValue) {
    homeAltitudeMin.value = newValue
  }

  function changeHomeLatitudeMax(newValue) {
    homeLatitudeMax.value = newValue
  }

  function changeHomeLongitudeMax(newValue) {
    homeLongitudeMax.value = newValue
  }

  function changeHomeAltitudeMax(newValue) {
    homeAltitudeMax.value = newValue
  }

  function changeVelocityXMin(newValue) {
    velocityXMin.value = newValue
  }

  function changeVelocityYMin(newValue) {
    velocityYMin.value = newValue
  }

  function changeVelocityZMin(newValue) {
    velocityZMin.value = newValue
  }

  function changeVelocityXMax(newValue) {
    velocityXMax.value = newValue
  }

  function changeVelocityYMax(newValue) {
    velocityYMax.value = newValue
  }

  function changeVelocityZMax(newValue) {
    velocityZMax.value = newValue
  }

  function changeConnected(newValue) {
    connected.value = newValue
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

  const validateDrone = (drone) => {
    const nameFilter = name.value === '' || drone.name === name.value
    const positionFilter =
      latitudeMin.value <= drone.latitude &&
      drone.latitude <= latitudeMax.value &&
      longitudeMin.value <= drone.longitude &&
      drone.longitude <= longitudeMax.value &&
      altitudeMin.value <= drone.altitude &&
      drone.altitude <= altitudeMax.value
    const homePositionFilter =
      homeLatitudeMin.value <= drone.home_latitude &&
      drone.home_latitude <= homeLatitudeMax.value &&
      homeLongitudeMin.value <= drone.home_longitude &&
      drone.home_longitude <= homeLongitudeMax.value &&
      homeAltitudeMin.value <= drone.home_altitude &&
      drone.home_altitude <= homeAltitudeMax.value
    const velocityFilter =
      velocityXMin.value <= drone.velocity_x &&
      drone.velocity_x <= velocityXMax.value &&
      velocityYMin.value <= drone.velocity_y &&
      drone.velocity_y <= velocityYMax.value &&
      velocityZMin.value <= drone.velocity_z &&
      drone.velocity_z <= velocityZMax.value
    const connectedFilter =
      connected.value === 'All' || convert(drone.connected) === connected.value
    return nameFilter && positionFilter && homePositionFilter && velocityFilter && connectedFilter
  }

  const convert = (connected) => {
    return connected ? 'Connected' : 'Not Connected'
  }

  const filterDrones = async () => {
    try {
      const csrfToken = await getCsrfToken()
      const formData = new FormData()
      formData.append('name', name.value)
      formData.append('latitude_min', parseFloat(latitudeMin.value))
      formData.append('longitude_min', parseFloat(longitudeMin.value))
      formData.append('altitude_min', parseFloat(altitudeMin.value))
      formData.append('home_latitude_min', parseFloat(homeLatitudeMin.value))
      formData.append('home_longitude_min', parseFloat(homeLongitudeMin.value))
      formData.append('home_altitude_min', parseFloat(homeAltitudeMin.value))
      formData.append('velocity_x_min', parseFloat(velocityXMin.value))
      formData.append('velocity_y_min', parseFloat(velocityYMin.value))
      formData.append('velocity_z_min', parseFloat(velocityZMin.value))
      formData.append('latitude_max', parseFloat(latitudeMax.value))
      formData.append('longitude_max', parseFloat(longitudeMax.value))
      formData.append('altitude_max', parseFloat(altitudeMax.value))
      formData.append('home_latitude_max', parseFloat(homeLatitudeMax.value))
      formData.append('home_longitude_max', parseFloat(homeLongitudeMax.value))
      formData.append('home_altitude_max', parseFloat(homeAltitudeMax.value))
      formData.append('velocity_x_max', parseFloat(velocityXMax.value))
      formData.append('velocity_y_max', parseFloat(velocityYMax.value))
      formData.append('velocity_z_max', parseFloat(velocityZMax.value))
      formData.append('connected', connected.value)
      const response = await fetch('http://localhost:5000/api/drones/filter', {
        method: 'POST',
        headers: {
          'Access-Control-Allow-Credentials': true,
          'X-CSRFToken': csrfToken
        },
        credentials: 'include',
        body: formData
      })
      if (response.status >= 400) {
        throw new Error('Network response was not ok')
      }
    } catch (error) {
      console.log(error)
    }
  }

  const filterDronesSocket = () => {
    const filterData = {
      user_id: Cookies.get('user_id'),
      name: name.value,
      latitude_min: latitudeMin.value,
      longitude_min: longitudeMin.value,
      altitude_min: altitudeMin.value,
      home_latitude_min: homeLatitudeMin.value,
      home_longitude_min: homeLongitudeMin.value,
      home_altitude_min: homeAltitudeMin.value,
      velocity_x_min: velocityXMin.value,
      velocity_y_min: velocityYMin.value,
      velocity_z_min: velocityZMin.value,
      latitude_max: latitudeMax.value,
      longitude_max: longitudeMax.value,
      altitude_max: altitudeMax.value,
      home_latitude_max: homeLatitudeMax.value,
      home_longitude_max: homeLongitudeMax.value,
      home_altitude_max: homeAltitudeMax.value,
      velocity_x_max: velocityXMax.value,
      velocity_y_max: velocityYMax.value,
      velocity_z_max: velocityZMax.value,
      connected: connected.value
    }

    return filterData
  }

  return {
    name,
    latitudeMin,
    longitudeMin,
    altitudeMin,
    latitudeMax,
    longitudeMax,
    altitudeMax,
    homeLatitudeMin,
    homeLongitudeMin,
    homeAltitudeMin,
    homeLatitudeMax,
    homeLongitudeMax,
    homeAltitudeMax,
    velocityXMin,
    velocityYMin,
    velocityZMin,
    velocityXMax,
    velocityYMax,
    velocityZMax,
    connected,
    changeName,
    changeLatitudeMin,
    changeLongitudeMin,
    changeAltitudeMin,
    changeLatitudeMax,
    changeLongitudeMax,
    changeAltitudeMax,
    changeHomeLatitudeMin,
    changeHomeLongitudeMin,
    changeHomeAltitudeMin,
    changeHomeLatitudeMax,
    changeHomeLongitudeMax,
    changeHomeAltitudeMax,
    changeVelocityXMin,
    changeVelocityYMin,
    changeVelocityZMin,
    changeVelocityXMax,
    changeVelocityYMax,
    changeVelocityZMax,
    changeConnected,
    filterDrones,
    filterDronesSocket,
    validateDrone
  }
})
