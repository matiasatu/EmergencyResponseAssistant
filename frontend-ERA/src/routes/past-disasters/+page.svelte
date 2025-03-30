<script lang="ts">
    import { onMount } from 'svelte';
    import * as login from "../../lib/login";

    let user = login.get_user();
    let summaries: string[] = [];

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
        summaries = await fetchSummaries(user);
        }
    });

    function formatText(text) {
    // Replace **text** with <strong>text</strong>
    const boldFormatted = text.replace(/\*\*(.*?)\*\*/g, '\n<strong>$1</strong>\n');
    
    // Replace \n with <br />
    return boldFormatted.replace(/\n/g, '<br />');
  }
</script>
  
<div>
    {#if user && summaries.length}
        <ul>
        {#each summaries as summary, i}
            <details>
                <summary>Summary #{i + 1}</summary>
                <p>{summary}</p>
            </details>
        {/each}
        </ul>
    {:else}
        <p>Loading summaries...</p>
    {/if}
</div>
  