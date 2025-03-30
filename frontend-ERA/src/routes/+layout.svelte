<script>
    import { goto } from '$app/navigation';
    import { page } from '$app/stores';
    import '../app.css';
    import { Navbar } from 'flowbite-svelte';
  
    $: currentPath = $page.url.pathname;
    $: hideFooter = currentPath === '/';
  </script>
  
  <div class="flex flex-col min-h-screen">
      <header class="flex-none bg-white shadow">
        <Navbar class="h-20 flex items-center justify-between px-4">
          <button onclick={() => goto('/')} class="flex items-center space-x-2">
            <a href="/">
                <img src="/logo.png" class="h-16" alt="Logo" />
            </a>
            
          </button>
  
          <div class="flex space-x-6">
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
          </div>
        </Navbar>
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
  