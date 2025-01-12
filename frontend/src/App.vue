<template>
    <main class="container pt-4">
        <nav>
            <router-link
                class="nav-link"
                :to="{name: 'Main Page'}"
            >
                Main Page
            </router-link>
            <router-link
                class="nav-link"
                :to="{name: 'Other Page'}"
            >
                Other Page
            </router-link>
            <router-link
                class="nav-link"
                :to="{name: 'Login'}"
            >
                Login
            </router-link>
            <router-link
                class="nav-link"
                :to="{name: 'Search Page'}"
            >
                Search
            </router-link>
        </nav>
        <RouterView class="flex-shrink-0" />
    </main>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { RouterView } from "vue-router";

export default defineComponent({
    components: { RouterView },
});
</script>

<style>
:root{
    --primary-color: #2D68FE;
    --primary-color-light: #2d68fe5d;
}


/* Additional custom styles */
.nav-link {
    text-decoration: none;
    padding: 0.5rem 1rem;
    margin-right: 1rem;
    font-weight: 900 !important;
}

.nav-link:hover {
    color: var(--primary-color) !important;
}

.router-link-active {
    color: var(--primary-color) !important;
    background-color: var(--primary-color-light) !important;
    font-weight: bold;
}

nav {
    margin-bottom: 2rem;
    padding: 1rem;
    background: #fff;
    border-radius: 4px;;
    display: flex;
    flex-direction: row;
    margin-right: 1rem;
}

.container {
    width: 100%;
    padding-right: 15px;
    padding-left: 15px;
    margin-right: auto;
    margin-left: auto;
    max-width: 1140px;
}

.pt-4 {
    padding-top: 1.5rem;
}
</style>
