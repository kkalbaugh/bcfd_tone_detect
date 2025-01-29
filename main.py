import numpy as np
import subprocess
from scipy.signal import find_peaks

def detect_tones(audio_data, tone_frequencies, threshold):
    """Detects tones in the given audio data."""

    # Perform FFT on the audio data
    fft_data = np.fft.fft(audio_data)
    frequencies = np.fft.fftfreq(len(audio_data))

    # Find peaks in the FFT
    peaks, _ = find_peaks(np.abs(fft_data), height=threshold)

    # Check if the detected peaks match any of the tone frequencies
    detected_tones = []
    for peak in peaks:
        frequency = frequencies[peak]
        for tone_frequency in tone_frequencies:
            if abs(frequency - tone_frequency) < 10:  # Tolerance for frequency matching
                detected_tones.append(tone_frequency)

    return detected_tones

if __name__ == "__main__":
    tone_frequencies = [919, 2940]  # Example tone frequencies
    threshold = 1000  # Adjust as needed

    # Use rtl_fm and sox to get audio data
    rtl_fm_process = subprocess.Popen(["rtl_fm", "-f", "483.800M", "-M", "fm", "-s", "22050", "-A", "fast", "-l", "0", "-E", "deemp"], stdout=subprocess.PIPE)
    sox_process = subprocess.Popen(["sox", "-", "-t", "raw", "-r", "22050", "-e", "signed-integer", "-b", "16", "-c", "1", "-"], stdin=rtl_fm_process.stdout, stdout=subprocess.PIPE)

    while True:
        audio_data = np.frombuffer(sox_process.stdout.read(22050), dtype=np.int16)
        detected_tones = detect_tones(audio_data, tone_frequencies, threshold)
        if detected_tones:
            print("Detected tones:", detected_tones)
