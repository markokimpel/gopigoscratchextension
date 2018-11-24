# https://github.com/markokimpel/gopigoscratchextension
#
# GoPiGo3 Server
#
# Access to camera's video stream.
#
# Copyright 2018 Marko Kimpel
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io
import threading

import picamera

class _JPEGFrameOutputBuffer:

    def __init__(self):
        self.buffer = io.BytesIO()
        self.frame = None
        self.condition = threading.Condition()

    def write(self, b):
        if b.startswith(b'\xff\xd8') and \
           self.buffer.tell() > 0:
            # new frame, existing buffer contains come content
            # size buffer to current positon 
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(b)

    def get_frame(self):
        with self.condition:
            self.condition.wait()
            return self.frame

class _CameraManager:

    def __init__(self):
        self.camera = None
        self.buffer = None
        self._consumers = 0
        self._lock = threading.Lock()

    def inc_consumers(self):
        with self._lock:
            if self._consumers == 0:
                self._start_camera()
            self._consumers += 1

    def dec_consumers(self):
        with self._lock:
            if self._consumers > 0:
                self._consumers -= 1
            if self._consumers == 0:
                self._stop_camera()

    def _start_camera(self):
        self.camera = picamera.PiCamera(resolution=(320, 240), framerate=10)
        self.buffer = _JPEGFrameOutputBuffer()
        self.camera.start_recording(self.buffer, format='mjpeg')

    def _stop_camera(self):
        if self.camera != None:
            self.camera.stop_recording()
            self.camera.close()
            self.camera = None
        if self.buffer != None:
            self.buffer = None

_camera_mgr = None
_camera_mgr_lock = threading.Lock()

def _get_camera_mgr():
    global _camera_mgr
    if _camera_mgr == None:
        with _camera_mgr_lock:
            if _camera_mgr == None:
                _camera_mgr = _CameraManager()
    return _camera_mgr

class CameraMJPEGStream:

    def __enter__(self):
        _get_camera_mgr().inc_consumers()
        return self

    def __exit__(self, type, value, traceback):
        _get_camera_mgr().dec_consumers()

    def get_frame(self):
        return _get_camera_mgr().buffer.get_frame()
