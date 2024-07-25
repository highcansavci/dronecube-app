<template>
  <NavbarComponent />
  <DroneSidebar />
  <div id="osm-map"></div>
  <ToastComponent ref="toastRef" />
</template>

<style>
body {
  padding: 0;
  margin: 0;
}

html,
body {
  height: 100%;
}

#osm-map {
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
}

#osm-map {
  opacity: 1;
}

.leaflet-popup-content {
  background: #f9f9f9;
  padding: 20px;
  margin-top: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  font-family: 'Montserrat', sans-serif;
  overflow: hidden;
  transition:
    background 1s,
    color 1s;
}

.leaflet-popup-content .fa {
  margin-left: 20px;
  font-size: 15px;
  color: #888;
  transition: margin-left 0.3s;
}

.leaflet-popup-content span {
  margin-left: 10px;
  font-size: 15px;
  font-weight: bold;
  color: #555;
}

.leaflet-popup-content ul {
  font-size: 15px;
  margin-top: 20px;
  color: #777;
  list-style-type: none;
  padding: 0;
  margin: 0;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.leaflet-popup-content li {
  padding: 15px 20px;
  border-bottom: 1px solid #ddd;
  transition:
    background 0.3s,
    color 0.3s;
}

.leaflet-popup-content li:last-child {
  border-bottom: none;
}

.leaflet-popup-content li:hover {
  background: #f0f0f0;
  color: #333;
}

.leaflet-popup-content:hover ul {
  color: #fff;
}

.leaflet-popup-content:hover li {
  border-bottom-color: #fff;
}

.leaflet-popup-content:hover .fa {
  margin-left: 30px;
}

.leaflet-popup-content .btn {
  display: block;
  padding: 10px 25px;
  margin: 20px auto;
  border-radius: 30px;
  border: 2px solid #fff;
  background: #fff;
  color: #000;
  font-size: 15px;
  font-weight: bold;
  text-align: center;
  transition:
    border 0.6s,
    background 0.6s,
    color 0.6s;
}

.leaflet-popup-content .btn:focus {
  box-shadow: none !important;
}

.leaflet-popup-content .btn:hover {
  border: 2px solid #000 !important;
  background: #000000 !important;
  color: #ffffff;
}

.leaflet-popup-content .btn .fa {
  margin-right: 10px;
}

.leaflet-popup-content #drone-img {
  width: 50px;
  height: 50px;
  transition: filter 0.6s;
}

.leaflet-popup-content:hover #drone-img {
  filter: invert(100%);
}
</style>

<script setup>
import NavbarComponent from '../components/NavbarComponent.vue'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'
import { onMounted, ref, reactive, watch } from 'vue'
import ToastComponent from '../components/ToastComponent.vue'
import DroneSidebar from '../components/drone/sidebar/DroneSidebar.vue'
import 'bootstrap/dist/js/bootstrap.bundle.js'
import 'bootstrap/dist/css/bootstrap.min.css'
import connectedDrone from '@/assets/imageedit_3_2653131340.png'
import disconnectedDrone from '@/assets/imageedit_6_6707006329.png'
import { useSocketStore } from '../stores/socketStore.js'
import { useDroneStore } from '../stores/droneStore.js'
import Cookies from 'js-cookie'
import eventBus from '../stores/eventBus.js'

let map = reactive({})
let droneDisconnectedIcon = reactive({})
let droneConnectedIcon = reactive({})
let markerArray = reactive({
  markerArrays: [],
  initialized: false
})
let toastRef = ref(null)
const socketStore = useSocketStore()
const droneStore = useDroneStore()
const selectedDroneId = ref(null)
let featureGroup = ref(null)

const handleDroneSelect = (droneId) => {
  selectedDroneId.value = droneId
}

watch(
  () => eventBus.drones,
  (newValue) => {
    if (featureGroup.value !== null) {
      map.removeLayer(featureGroup.value)
      featureGroup.value.clearLayers()
    }
    markerArray.markerArrays = newValue.map((drone) => pinpointDrones(drone))
  },
  { deep: true }
)

