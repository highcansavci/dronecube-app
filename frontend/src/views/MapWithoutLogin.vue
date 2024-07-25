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
            <router-link class="nav-link active" :to="{ name: 'login-register' }"
              >LOGIN / SIGN UP</router-link
            >
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <div id="osm-map"></div>
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

.leaflet-popup-content {
  background: #f9f9f9;
  padding: 10px;
  margin-top: 20px;
}

.leaflet-popup-content .fa {
  margin: 0 10px;
  font-size: 20px;
}

.leaflet-popup-content span {
  margin: 3px;
  font-size: 20px;
  font-weight: bold;
}

.leaflet-popup-content ul {
  font-size: 15px;
  margin-top: 20px;
  color: #777;
}

.leaflet-popup-content:hover {
  background: #000;
  color: #fff;
  border-radius: 50px 50px 50px 50px;
  transition: 1s;
}

.leaflet-popup-content:hover ul {
  color: #fff;
}

.leaflet-popup-content:hover .fa {
  margin-left: 10px;
}

.leaflet-popup-content .btn {
  padding: 10px 25px 10px 25px;
  margin-left: auto;
  margin-right: auto;
  border-radius: 30px;
  border: 2px solid #fff;
  background: #fff;
  color: #000;
}

.leaflet-popup-content .btn:focus {
  box-shadow: none !important;
}

.leaflet-popup-content .btn:hover {
  border: 2px solid #000 !important;
  background: #000000 !important;
  color: #ffffff;
  transition: 0.6s;
}

.leaflet-popup-content .btn:hover #task {
  color: white;
}

.leaflet-popup-content .btn .fa {
  margin-right: 10px;
}

.leaflet-popup-content #drone-img {
  width: 1vw;
  height: 1vh;
}

.leaflet-popup-content:hover #drone-img {
  filter: invert(100%);
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
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import "bootstrap/dist/js/bootstrap.bundle.js";
import "bootstrap/dist/css/bootstrap.min.css";
import { onMounted } from "vue";

onMounted(() => {
  L.CursorHandler = L.Handler.extend({
    addHooks: function () {
      this._popup = new L.Popup();
      this._map.on("mouseover", this._open, this);
      this._map.on("mousemove", this._update, this);
      this._map.on("mouseout", this._close, this);
    },

    removeHooks: function () {
      this._map.off("mouseover", this._open, this);
      this._map.off("mousemove", this._update, this);
      this._map.off("mouseout", this._close, this);
    },

    _open: function (e) {
      this._update(e);
      this._popup.openOn(this._map);
    },

    _close: function () {
      this._map.closePopup(this._popup);
    },

    _update: function (e) {
      this._popup
        .setLatLng(e.latlng)
        .setContent(
          "<b>Latitude: " +
            e.latlng.lat +
            "</b><br><b>Longitude: " +
            e.latlng.lng +
            "</b>"
        );
    },
  });

  L.Map.addInitHook("addHandler", "cursor", L.CursorHandler);

  // Get map container
  const element = document.getElementById("osm-map");
  // Create Leaflet map
  const map = L.map(element, { zoomControl: false, cursor: true });
  L.tileLayer("http://{s}.tile.osm.org/{z}/{x}/{y}.png", {
    attribution:
      '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 19,
  }).addTo(map);
  // Toggle zoom option on bottom right
  L.control
    .zoom({
      position: "bottomright",
    })
    .addTo(map);
  // Set map center to Turkey coords.
  const target = L.latLng("39", "35");
  // Set view and fly to map
  map.setView(target, 1);
  map.flyTo(target, 7);
});
</script>
