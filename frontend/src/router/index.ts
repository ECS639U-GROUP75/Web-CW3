// Example of how to use Vue Router

import { createRouter, createWebHistory } from 'vue-router'

// 1. Define route components.
// These can be imported from other files
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
        { path: '/', name: 'Profile', component: ProfilePage},
        { path: '/Hobbies/', name: 'Hobbies Page', component: HobbiesPage },
        { path: '/friends/', name: 'Friends Page', component: FriendsPage}
    ]
})

export default router
