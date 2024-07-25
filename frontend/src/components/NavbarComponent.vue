<template>
  <nav id="navbar" class="navbar navbar-dark bg-dark fixed-top">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">
        <img
          src="../assets/1679312428346-removebg-preview.png"
          id="logo"
          alt="DRONECUBE"
          width="30"
          height="24"
        />
        DRONECUBE
      </a>
      <div class="navbars">
        <ul class="navbar-nav tabs">
          <li class="nav-item">
            <router-link class="nav-link active" :to="{ name: 'home' }">HOME</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link active" :to="{ name: 'drones' }">DRONES</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link active" :to="{ name: 'tasks' }">TASKS</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link active" :to="{ name: 'login-register' }"
              >LOGOUT</router-link
            >
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<style scoped>
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

.navbar-dark {
  opacity: 0.2;
}

.navbar-dark:hover {
  opacity: 1;
}

.navbar-dark:hover + #osm-map {
  opacity: 0.2;
}

#logo {
  scale: 1.3;
  margin-right: 3px;
}

.navbars {
  width: 25%;
}

.tabs {
  flex-direction: row;
  justify-content: space-evenly;
}
</style>

<script setup>
import 'bootstrap/dist/js/bootstrap.bundle.js'
import 'bootstrap/dist/css/bootstrap.min.css'
</script>
