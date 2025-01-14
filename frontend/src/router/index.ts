// Example of how to use Vue Router

import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/userStore'

// 1. Define route components.
// These can be imported from other files
import Login from '../pages/Login.vue';
import HobbiesPage from '../pages/HobbiesPage.vue';
import ProfilePage from '../pages/ProfilePage.vue';
import FriendsPage from '../pages/FriendsPage.vue';

let base = (import.meta.env.MODE == 'development') ? import.meta.env.BASE_URL : ''

// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
const router = createRouter({
    history: createWebHistory(base),
    routes: [
        { path: '/', redirect: {name: 'Profile'}},
        { path: '/login', name: 'Login', component: Login },
        { path: '/Hobbies', name: 'Hobbies Page', component: HobbiesPage, meta: { requiresAuth: true} },
        { path: '/profile', name: 'Profile', component: ProfilePage, meta: { requiresAuth: true}},
        { path: '/friends', name: 'Friends Page', component: FriendsPage, meta: { requiresAuth: true}}
    ]
})

router.beforeEach((to, _, next) => {
    const userStore = useUserStore()
    
    if (to.meta.requiresAuth && !userStore.isAuthenticated) {
        next({ name: 'Login' })
    } else {
        next()
    }
})

export default router
