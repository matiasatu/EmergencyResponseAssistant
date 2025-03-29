<script>
  import { goto } from '$app/navigation';
  
  const signUp = () => goto('/create-account');
  const currentDisaster = () => goto('/current-disaster');
  const pastDisasters = () => goto('/past-disasters');
</script>

<main >
  <div class="container">
    
    <div class="title">
      <h1>Emergency Response Assistant</h1>
      <p>
        Sign up for automated notifications about emergencies in your area, with specialized suggestions using your info.
      </p>
    </div>
    
    
    <!-- Action Buttons -->
    <div class="action-buttons">
      <button 
        on:click={signUp} 
        class="action-btn">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
        </svg>
        Sign Up
      </button>
      
      <button 
        on:click={currentDisaster} 
        class="action-btn">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2h-1V9a1 1 0 00-1-1z" clip-rule="evenodd" />
        </svg>
        Current Disasters
      </button>

    
    <button 
      on:click={pastDisasters} 
      class="action-btn">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd" />
      </svg>
      Past Disasters
    </button>
  </div>
    
  
  <!-- Footer -->
  <footer class="footer">
    <div class="">
      <p class="opacity-70 text-sm">© 2025 Emergency Response Assistant. All rights reserved.</p>
    </div>
  </footer>
</main>

<style>
  .container {
    padding: 16px;
    display: flex;
    flex-direction: column;
  }

  .title {
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  .action-buttons {
    padding: 50px 50px;
    display: flex;
    justify-content: space-evenly;
    align-items: center;
  }

  .action-btn {
    width: 100px;
    height: 100px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  .footer {
    display: flex;
    justify-content: center;
    align-items: center;
  }
</style>