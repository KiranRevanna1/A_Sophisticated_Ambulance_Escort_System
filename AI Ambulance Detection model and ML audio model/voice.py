import pyaudio
import librosa
import numpy as np
import time

# Constants
CHUNK_SIZE = 126      
FORMAT = pyaudio.paInt16
CHANNELS = 1
SAMPLE_RATE = 44100
THRESHOLD = 2
MIN_AMPLITUDE = 10000  # Minimum amplitude threshold for audio signal
SLEEP_TIME = 30  # Sleep time in seconds
COOLDOWN_TIME = 2  # Cooldown time in seconds

# Load the siren sound file for comparison
siren_sound, _ = librosa.load('siren.wav', sr=SAMPLE_RATE)

last_detection_time = 0  # Variable to track the time of the last detection

def detect_siren(stream):
    global last_detection_time

    # Read audio data from the stream
    audio_data = stream.read(CHUNK_SIZE, exception_on_overflow=False)

    # Convert audio data to numpy array
    audio_np = np.frombuffer(audio_data, dtype=np.int16)

    # Normalize the audio data
    audio_normalized = audio_np / np.max(np.abs(audio_np))

    # Check if the audio signal exceeds the minimum amplitude threshold
    if np.max(np.abs(audio_np)) < MIN_AMPLITUDE:
        return

    # Adjust the length of the audio signal to match siren_sound
    pad_length = len(siren_sound) - len(audio_normalized)
    if pad_length > 0:
        audio_adjusted = np.pad(audio_normalized, (0, pad_length), mode='constant')
    else:
        audio_adjusted = audio_normalized[:len(siren_sound)]

    # Extract the tempogram of the audio signal
    tempogram = librosa.feature.tempogram(y=audio_adjusted, sr=SAMPLE_RATE)

    # Calculate the similarity between the tempogram and siren sound
    similarity = np.correlate(tempogram[0], siren_sound, mode='valid')

    # Check if similarity exceeds threshold and cooldown period has passed
    current_time = time.time()
    if np.max(similarity) > THRESHOLD and (current_time - last_detection_time) > COOLDOWN_TIME:
        print("Ambulance siren detected!")
        last_detection_time = current_time  # Update the last detection time

        # Clear the chunk memory
        stream.read(stream.get_read_available(), exception_on_overflow=False)

        # Call your function here
        your_function()

        # Sleep for specified time with countdown
        remaining_time = SLEEP_TIME
        while remaining_time > 0:
            print(f"Sleeping for {remaining_time} seconds...")
            time.sleep(1)
            remaining_time -= 1

def your_function():
    # Implement your desired functionality here
    print("Calling your function...")

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open audio stream
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=SAMPLE_RATE, input=True, frames_per_buffer=CHUNK_SIZE)

# Start real-time audio processing
print("Listening for ambulance sirens...")
while True:
    detect_siren(stream)

# Close the audio stream
stream.stop_stream()
stream.close()
audio.terminate()
