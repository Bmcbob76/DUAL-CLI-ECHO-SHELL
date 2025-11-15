// Enhanced Voice Recognition with Wakeword Detection
// Background noise reduction and expanded wakeword list

let recognition = null;
let voiceRecognitionActive = false;
let listeningForCommand = false;
const WAKEWORDS = [
    'echo',
    'echo prime',
    'hey echo',
    'okay echo',
    'computer',
    'jarvis',
    'friday',
    'assistant',
    'commander',
    'system'
];

function startVoiceRecognition() {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        console.error('Speech recognition not supported');
        return;
    }
    
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    
    // Configuration for optimal performance
    recognition.continuous = true;
    recognition.interimResults = true; // Enable for faster response
    recognition.maxAlternatives = 3; // Get multiple alternatives for better accuracy
    
    // Background noise reduction
    if (recognition.audioContext) {
        try {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const source = audioContext.createMediaStreamSource(stream);
            const filter = audioContext.createBiquadFilter();
            
            // High-pass filter to reduce low-frequency noise
            filter.type = 'highpass';
            filter.frequency.value = 200; // Cut frequencies below 200Hz
            
            source.connect(filter);
            filter.connect(audioContext.destination);
        } catch (e) {
            console.log('Audio filtering not available, using default');
        }
    }
    
    recognition.onstart = () => {
        voiceRecognitionActive = true;
        console.log('🎤 Voice recognition started - listening for wakewords:', WAKEWORDS.join(', '));
        updateVoiceButton(true);
    };
    
    recognition.onresult = (event) => {
        const results = Array.from(event.results);
        const lastResult = results[results.length - 1];
        
        if (!lastResult.isFinal) {
            // Interim results - check for wakeword
            const transcript = lastResult[0].transcript.toLowerCase().trim();
            
            if (!listeningForCommand) {
                // Check for wakeword
                const foundWakeword = WAKEWORDS.some(wakeword => 
                    transcript.includes(wakeword)
                );
                
                if (foundWakeword) {
                    listeningForCommand = true;
                    console.log('🎯 Wakeword detected! Listening for command...');
                    playWakewordSound();
                    showListeningIndicator();
                    
                    // Extract command after wakeword
                    let command = transcript;
                    WAKEWORDS.forEach(wakeword => {
                        const index = command.indexOf(wakeword);
                        if (index !== -1) {
                            command = command.substring(index + wakeword.length).trim();
                        }
                    });
                    
                    if (command) {
                        console.log('📝 Partial command:', command);
                    }
                }
            } else {
                // Already listening for command - show interim text
                const command = transcript;
                console.log('📝 Interim command:', command);
                showInterimCommand(command);
            }
        } else {
            // Final result
            const transcript = lastResult[0].transcript.toLowerCase().trim();
            const confidence = lastResult[0].confidence;
            
            if (listeningForCommand) {
                // Extract command after wakeword
                let command = transcript;
                WAKEWORDS.forEach(wakeword => {
                    const index = command.indexOf(wakeword);
                    if (index !== -1) {
                        command = command.substring(index + wakeword.length).trim();
                    }
                });
                
                if (command && confidence > 0.5) {
                    console.log('✅ Command received:', command, 'Confidence:', confidence);
                    processVoiceCommand(command);
                    hideListeningIndicator();
                }
                
                // Reset listening state after 3 seconds
                setTimeout(() => {
                    listeningForCommand = false;
                }, 3000);
            }
        }
    };
    
    recognition.onerror = (event) => {
        console.error('Voice recognition error:', event.error);
        if (event.error === 'aborted' || event.error === 'network') {
            // Auto-restart on common errors
            setTimeout(() => {
                if (voiceRecognitionActive) {
                    recognition.start();
                }
            }, 1000);
        }
    };
    
    recognition.onend = () => {
        console.log('Voice recognition ended');
        if (voiceRecognitionActive) {
            // Auto-restart for continuous listening
            setTimeout(() => {
                recognition.start();
            }, 500);
        }
    };
    
    try {
        recognition.start();
    } catch (error) {
        console.error('Failed to start recognition:', error);
    }
}

function stopVoiceRecognition() {
    if (recognition) {
        voiceRecognitionActive = false;
        listeningForCommand = false;
        recognition.stop();
        updateVoiceButton(false);
        hideListeningIndicator();
    }
}

function playWakewordSound() {
    // Play subtle beep when wakeword detected
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    oscillator.frequency.value = 800;
    oscillator.type = 'sine';
    gainNode.gain.value = 0.1;
    
    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.1);
}

function showListeningIndicator() {
    // Visual feedback when listening for command
    const indicator = document.createElement('div');
    indicator.id = 'voice-listening-indicator';
    indicator.innerHTML = '🎤 Listening...';
    indicator.style.cssText = `
        position: fixed;
        top: 80px;
        right: 20px;
        background: #007acc;
        color: white;
        padding: 12px 20px;
        border-radius: 4px;
        font-weight: 600;
        z-index: 9999;
        animation: pulse 1s infinite;
    `;
    document.body.appendChild(indicator);
}

function hideListeningIndicator() {
    const indicator = document.getElementById('voice-listening-indicator');
    if (indicator) {
        indicator.remove();
    }
}

function showInterimCommand(command) {
    let indicator = document.getElementById('voice-listening-indicator');
    if (indicator) {
        indicator.innerHTML = `🎤 "${command}"`;
    }
}

function updateVoiceButton(active) {
    // Update the voice control button in header
    const btn = document.querySelector('.voice-control-btn');
    if (btn) {
        btn.style.background = active ? '#f44336' : '#007acc';
        btn.textContent = active ? '🔴 Stop Voice' : '🎤 Start Voice';
    }
}

async function processVoiceCommand(command) {
    console.log('Processing voice command:', command);
    
    // Insert command into message input
    const input = document.getElementById('message-input');
    if (input) {
        input.value = command;
        
        // Auto-send or wait for confirmation
        const autoSend = localStorage.getItem('echoVoiceAutoSend') === 'true';
        if (autoSend) {
            await sendMessage();
        } else {
            // Highlight input to show command was captured
            input.focus();
            input.select();
        }
    }
}
