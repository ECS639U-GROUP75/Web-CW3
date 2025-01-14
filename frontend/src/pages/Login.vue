<template>
  <div class="login">
    <div id="container">
      <div id="header">
        <h1>{{ isLogin ? 'Login' : 'Register' }}</h1>
      </div>
      <div id="content">
        <form @submit.prevent="isLogin ? handleLogin() : handleRegister()">
          <div class="form-row" v-if="!isLogin">
            <label for="email">Email:</label>
            <input 
              type="email" 
              id="email" 
              v-model="email" 
              required
            />
          </div>
          <div class="form-row">
            <label for="username">Username:</label>
            <input 
              type="text" 
              id="username" 
              v-model="username" 
              required
              autocomplete="username"
            />
          </div>
          <div class="form-row" v-if="!isLogin">
            <label for="first_name">First Name:</label>
            <input 
              type="text" 
              id="first_name" 
              v-model="first_name" 
              required
            />
          </div>
          <div class="form-row" v-if="!isLogin">
            <label for="last_name">Last Name:</label>
            <input 
              type="text" 
              id="last_name" 
              v-model="last_name" 
              required
            />
          </div>
          <div class="form-row" v-if="!isLogin">
            <label for="date_of_birth">Date of Birth:</label>
            <input 
              type="date" 
              id="date_of_birth" 
              v-model="date_of_birth" 
              required
            />
          </div>
          <div class="form-row">
            <label for="password">Password:</label>
            <input 
              type="password" 
              id="password" 
              v-model="password" 
              required
              autocomplete="current-password"
            />
          </div>
          <div class="submit-row">
            <input type="submit" :value="isLogin ? 'Log in' : 'Register'" />
          </div>
          <div v-if="error" class="errornote">
            {{ error }}
          </div>
          <div class="toggle-form">
            <a href="#" @click.prevent="toggleForm">
              {{ isLogin ? "Don't have an account? Register here" : 'Already have an account? Login here' }}
            </a>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '../stores/userStore'

export default defineComponent({
  name: 'LoginView',
  setup() {
    const router = useRouter();
    const isLogin = ref(true);
    const username = ref('');
    const password = ref('');
    const first_name = ref('');
    const last_name = ref('');
    const email = ref('');
    const date_of_birth = ref('');
    const error = ref('');
    const csrfToken = ref('');
    const userStore = useUserStore()

    const getCsrfToken = async () => {
      try {
        const response = await fetch('/api/login/', {
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
          },
        });
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        if (data.csrfToken) {
          csrfToken.value = data.csrfToken;
        } else {
          throw new Error('No CSRF token in response');
        }
      } catch (err) {
        console.error('Error fetching CSRF token:', err);
        error.value = 'Failed to initialize login form';
      }
    };

    const toggleForm = () => {
      isLogin.value = !isLogin.value;
      error.value = '';
      username.value = '';
      password.value = '';
      first_name.value = '';
      last_name.value = '';
      email.value = '';
      date_of_birth.value = '';
    };

    const handleLogin = async () => {
      try {
        const response = await fetch('/api/login/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken.value,
          },
          body: JSON.stringify({
            username: username.value,
            password: password.value,
          }),
          credentials: 'include',
        });

        const data = await response.json();

        if (response.ok) {
          userStore.setUser(data.user)
          router.push('/');
        } else {
          error.value = data.message || 'Login failed';
        }
      } catch (err) {
        error.value = 'An error occurred during login';
        console.error('Login error:', err);
      }
    };

    const handleRegister = async () => {
      try {
        const response = await fetch('api/register/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken.value,
          },
          body: JSON.stringify({
            username: username.value,
            password: password.value,
            first_name: first_name.value,
            last_name: last_name.value,
            email: email.value,
            date_of_birth: date_of_birth.value,
          }),
          credentials: 'include',
        });

        const data = await response.json();

        if (response.ok) {
          await handleLogin();
        } else {
          error.value = data.message || 'Registration failed';
        }
      } catch (err) {
        error.value = 'An error occurred during registration';
        console.error('Registration error:', err);
      }
    };

    onMounted(() => {
      getCsrfToken();
    });

    return {
      isLogin,
      username,
      password,
      first_name,
      last_name,
      email,
      date_of_birth,
      error,
      toggleForm,
      handleLogin,
      handleRegister,
    };
  },
});
</script>

<style>

.toggle-form {
  text-align: center;
  margin-top: 1rem;
}

.toggle-form a {
  color: var(--link-fg);
  text-decoration: none;
}

.toggle-form a:hover {
  color: var(--link-hover-color);
  text-decoration: underline;
}

.errornote {
  background: var(--error-bg);
  border: 1px solid var(--error-fg);
  border-radius: 4px;
  padding: 8px 12px;
  margin: 8px 0;
  color: var(--error-fg);
}

.form-row {
    margin-bottom: 1rem;
}

.form-row label {
    display: block;
    margin-bottom: 0.5rem;
}

.form-row input {
    display: block;
    width: 100%;
    padding: 0.375rem 0.75rem;
    font-size: 1rem;
    line-height: 1.5;
    color: #495057;
    background-color: #fff;
    background-clip: padding-box;
    border: 1px solid #ced4da;
    border-radius: 0.25rem;
    transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.form-row input:focus {
    color: #495057;
    background-color: #fff;
    border-color: #80bdff;
    outline: 0;
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

/* button styles */

.btn {
    display: inline-block;
    font-weight: 400;
    text-align: center;
    vertical-align: middle;
    user-select: none;
    padding: 0.375rem 0.75rem;
    font-size: 1rem;
    line-height: 1.5;
    border-radius: 0.25rem;
    transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out, border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.btn-primary {
    color: #fff;
    background-color: var(--primary-color);
    border: 1px solid var(--primary-color);
}

.btn-primary:hover {
    background-color: #0056b3;
    border-color: #0056b3;
}

.router-link-active {
    color: var(--primary-color);
    font-weight: bold;
}

.login {
    background: var(--darkened-bg);
    height: auto;
}

.login #header {
    height: auto;
    padding: 15px 16px;
    justify-content: center;
}

.login #header h1 {
    font-size: 1.125rem;
    margin: 0;
}

.login #header h1 a {
    color: var(--header-link-color);
}

.login #content {
    padding: 20px;
}

.login #container {
    background: var(--body-bg);
    border: 1px solid var(--hairline-color);
    border-radius: 4px;
    overflow: hidden;
    width: 28em;
    min-width: 300px;
    margin: 100px auto;
    height: auto;
}

.login .form-row label {
    display: block;
    line-height: 2em;
}

.login .submit-row {
    padding: 1em 0 0 0;
    margin: 0;
    text-align: center;
}
</style>
