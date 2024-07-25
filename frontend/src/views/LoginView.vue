<template>
  <div id="login" class="login">
    <img src="../assets/1679312428346-removebg-preview.png" alt="" />
    <div class="container" id="container">
      <div class="form-container sign-up-container">
        <form method="post" @submit.prevent="onSignUp">
          <h1>Create Account</h1>
          <br />
          <input type="text" placeholder="Username" name="username" v-model="username" />
          <span v-if="errors.username" class="error-message">{{ errors.username }}</span>
          <input type="email" placeholder="Email" name="email" v-model="email" />
          <span v-if="errors.email" class="error-message">{{ errors.email }}</span>
          <input type="password" placeholder="Password" name="password" v-model="password" />
          <span v-if="errors.password" class="error-message">{{ errors.password }}</span>
          <br />
          <button type="submit">Sign Up</button>
        </form>
      </div>
      <div class="form-container sign-in-container">
        <form method="post" @submit.prevent="onLogin">
          <h1>Sign In</h1>
          <br />
          <input type="text" placeholder="Username" name="username" v-model="usernameLogin" />
          <span v-if="errorsLogin.username" class="error-message">{{ errorsLogin.username }}</span>
          <input type="email" placeholder="Email" name="email" v-model="emailLogin" />
          <span v-if="errorsLogin.email" class="error-message">{{ errorsLogin.email }}</span>
          <input type="password" placeholder="Password" name="password" v-model="passwordLogin" />
          <span v-if="errorsLogin.password" class="error-message">{{ errorsLogin.password }}</span>
          <div class="remember-me">
            <input type="checkbox" id="rememberMe" v-model="rememberMe" />
            <label for="rememberMe">Remember Me</label>
          </div>
          <button type="submit">Sign In</button>
          <router-link class="reset-password" :to="{ name: 'reset-password' }"
            >Forgot your password?</router-link
          >
        </form>
      </div>
      <div class="overlay-container">
        <div class="overlay">
          <div class="overlay-panel overlay-left">
            <h1>Welcome Back!</h1>
            <p>To start monitoring please login with your personal information.</p>
            <button class="ghost" id="signIn">Sign In</button>
          </div>
          <div class="overlay-panel overlay-right">
            <h1>Hello, Tracker!</h1>
            <p>Enter your personal details and start the drone monitoring.</p>
            <button class="ghost" id="signUp">Sign Up</button>
          </div>
        </div>
      </div>
      <ToastComponent ref="toastRef" />
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css?family=Montserrat:400,800');

* {
  box-sizing: border-box;
}

body {
  background: #ffffff;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  font-family: 'Montserrat', sans-serif;
  height: 100vh;
  width: 100vw;
  margin: -20px 0 50px;
}

#login {
  background: #000000;
  width: 100vw;
  height: 100vh;
  transition: 2s;
}

#login img {
  display: block;
  margin-left: auto;
  margin-right: auto;
}

#login:has(#container:hover) {
  background: #ffffff;
  transition: 2s;
}

.container:hover body {
  background-color: #000;
  transition: 1s;
}

h1 {
  font-weight: bold;
  margin: 0;
}

h2 {
  text-align: center;
}

p {
  font-size: 14px;
  font-weight: 100;
  line-height: 20px;
  letter-spacing: 0.5px;
  margin: 20px 0 30px;
}

span {
  font-size: 12px;
}

