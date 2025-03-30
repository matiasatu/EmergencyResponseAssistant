<script lang="ts">
    import * as login from "../../../lib/login";
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";
  
    export let data: {
      username: string;
    };
  
    onMount(() => {
      login.change_user(data.username);
      goto("/current-disaster");
    });
    
</script>
  
<h1>Welcome, {data.username}!</h1>