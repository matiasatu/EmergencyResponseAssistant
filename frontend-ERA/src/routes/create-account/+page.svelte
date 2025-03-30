<script>
    import { goto } from "$app/navigation";


  let bio = '';
  let showFeedback = false;

  // Form data
  let username = '';
  let email = '';
  let phoneNumber = '';
  let location = '';
  let onInitialForm = true;
  // Form state
  let usernameError = '';
  let emailError = '';
  let phoneNumberError = '';
  let bioError = '';
  let formSubmitted = false;
  let nextBtnClicked = false;
  let formSuccess = false;
  let isLoading = false;
  let serverError = '';
  let bioFeedback = "No feedback at the moment.";
  let feedbackInterval;
  let intervalStarted = false;

  const API_URL = 'http://localhost:8000/create-account';

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

  function validateEmail() {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email) {
      emailError = 'Email is required';
      return false;
    } else if (!emailRegex.test(email)) {
      emailError = 'Please enter a valid email address';
      return false;
    }
    emailError = '';
    return true;
  }

  function validatePhoneNumber() {
    const phoneRegex = /^\d{10}$/;
    if (!phoneNumber) {
      phoneNumberError = 'Phone number is required';
      return false;
    } else if (!phoneRegex.test(phoneNumber.replace(/\D/g, ''))) {
      phoneNumberError = 'Please enter a valid 10-digit phone number';
      return false;
    }
    phoneNumberError = '';
    return true;
  }

  function validateBio() {
    if (!bio) {
      bioError = 'Bio is required';
      return false;
    } else if (bio.length < 10) {
      bioError = 'Bio must be at least 10 characters';
      return false;
    }
    bioError = '';
    return true;
  }

  async function getGroqFeedback(bio) {
    try {
      const response = await fetch('http://127.0.0.1:8000/live-feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ "username": username, "msg": bio }), 
      });

      if (!response.ok) {
        const error = await response.text()
        throw new Error(`Request failed: ${error}`)
      }

      let data = await response.json()
      data = JSON.parse(data)
      console.log("called groq")
      if(data.new_response){
        bioFeedback = data.response
      }
      return;

    } catch (error) {
      bioFeedback = "No feedback at the moment."
      console.error('Error fetching Groq feedback:', error)
    }
  }

  // Start interval when input is first detected:
  function handleBioInput() {
    if (!intervalStarted) {
      intervalStarted = true;
      
      // Immediately get feedback first:
      getGroqFeedback(bio);

      feedbackInterval = setInterval(() => {
        getGroqFeedback(bio);
      }, 3000);
    }
  }

  function handleNext() {
    nextBtnClicked = true;
    const isUsernameValid = validateUsername();
    const isEmailValid = validateEmail();
    const isPhoneNumberValid = validatePhoneNumber();

    if (isUsernameValid && isEmailValid && isPhoneNumberValid) {
      onInitialForm = false;
    }
  
  }
  async function handleSubmit() {
    formSubmitted = true;
    serverError = '';
    
    const isBioValid = validateBio();
    
    if (isBioValid) {
      isLoading = true;
      
      try {
        const profileData = {
          username,
          email,
          phone_number: phoneNumber.replace(/\D/g, ''),
          location,
          bio
        };
        


        const response = await fetch(API_URL, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(profileData)
        });
        
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Failed to create profile');
        }
        
        const data = await response.json();
        console.log('Profile created:', data);
        
        formSuccess = true;
        clearInterval(feedbackInterval)

        setTimeout(() => {
          username = '';
          email = '';
          phoneNumber = '';
          location = '';
          bio = '';
          formSubmitted = false;
          onInitialForm = true;
          formSuccess = false;
          nextBtnClicked = false;
          goto('/')
        }, 3000);
        
      } catch (error) {
        console.error('Error creating profile:', error);
        serverError = error.message || 'An unexpected error occurred';
      } finally {
        isLoading = false;
        
      }
    }
  }

  function formatPhoneNumber(event) {
    const cleanNumber = event.target.value.replace(/\D/g, '');
    
    if (cleanNumber.length <= 3) {
      phoneNumber = cleanNumber;
    } else if (cleanNumber.length <= 6) {
      phoneNumber = cleanNumber.slice(0, 3) + '-' + cleanNumber.slice(3);
    } else {
      phoneNumber = cleanNumber.slice(0, 3) + '-' + cleanNumber.slice(3, 6) + '-' + cleanNumber.slice(6, 10);
    }
  }
</script>

