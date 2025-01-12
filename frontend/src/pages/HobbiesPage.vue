<template>
  <div class="h1 mb-4">
    {{ title }}
  </div>
  <div class="h4 mb-4">
    This is a page to see other users with similar hobbies.
  </div>

  <div v-if="loading" class="text-center">
    Loading...
  </div>

  <div v-else-if="error" class="alert alert-danger">
    {{ error }}
  </div>

  <div v-else class="table-responsive">
    <table class="table table-striped">
      <thead>
        <tr>
          <th>Username</th>
          <th>Full Name</th>
          <th>Number of Hobbies</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.username">
          <td>{{ user.username }}</td>
          <td>{{ formatFullName(user) }}</td>
          <td>{{ user.hobby_count }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

interface User {
  username: string;
  first_name: string;
  last_name: string;
  hobby_count: number;
}


export default defineComponent({
  inheritAttrs: false,
  data() {
    return {
      title: "Hobbies Page",
      users: [] as User[],
      error: null as string | null,
      loading: true,
    };
  },

  methods: {
    formatFullName(user: User): string {
      if (user.first_name || user.last_name) {
        return `${user.first_name} ${user.last_name}`.trim();
      }
      return 'N/A';
    },

    async fetchUsers() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await fetch('/api/users-hobbies/');
        const contentType = response.headers.get("content-type");
        
        if (!response.ok) {
          throw new Error('Failed to fetch users');
        }

        if (!contentType || !contentType.includes("application/json")) {
          throw new Error('Invalid response format');
        }

        const data = await response.json();
        
        if (data.error) {
          throw new Error(data.error);
        }
        
        this.users = data.users;
      } catch (err) {
        this.error = err instanceof Error ? err.message : 'An error occurred';
      } finally {
        this.loading = false;
      }
    },
  },

  mounted() {
    this.fetchUsers();
  },
});
</script>

<style scoped>
.table {
  margin-top: 1rem;
}
</style>
