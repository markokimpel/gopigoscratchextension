# https://github.com/markokimpel/gopigoscratchextension
#
# GoPiGo3 Server
#
# HTTP interface to the Python API of the GoPiGo3.
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
#
# User pages:
#     /                 homepage
#     /controller.html  UI to manually control GoPiGo3
#
# Scratch extension:
#     /scratch_extension.js
#
# RESTful webservices (request/response format is JSON):
#     GET  /ping
#          { "server": "gpg3", "v1": "supported" }
#     GET  /v1/ping
#          { "server": "gpg3" }
#
#     GET  /v1/platform/information
#          { "manufacturer": "Dexter Industries",
#            "board_name": "GoPiGo3",
#            "hardware_version": "3.x.x",
#            "firmware_version": "1.0.0",
#            "hardware_serial_number": "0123456789ABCDEF0123456789ABCDEF" }
#     GET  /v1/platform/voltages/5v
#          { "voltage": 4.931 }
#     GET  /v1/platform/voltages/battery
#          { "voltage": 9.434 }
#
#     PUT  /v1/blinkers[/left|right] { "state": "on"|"off" }
#     PUT  /v1/eyes[/left|right] { "red": 255, "green": 0, "blue": 0 } (range 0..255)
#
#     POST /v1/motors/drive { "direction": "forward"|"backward", "speed": [pct] [, "distance": [mm]] }
#     POST /v1/motors/turn { "direction": right"|"left", "speed": [pct] [, "degrees": [degrees]] }
#     POST /v1/motors/move { left_direction: "forward"|"backward", "left_speed": [pct], "right_direction"="forward"|"backward", "right_speed": [pct] }
#     POST /v1/motors/stop
#     GET  /v1/motors/status
#          { left:  { "flags": 0, "power": 52, "encoder": 5270, "dps": 175 },
#            right: { "flags": 0, "power": 54, "encoder": 5624, "dps": 174 } }
#
#     GET  /v1/sensors/I2C/distance/distance
#          { "distance": 523 } (in mm)

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from mimetypes import MimeTypes
import socket
import urllib.parse

from easygopigo3 import EasyGoPiGo3

