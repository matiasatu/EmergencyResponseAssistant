<script>
  // Form data
  let username = '';
  let email = '';
  let phoneNumber = '';
  let zipcode = '';
  let bio = '';
  
  // Form state
  let usernameError = '';
  let emailError = '';
  let phoneNumberError = '';
  let zipcodeError = '';
  let bioError = '';
  let formSubmitted = false;
  let formSuccess = false;
  let isLoading = false;
  let serverError = '';

  // API endpoint for your FastAPI backend
  const API_URL = 'http://localhost:5173/create-account';  // Update this with your actual API URL

  // Validate username
  function validateUsername() {
    if (!username) {
      usernameError = 'Username is required';
      return false;
    } else if (username.length < 3) {
      usernameError = 'Username must be at least 3 characters';
      return false;
    } else {
      usernameError = '';
      return true;
    }
  }

  // Validate email
  function validateEmail() {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email) {
      emailError = 'Email is required';
      return false;
    } else if (!emailRegex.test(email)) {
      emailError = 'Please enter a valid email address';
      return false;
    } else {
      emailError = '';
      return true;
    }
  }

  // Validate phone number
  function validatePhoneNumber() {
    const phoneRegex = /^\d{10}$/;
    if (!phoneNumber) {
      phoneNumberError = 'Phone number is required';
      return false;
    } else if (!phoneRegex.test(phoneNumber.replace(/\D/g, ''))) {
      phoneNumberError = 'Please enter a valid 10-digit phone number';
      return false;
    } else {
      phoneNumberError = '';
      return true;
    }
  }

  // Validate zipcode
  function validateZipcode() {
    const zipRegex = /^\d{5}(-\d{4})?$/;
    if (!zipcode) {
      zipcodeError = 'Zip code is required';
      return false;
    } else if (!zipRegex.test(zipcode)) {
      zipcodeError = 'Please enter a valid 5-digit zip code or ZIP+4';
      return false;
    } else {
      zipcodeError = '';
      return true;
    }
  }

  // Validate bio
  function validateBio() {
    if (!bio) {
      bioError = 'Bio is required';
      return false;
    } else if (bio.length < 10) {
      bioError = 'Bio must be at least 10 characters';
      return false;
    } else {
      bioError = '';
      return true;
    }
  }

  // Format zipcode as user types
  function formatZipcode(event) {
    const value = event.target.value;
    // Only allow digits and hyphen
    zipcode = value.replace(/[^\d-]/g, '');
    
    // Ensure only one hyphen max and format for ZIP+4
    const parts = zipcode.split('-');
    if (parts.length > 2) {
      zipcode = parts[0] + '-' + parts.slice(1).join('');
    }
    
    // Limit first part to 5 digits and second part to 4 digits
    if (parts.length === 2) {
      const firstPart = parts[0].slice(0, 5);
      const secondPart = parts[1].slice(0, 4);
      zipcode = firstPart + (secondPart ? '-' + secondPart : '');
    } else if (parts.length === 1) {
      zipcode = parts[0].slice(0, 5);
    }
  }

  // Handle form submission
  async function handleSubmit() {
    formSubmitted = true;
    serverError = '';
    
    const isUsernameValid = validateUsername();
    const isEmailValid = validateEmail();
    const isPhoneNumberValid = validatePhoneNumber();
    const isZipcodeValid = validateZipcode();
    const isBioValid = validateBio();
    
    if (isUsernameValid && isEmailValid && isPhoneNumberValid && isZipcodeValid && isBioValid) {
      isLoading = true;
      
      try {
        // Prepare the data for the API
        const profileData = {
          username,
          email,
          phone_number: phoneNumber.replace(/\D/g, ''), // Send clean number without dashes
          zipcode: zipcode.replace(/[^\d]/g, ''), // Send digits only for DB storage
          bio
        };
        
        // Send POST request to FastAPI backend
        const response = await fetch(API_URL, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(profileData)
        });
        
        if (!response.ok) {
          // Handle non-2xx responses
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Failed to create profile');
        }
        
        const data = await response.json();
        console.log('Profile created:', data);
        
        // Show success message
        formSuccess = true;
        
        // Reset form after successful submission
        setTimeout(() => {
          username = '';
          email = '';
          phoneNumber = '';
          zipcode = '';
          bio = '';
          formSubmitted = false;
          formSuccess = false;
        }, 3000);
      } catch (error) {
        console.error('Error creating profile:', error);
        serverError = error.message || 'An unexpected error occurred';
      } finally {
        isLoading = false;
      }
    }
  }

  // Format phone number as user types
  function formatPhoneNumber(event) {
    // Get only numbers from input
    const cleanNumber = event.target.value.replace(/\D/g, '');
    
    // Format with dashes
    if (cleanNumber.length <= 3) {
      phoneNumber = cleanNumber;
    } else if (cleanNumber.length <= 6) {
      phoneNumber = cleanNumber.slice(0, 3) + '-' + cleanNumber.slice(3);
    } else {
      phoneNumber = cleanNumber.slice(0, 3) + '-' + cleanNumber.slice(3, 6) + '-' + cleanNumber.slice(6, 10);
    }
  }
</script>

<main class="w-full flex justify-center items-center min-h-screen bg-gray-100 p-6">
  <div class="bg-white shadow-lg rounded-lg p-6 max-w-lg w-full">
    <h1 class="text-2xl font-bold text-center text-gray-700 mb-6">Create Your Profile</h1>
    
    {#if formSuccess}
      <div class="bg-green-100 text-green-700 p-4 rounded mb-4 text-center">
        <p>Profile created successfully!</p>
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
            on:blur={validateUsername}
          />
          {#if formSubmitted && usernameError}
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
          {#if formSubmitted && emailError}
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
          {#if formSubmitted && phoneNumberError}
            <p class="text-red-500 text-sm mt-1">{phoneNumberError}</p>
          {/if}
        </div>
        
        <div>
          <label for="zipcode" class="block text-gray-600 font-medium">Zip Code <span class="text-red-500">*</span></label>
          <input 
            type="text" 
            id="zipcode" 
            value={zipcode}
            class="w-full p-2 border rounded focus:ring focus:ring-blue-300 {formSubmitted && zipcodeError ? 'border-red-500' : 'border-gray-300'}" 
            on:input={formatZipcode}
            on:blur={validateZipcode}
            placeholder="12345 or 12345-6789"
          />
          {#if formSubmitted && zipcodeError}
            <p class="text-red-500 text-sm mt-1">{zipcodeError}</p>
          {/if}
        </div>
        
        <div>
          <label for="bio" class="block text-gray-600 font-medium">Bio <span class="text-red-500">*</span></label>
          <textarea 
            id="bio" 
            bind:value={bio} 
            class="w-full p-2 border rounded focus:ring focus:ring-blue-300 {formSubmitted && bioError ? 'border-red-500' : 'border-gray-300'}" 
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
        
        {#if serverError}
          <div class="bg-red-100 text-red-700 p-4 rounded mb-4 text-center">
            <p>{serverError}</p>
          </div>
        {/if}
        
        <button type="submit" class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition disabled:bg-gray-400" disabled={isLoading}>
          {#if isLoading}
            Creating Profile...
          {:else}
            Create Profile
          {/if}
        </button>
      </form>
    {/if}
  </div>
</main>