.forgot-password {
  color: #333;
  font-size: 14px;
  text-decoration: none;
  margin: 15px 0;
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

form {
  background-color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: 0 50px;
  height: 100%;
  text-align: center;
}

input {
  background-color: #eee;
  border: none;
  padding: 12px 15px;
  margin: 8px 0;
  width: 100%;
}

.container {
  background-color: #fff;
  border-radius: 10px;
  box-shadow:
    0 14px 28px rgba(0, 0, 0, 0.25),
    0 10px 10px rgba(0, 0, 0, 0.22);
  position: relative;
  overflow: hidden;
  width: 60%;
  max-width: 100%;
  min-height: 60%;
}

.form-container {
  position: absolute;
  top: 0;
  height: 100%;
  transition: all 0.6s ease-in-out;
}

.sign-in-container {
  left: 0;
  width: 50%;
  z-index: 2;
}

.container.right-panel-active .sign-in-container {
  transform: translateX(100%);
}

.sign-up-container {
  left: 0;
  width: 50%;
  opacity: 0;
  z-index: 1;
}

.container.right-panel-active .sign-up-container {
  transform: translateX(100%);
  opacity: 1;
  z-index: 5;
  animation: show 0.6s;
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

.container.right-panel-active .overlay-right {
  transform: translateX(20%);
}

.social-container {
  margin: 20px 0;
}

.social-container a {
  border: 1px solid #dddddd;
  border-radius: 50%;
  display: inline-flex;
  justify-content: center;
  align-items: center;
  margin: 0 5px;
  height: 40px;
  width: 40px;
}

footer {
  background-color: #222;
  color: #fff;
  font-size: 14px;
  bottom: 0;
  position: fixed;
  left: 0;
  right: 0;
  text-align: center;
  z-index: 999;
}

footer p {
  margin: 10px 0;
}

footer i {
  color: black;
}

footer a {
  color: #3c97bf;
  text-decoration: none;
}

.remember-me {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 10px;
  margin-bottom: 10px;
  margin-left: -2px;
  width: 25%;
}

.remember-me input[type='checkbox'] {
  margin-right: 10px;
}

.remember-me label {
  margin-left: 5px;
  white-space: nowrap;
}

.error-message {
  color: red;
}

.reset-password {
  color: #333;
  font-size: 14px;
  text-decoration: none;
  margin: 15px 0;
}

@media screen and (max-width: 768px) {
  h1 {
    font-size: 20px;
  }

  input {
    font-size: 10px;
  }

  .remember-me label {
    font-size: 10px;
  }

  p {
    font-size: 9px;
  }

  button {
    height: 10%;
    width: fit-content;
    padding: 5px 10px;
  }
}

@media screen and (max-width: 768px) {
  .reset-password {
    font-size: 10px;
  }
}
</style>

<script setup>
import ToastComponent from '../components/ToastComponent.vue'
import 'bootstrap/dist/js/bootstrap.bundle.js'
import 'bootstrap/dist/css/bootstrap.min.css'
import { onMounted, reactive, ref, watch } from 'vue'
import { useRouter } from 'vue-router'

let toastRef = ref(null)
let errorsLogin = reactive({})
let errors = reactive({})
let username = ref('')
let email = ref('')
let password = ref('')
let usernameLogin = ref('')
let emailLogin = ref('')
let passwordLogin = ref('')
let rememberMe = ref(false)
const router = useRouter()

// eslint-disable-next-line no-unused-vars
watch(usernameLogin, (newValue, _oldValue) => {
  if (!newValue) {
    errorsLogin.username = 'Username is required'
  } else {
    errorsLogin.username = ''
  }
})

// eslint-disable-next-line no-unused-vars
watch(emailLogin, (newValue, _oldValue) => {
  if (!newValue) {
    errorsLogin.email = 'Email is required'
  } else if (!newValue.includes('@')) {
    errorsLogin.email = 'A valid email is required'
  } else {
    errorsLogin.email = ''
  }
})

// eslint-disable-next-line no-unused-vars
watch(passwordLogin, (newValue, _oldValue) => {
  if (!newValue) {
    errorsLogin.password = 'Password is required'
  } else {
    errorsLogin.password = ''
  }
})

// eslint-disable-next-line no-unused-vars
watch(username, (newValue, _oldValue) => {
  if (!newValue) {
    errors.username = 'Username is required'
  } else {
    errors.username = ''
  }
})

// eslint-disable-next-line no-unused-vars
watch(email, (newValue, _oldValue) => {
  if (!newValue) {
    errors.email = 'Email is required'
  } else if (!newValue.includes('@')) {
    errors.email = 'A valid email is required'
  } else {
    errors.email = ''
  }
})

// eslint-disable-next-line no-unused-vars
watch(password, (newValue, _oldValue) => {
  if (!newValue) {
    errors.password = 'Password is required'
  } else if (newValue.length < 10) {
    errors.password = 'Password must be at least 10 characters long'
  } else if (!/[A-Z]/.test(newValue)) {
    errors.password = 'Password must contain at least one uppercase letter'
  } else if (!/[a-z]/.test(newValue)) {
    errors.password = 'Password must contain at least one lowercase letter'
  } else if (!/[0-9]/.test(newValue)) {
    errors.password = 'Password must contain at least one number'
  } else {
    errors.password = ''
  }
})

onMounted(() => {
  const container = document.getElementById('container')
  const signUpButton = document.getElementById('signUp')
  if (signUpButton) {
    signUpButton.addEventListener('click', () => {
      container.classList.add('right-panel-active')
    })
  }
  const signInButton = document.getElementById('signIn')
  if (signUpButton) {
    signInButton.addEventListener('click', () => {
      container.classList.remove('right-panel-active')
    })
  }
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

const validateLogin = () => {
  const errors = []
  if (!usernameLogin.value) {
    errors.push('Username is required.')
  }
  if (!emailLogin.value) {
    errors.push('Email is required.')
  } else if (!emailLogin.value.includes('@')) {
    errors.push('A valid email is required.')
  }
  if (!passwordLogin.value) {
    errors.push('Password is required.')
  }
  return errors
}

const onLogin = async () => {
  try {
    const errorsValidate = validateLogin()
    if (Object.keys(errorsValidate).length > 0) {
      toastRef.value.showMessage({
        messages: errorsValidate,
        type: 'error'
      })
      return
    }
    const csrfToken = await getCsrfToken()
    const formData = new FormData()
    formData.append('username', usernameLogin.value)
    formData.append('email', emailLogin.value)
    formData.append('password', passwordLogin.value)
    formData.append('remember_me', rememberMe.value)
    formData.append('action', 'login')
    const response = await fetch('http://localhost:5000/login-register', {
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
      messages: data.message,
      type: 'success'
    })

    toastRef.value.showMessage({
      messages: 'Redirected to main page after 4 seconds',
      type: 'success'
    })

    setTimeout(() => {
      router.push('/home')
    }, 4000)
  } catch (error) {
    console.error(error)
  }
}

const validateSignUp = () => {
  const errors = []
  if (!username.value) {
    errors.push('Username is required')
  }
  if (!email.value) {
    errors.push('Email is required')
  } else if (!email.value.includes('@')) {
    errors.push('A valid email is required')
  }
  if (!password.value) {
    errors.push('Password is required')
  } else {
    if (password.value.length < 10) {
      errors.push('Password must be at least 10 characters long')
    }
    if (!/[A-Z]/.test(password.value)) {
      errors.push('Password must contain at least one uppercase letter')
    }
    if (!/[a-z]/.test(password.value)) {
      errors.push('Password must contain at least one lowercase letter')
    }
    if (!/[0-9]/.test(password.value)) {
      errors.push('Password must contain at least one number')
    }
  }
  return errors
}

const onSignUp = async () => {
  try {
    const errorsValidate = validateSignUp()
    if (Object.keys(errorsValidate).length > 0) {
      toastRef.value.showMessage({
        messages: errorsValidate,
        type: 'error'
      })
      return
    }
    const csrfToken = await getCsrfToken()
    const formData = new FormData()
    formData.append('username', username.value)
    formData.append('email', email.value)
    formData.append('password', password.value)
    formData.append('action', 'sign-up')
    const response = await fetch('http://localhost:5000/login-register', {
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
      messages: data.message,
      type: 'success'
    })
  } catch (error) {
    console.error('Error:', error)
  }
}
</script>
