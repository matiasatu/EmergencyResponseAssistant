<script>
  import { goto } from '$app/navigation';
  
  const signIn = () => goto('/login'); // Placeholder route
</script>

<main class="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-blue-500 to-indigo-600 text-white text-center px-6">
  <h1 class="text-4xl font-bold mb-4">Emergency Response Assistant</h1>
  <p class="text-lg max-w-2xl">
    Get real-time emergency alerts tailored to your personal needs. Using AI-powered analysis, we provide
    clear and actionable reports during critical situations.
  </p>
  <button on:click={signIn} class="mt-6 px-6 py-3 bg-white text-blue-600 rounded-lg shadow-lg text-lg font-semibold hover:bg-gray-100 transition">
    Sign In
  </button>
</main>
