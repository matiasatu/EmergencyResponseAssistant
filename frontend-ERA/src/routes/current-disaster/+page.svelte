<script>
  import { onMount } from 'svelte';

  let summaryText = 'No summary available';
  let isLoading = true;
  let hasError = false;
  let errorMessage = '';

  async function fetchSummary() {
    isLoading = true;
    hasError = false;

    try {
      const response = await fetch('http://127.0.0.1:8000/summary/ggarzia');

      if (!response.ok) {
        throw new Error(`Error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      const parsed = JSON.parse(data)
      console.log(parsed.summary);

      summaryText = parsed.summary || 'No summary available';
    } catch (error) {
      console.error('Failed to fetch summary:', error);
      hasError = true;
      errorMessage = error.message || 'Failed to fetch summary';
    } finally {
      isLoading = false;
    }
  }

  function handleRefresh() {
    fetchSummary();
  }

  onMount(fetchSummary);
</script>

<main class="max-w-3xl mx-auto p-8 font-sans">
  <h1 class="text-2xl font-bold text-gray-800 mb-8 pb-2 border-b border-gray-200">Summary</h1>
  
  {#if isLoading}
    <div class="flex flex-col items-center my-8">
      <p class="text-gray-600 mb-4">Loading summary...</p>
      <div class="w-8 h-8 border-4 border-blue-200 border-t-blue-500 rounded-full animate-spin"></div>
    </div>
  {:else if hasError}
    <div class="bg-red-50 border-l-4 border-red-600 p-4 my-4">
      <p class="text-red-700">Failed to load summary: {errorMessage}</p>
      <button 
        on:click={handleRefresh}
        class="mt-2 bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded transition-colors duration-200"
      >
        Try Again
      </button>
    </div>
  {:else}
    <div class="bg-gray-50 p-6 rounded-lg shadow-sm mb-4">
      <p class="text-gray-800">{summaryText}</p>
      <button 
        on:click={handleRefresh}
        class="mt-4 bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded transition-colors duration-200"
      >
        Refresh
      </button>
    </div>
  {/if}
</main>