class GPG3HTTPRequestHandler(BaseHTTPRequestHandler):

    # whitelist of allowed paths
    ALLOWED_TEXT_DOWNLOADS = {
        "/",
        "/controller.html",
        "/controller.js",
        "/scratch_extension.js",
        "/jquery/jquery-3.2.1.min.js",
        "/bootstrap/css/bootstrap.min.css",
        "/bootstrap/js/bootstrap.min.js"
        }

    # whitelist of allowed paths
    ALLOWED_BINARY_DOWNLOADS = {
        "/favicon.ico"
        }

    def do_GET(self):

        # text file download with placeholder support
        if self.path in self.ALLOWED_TEXT_DOWNLOADS:

            # strip off leading '/'
            fname = self.path[1:]
            if fname == "":
                fname = "index.html"

            # read file
            with open(fname, "r") as f:
                content = f.read()

            # replace placeholders
            host_port = self.headers.get('Host')
            if host_port is None:
                host_port = 'localhost'

            content = content.replace('{{host_port}}', host_port)

            self.send_response(200)

            # set Content-Type
            # guess content type based on URL path
            content_type = MimeTypes().guess_type(fname)[0]
            if content_type is not None:
                self.send_header('Content-Type', content_type + "; charset=UTF-8")
            # TODO: send Content-Length header
            self.end_headers()

            # send content to requester
            self.wfile.write(content.encode())

        # binary file download
        elif self.path in self.ALLOWED_BINARY_DOWNLOADS:

            # strip off leading '/'
            fname = self.path[1:]

            # read file
            with open(fname, "rb") as f:
                content = f.read()

            self.send_response(200)

            # set Content-Type
            content_type = MimeTypes().guess_type(fname)[0]
            if content_type is not None:
                self.send_header('Content-Type', content_type)
            # TODO: send Content-Length header
            self.end_headers()

            # send content to requester
            self.wfile.write(content)

        elif self.path == '/ping':
            data = {'server': 'gpg3', 'v1': 'supported'}
            self.send_json_response(data)

        elif self.path == '/v1/ping':
            data = {'server': 'gpg3'}
            self.send_json_response(data)

        elif self.path == '/v1/platform/information':
            data = {
                'manufacturer': gpg3.get_manufacturer(),
                'board_name': gpg3.get_board(),
                'hardware_version': gpg3.get_version_hardware(),
                'firmware_version': gpg3.get_version_firmware(),
                'hardware_serial_number': gpg3.get_id()
                }
            self.send_json_response(data)

        elif self.path == '/v1/platform/voltages/5v':
            data = {'voltage': gpg3.get_voltage_5v()}
            self.send_json_response(data)

        elif self.path == '/v1/platform/voltages/battery':
            data = {'voltage': gpg3.get_voltage_battery()}
            self.send_json_response(data)

        elif self.path == '/v1/sensors/I2C/distance/distance':

            dist = distance_sensor.read_mm()

            data = {'distance' : dist}
            self.send_json_response(data)

        elif self.path == '/v1/motors/status':

            (left_flags, left_power, left_encoder, left_dps) = \
                gpg3.get_motor_status(gpg3.MOTOR_LEFT)
            (right_flags, right_power, right_encoder, right_dps) = \
                gpg3.get_motor_status(gpg3.MOTOR_RIGHT)

            data = {
                'left': {
                    'flags': left_flags,
                    'power': left_power,
                    'encoder': left_encoder,
                    'dps': left_dps
                    },
                'right': {
                    'flags': right_flags,
                    'power': right_power,
                    'encoder': right_encoder,
                    'dps': right_dps
                    }
                }

            self.send_json_response(data)

        else:
            self.send_error(404, "Unknown path " + self.path)

    def do_PUT(self):

        if self.path.startswith('/v1/blinkers'):

            # read and parse PUT data
            data_bytes = self.rfile.read(int(self.headers['Content-Length']))
            data_string = data_bytes.decode()
            data = json.loads(data_string)

            # blinkers_id from URL
            blinkers_id = urllib.parse.unquote(self.path[13:])
            if blinkers_id not in {'', 'left', 'right'}:
                self.send_error(400, "Unknown blinkers_id " + blinkers_id)
                return

            # state from PUT data
            state = data['state']
            if state not in {'on', 'off'}:
                self.send_error(400, "Unknown state " + data['state'])
                return

            # Class EasyGoPiGo3 offers no method to change both blinkers with a
            # single SPI transfer. Using GoPiGo3.set_led directly.

            # map to GoPiGo3.set_led parameters
            led = {
                '': gpg3.LED_LEFT_BLINKER | gpg3.LED_RIGHT_BLINKER,
                'left': gpg3.LED_LEFT_BLINKER,
                'right': gpg3.LED_RIGHT_BLINKER
                }[blinkers_id]

            brightness = {
                'on': 255,
                'off': 0
                }[state]

            gpg3.set_led(led, brightness)

            self.send_response(204)
            if self.headers.get('Origin') is not None:
                self.send_header("Access-Control-Allow-Origin", self.headers.get('Origin'))
            self.end_headers()

        elif self.path.startswith('/v1/eyes'):

            # read and parse PUT data
            data_bytes = self.rfile.read(int(self.headers['Content-Length']))
            data_string = data_bytes.decode()
            data = json.loads(data_string)

            # eyes_id from URL
            eyes_id = urllib.parse.unquote(self.path[9:])
            if eyes_id not in {'', 'left', 'right'}:
                self.send_error(400, "Unknown eyes_id " + blinkers_id)
                return

            # color from PUT data

            if not self.is_convertible_to_int(data['red']):
                self.send_error(400, "Parameter red not an int ({})".format(data['red']))
                return
            red = int(data['red'])
            if red < 0 or red > 255:
                self.send_error(400, "Parameter red not in range 0..255 ({})".format(red))
                return

            if not self.is_convertible_to_int(data['green']):
                self.send_error(400, "Parameter green not an int ({})".format(data['green']))
                return
            green = int(data['green'])
            if green < 0 or green > 255:
                self.send_error(400, "Parameter green not in range 0..255 ({})".format(green))
                return

            if not self.is_convertible_to_int(data['blue']):
                self.send_error(400, "Parameter blue not an int ({})".format(data['blue']))
                return
            blue = int(data['blue'])
            if blue < 0 or blue > 255:
                self.send_error(400, "Parameter blue not in range 0..255 ({})".format(blue))
                return

            # Class EasyGoPiGo3 offers some eye open/close semantic that is
            # rather confusing than helpful. Also, the class does not provide
            # a method to change both eyes with a single SPI transfer. Using
            # GoPiGo3.set_led directly.

            # map to GoPiGo3.set_led parameters
            led = {
                '': gpg3.LED_LEFT_EYE | gpg3.LED_RIGHT_EYE,
                'left': gpg3.LED_LEFT_EYE,
                'right': gpg3.LED_RIGHT_EYE
                }[eyes_id]

            gpg3.set_led(led, red, green, blue)

            self.send_response(204)
            if self.headers.get('Origin') is not None:
                self.send_header("Access-Control-Allow-Origin", self.headers.get('Origin'))
            self.end_headers()

            """
            elif self.path == '/v1/move':

                # read and parse POST data
                data_string = self.rfile.read(int(self.headers['Content-Length']))
                data = json.loads(data_string)

                # direction from POST data
                direction = data['direction']
                if direction not in {'forward','reverse','right','left'}:
                    self.send_error(400, "Unknown direction " + direction)
                    return

                if not self.is_convertible_to_float(data['speed']):
                    self.send_error(400, "Parameter speed not a float (%s)" % data['speed'])
                    return
                speed = float(data['speed'])
                if speed < 0 or speed > 100:
                    self.send_error(400, "Parameter speed not in range 0..100 (%f)" % speed)
                    return

                if not self.is_convertible_to_float(data['duration']):
                    self.send_error(400, "Parameter duration not a float (%s)" % data['duration'])
                    return
                duration = float(data['duration'])
                if duration < 0:
                    self.send_error(400, "Parameter duration less than 0 (%f)" % duration)
                    return

                if direction == 'forward':
                    rrb3.forward(duration, speed / 100)
                elif direction == 'reverse':
                    rrb3.reverse(duration, speed / 100)
                elif direction == 'right':
                    rrb3.right(duration, speed / 100)
                else:
                    rrb3.left(duration, speed / 100)

                self.send_json_response({})

            elif self.path == '/v1/motors':

                # read and parse POST data
                data_string = self.rfile.read(int(self.headers['Content-Length']))
                data = json.loads(data_string)

                if data['left_direction'] == 'forward':
                    left_direction = 0
                elif data['left_direction'] == 'reverse':
                    left_direction = 1
                else:
                    self.send_error(400, "Unknown left_direction " + data['left_direction'])
                    return

                if not self.is_convertible_to_float(data['left_speed']):
                    self.send_error(400, "Parameter left_speed not a float (%s)" % data['left_speed'])
                    return
                left_speed = float(data['left_speed'])
                if left_speed < 0 or left_speed > 100:
                    self.send_error(400, "Parameter left_speed not in range 0..100 (%f)" % left_speed)
                    return

                if data['right_direction'] == 'forward':
                    right_direction = 0
                elif data['right_direction'] == 'reverse':
                    right_direction = 1
                else:
                    self.send_error(400, "Unknown right_direction " + data['right_direction'])
                    return

                if not self.is_convertible_to_float(data['right_speed']):
                    self.send_error(400, "Parameter right_speed not a float (%s)" % data['right_speed'])
                    return
                right_speed = float(data['right_speed'])
                if right_speed < 0 or right_speed > 100:
                    self.send_error(400, "Parameter right_speed not in range 0..100 (%f)" % right_speed)
                    return

                rrb3.set_motors(right_speed / 100, right_direction, left_speed / 100, left_direction)

                self.send_json_response({})

            elif self.path == '/v1/stop':

                rrb3.stop()

                self.send_json_response({})
            """
        else:
            self.send_error(404, "Unknown path " + self.path)

    def do_OPTIONS(self):

        # needed for CORS pre-flight requests

        if self.headers.getheader('Origin') is None:
            self.send_error(501, "Non-CORS OPTIONS request not implemented")
            return

        self.send_response(200)

        self.send_header("Access-Control-Allow-Origin", self.headers.getheader('Origin'))
        self.send_header("Access-Control-Allow-Methods", "GET, PUT, POST, OPTIONS")

        if self.headers.getheader('Access-Control-Request-Headers') is not None:
            self.send_header("Access-Control-Allow-Headers", self.headers.getheader('Access-Control-Request-Headers'))

        self.end_headers()

    def send_json_response(self, data):
        data_string = json.dumps(data)
        self.send_response(200)
        if self.headers.get('Origin') is not None:
            self.send_header("Access-Control-Allow-Origin", self.headers.get('Origin'))
        self.send_header("Content-Type", "application/json; charset=UTF-8")
        # TODO: write Content-Length
        self.end_headers()
        self.wfile.write(data_string.encode())

    def is_convertible_to_int(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def is_convertible_to_float(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

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

if __name__ == "__main__":

    # TODO: make port configurable
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, GPG3HTTPRequestHandler)

    # should always print IP address '0.0.0.0' which means listing at all IPs
    print("Server listening at " + httpd.server_address[0] + ":" + str(httpd.server_address[1]))
    print("")

    own_ip = get_own_ip()
    print("GPG3 Server homepage : http://" + own_ip + ":" + str(httpd.server_address[1]) + "/")
    print("Scratch extension URL: http://" + own_ip + ":" + str(httpd.server_address[1]) + "/scratch_extension.js")
    print("")

    print("Press Ctrl-C to stop server")

    gpg3 = EasyGoPiGo3(use_mutex=True)

    distance_sensor = gpg3.init_distance_sensor()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        gpg3.reset_all()
