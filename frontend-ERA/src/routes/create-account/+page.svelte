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

<main class="container">
  <div class="profile-card">
    <h1>Create Your Profile</h1>
    
    {#if formSuccess}
      <div class="success-message">
        <p>Profile created successfully!</p>
      </div>
    {:else}
      <form on:submit|preventDefault={handleSubmit}>
        <div class="form-group">
          <label for="username">Username <span class="required">*</span></label>
          <input 
            type="text" 
            id="username" 
            bind:value={username} 
            class:error={formSubmitted && usernameError} 
            on:blur={validateUsername}
          />
          {#if formSubmitted && usernameError}
            <p class="error-message">{usernameError}</p>
          {/if}
        </div>
        
        <div class="form-group">
          <label for="email">Email <span class="required">*</span></label>
          <input 
            type="email" 
            id="email" 
            bind:value={email} 
            class:error={formSubmitted && emailError} 
            on:blur={validateEmail}
          />
          {#if formSubmitted && emailError}
            <p class="error-message">{emailError}</p>
          {/if}
        </div>
        
        <div class="form-group">
          <label for="phoneNumber">Phone Number <span class="required">*</span></label>
          <input 
            type="tel" 
            id="phoneNumber" 
            value={phoneNumber}
            class:error={formSubmitted && phoneNumberError} 
            on:input={formatPhoneNumber}
            on:blur={validatePhoneNumber}
            placeholder="123-456-7890"
          />
          {#if formSubmitted && phoneNumberError}
            <p class="error-message">{phoneNumberError}</p>
          {/if}
        </div>
        
        <div class="form-group">
          <label for="zipcode">Zip Code <span class="required">*</span></label>
          <input 
            type="text" 
            id="zipcode" 
            value={zipcode}
            class:error={formSubmitted && zipcodeError} 
            on:input={formatZipcode}
            on:blur={validateZipcode}
            placeholder="12345 or 12345-6789"
          />
          {#if formSubmitted && zipcodeError}
            <p class="error-message">{zipcodeError}</p>
          {/if}
        </div>
        
        <div class="form-group">
          <label for="bio">Bio <span class="required">*</span></label>
          <textarea 
            id="bio" 
            bind:value={bio} 
            class:error={formSubmitted && bioError} 
            on:blur={validateBio}
            rows="4"
            placeholder="Tell us about yourself..."
          ></textarea>
          {#if formSubmitted && bioError}
            <p class="error-message">{bioError}</p>
          {/if}
          <div class="character-count">
            {bio.length} characters
          </div>
        </div>
        
        {#if serverError}
          <div class="server-error">
            <p>{serverError}</p>
          </div>
        {/if}
        
        <button type="submit" class="submit-button" disabled={isLoading}>
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

<style>
  .container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background-color: #f5f5f5;
    padding: 20px;
  }
  
  .profile-card {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    padding: 32px;
    width: 100%;
    max-width: 500px;
  }
  
  h1 {
    margin-top: 0;
    margin-bottom: 24px;
    color: #333;
    font-size: 24px;
    text-align: center;
  }
  
  .form-group {
    margin-bottom: 20px;
  }
  
  label {
    display: block;
    margin-bottom: 6px;
    font-weight: 600;
    color: #555;
  }
  
  .required {
    color: #e53935;
  }
  
  input, textarea {
    width: 100%;
    padding: 10px 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 16px;
    transition: border-color 0.2s;
  }
  
  input:focus, textarea:focus {
    border-color: #4a90e2;
    outline: none;
  }
  
  input.error, textarea.error {
    border-color: #e53935;
  }
  
  .error-message {
    color: #e53935;
    font-size: 14px;
    margin-top: 4px;
    margin-bottom: 0;
  }
  
  .server-error {
    background-color: #ffebee;
    border: 1px solid #ffcdd2;
    border-radius: 4px;
    padding: 12px;
    margin-bottom: 20px;
    color: #c62828;
  }
  
  .character-count {
    text-align: right;
    font-size: 12px;
    color: #777;
    margin-top: 4px;
  }
  
  .submit-button {
    background-color: #4a90e2;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 12px 20px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    width: 100%;
    transition: background-color 0.2s;
  }
  
  .submit-button:hover:not(:disabled) {
    background-color: #3a7bd5;
  }
  
  .submit-button:disabled {
    background-color: #b0bec5;
    cursor: not-allowed;
  }
  
  .success-message {
    background-color: #e8f5e9;
    border: 1px solid #c8e6c9;
    border-radius: 4px;
    padding: 16px;
    text-align: center;
    color: #2e7d32;
  }
</style>