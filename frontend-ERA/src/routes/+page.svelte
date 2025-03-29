<script>
  import { goto } from '$app/navigation';
  
  const signUp = () => goto('/create-account');
  const currentDisaster = () => goto('/current-disaster');
  const pastDisasters = () => goto('/past-disasters');
</script>

<main>

  <div>
    <div class="relative w-full h-[500px] overflow-hidden">
      <video
        autoplay
        muted
        loop
        playsinline
        class="absolute top-0 left-0 w-full h-full object-cover z-[-1]"
      >
        <source src="/backgroundvid.mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>
    
      <div class="absolute top-0 left-0 w-full h-full bg-black/20 z-[-1]"></div>

      <div class="relative flex flex-col justify-center items-center h-full text-white text-center px-4 z-10">
        <div class="flex flex-row">
        <h1 class="pb-1 text-6xl font-bold">guardian</h1>
        <h1 class="pb-1 text-6xl font-bold brand-text">.ai</h1>
        </div>
        <h2 class="pb-10 text-2xl gray-text">an emergency response assistant</h2>
        <div class="w-[50%]">
          <p class="text-md gray-text">
            Sign up to receive instant alerts about emergencies in your area—tailored specifically to you.
            guardian.ai harnesses the speed of modern AI to deliver personalized disaster guidance and help keep you safe when it matters most.          </p>     
        </div>
      </div>
    </div>
    
    
    
    <!-- Action Buttons -->
    <div class="flex pt-30 pb-30 w-full justify-center text-center items-center gap-10 img-bg">
      <button 
        on:click={signUp} 
        class="flex justify-center text-center items-center gap-2 bg-black text-white size-50 px-5 py-2 rounded-full shadow-md hover:bg-brand transition">
        Sign Up
      </button>
      
      <button 
        on:click={currentDisaster} 
        class="flex justify-center items-center gap-2 bg-black text-white size-50 px-5 py-2 rounded-full shadow-md hover:bg-brand transition">
        Current Disasters
      </button>

      <button 
        on:click={pastDisasters} 
        class="flex justify-center items-center gap-2 bg-black text-white size-50 px-5 py-2 rounded-full shadow-md hover:bg-brand transition">

        Past Disasters
      </button>
    </div>

  </div>
</main>


