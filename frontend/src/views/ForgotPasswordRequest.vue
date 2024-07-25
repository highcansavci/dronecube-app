<template>
  <div id="reset-password" class="reset-password">
    <img src="../assets/1679312428346-removebg-preview.png" alt="" />
    <div class="container" id="container">
      <div class="form-container request-password-container">
        <form method="post" @submit.prevent="onResetPassword">
          <h1>Reset Password Request</h1>
          <br />
          <input type="email" placeholder="Email" name="email" v-model="email" />
          <span v-if="errors.email" class="error-message">{{ errors.email }}</span>
          <button type="submit">Send Request</button>
        </form>
      </div>
      <div class="overlay-container">
        <div class="overlay">
          <div class="overlay-panel overlay-right">
            <p id="go-back">
              Go back
              <span
                ><router-link class="home" :to="{ name: 'login-register' }"
                  >home</router-link
                >
              </span>
            </p>
          </div>
        </div>
      </div>
      <ToastComponent ref="toastRef" />
    </div>
  </div>
</template>

<style scoped>
@import url("https://fonts.googleapis.com/css?family=Montserrat:400,800");

* {
  box-sizing: border-box;
}

body {
  background: #ffffff;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  font-family: "Montserrat", sans-serif;
  height: 100vh;
  width: 100vw;
  margin: -20px 0 50px;
}

#reset-password {
  background: #000000;
  width: 100vw;
  height: 100vh;
  transition: 2s;
}

#reset-password img {
  display: block;
  margin-left: auto;
  margin-right: auto;
}

#reset-password:has(#container:hover) {
  background: #ffffff;
  transition: 2s;
}

.container:hover body {
  background-color: #000;
  transition: 1s;
}

h1 {
  font-weight: bold;
  font-size: 30px;
  margin: 0;
}

h2 {
  text-align: center;
}

p {
  color: #ffffff;
  font-size: 40px;
  font-weight: 100;
  line-height: 20px;
  letter-spacing: 0.5px;
  margin: 20px 0 30px;
}

a {
  color: #000000;
  font-size: 14px;
  text-decoration: none;
  margin: 15px 0;
}

span {
  font-size: 12px;
}

form {
  background-color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 30px;
  flex-direction: column;
  padding: 0 50px 0 50px;
  height: 100%;
  text-align: center;
}

button {
  border-radius: 20px;
  border: 1px solid #000000;
  background-color: #000000;
  color: #ffffff;
  font-size: 12px;
  font-weight: bold;
  padding: 12px 45px;
  letter-spacing: 1px;
  text-transform: uppercase;
  transition: transform 80ms ease-in;
  cursor: pointer;
  margin-top: 20px;
}

button:active {
  transform: scale(0.95);
}

button:focus {
  outline: none;
}

button.ghost {
  background-color: transparent;
  border-color: #ffffff;
}

input {
  background-color: #eee;
  border: none;
  padding: 12px 15px;
  margin: 8px 0;
  width: 100%;
  min-width: 50%;
}

.container {
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22);
  position: relative;
  overflow: hidden;
  width: 60%;
  max-width: 100%;
  min-height: 60%;
}

.form-container {
  padding: 50px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 50%;
  transition: all 0.6s ease-in-out;
}

.request-password-container {
  left: 0;
  width: 50%;
  opacity: 1;
  z-index: 1;
}

@keyframes show {
  0%,
  49.99% {
    opacity: 0;
    z-index: 1;
  }

  50%,
  100% {
    opacity: 1;
    z-index: 5;
  }
}

.overlay-container {
  position: absolute;
  top: 0;
  left: 50%;
  width: 50%;
  height: 100%;
  overflow: hidden;
  transition: transform 0.6s ease-in-out;
  z-index: 100;
}

.container.right-panel-active .overlay-container {
  transform: translateX(-100%);
}

