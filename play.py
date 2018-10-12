import pyaudio

from ctypes import *
from contextlib import contextmanager

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)


def fillbuff( in_data, frame_count, time_info, status_flags):
    pass


with noalsaerr():
    _audio_interface = pyaudio.PyAudio()
_audio_stream = _audio_interface.open(    format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=48000,
            input_device_index=2,
            input=True, frames_per_buffer=1024,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            #stream_callback=fillbuff,
        )

_audio_stream.stop_stream()
_audio_stream.close()


_audio_stream = _audio_interface.open(    format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=48000,
            input_device_index=2,
            input=True, frames_per_buffer=1024,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=fillbuff,
        )

