<script lang="ts">
    import { onMount } from 'svelte';
    import * as login from "../../lib/login";

    let user = login.get_user();
    let summaries: string[] = [];
    let isLoading = true;


    async function fetchSummaries(username: string): Promise<string[]> {
        try {
        const res = await fetch(`http://10.60.25.182:8000/history/${username}`);

        if (!res.ok) {
            throw new Error(`Failed to fetch summaries: ${res.status} ${res.statusText}`);
        }

        const data = await res.json();
        return data.summaries;
        } catch (error) {
            console.error(error);
            return [];
        }
    }

    onMount(async () => {
        if (user) {
            summaries = await fetchSummaries(user)
            console.log(summaries)
            isLoading = false
        }
    });

    function formatText(text) {
    // Replace **text** with <strong>text</strong>
    const boldFormatted = text.replace(/\*\*(.*?)\*\*/g, '\n<strong>$1</strong>\n');
    
    // Replace \n with <br />
    return boldFormatted.replace(/\n/g, '<br />');
  }
</script>
  
<main class="max-w-3xl mx-auto p-8">
    {#if user}
        <h1 class="text-2xl font-bold text-gray-800 mb-8 pb-2 border-b border-gray-200">
            Disaster history
            <span class="brand-text">for {user}</span>
        </h1>
        {#if isLoading}
            <h1 class="text-xl font-bold text-gray-800">Loading...</h1>
        {/if}

        {#if summaries.length}
            <ul>
            {#each summaries as summary, i}
                <div class="bg-gray-50 p-6 rounded-lg shadow-sm mb-4">
                    <details>
                        <summary>Summary #{i + 1}</summary>
                        <p class="text-gray-800">{@html formatText(summary)}</p>
                    </details>
                </div>
            {/each}
            </ul>
        {:else}
            <p>No summaries available.</p>
        {/if}
    {:else}
        <h1 class="text-2xl font-bold text-gray-800 mb-8 pb-2 border-b border-gray-200">You are not signed in.</h1>
    {/if}
</main>
  