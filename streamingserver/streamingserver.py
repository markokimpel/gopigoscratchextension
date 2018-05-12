# Provide Raspberry Pi's camera view in web streaming format.
#
# The M-JPEG format is used. Each frame is an individual JPEG. There is no cross
# frame optimization. This leads to a high bandwidth requirement but seems to be
# pretty well supported by browsers. The Raspberry Pi Camera can produce the
# JPEG frames in hardware, CPU utilization is at a minimum.
#
# The implementation is based on sample code in the Picamera tutorial by Dave Jones,
# https://picamera.readthedocs.io/en/release-1.13/recipes2.html#web-streaming.

import io
import picamera
import logging
import socket
import socketserver
from threading import Condition
from http import server

PAGE="""\
<html>
<head>
<title>Robot's view</title>
</head>
<body>
<img src="stream.mjpg" width="320" height="240" />
</body>
</html>
"""

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

# Try to find own ip address by establishing connection to arbitrary host
# (without sending data).
def get_own_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except:
        # fallback
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

# This resolution and framerate produces a data stream with about 1.5 Mbps.
with picamera.PiCamera(resolution='320x240', framerate=10) as camera:
    print("Camera: " + str(camera.resolution) + ", " + str(camera.framerate.numerator) + " fps")
    print()

    output = StreamingOutput()
    # TODO: start recording when a client connects (to save energy)
    camera.start_recording(output, format='mjpeg')

    try:
        address = ('', 8081)
        server = StreamingServer(address, StreamingHandler)
        try:
            # should always print IP address '0.0.0.0' which means listening at all IPs
            print("Server listening at " + server.server_address[0] + ":" + str(server.server_address[1]))
            print("")

            own_ip = get_own_ip()
            print("Browser URL: http://" + own_ip + ":" + str(server.server_address[1]) + "/")
            print("")

            print("Press Ctrl-C to stop server")

            try:
                server.serve_forever()
            except KeyboardInterrupt:
                pass

        finally:
            server.server_close()

    finally:
        camera.stop_recording()
