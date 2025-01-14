<template>
  <div class="h1 mb-4">
    {{ title }}
  </div>
  <div class="h4 mb-4">
    This is a page to see other users with similar hobbies.
  </div>

  <div class="mb-4" id="filter-container">
    <input type="number" v-model="minAge" placeholder="Min Age" />
    <input type="number" v-model="maxAge" placeholder="Max Age" />
    <button class="btn btn-primary" @click="fetchUsers">Apply Filter</button>
    <button class="btn btn-primary" @click="resetFilter">Reset Filter</button>
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
          <th>Common Hobbies</th>
          <th>Age</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.username">
          <td>{{ user.username }}</td>
          <td>{{ formatFullName(user) }}</td>
          <td>{{ user.common_hobby_count }}</td>
          <td>{{ user.age }}</td>
          <td>
            <button class="btn btn-primary">Send Friend Request</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div class="pagination">
      <button class="btn btn-primary" @click="changePage(currentPage - 1)" :disabled="!hasPrevious">Previous</button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button class="btn btn-primary" @click="changePage(currentPage + 1)" :disabled="!hasNext">Next</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

interface User {
  username: string;
  first_name: string;
  last_name: string;
  common_hobby_count: number;
  age: number;
}

export default defineComponent({
  inheritAttrs: false,
  data() {
    return {
      title: "Hobbies Page",
      users: [] as User[],
      error: null as string | null,
      loading: true,
      minAge: null,
      maxAge: null,
      currentPage: 1,
      totalPages: 1,
      hasNext: false,
      hasPrevious: false,
    };
  },

  methods: {
    formatFullName(user: User): string {
      if (user.first_name || user.last_name) {
        return `${user.first_name} ${user.last_name}`.trim();
      }
      return 'N/A';
    },

    resetFilter() {
      this.minAge = null;
      this.maxAge = null;
      this.currentPage = 1;
      this.fetchUsers();
    },

    async fetchUsers() {
      this.loading = true;
      this.error = null;

      try {
        const minAgeValue = this.minAge !== null ? this.minAge : 0;
        const maxAgeValue = this.maxAge !== null ? this.maxAge : 100;

        const url = `/api/users-hobbies/?min_age=${minAgeValue}&max_age=${maxAgeValue}&page=${this.currentPage}`;
        console.log("Fetching users from:", url);

        const response = await fetch(url);
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
        this.hasNext = data.has_next;
        this.hasPrevious = data.has_previous;
        this.currentPage = data.current_page;
        this.totalPages = data.total_pages;
      } catch (err) {
        this.error = err instanceof Error ? err.message : 'An error occurred';
      } finally {
        this.loading = false;
      }
    },

    changePage(page: number) {
      if (page > 0 && page <= this.totalPages) {
        this.currentPage = page;
        this.fetchUsers();
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

#filter-container {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}
</style>
