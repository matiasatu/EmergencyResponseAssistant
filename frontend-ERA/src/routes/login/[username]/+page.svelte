<script lang="ts">
    import * as login from "../../../lib/login"
    import { goto } from "$app/navigation";

    export let data: {
      username: string;
    };

    login.change_user(data.username)

    goto("/current-disaster")

</script>
  
<h1>Welcome, {data.username}!</h1>