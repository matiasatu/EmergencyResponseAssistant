<script>
  import * as login from "../lib/login"
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';
  import '../app.css';
  import { Navbar } from 'flowbite-svelte';
  
  let user = login.get_user()
  let isMenuOpen = false;

  $: currentPath = $page.url.pathname;
  $: hideFooter = currentPath === '/';

  function handleLogout() {
      login.logout()
  }

  function toggleMenu() {
      isMenuOpen = !isMenuOpen;
  }
</script>

<div class="flex flex-col min-h-screen">
    <header class="flex-none bg-white shadow">
      <Navbar class="h-20 flex items-center justify-between px-4">
        <button on:click={() => goto('/')} class="flex items-center space-x-2">
          <a href="/">
              <img src="/logo.png" class="h-16" alt="Logo" />
          </a>
        </button>

        <!-- Mobile hamburger button -->
        <button 
          class="md:hidden text-gray-600 focus:outline-none" 
          on:click={toggleMenu}
          aria-label="Toggle menu"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            {#if isMenuOpen}
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            {:else}
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
            {/if}
          </svg>
        </button>

        <!-- Desktop menu -->
        <div class="hidden md:flex space-x-6">
          <li class="list-none">
            <a href="/" class="text-xl text-gray-600 hover:text-orange-500">Home</a>
          </li>
          <li class="list-none">
            <a href="/current-disaster" class="text-xl text-gray-600 hover:text-orange-500">Ongoing Disasters</a>
          </li>
          <li class="list-none">
            <a href="/past-disasters" class="text-xl text-gray-600 hover:text-orange-500">Past Disasters</a>
          </li>
          <li class="list-none">
              <a href="/login" class="text-xl text-gray-600 hover:text-orange-500">Login</a>
          </li>
          <!-- <li class="list-none">
              <a href="#" on:click|preventDefault={handleLogout} class="text-xl text-gray-600 hover:text-orange-500">Logout</a>
          </li> -->
        </div>
      </Navbar>

      <!-- Mobile menu (collapsible) -->
      {#if isMenuOpen}
        <div class="md:hidden bg-white py-2 px-4 shadow-lg">
          <ul class="space-y-4">
            <li>
              <a href="/" class="block text-xl text-gray-600 hover:text-orange-500">Home</a>
            </li>
            <li>
              <a href="/current-disaster" class="block text-xl text-gray-600 hover:text-orange-500">Ongoing Disasters</a>
            </li>
            <li>
              <a href="/past-disasters" class="block text-xl text-gray-600 hover:text-orange-500">Past Disasters</a>
            </li>
            <li>
              <a href="/login" class="block text-xl text-gray-600 hover:text-orange-500">Login</a>
            </li>
            <!-- <li>
              <a href="#" on:click|preventDefault={handleLogout} class="block text-xl text-gray-600 hover:text-orange-500">Logout</a>
            </li> -->
          </ul>
        </div>
      {/if}
    </header>

  <div class="flex flex-col flex-1 w-full">
    <main class="flex-1 w-full h-full">
      <slot />
    </main>

    {#if !hideFooter}
      <footer class="flex-none bg-gray-200 py-6">
        <div class="container mx-auto text-center text-gray-600">
          © {new Date().getFullYear()} guardian.ai. All rights reserved.
        </div>
      </footer>
    {/if}
  </div>
</div>