.overlay {
  background: #000000;
  background: -webkit-linear-gradient(to right, #000000, #777777);
  background: linear-gradient(to right, #000000, #777777);
  background-repeat: no-repeat;
  background-size: cover;
  background-position: 0 0;
  color: #ffffff;
  position: relative;
  left: -100%;
  height: 100%;
  width: 200%;
  transform: translateX(0);
  transition: transform 0.6s ease-in-out;
}

.container.right-panel-active .overlay {
  transform: translateX(50%);
}

.overlay-panel {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: 0 40px;
  text-align: center;
  top: 0;
  height: 100%;
  width: 50%;
  transform: translateX(0);
  transition: transform 0.6s ease-in-out;
}

.overlay-left {
  transform: translateX(-20%);
}

.container.right-panel-active .overlay-left {
  transform: translateX(0);
}

.overlay-right {
  right: 0;
  transform: translateX(0);
}

.error-message {
  color: red;
}

.home {
  font-size: 40px;
  font-weight: bold;
}

/* Media queries for responsiveness */

@media (max-width: 768px) {
  .container {
    flex-direction: column;
    width: 90%;
    min-height: auto;
  }

  form {
    padding: 10px;
  }

  .form-container,
  .overlay-container {
    width: 50%;
  }

  .form-container {
    padding: 20px;
  }

  .btn {
    width: 100%;
  }

  #go-back {
    font-size: 20px;
  }

  .home {
    font-size: 20px;
  }

  .overlay {
    padding: 20px;
  }
}

@media (max-width: 768px) {
  input {
    width: 100%;
  }

  .btn {
    font-size: 10px;
    padding: 10px 30px;
  }

  .overlay {
    font-size: 14px;
  }
}

@media screen and (min-width: 768px) and (max-width: 1150px) {
  .container {
    flex-direction: column;
    width: 90%;
    min-height: auto;
  }

  .form-container,
  .overlay-container {
    width: 50%;
  }

  .form-container {
    padding: 20px;
  }

  .btn {
    width: 100%;
  }

  #go-back {
    font-size: 30px;
  }

  .home {
    font-size: 30px;
  }

  .overlay {
    padding: 20px;
  }
}

@media screen and (min-width: 768px) and (max-width: 1150px) {
  input {
    padding: 10px;
    margin: 5px 0;
  }

  .btn {
    font-size: 10px;
    padding: 10px 30px;
  }

  .overlay {
    font-size: 14px;
  }
}
</style>

<script setup>
import ToastComponent from "../components/ToastComponent.vue";
import "bootstrap/dist/js/bootstrap.bundle.js";
import "bootstrap/dist/css/bootstrap.min.css";
import { reactive, ref, watch } from "vue";

let toastRef = ref(null);
let errors = reactive({});
let email = ref("");

// eslint-disable-next-line no-unused-vars
watch(email, (newValue, _oldValue) => {
  if (!newValue) {
    errors.email = "Email is required";
  } else if (!newValue.includes("@")) {
    errors.email = "A valid email is required";
  } else {
    errors.email = "";
  }
});

const getCsrfToken = async () => {
  try {
    const response = await fetch("http://localhost:5000/csrf-token", {
      credentials: "include",
    });
    if (!response.ok) {
      throw new Error("Failed to fetch CSRF token");
    }
    const data = await response.json();
    return data.csrf_token;
  } catch (error) {
    console.error("Error fetching CSRF token:", error);
    return null;
  }
};
const validateResetPassword = () => {
  const errors = [];
  if (!email.value) {
    errors.push("Email is required");
  } else if (!email.value.includes("@")) {
    errors.push("A valid email is required");
  }
  return errors;
};

const onResetPassword = async () => {
  try {
    const errorsValidate = validateResetPassword();
    if (Object.keys(errorsValidate).length > 0) {
      toastRef.value.showMessage({
        messages: errorsValidate,
        type: "error",
      });
      return;
    }
    const csrfToken = await getCsrfToken();
    const formData = new FormData();
    formData.append("email", email.value);
    const response = await fetch("http://localhost:5000/reset-password", {
      method: "POST",
      headers: {
        "Access-Control-Allow-Credentials": true,
        "X-CSRFToken": csrfToken,
      },
      credentials: "include",
      body: formData,
    });
    const data = await response.json();

    if (response.status >= 400) {
      toastRef.value.showMessage({
        messages: data.message,
        type: "error",
      });
      throw new Error("Network response was not ok");
    } else if (response.status >= 300) {
      toastRef.value.showMessage({
        messages: data.message,
        type: "warn",
      });
      return;
    }

    toastRef.value.showMessage({
      messages: data.message,
      type: "success",
    });
  } catch (error) {
    console.error(error);
  }
};
</script>
