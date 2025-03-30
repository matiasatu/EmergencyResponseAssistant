<script>
    import * as login from '../../lib/login'

    let username = ""
    let formSubmitted = false
    let isLoading = false
    let formSuccess = false
    
    let usernameError = ""
    let serverError = ""

    function validateUsername() {
        if (!username) {
        usernameError = 'Username is required';
        return false;
        } else if (username.length < 3) {
        usernameError = 'Username must be at least 3 characters';
        return false;
        }
        usernameError = '';
        return true;
    }

    async function handleSubmit() {
        const isUsernameValid = validateUsername();
        formSubmitted = true
        serverError = ''
        isLoading = true

        if (isUsernameValid) {
            let result = await login.change_user(username)
            if (result == false) {
                usernameError = "User not found."
                formSuccess = false
                isLoading = false
            } else {
                formSuccess = true
                isLoading = false
            }
        }


    }
</script>

<main class="w-full flex flex-row justify-center h-screen bg-gray-100 p-6">

    
        <div class="absolute bg-white shadow-lg rounded-lg p-6 max-w-lg w-full min-h-[300px] flex flex-col justify-center">
            <h1 class="text-2xl font-bold text-center text-gray-700 mb-6">Login</h1>
            {#if formSuccess} 
            <div class="bg-green-100 text-green-700 p-4 rounded mb-4 text-center">
                <p>Signed in successfully!</p>
            </div>
            {:else}
            <form on:submit|preventDefault={handleSubmit} class="space-y-4">
                <div>
                    <label for="username" class="block text-gray-600 font-medium">Username <span class="text-red-500">*</span></label>
                    <input 
                    type="text" 
                    id="username" 
                    bind:value={username} 
                    class="w-full p-2 border rounded focus:ring focus:ring-blue-300 {formSubmitted && usernameError ? 'border-red-500' : 'border-gray-300'}" 
                    />
                    {#if formSubmitted && usernameError}
                    <p class="text-red-500 text-sm mt-1">{usernameError}</p>
                    {/if}
                </div>

                <button type="submit" class="w-full brand-bg text-white py-2 rounded hover:bg-blue-700 transition disabled:bg-gray-400" disabled={isLoading}>
                    {#if isLoading}
                        Logging In...
                    {:else}
                        Log In
                    {/if}
                </button>

            </form>
            <div class="pt-2">
                <p>Don't have an account? <a class="brand-text" href="/create-account">Sign Up</a></p>
            </div>
            {/if}

        </div>
    
</main>