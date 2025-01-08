<template>
    <main class="container pt-4">
        <nav>
            <router-link
                class="nav-link"
                :to="{name: 'Main Page'}"
            >
                Main Page
            </router-link>
            |
            <router-link
                class="nav-link"
                :to="{name: 'Other Page'}"
            >
                Other Page
            </router-link>
            |
            <router-link
                class="nav-link"
                :to="{name: 'Login'}"
            >
                Login
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
@import './styles/base.css';

/* Additional custom styles */
.nav-link {
    text-decoration: none;
    padding: 0.5rem 1rem;
}

.nav-link:hover {
    color: var(--link-hover-color);
}

.router-link-active {
    color: var(--link-selected-fg);
    font-weight: bold;
}

nav {
    margin-bottom: 2rem;
    padding: 1rem;
    background: var(--body-bg);
    border-radius: 4px;
    border: 1px solid var(--hairline-color);
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 1rem;
}
</style>
