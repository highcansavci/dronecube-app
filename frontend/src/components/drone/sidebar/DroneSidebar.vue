<template>
  <section class="sidebar">
    <DroneName />
    <DronePosition />
    <DroneHomePosition />
    <DroneVelocity />
    <DroneConnected />
    <DroneButtons :selectedDroneId="selectedDroneId" />
  </section>
</template>

<script setup>
import { defineProps, toRefs, watch } from 'vue'
import DroneName from './DroneName.vue'
import DronePosition from './DronePosition.vue'
import DroneHomePosition from './DroneHomePosition.vue'
import DroneVelocity from './DroneVelocity.vue'
import DroneConnected from './DroneConnected.vue'
import DroneButtons from './DroneButtons.vue'
import { useDroneStore } from '@/stores/droneStore'
import { useSocketStore } from '@/stores/socketStore'
import Cookies from 'js-cookie'

const props = defineProps({
  selectedDroneId: {
    type: Number,
    default: null
  }
})

const { selectedDroneId } = toRefs(props)
const droneStore = useDroneStore()
const socketStore = useSocketStore()

socketStore.initialize(Cookies.get('user_id'))

watch(
  () => droneStore.name,
  () => {
    socketStore.filterDrones()
  }
)
watch(
  () => droneStore.latitudeMin,
  () => {
    socketStore.filterDrones()
  }
)
watch(
  () => droneStore.longitudeMin,
  () => {
    socketStore.filterDrones()
  }
)
watch(
  () => droneStore.altitudeMin,
  () => {
    socketStore.filterDrones()
  }
)
watch(
  () => droneStore.homeLatitudeMin,
  () => {
    socketStore.filterDrones()
  }
)
watch(
  () => droneStore.homeLongitudeMin,
  () => {
    socketStore.filterDrones()
  }
)
watch(
  () => droneStore.homeAltitudeMin,
  () => {
    socketStore.filterDrones()
  }
)
watch(
  () => droneStore.velocityXMin,
  () => {
    socketStore.filterDrones()
  }
)
watch(
  () => droneStore.velocityYMin,
  () => {
    socketStore.filterDrones()
  }
)
watch(
  () => droneStore.velocityZMin,
  () => {
    socketStore.filterDrones()
  }
)

watch(
  () => droneStore.latitudeMax,
  () => {
    socketStore.filterDrones()
  }
)
watch(
  () => droneStore.longitudeMax,
  () => {
    socketStore.filterDrones()
  }
)
watch(
  () => droneStore.altitudeMax,
  () => {
    socketStore.filterDrones()
  }
)
watch(
  () => droneStore.homeLatitudeMax,
  () => {
    socketStore.filterDrones()
  }
)
watch(
  () => droneStore.homeLongitudeMax,
  () => {
    socketStore.filterDrones()
  }
)
watch(
  () => droneStore.homeAltitudeMax,
  () => {
    socketStore.filterDrones()
  }
)
watch(
  () => droneStore.velocityXMax,
  () => {
    socketStore.filterDrones()
  }
)
watch(
  () => droneStore.velocityYMax,
  () => {
    socketStore.filterDrones()
  }
)
watch(
  () => droneStore.velocityZMax,
  () => {
    socketStore.filterDrones()
  }
)

watch(
  () => droneStore.connected,
  () => {
    socketStore.filterDrones()
  }
)
</script>

<style scoped>
.sidebar {
  width: 15%;
  position: fixed;
  height: 100%;
  border-right: 2px solid #e5e5e5;
  z-index: 3;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 3.4rem;
  overflow-y: auto;
  opacity: 0.2;
  background-color: rgba(34, 34, 34, 0.8);
}

.sidebar:hover {
  opacity: 1;
}
</style>
