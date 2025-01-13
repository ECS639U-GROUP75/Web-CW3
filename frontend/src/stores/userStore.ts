import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    isAuthenticated: false,
    username: '',
    firstName: '',
    lastName: ''
  }),
  
  actions: {
    setUser(userData: any) {
      this.isAuthenticated = true
      this.username = userData.username
      this.firstName = userData.first_name
      this.lastName = userData.last_name
    },
    
    clearUser() {
      this.isAuthenticated = false
      this.username = ''
      this.firstName = ''
      this.lastName = ''
    }
  }
}) 