<main class="relative w-full flex flex-row justify-center min-h-[678px] items-stretch bg-gray-100 p-6">
  <!-- form div -->
  <div 
  class="absolute bg-white z-5 top-[60px] shadow-lg rounded-lg p-6 max-w-lg w-full h-[550px] transition-transform duration-1000"
  class:translate-x-0={onInitialForm}
  class:-translate-x-[50%]={!onInitialForm}
  >
    <h1 class="text-2xl font-bold text-center text-gray-700 mb-6">Create Your Profile</h1>
    
    {#if formSuccess}
      <div class="bg-green-100 text-green-700 p-4 rounded mb-4 text-center">
        <p>Profile created successfully!</p>
      </div>
    {:else}
      <form on:submit|preventDefault={handleSubmit} class="space-y-4">
        {#if onInitialForm}
        <div>
          <label for="username" class="block text-gray-600 font-medium">Username <span class="text-red-500">*</span></label>
          <input 
            type="text" 
            id="username" 
            bind:value={username} 
            class="w-full p-2 border rounded focus:ring focus:ring-blue-300 {formSubmitted && usernameError ? 'border-red-500' : 'border-gray-300'}" 
            on:blur={validateUsername}
          />
          {#if nextBtnClicked && usernameError}
            <p class="text-red-500 text-sm mt-1">{usernameError}</p>
          {/if}
        </div>
        
        <div>
          <label for="email" class="block text-gray-600 font-medium">Email <span class="text-red-500">*</span></label>
          <input 
            type="email" 
            id="email" 
            bind:value={email} 
            class="w-full p-2 border rounded focus:ring focus:ring-blue-300 {formSubmitted && emailError ? 'border-red-500' : 'border-gray-300'}" 
            on:blur={validateEmail}
          />
          {#if nextBtnClicked && emailError}
            <p class="text-red-500 text-sm mt-1">{emailError}</p>
          {/if}
        </div>
        
        <div>
          <label for="phoneNumber" class="block text-gray-600 font-medium">Phone Number <span class="text-red-500">*</span></label>
          <input 
            type="tel" 
            id="phoneNumber" 
            value={phoneNumber}
            class="w-full p-2 border rounded focus:ring focus:ring-blue-300 {formSubmitted && phoneNumberError ? 'border-red-500' : 'border-gray-300'}" 
            on:input={formatPhoneNumber}
            on:blur={validatePhoneNumber}
            placeholder="123-456-7890"
          />
          {#if nextBtnClicked && phoneNumberError}
            <p class="text-red-500 text-sm mt-1">{phoneNumberError}</p>
          {/if}
        </div>
        
        <div>
          <label for="location" class="block text-gray-600 font-medium">Location</label>
          <input 
            type="text" 
            id="location" 
            bind:value={location} 
            class="w-full p-2 border rounded focus:ring focus:ring-blue-300 border-gray-300"
            placeholder="Enter your city or region"
          />
        </div>
        {/if}

        {#if !onInitialForm}
          <div>
            <label for="bio" class="block text-gray-600 font-medium">Bio <span class="text-red-500">*</span></label>
            <textarea 
              id="bio" 
              bind:value={bio} 
              on:input={handleBioInput}
              class="w-full p-2 border h-[300px;] rounded focus:ring focus:ring-blue-300 {formSubmitted && bioError ? 'border-red-500' : 'border-gray-300'}" 
              on:blur={validateBio}
              rows="4"
              placeholder="Tell us about yourself..."
            ></textarea>
            {#if formSubmitted && bioError}
              <p class="text-red-500 text-sm mt-1">{bioError}</p>
            {/if}
            <div class="text-sm text-gray-500 mt-1">
              {bio.length} characters
            </div>
          </div>
        {/if}
        
        {#if serverError}
          <div class="bg-red-100 text-red-700 p-4 rounded mb-4 text-center">
            <p>{serverError}</p>
          </div>
        {/if}
        
        {#if !onInitialForm}
          <button type="submit" class="w-full brand-bg text-white py-2 rounded hover:bg-blue-700 transition disabled:bg-gray-400" disabled={isLoading}>
            {#if isLoading}
              Creating Profile...
            {:else}
              Create Profile
            {/if}
          </button>
        {:else if onInitialForm}
          <button type="button" on:click={handleNext} class="w-full brand-bg text-white py-2 rounded hover:bg-blue-700 transition disabled:bg-gray-400" disabled={isLoading}>
            Next
          </button>
        {/if}
      </form>
      <div class="pt-2">
        <p>Already have an account? <a class="brand-text" href="/login">Login</a></p>
      </div>
    {/if}

  </div>

  <!-- Feedback div -->
  <div 
  class="absolute brand-secondary-bg z-0 top-[60px] h-[550px] flex flex-col shadow-lg rounded-lg p-4 max-w-lg w-full items-stretch gap-2 transition-transform duration-1000"
  class:translate-x-0={onInitialForm}
  class:translate-x-[50%]={!onInitialForm}
  class:opacity-0={onInitialForm}
  class:opacity-100={!onInitialForm}
>
  <h1 class="text-3xl text-white font-bold"> Consider adding.... </h1>  
  <div class="bg-white shadow-base rounded-lg p-4 max-w-lg flex-1 w-full items-stretch">
    <p>
      {bioFeedback}
    </p>
  </div>
</div>
</main>

