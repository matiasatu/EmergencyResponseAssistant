<script>
    // Form data
    let username = '';
    let phoneNumber = '';
    let bio = '';
    
    // Form validation
    let usernameError = '';
    let phoneNumberError = '';
    let bioError = '';
    let formSubmitted = false;
    let formSuccess = false;
  
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
  a
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
  
    // Handle form submission
    function handleSubmit() {
      formSubmitted = true;
      
      const isUsernameValid = validateUsername();
      const isPhoneNumberValid = validatePhoneNumber();
      const isBioValid = validateBio();
      
      if (isUsernameValid && isPhoneNumberValid && isBioValid) {
        // In a real app, you would send the data to your backend here
        console.log('Form submitted:', { username, phoneNumber, bio });
        
        // Show success message
        formSuccess = true;
        
        // Reset form after successful submission
        setTimeout(() => {
          username = '';
          phoneNumber = '';
          bio = '';
          formSubmitted = false;
          formSuccess = false;
        }, 3000);
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
          
          <button type="submit" class="submit-button">Create Profile</button>
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
    
    .submit-button:hover {
      background-color: #3a7bd5;
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