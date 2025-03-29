<script>
  import { goto } from '$app/navigation';
  
  const signUp = () => goto('/create-account');
  const currentDisaster = () => goto('/current-disaster');
  const pastDisasters = () => goto('/past-disasters');
</script>

<div class="relative flex-1 flex flex-col justify-center align-center w-full h-screen overflow-hidden">
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
  <div class="relative flex flex-col justify-center items-center text-white text-center px-4 z-10">
    <div class="flex items-center justify-center">
      <h1 class="pb-1 text-6xl font-bold">guardian</h1>
      <h1 class="pb-1 text-6xl font-bold brand-text">.ai</h1>
    </div>
  
    <h2 class="pb-10 text-2xl">an emergency response assistant</h2>
  
    <div class="w-full md:w-1/2 space-y-4">
      <p class="text-lg">
        Sign up to receive instant alerts about emergencies in your area— 
        <span class="text-xl font-bold brand-text">tailored specifically to you.</span>
      </p>
  
      <p class="text-lg">
        guardian.ai harnesses the speed of modern AI to deliver personalized disaster guidance and help 
        <span class="text-xl font-bold brand-text">keep you safe</span> when it matters most.
      </p>
    </div>
  </div>
  
  <div class="flex w-full justify-center text-center items-center pt-20 gap-20 img-bg">
    <button 
      on:click={signUp} 
      class="landing-btn flex justify-center flex-row items-center gap-2 bg-white w-50 h-20 px-5 py-2 rounded-full shadow-md transition">
      <img class="w-[30px] h-[30px]" alt="disaster icon" src="person_add.png">
      Sign Up
    </button>
    
    <button 
      on:click={currentDisaster} 
      class="landing-btn flex justify-center flex-row items-center gap-2 bg-white w-50 h-20 px-5 py-2 rounded-full shadow-md transition">
      <img class="w-[30px] h-[30px]" alt="disaster icon" src="disaster.png">
      Current Disasters
    </button>
  
    <button 
      on:click={pastDisasters} 
      class="landing-btn flex justify-center flex-row items-center gap-2 bg-white w-50 h-20 px-5 py-2 rounded-full shadow-md transition">
      <img class="w-[30px] h-[30px]" alt="disaster icon" src="history.png">
      Past Disasters
    </button>
  </div>
</div>







