<template>
    <div>
      <h1>Friend Requests</h1>
      <table class="table">
        <thead>
          <tr>
            <th>From</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in friendRequests" :key="request.id">
            <td>{{ request.user__username }}</td>
            <td>
              <button @click="acceptRequest(request.id)">Accept</button>
              <button @click="rejectRequest(request.id)">Reject</button>
            </td>
          </tr>
        </tbody>
      </table>
  
      <h2>Current Friends</h2>
      <table class="table">
        <thead>
          <tr>
            <th>Friend</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="friend in currentFriends" :key="friend.friend__username">
            <td>{{ friend.friend__username }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script lang="ts">
      import { defineComponent } from "vue";
  
      export default defineComponent({
          data() {
              return {
                  title: "Friends Page",
              }
          }
      })
  </script>
  
  <style scoped>
  </style>
