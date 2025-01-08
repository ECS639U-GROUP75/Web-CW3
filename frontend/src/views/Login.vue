<template>
  <div class="login">
    <div id="container">
      <div id="header">
        <h1>{{ isLogin ? 'Login' : 'Register' }}</h1>
      </div>
      <div id="content">
        <form @submit.prevent="isLogin ? handleLogin : handleRegister">
          <div class="form-row" v-if="!isLogin">
            <label for="first_name">First Name:</label>
            <input 
              type="text" 
              id="first_name" 
              v-model="first_name" 
              v-if="!isLogin"
              required
            />
          </div>
          <div class="form-row" v-if="!isLogin">
            <label for="last_name">Last Name:</label>
            <input 
              type="text" 
              id="last_name" 
              v-model="last_name" 
              v-if="!isLogin"
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
import { defineComponent, ref } from 'vue';
import { useRouter } from 'vue-router';

export default defineComponent({
  name: 'LoginView',
  setup() {
    const router = useRouter();
    const isLogin = ref(true);
    const username = ref('');
    const password = ref('');
    const first_name = ref('');
    const last_name = ref('');
    const error = ref('');

    const toggleForm = () => {
      isLogin.value = !isLogin.value;
      error.value = '';
      username.value = '';
      password.value = '';
      first_name.value = '';
      last_name.value = '';
    };

    const handleLogin = async () => {
      try {
        const response = await fetch('/api/login/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: username.value,
            password: password.value,
          }),
        });

        if (response.ok) {
          router.push('/');
        } else {
          const data = await response.json();
          error.value = data.message || 'Login failed';
        }
      } catch (err) {
        error.value = 'An error occurred during login';
        console.error('Login error:', err);
      }
    };

    const handleRegister = async () => {
      try {
        const response = await fetch('/api/register/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: username.value,
            password: password.value,
            first_name: first_name.value,
            last_name: last_name.value,
          }),
        });

        if (response.ok) {
          // Automatically log in after successful registration
          await handleLogin();
        } else {
          const data = await response.json();
          error.value = data.message || 'Registration failed';
        }
      } catch (err) {
        error.value = 'An error occurred during registration';
        console.error('Registration error:', err);
      }
    };

    return {
      isLogin,
      username,
      password,
      first_name,
      last_name,
      error,
      toggleForm,
      handleLogin,
      handleRegister,
    };
  },
});
</script>

<style>
@import '../styles/login.css';

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
</style>