watch(
  () => markerArray.markerArrays,
  (newValue) => {
    if (markerArray.initialized && newValue.length > 0) {
      featureGroup.value = L.featureGroup(newValue).addTo(map)
      if (!isNaN(featureGroup.value.getBounds().lat) && !isNaN(featureGroup.value.getBounds().lng))
        map.fitBounds(featureGroup.value.getBounds().pad(0.5))
    } else {
      let target = L.latLng('39', '35')
      map.setView(target, 1)
      map.flyTo(target, 7)
    }
  }
)

const fetchDrones = () => {
  try {
    toastRef.value.showMessage({
      messages: 'Drones are successfully fetched.',
      type: 'success'
    })
    const data = socketStore.drones
    if (data.length > 0) {
      markerArray.markerArrays = data.map((drone) => pinpointDrones(drone))
      featureGroup.value = L.featureGroup(markerArray.markerArrays).addTo(map)
      if (!isNaN(featureGroup.value.getBounds().lat) && !isNaN(featureGroup.value.getBounds().lng))
        map.flyToBounds(featureGroup.value.getBounds().pad(0.5))
    } else {
      let target = L.latLng('39', '35')
      map.setView(target, 1)
      map.flyTo(target, 7)
    }
  } catch (error) {
    console.error('Error:', error)
  }
}

const connected = (connected) => {
  return connected ? 'True' : 'False'
}

const pinpointDrones = (drone) => {
  let target = L.latLng(drone.latitude, drone.longitude)
  map.setView(target, 1)
  let myPopup = L.DomUtil.create('div', 'infoWindow')
  myPopup.innerHTML =
    '<div class="popup-box">' +
    '<i class="fa fas fa-rocket"></i>' +
    '<span>Drone Information</span>' +
    '<ul>' +
    '<li>ID: ' +
    drone.id +
    '</li>' +
    '<li>Name: ' +
    drone.name +
    '</li>' +
    '<li>Altitude: ' +
    drone.altitude +
    '</li>' +
    '<li>Connected: ' +
    connected(drone.connected) +
    '</li>' +
    '</ul>' +
    '</div>'
  const droneIcon = drone.connected ? droneConnectedIcon : droneDisconnectedIcon
  let DronecubeMarker = L.Marker.extend({
    options: {
      id: drone.id,
      name: drone.name,
      latitude: drone.latitude,
      longitude: drone.longitude,
      altitude: drone.altitude,
      connected: drone.connected
    }
  })
  const marker = new DronecubeMarker(target, {
    id: drone.id,
    name: drone.name,
    latitude: drone.latitude,
    longitude: drone.longitude,
    altitude: drone.altitude,
    connected: drone.connected
  })
    .setIcon(droneIcon)
    .on('click', onMarkerClick)
    .on('dblclick', connectionStatus)
    .bindPopup(myPopup)
  return marker
}

const connectionStatus = (event) => {
  try {
    map.closePopup()
    socketStore.socketClient.emit('update_connection_status', {
      id: event.target.options.id,
      user_id: Cookies.get('user_id')
    })
    event.target.options.connected = !event.target.options.connected
    toastRef.value.showMessage({
      messages: event.target.options.connected
        ? `The drone ${event.target.options.id} is connected.`
        : `The drone ${event.target.options.id} is disconnected.`,
      type: 'success'
    })
    const droneIcon = event.target.options.connected ? droneConnectedIcon : droneDisconnectedIcon
    event.target.setIcon(droneIcon)
    const droneData = socketStore.drones.find((drone) => drone.id === event.target.options.id)
    droneData.connected = event.target.options.connected
    if (!droneStore.validateDrone(droneData)) {
      socketStore.drones.pop(droneData)
      eventBus.drones.pop(droneData)
    }
  } catch (error) {
    console.error(error)
  }
}

const onMapClick = (event) => {
  try {
    const droneData = {
      user_id: Cookies.get('user_id'),
      name: 'Drone Cube',
      latitude: parseFloat(event.latlng.lat),
      longitude: parseFloat(event.latlng.lng),
      altitude: 35,
      home_latitude: 35,
      home_longitude: 35,
      home_altitude: 35,
      velocity_x: 35,
      velocity_y: 35,
      velocity_z: 35,
      connected: 'Connected'
    }

    if (!droneStore.validateDrone(droneData)) {
      toastRef.value.showMessage({
        messages: 'Drone cannot be created outside of current filters.',
        type: 'error'
      })
      return
    }

    socketStore.socketClient.emit('create_drone', droneData)
    toastRef.value.showMessage({
      messages: 'Drone is successfully created.',
      type: 'success'
    })
  } catch (error) {
    console.log(error)
  }
}

