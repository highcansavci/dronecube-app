<template>
  <div id="change-password" class="change-password">
    <img src="../assets/1679312428346-removebg-preview.png" alt="" />
    <div class="container" id="container">
      <div class="form-container request-password-container">
        <form method="post" @submit.prevent="onResetPassword">
          <h1>Reset Password</h1>
          <br />
          <input
            type="password"
            placeholder="New Password"
            name="newPassword"
            v-model="newPassword"
          />
          <span v-if="errors.newPassword" class="error-message">{{
            errors.newPassword
          }}</span>
          <input
            type="password"
            placeholder="Repeat Password"
            name="repeatPassword"
            v-model="repeatPassword"
          />
          <span v-if="errors.repeatPassword" class="error-message">{{
            errors.repeatPassword
          }}</span>
          <button type="submit">Reset Password</button>
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

#change-password {
  background: #000000;
  width: 100vw;
  height: 100vh;
  transition: 2s;
}

#change-password img {
  display: block;
  margin-left: auto;
  margin-right: auto;
}

#change-password:has(#container:hover) {
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
import { reactive, ref, watch, defineProps } from "vue";
import { useRouter } from "vue-router";

let toastRef = ref(null);
let errors = reactive({});
let newPassword = ref("");
let repeatPassword = ref("");
const { token, userId } = defineProps({
  token: String,
  userId: String,
});
const router = useRouter();

// eslint-disable-next-line no-unused-vars
watch(newPassword, (newValue, _oldValue) => {
  if (!newValue) {
    errors.newPassword = "Password is required";
  } else if (newValue.length < 10) {
    errors.newPassword = "Password must be at least 10 characters long";
  } else if (!/[A-Z]/.test(newValue)) {
    errors.newPassword = "Password must contain at least one uppercase letter";
  } else if (!/[a-z]/.test(newValue)) {
    errors.newPassword = "Password must contain at least one lowercase letter";
  } else if (!/[0-9]/.test(newValue)) {
    errors.newPassword = "Password must contain at least one number";
  } else {
    errors.newPassword = "";
  }
});

// eslint-disable-next-line no-unused-vars
watch(repeatPassword, (newValue, _oldValue) => {
  if (!newValue) {
    errors.repeatPassword = "Password is required";
  } else if (newValue.length < 10) {
    errors.repeatPassword = "Password must be at least 10 characters long";
  } else if (!/[A-Z]/.test(newValue)) {
    errors.repeatPassword = "Password must contain at least one uppercase letter";
  } else if (!/[a-z]/.test(newValue)) {
    errors.repeatPassword = "Password must contain at least one lowercase letter";
  } else if (!/[0-9]/.test(newValue)) {
    errors.repeatPassword = "Password must contain at least one number";
  } else if (newValue !== newPassword.value) {
    errors.repeatPassword = "Passwords should match";
  } else {
    errors.repeatPassword = "";
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
  if (!newPassword.value) {
    errors.push("New password is required");
  } else {
    if (newPassword.value.length < 10) {
      errors.push("New password must be at least 10 characters long");
    }
    if (!/[A-Z]/.test(newPassword.value)) {
      errors.push("New password must contain at least one uppercase letter");
    }
    if (!/[a-z]/.test(newPassword.value)) {
      errors.push("New password must contain at least one lowercase letter");
    }
    if (!/[0-9]/.test(newPassword.value)) {
      errors.push("New password must contain at least one number");
    }
  }

  if (!repeatPassword.value) {
    errors.push("Repeat password is required");
  } else {
    if (repeatPassword.value.length < 10) {
      errors.push("Repeat password must be at least 10 characters long");
    }
    if (!/[A-Z]/.test(repeatPassword.value)) {
      errors.push("Repeat password must contain at least one uppercase letter");
    }
    if (!/[a-z]/.test(repeatPassword.value)) {
      errors.push("Repeat password must contain at least one lowercase letter");
    }
    if (!/[0-9]/.test(repeatPassword.value)) {
      errors.push("Repeat password must contain at least one number");
    }
    if (repeatPassword.value !== newPassword.value) {
      errors.push("Passwords should match");
    }
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
    formData.append("new_password", newPassword.value);
    formData.append("repeat_password", repeatPassword.value);
    const response = await fetch(
      `http://localhost:5000/reset-password/${token}/${userId}`,
      {
        method: "POST",
        headers: {
          "Access-Control-Allow-Credentials": true,
          "X-CSRFToken": csrfToken,
        },
        credentials: "include",
        body: formData,
      }
    );
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

    toastRef.value.showMessage({
      messages: "Redirected to login page after 4 seconds",
      type: "success",
    });

    setTimeout(() => {
      router.push("/login-register");
    }, 4000); // Redirect after 4 seconds
  } catch (error) {
    console.error(error);
  }
};
</script>
