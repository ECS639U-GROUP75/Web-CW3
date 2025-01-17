<template>
    <div>
      <h1>Friend Requests</h1>
      <table class="table table-striped">
        <thead>
          <tr>
            <th>From</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in friendRequests" :key="request.id">
            <td>{{ request.user__username }}</td>
            <td class="d-flex mt-0">
              <button id="accept-friend-request" class="btn btn-primary" @click="acceptRequest(request.id)">Accept</button>
              <button class="btn btn-danger mx-2" @click="rejectRequest(request.id)">Reject</button>
            </td>
          </tr>
        </tbody>
      </table>
  
      <h2>Current Friends</h2>
      <table class="table table-striped">
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
      import { defineComponent, ref, onMounted } from "vue";
      import { getCsrfToken } from '../utils/auth.ts';
  
      interface FriendRequest {
          id: number;
          user__username: string;
      }
  
      interface CurrentFriend {
          friend__username: string;
      }
  
      export default defineComponent({
          setup() {
              const friendRequests = ref<FriendRequest[]>([]);
              const currentFriends = ref<CurrentFriend[]>([]);
  
              const fetchFriendRequests = async () => {
                  try {
                      const response = await fetch('/api/friend-requests/');
                      if (response.status === 401) {
                          window.location.href = '/login/';
                          return;
                      }
                      if (!response.ok) {
                          throw new Error('Failed to fetch friend requests');
                      }
                      const data = await response.json();
                      friendRequests.value = data.requests as FriendRequest[];
                  } catch (error) {
                      console.error('Error fetching friend requests:', error);
                  }
              };
  
              const fetchCurrentFriends = async () => {
                  try {
                      const response = await fetch('/api/current-friends/');
                      if (response.status === 401) {
                          window.location.href = '/login/';
                          return;
                      }
                      if (!response.ok) {
                          throw new Error('Failed to fetch current friends');
                      }
                      const data = await response.json();
                      currentFriends.value = data.friends as CurrentFriend[];
                  } catch (error) {
                      console.error('Error fetching current friends:', error);
                  }
              };
  
              const acceptRequest = async (requestId: number) => {
                  try {
                      const csrfToken = await getCsrfToken();
                      const response = await fetch(`/api/accept-friend-request/${requestId}/`, {
                          method: 'POST',
                          headers: {
                              'Content-Type': 'application/json',
                              'X-CSRFToken': csrfToken,
                          },
                      });
                      if (!response.ok) {
                          throw new Error('Failed to accept friend request');
                      }
                      await fetchFriendRequests();
                      await fetchCurrentFriends();
                  } catch (error) {
                      console.error('Error accepting friend request:', error);
                  }
              };
  
              const rejectRequest = async (requestId: number) => {
                  try {
                      const csrfToken = await getCsrfToken();
                      const response = await fetch(`/api/reject-friend-request/${requestId}/`, {
                          method: 'POST',
                          headers: {
                              'Content-Type': 'application/json',
                              'X-CSRFToken': csrfToken,
                          },
                      });
                      if (!response.ok) {
                          throw new Error('Failed to reject friend request');
                      }
                      await fetchFriendRequests();
                  } catch (error) {
                      console.error('Error rejecting friend request:', error);
                  }
              };
  
              onMounted(() => {
                  fetchFriendRequests();
                  fetchCurrentFriends();
              });
  
              return {
                  friendRequests,
                  currentFriends,
                  acceptRequest,
                  rejectRequest,
              };
          }
      })
  </script>
  
  <style scoped>
  </style>
