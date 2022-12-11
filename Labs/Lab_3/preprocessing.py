import tensorflow as tf
import tensorflow_io as tfio
import numpy as np

LABELS = ['down', 'go', 'left', 'no', 'right', 'stop', 'up', 'yes']

def get_audio_and_label(filename):

    audio_binary = tf.io.read_file(filename)
    audio, sampling_rate = tf.audio.decode_wav(audio_binary)

    path_parts = tf.strings.split(filename, '/')
    path_end = path_parts[-1]
    file_part = tf.strings.split(path_end, '_')
    label = file_part[0]

    # tf.squeeze removes from tensor all size-1 dimensions
    audio = tf.squeeze(audio)

    # create a tensor of all zeros [tf.zeros(shape,dtype)]
    # in this case, we create a padding for the audio tensor
    zero_padding = tf.zeros(sampling_rate - tf.shape(audio), dtype=tf.float32)
    audio_padded = tf.concat([audio, zero_padding], axis=0)

    return (audio_padded, sampling_rate, label)

# This method computes the magnitude of the STFT of a WAV file
def get_spectrogram(filename, downsampling_rate, frame_length_in_s, frame_step_in_s):

    audio_padded, sampling_rate, label = get_audio_and_label(filename)

    if downsampling_rate != sampling_rate:
        sampling_rate_int64 = tf.cast(sampling_rate, tf.int64)
        audio_padded = tfio.audio.resample(audio_padded, sampling_rate_int64, downsampling_rate)

    sampling_rate_float32 = tf.cast(downsampling_rate, tf.float32)
    frame_length = int(frame_length_in_s * sampling_rate_float32)
    frame_step = int(frame_step_in_s * sampling_rate_float32)

    stft = tf.signal.stft(
        audio_padded,
        frame_length=frame_length,
        frame_step=frame_step,
        fft_length=frame_length
    )
    spectrogram = tf.abs(stft)

    return (spectrogram, sampling_rate, label)

# This method computes the log-Mel spectrogram of a WAV file
def get_log_mel_spectrogram(filename, downsampling_rate, frame_length_in_s, frame_step_in_s, num_mel_bins, lower_frequency, upper_frequency):
    
    spectrogram, sampling_rate, label = get_spectorgram(filename, downsampling_rate, frame_length_in_s, frame_step_in_s)

    # Convert to mel-spectogram
    mel_spectrogram = tfio.audio.melscale(
        spectrogram = spectrogram,
        rate = sampling_rate,
        mels = num_mel_bins,
        fmin = lower_frequency,
        fmax = upper_frequency
    )

    log_mel_spectogram = log10(mel_spectrogram)
    
    return (log_mel_spectogram, label)

# This method computes the MFCCs of a WAV file
def get_mfccs(filename, downsampling_rate, frame_length_in_s, frame_step_in_s, num_mel_bins, lower_frequency, upper_frequency, num_coefficients):

    log_mel_spectogram, label = get_mfccs(filename, downsampling_rate, frame_length_in_s, frame_step_in_s, num_mel_bins, lower_frequency, upper_frequency)
    mfccs = tf.signal.mfccs_from_log_mel_spectrograms(
        log_mel_spectrograms
    )

    return (mfccs, label)

def log10(x):
  numerator = tf.log(x)
  denominator = tf.log(tf.constant(10, dtype=numerator.dtype))
  return numerator / denominator
