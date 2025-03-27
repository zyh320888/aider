document.addEventListener('DOMContentLoaded', function() {
  let player; // Store player reference to make it accessible to click handlers
  let globalAudio; // Global audio element to be reused
  
  // Detect if device likely has no physical keyboard
  function detectNoKeyboard() {
    // Check if it's a touch device (most mobile devices)
    const isTouchDevice = ('ontouchstart' in window) || 
                         (navigator.maxTouchPoints > 0) ||
                         (navigator.msMaxTouchPoints > 0);
                         
    // Check common mobile user agents as additional signal
    const isMobileUA = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    
    // If it's a touch device and has a mobile user agent, likely has no physical keyboard
    if (isTouchDevice && isMobileUA) {
      document.body.classList.add('no-physical-keyboard');
    }
  }
  
  // Run detection
  detectNoKeyboard();
  
  // Parse the transcript section to create markers and convert timestamps to links
  function parseTranscript() {
    const markers = [];
    // Find the Commentary heading
    const transcriptHeading = Array.from(document.querySelectorAll('h2')).find(el => el.textContent.trim() === 'Commentary');
    
    if (transcriptHeading) {
      // Get all list items after the transcript heading
      let currentElement = transcriptHeading.nextElementSibling;
      
      while (currentElement && currentElement.tagName === 'UL') {
        const listItems = currentElement.querySelectorAll('li');
        
        listItems.forEach(item => {
          const text = item.textContent.trim();
          const match = text.match(/(\d+):(\d+)\s+(.*)/);
          
          if (match) {
            const minutes = parseInt(match[1], 10);
            const seconds = parseInt(match[2], 10);
            const timeInSeconds = minutes * 60 + seconds;
            const formattedTime = `${minutes}:${seconds.toString().padStart(2, '0')}`;
            const message = match[3].trim();
            
            // Create link for the timestamp
            const timeLink = document.createElement('a');
            timeLink.href = '#';
            timeLink.textContent = formattedTime;
            timeLink.className = 'timestamp-link';
            timeLink.dataset.time = timeInSeconds;
            timeLink.dataset.message = message;
            
            // Add click event to seek the player
            timeLink.addEventListener('click', function(e) {
              e.preventDefault();
              if (player && typeof player.seek === 'function') {
                player.seek(timeInSeconds);
                player.play();
                
                // Also trigger toast and speech
                showToast(message);
                speakText(message, timeInSeconds);
                
                // Highlight this timestamp
                highlightTimestamp(timeInSeconds);
              }
            });
            
            // Replace text with the link + message
            item.textContent = '';
            item.appendChild(timeLink);
            item.appendChild(document.createTextNode(' ' + message));
            
            // Add class and click handler to the entire list item
            item.classList.add('transcript-item');
            item.dataset.time = timeInSeconds;
            item.dataset.message = message;
            
            item.addEventListener('click', function(e) {
              // Prevent click event if the user clicked directly on the timestamp link
              // This prevents double-firing of the event
              if (e.target !== timeLink) {
                e.preventDefault();
                if (player && typeof player.seek === 'function') {
                  player.seek(timeInSeconds);
                  player.play();
                  
                  // Also trigger toast and speech
                  showToast(message);
                  speakText(message, timeInSeconds);
                  
                  // Highlight this timestamp
                  highlightTimestamp(timeInSeconds);
                }
              }
            });
            
            markers.push([timeInSeconds, message]);
          }
        });
        
        currentElement = currentElement.nextElementSibling;
      }
    }
    
    return markers;
  }

  // Parse transcript and create markers
  const markers = parseTranscript();
  
  // Create player with a single call
  player = AsciinemaPlayer.create(
    recording_url,
    document.getElementById('demo'),
    {
      speed: 1.25,
      idleTimeLimit: 1,
      theme: "aider",
      poster: "npt:0:01",
      markers: markers,
      controls: true
    }
  );
  
  // Focus on the player element so keyboard shortcuts work immediately
  setTimeout(() => {
    // Use setTimeout to ensure the player is fully initialized
    if (player && typeof player.focus === 'function') {
      player.focus();
    } else {
      // If player doesn't have a focus method, try to find and focus the terminal element
      const playerElement = document.querySelector('.asciinema-terminal');
      if (playerElement) {
        playerElement.focus();
      } else {
        // Last resort - try to find element with tabindex
        const tabbableElement = document.querySelector('[tabindex]');
        if (tabbableElement) {
          tabbableElement.focus();
        }
      }
    }
  }, 100);
  
  // Track active toast elements
  let activeToast = null;
  
  // Function to display toast notification
  function showToast(text) {
    // Get the appropriate container based on fullscreen state
    let container = document.getElementById('toast-container');
    const isFullscreen = document.fullscreenElement || 
                         document.webkitFullscreenElement || 
                         document.mozFullScreenElement || 
                         document.msFullscreenElement;
    
    // If in fullscreen, check if we need to create a fullscreen toast container
    if (isFullscreen) {
      // Target the fullscreen element as the container parent
      const fullscreenElement = document.fullscreenElement || 
                               document.webkitFullscreenElement || 
                               document.mozFullScreenElement || 
                               document.msFullscreenElement;
      
      // Look for an existing fullscreen toast container
      let fsContainer = fullscreenElement.querySelector('.fs-toast-container');
      
      if (!fsContainer) {
        // Create a new container for fullscreen mode
        fsContainer = document.createElement('div');
        fsContainer.className = 'toast-container fs-toast-container';
        fsContainer.id = 'fs-toast-container';
        fullscreenElement.appendChild(fsContainer);
      }
      
      container = fsContainer;
    }
    
    // Remove any existing toast
    if (activeToast) {
      hideToast(activeToast);
    }
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = 'toast-notification';
    toast.textContent = text;
    
    // Add to container
    container.appendChild(toast);
    
    // Store reference to active toast
    activeToast = {
      element: toast,
      container: container
    };
    
    // Show toast with animation
    requestAnimationFrame(() => {
      toast.style.opacity = '1';
    });
    
    // Hide after delay
    setTimeout(() => {
      hideToast(activeToast);
    }, 5000);
    
    return toast;
  }
  
  // Function to hide toast notification
  function hideToast(toastInfo) {
    if (!toastInfo || !toastInfo.element) return;
    
    // Fade out with animation
    toastInfo.element.style.opacity = '0';
    
    // Remove from DOM after animation completes
    setTimeout(() => {
      if (toastInfo.element.parentNode === toastInfo.container) {
        toastInfo.container.removeChild(toastInfo.element);
      }
      
      // Clear active toast if this is the one we're hiding
      if (activeToast === toastInfo) {
        activeToast = null;
      }
    }, 300);
  }
  
  // Use browser TTS if available
  function useBrowserTTS(text) {
    if (!('speechSynthesis' in window)) {
      return false;
    }
    
    try {
      // Check if speech synthesis is available and not speaking
      if (speechSynthesis.speaking) {
        speechSynthesis.cancel();
      }
      
      // Create utterance
      const utterance = new SpeechSynthesisUtterance(text);
      
      // Try to find a good voice
      let voices = speechSynthesis.getVoices();
      if (voices.length === 0) {
        // If voices aren't loaded yet, wait for them
        speechSynthesis.onvoiceschanged = function() {
          voices = speechSynthesis.getVoices();
          setVoice();
        };
      } else {
        setVoice();
      }
      
      function setVoice() {
        // Prefer English voices in this order: US English, UK English, any English
        const preferredVoices = voices.filter(v => v.lang.includes('en-US'));
        if (preferredVoices.length === 0) {
          const ukVoices = voices.filter(v => v.lang.includes('en-GB'));
          if (ukVoices.length === 0) {
            const anyEnglish = voices.filter(v => v.lang.includes('en'));
            if (anyEnglish.length > 0) {
              utterance.voice = anyEnglish[0];
            }
          } else {
            utterance.voice = ukVoices[0];
          }
        } else {
          utterance.voice = preferredVoices[0];
        }
      }
      
      // Adjust rate and pitch for clarity
      utterance.rate = 1.1;
      utterance.pitch = 1.0;
      
      // Speak
      speechSynthesis.speak(utterance);
      return true;
    } catch (e) {
      console.warn('TTS error:', e);
      return false;
    }
  }
  
  // Function to speak text using audio or TTS
  function speakText(text, timeInSeconds) {
    // If TTS isn't supported or failed, don't do anything
    if (!('speechSynthesis' in window) && !('AudioContext' in window || 'webkitAudioContext' in window)) {
      return false;
    }
    
    // Don't do TTS on mobile due to inconsistent support
    if (document.body.classList.contains('no-physical-keyboard')) {
      return false;
    }
    
    // Get user preference for audio narration
    const narrateEnabled = localStorage.getItem('demo-narrate-enabled');
    
    // If user explicitly disabled narration, skip
    if (narrateEnabled === 'false') {
      return false;
    }
    
    // Step 1: Check if we have a pre-recorded audio for this timestamp
    const audioData = window.timestampAudios || {};
    
    if (audioData[timeInSeconds]) {
      const audioUrl = audioData[timeInSeconds];
      
      // Stop any in-progress TTS
      if ('speechSynthesis' in window && speechSynthesis.speaking) {
        speechSynthesis.cancel();
      }
      
      // Stop any existing audio
      if (globalAudio) {
        globalAudio.pause();
        globalAudio = null;
      }
      
      // Create audio element
      const audio = new Audio(audioUrl);
      globalAudio = audio;
      
      // Play audio
      audio.play().catch(e => {
        console.warn('Audio play error:', e);
        // Fallback to TTS
        useBrowserTTS(text);
      });
      
      return true;
    } else {
      // Otherwise, try browser TTS for modern browsers
      return useBrowserTTS(text);
    }
  }
  
  // Function to handle highlighting active timestamp
  function highlightTimestamp(timeInSeconds) {
    // Find all timestamps
    const allTimestamps = document.querySelectorAll('.timestamp-link');
    
    // Remove highlight from all
    allTimestamps.forEach(link => {
      link.classList.remove('timestamp-active');
      const parent = link.closest('li');
      if (parent) {
        parent.classList.remove('active-marker');
      }
    });
    
    // Set current highlight
    const currentTimestamp = Array.from(allTimestamps).find(
      link => parseFloat(link.dataset.time) === timeInSeconds
    );
    
    if (currentTimestamp) {
      currentTimestamp.classList.add('timestamp-active');
      
      // Make sure parent list item is also highlighted
      const parent = currentTimestamp.closest('li');
      if (parent) {
        parent.classList.add('active-marker');
        
        // Scroll to make visible if needed
        const parentRect = parent.getBoundingClientRect();
        const isVisible = (
          parentRect.top >= 0 &&
          parentRect.bottom <= window.innerHeight
        );
        
        if (!isVisible) {
          parent.scrollIntoView({
            behavior: 'smooth',
            block: 'center'
          });
        }
      }
    }
  }
  
  // If player provides a timeupdate event, use it to update highlights
  if (player && typeof player.addEventListener === 'function') {
    player.addEventListener('timeupdate', function(event) {
      const currentTime = Math.floor(event.currentTime);
      const markers = parseTranscript();
      
      // Find the nearest matching marker
      let nearestMarker = null;
      let smallestDiff = Infinity;
      
      markers.forEach(marker => {
        const time = marker[0];
        const diff = Math.abs(currentTime - time);
        
        // Only consider markers before or at current time, within 1 second
        if (time <= currentTime && diff < smallestDiff && diff <= 1) {
          smallestDiff = diff;
          nearestMarker = marker;
        }
      });
      
      if (nearestMarker) {
        highlightTimestamp(nearestMarker[0]);
      }
    });
  }
}); 