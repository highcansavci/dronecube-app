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

export const useTaskStore = defineStore('task', () => {
  const title = ref(loadState('task_title', ''))
  const latitudeMin = ref(loadState('task_latitudeMin', -90))
  const longitudeMin = ref(loadState('task_longitudeMin', -180))
  const altitudeMin = ref(loadState('task_altitudeMin', -99999))
  const latitudeMax = ref(loadState('task_latitudeMax', 90))
  const longitudeMax = ref(loadState('task_longitudeMax', 180))
  const altitudeMax = ref(loadState('task_altitudeMax', 99999))
  const startDateMin = ref(loadState('task_startDateMin', new Date(1900, 0, 1)))
  const endDateMin = ref(loadState('task_endDateMin', new Date(1900, 0, 1)))
  const startDateMax = ref(loadState('task_startDateMax', new Date(2100, 11, 31)))
  const endDateMax = ref(loadState('task_endDateMax', new Date(2100, 11, 31)))
  const completed = ref(loadState('task_completed', 'All'))

  // Watchers to save state to local storage
  watch(title, (newValue) => saveState('task_title', newValue))
  watch(latitudeMin, (newValue) => saveState('task_latitudeMin', newValue))
  watch(longitudeMin, (newValue) => saveState('task_longitudeMin', newValue))
  watch(altitudeMin, (newValue) => saveState('task_altitudeMin', newValue))
  watch(latitudeMax, (newValue) => saveState('task_latitudeMax', newValue))
  watch(longitudeMax, (newValue) => saveState('task_longitudeMax', newValue))
  watch(altitudeMax, (newValue) => saveState('task_altitudeMax', newValue))
  watch(startDateMin, (newValue) => saveState('task_startDateMin', newValue))
  watch(startDateMax, (newValue) => saveState('task_startDateMax', newValue))
  watch(endDateMin, (newValue) => saveState('task_endDateMin', newValue))
  watch(endDateMax, (newValue) => saveState('task_endDateMax', newValue))
  watch(completed, (newValue) => saveState('task_completed', newValue))

  // Change functions
  function changeTitle(newValue) {
    title.value = newValue
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

  function changeStartDateMin(newValue) {
    startDateMin.value = newValue
  }

  function changeStartDateMax(newValue) {
    startDateMax.value = newValue
  }

  function changeEndDateMin(newValue) {
    endDateMin.value = newValue
  }

  function changeEndDateMax(newValue) {
    endDateMax.value = newValue
  }

  function changeCompleted(newValue) {
    completed.value = newValue
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

  const validateTask = (task) => {
    const titleFilter = title.value === '' || task.title === title.value
    const positionFilter =
      latitudeMin.value <= task.latitude &&
      task.latitude <= latitudeMax.value &&
      longitudeMin.value <= task.longitude &&
      task.longitude <= longitudeMax.value &&
      altitudeMin.value <= task.altitude &&
      task.altitude <= altitudeMax.value
    const dateFilter =
      startDateMin.value <= task.start_date &&
      task.start_date <= startDateMax.value &&
      endDateMin.value <= task.end_date &&
      task.end_date <= endDateMax.value
    const completedFilter = completed.value === 'All' || convert(task.completed) === completed.value
    return titleFilter && positionFilter && dateFilter && completedFilter
  }

  const convert = (connected) => {
    return connected ? 'Completed' : 'Not Completed'
  }

  const filterTasks = async () => {
    try {
      const csrfToken = await getCsrfToken()
      const formData = new FormData()
      formData.append('title', title.value)
      formData.append('latitude_min', parseFloat(latitudeMin.value))
      formData.append('longitude_min', parseFloat(longitudeMin.value))
      formData.append('altitude_min', parseFloat(altitudeMin.value))
      formData.append('latitude_max', parseFloat(latitudeMax.value))
      formData.append('longitude_max', parseFloat(longitudeMax.value))
      formData.append('altitude_max', parseFloat(altitudeMax.value))
      formData.append('start_date_min', parseFloat(startDateMin.value))
      formData.append('end_date_min', parseFloat(endDateMin.value))
      formData.append('start_date_max', parseFloat(startDateMax.value))
      formData.append('end_date_max', parseFloat(endDateMax.value))
      formData.append('completed', completed.value)
      const response = await fetch('http://localhost:5000/api/tasks/filter', {
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

  const filterTasksSocket = () => {
    const filterData = {
      user_id: Cookies.get('user_id'),
      title: title.value,
      latitude_min: latitudeMin.value,
      longitude_min: longitudeMin.value,
      altitude_min: altitudeMin.value,
      latitude_max: latitudeMax.value,
      longitude_max: longitudeMax.value,
      altitude_max: altitudeMax.value,
      start_date_min: startDateMin.value,
      end_date_min: endDateMin.value,
      start_date_max: startDateMax.value,
      end_date_max: endDateMax.value,
      completed: completed.value
    }

    return filterData
  }

  const filterAssignedTasksSocket = (selectedDroneId) => {
    const filterData = {
      user_id: Cookies.get('user_id'),
      assigned_drone_id: selectedDroneId,
      title: title.value,
      latitude_min: latitudeMin.value,
      longitude_min: longitudeMin.value,
      altitude_min: altitudeMin.value,
      latitude_max: latitudeMax.value,
      longitude_max: longitudeMax.value,
      altitude_max: altitudeMax.value,
      start_date_min: startDateMin.value,
      end_date_min: endDateMin.value,
      start_date_max: startDateMax.value,
      end_date_max: endDateMax.value,
      completed: completed.value
    }

    return filterData
  }

  const filterExecutingTasksSocket = (selectedDroneId) => {
    const filterData = {
      user_id: Cookies.get('user_id'),
      executing_drone_id: selectedDroneId,
      title: title.value,
      latitude_min: latitudeMin.value,
      longitude_min: longitudeMin.value,
      altitude_min: altitudeMin.value,
      latitude_max: latitudeMax.value,
      longitude_max: longitudeMax.value,
      altitude_max: altitudeMax.value,
      start_date_min: startDateMin.value,
      end_date_min: endDateMin.value,
      start_date_max: startDateMax.value,
      end_date_max: endDateMax.value,
      completed: completed.value
    }

    return filterData
  }

  return {
    title,
    latitudeMin,
    longitudeMin,
    altitudeMin,
    latitudeMax,
    longitudeMax,
    altitudeMax,
    startDateMin,
    endDateMin,
    startDateMax,
    endDateMax,
    completed,
    changeTitle,
    changeLatitudeMin,
    changeLongitudeMin,
    changeAltitudeMin,
    changeLatitudeMax,
    changeLongitudeMax,
    changeAltitudeMax,
    changeStartDateMin,
    changeStartDateMax,
    changeEndDateMin,
    changeEndDateMax,
    changeCompleted,
    filterTasks,
    filterTasksSocket,
    filterAssignedTasksSocket,
    filterExecutingTasksSocket,
    validateTask
  }
})