const onMarkerClick = (event) => {
  try {
    const droneId = event.target.options.id
    handleDroneSelect(droneId)
    socketStore.socketClient.emit('request_drone_data', {
      id: droneId,
      user_id: Cookies.get('user_id')
    })

    socketStore.socketClient.on('drone_data_response', (droneData) => {
      console.log('response')
      if (droneData.id === droneId) {
        const popupContent = `
          <div class="popup-box">
            <i class="fa fas fa-rocket"></i>
            <span>Drone Information</span>
            <ul>
              <li>ID: ${droneData.id}</li>
              <li>Name: ${droneData.name}</li>
              <li>Altitude: ${droneData.altitude}</li>
              <li>Connected: ${connected(droneData.connected)}</li>
            </ul>
          </div>
        `
        event.target.setPopupContent(popupContent)
        event.target.options.name = droneData.name
        event.target.options.latitude = droneData.latitude
        event.target.options.longitude = droneData.longitude
        event.target.options.altitude = droneData.altitude
        event.target.options.connected = droneData.connected
      }
    })
  } catch (error) {
    console.error(error)
  }
}

onMounted(() => {
  socketStore.initialize(Cookies.get('user_id'))
  L.CursorHandler = L.Handler.extend({
    addHooks: function () {
      this._popup = new L.Popup()
      this._map.on('mouseover', this._open, this)
      this._map.on('mousemove', this._update, this)
      this._map.on('mouseout', this._close, this)
      this._map.on('click', this._open, this)
      this._map.on('dblclick', this._close, this)
    },

    removeHooks: function () {
      this._map.off('mouseover', this._open, this)
      this._map.off('mousemove', this._update, this)
      this._map.off('mouseout', this._close, this)
      this._map.off('click', this._open, this)
      this._map.off('dblclick', this._close, this)
    },

    _open: function (e) {
      this._update(e)
      this._popup.openOn(this._map)
    },

    _close: function () {
      this._map.closePopup(this._popup)
    },

    _update: function (e) {
      this._popup
        .setLatLng(e.latlng)
        .setContent(
          '<b>Latitude: ' + e.latlng.lat + '</b><br><b>Longitude: ' + e.latlng.lng + '</b>'
        )
    }
  })

  L.Map.addInitHook('addHandler', 'cursor', L.CursorHandler)
  let element = document.getElementById('osm-map')
  map = L.map(element, {
    zoomControl: false,
    cursor: true,
    doubleClickZoom: false,
    enableHighAccuracy: true
  })
  L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 10000
  }).addTo(map)

  droneDisconnectedIcon = L.icon({
    iconUrl: disconnectedDrone,
    iconSize: [38, 38], // size of the icon
    shadowSize: [0, 0], // size of the shadow
    iconAnchor: [22, 94], // point of the icon which will correspond to marker's location
    shadowAnchor: [4, 62], // the same for the shadow
    popupAnchor: [-3, -76] // point from which the popup should open relative to the iconAnchor
  })

  droneConnectedIcon = L.icon({
    iconUrl: connectedDrone,
    iconSize: [38, 38], // size of the icon
    shadowSize: [0, 0], // size of the shadow
    iconAnchor: [22, 94], // point of the icon which will correspond to marker's location
    shadowAnchor: [4, 62], // the same for the shadow
    popupAnchor: [-3, -76] // point from which the popup should open relative to the iconAnchor
  })
  L.control
    .zoom({
      position: 'bottomright'
    })
    .addTo(map)
  let bounds = [
    [droneStore.latitudeMin, droneStore.latitudeMax],
    [droneStore.longitudeMin, droneStore.longitudeMax]
  ]
  L.rectangle(bounds, { color: 'red', weight: 1, fillOpacity: 0.2 }).addTo(map)
  fetchDrones()
  map.cursor.enable()
  map.on('dblclick', onMapClick)
  markerArray.initialized = true
  socketStore.socketClient.on('drone_created', () => {
    socketStore.filterDrones()
  })
})
</script>
