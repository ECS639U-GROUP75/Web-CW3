<template>
  <div class="h1 mb-4">
    {{ title }}
  </div>
  <div class="h4 mb-4">
    This is a page to see other users with similar hobbies.
  </div>

  <div class="mb-4" id="filter-container">
    <input id="min-age" type="number" v-model="minAge" placeholder="Min Age" />
    <input id="max-age" type="number" v-model="maxAge" placeholder="Max Age" />
    <button id="apply-filter" class="btn btn-primary" @click="fetchUsers">Apply Filter</button>
    <button class="btn btn-primary" @click="resetFilter">Reset Filter</button>
  </div>

  <div v-if="loading" class="text-center">
    Loading...
  </div>

  <div v-else-if="error" class="alert alert-danger">
    {{ error }}
  </div>

  <div v-else class="table-responsive">
    <table id="user-table" class="table table-striped">
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
            <template v-if="friendRequestStatus[user.username]">
              <span :style="{ color: friendRequestStatus[user.username].color }">
                {{ friendRequestStatus[user.username].message }}
              </span>
            </template>
            <template v-else>
              <button id="send-friend-request" class="btn btn-primary" @click="sendFriendRequest(user.username)">Send Friend Request</button>
            </template>
          </td>
        </tr>
      </tbody>
    </table>
    <div class="pagination align-items-center mt-4 justify-content-between">
      <button class="btn btn-primary" @click="changePage(currentPage - 1)" :disabled="!hasPrevious">Previous</button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button class="btn btn-primary" @click="changePage(currentPage + 1)" :disabled="!hasNext">Next</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import { getCsrfToken } from '../utils/auth.ts';

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
      friendRequestStatus: ref({}),
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

    async sendFriendRequest(username: string) {
      try {
        const csrfToken = await getCsrfToken();
        const response = await fetch(`/api/send-friend-request/${username}/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
          },
        });
        const data = await response.json();
        
      
        if (data.message === 'Friend request sent'){
          this.friendRequestStatus[username] = { message: 'Friend request sent', color: 'green' };
        } else if (data.message === 'Friendship already exists' ) {
          this.friendRequestStatus[username] = { message: 'Friendship already exists', color: 'blue' };
        } else if (data.message === 'Friend request already sent') {
          this.friendRequestStatus[username] = { message: 'Pending request already exists', color: 'orange' };
        } else if (data.message === 'Friend request was rejected previously') {
          this.friendRequestStatus[username] = { message: 'User previously rejected request', color: 'red' };
        } else if (data.message === 'User not found') {
          this.friendRequestStatus[username] = { message: 'User not found', color: 'red' };
        } else if (data.message === 'Unauthorized') {
          this.friendRequestStatus[username] = { message: 'Unauthorized', color: 'red' };
        } else {
          this.friendRequestStatus[username] = { message: 'Error sending friend request', color: 'red' };
        }
      } catch (error) {
        console.error('Error sending friend request:', error);
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
