/* https://github.com/markokimpel/gopigoscratchextension
 *
 * Extension for Scratch 2 and scratchx.org
 *
 * Definition of custom Scratch blocks and logic to call GoPiGo3 server from Scratch.
 *
 * Copyright 2018 Marko Kimpel
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

(function(ext) {

  // host_port in double curly brackets is a placeholder that is replaced by
  // the server before sent to the client.
  var baseUrl = "http://{{host_port}}";

  ext._shutdown = function() {};

  ext._getStatus = function() {
    return {status: 2, msg: "Ready"};
  };

  ext.setBlinkers = function(blinkers, state, callback) {
    var url = baseUrl + "/v1/blinkers";
    if (blinkers == "left blinker") {
      url += "/left";
    } else if (blinkers == "right blinker") {
      url += "/right";
    }
    $.ajax({
      method: "PUT",
      url: url,
      data: JSON.stringify({state: state}),
      contentType: "application/json; charset=UTF-8",
      complete: function(jqXHR, textStatus) {
        callback();
      }
    });
  };

  ext.setEyes = function(eyes, red, green, blue, callback) {
    var url = baseUrl + "/v1/eyes";
    if (eyes == "left eye") {
      url += "/left";
    } else if (eyes == "right eye") {
      url += "/right";
    }
    $.ajax({
      method: "PUT",
      url: url,
      data: JSON.stringify({
        red: red * 255 / 100,
        green: green * 255 / 100,
        blue: blue * 255 / 100
      }),
      contentType: "application/json; charset=UTF-8",
      complete: function(jqXHR, textStatus) {
        callback();
      }
    });
  };

  ext.drive = function(direction, distance, speed, callback) {
    $.ajax({
      method: "POST",
      url: baseUrl + "/v1/motors/drive",
      data: JSON.stringify({
        direction: direction,
        speed: speed,
        distance: distance * 10
      }),
      contentType: "application/json; charset=UTF-8",
      complete: function(jqXHR, textStatus) {
        callback();
      }
    });
  };

  ext.driveContiniously = function(direction, speed, callback) {
    $.ajax({
      method: "POST",
      url: baseUrl + "/v1/motors/drive",
      data: JSON.stringify({
        direction: direction,
        speed: speed
      }),
      contentType: "application/json; charset=UTF-8",
      complete: function(jqXHR, textStatus) {
        callback();
      }
    });
  };

  ext.turn = function(angle, direction, speed, callback) {
    $.ajax({
      method: "POST",
      url: baseUrl + "/v1/motors/turn",
      data: JSON.stringify({
        direction: direction,
        speed: speed,
        angle: angle
      }),
      contentType: "application/json; charset=UTF-8",
      complete: function(jqXHR, textStatus) {
        callback();
      }
    });
  };

  ext.turnContiniously = function(direction, speed, callback) {
    $.ajax({
      method: "POST",
      url: baseUrl + "/v1/motors/turn",
      data: JSON.stringify({
        direction: direction,
        speed: speed
      }),
      contentType: "application/json; charset=UTF-8",
      complete: function(jqXHR, textStatus) {
        callback();
      }
    });
  };

  ext.setMotors = function(leftDirection, leftSpeed, rightDirection, rightSpeed, callback) {
    $.ajax({
      method: "POST",
      url: baseUrl + "/v1/motors/set",
      data: JSON.stringify({
        left_direction: leftDirection,
        left_speed: leftSpeed,
        right_direction: rightDirection,
        right_speed: rightSpeed,
      }),
      contentType: "application/json; charset=UTF-8",
      complete: function(jqXHR, textStatus) {
        callback();
      }
    });
  };

  ext.stopMotors = function(callback) {
    $.ajax({
      method: "POST",
      url: baseUrl + "/v1/motors/stop",
      complete: function(jqXHR, textStatus) {
        callback();
      }
    });
  };

  ext.setServo = function(servo, position, callback) {
    var url = baseUrl + "/v1/servos/";
    if (servo == "Servo 1") {
      url += "SERVO1";
    } else {
      url += "SERVO2";
    }
    url += "/position"
    $.ajax({
      method: "PUT",
      url: url,
      data: JSON.stringify({position: position}),
      contentType: "application/json; charset=UTF-8",
      complete: function(jqXHR, textStatus) {
        callback();
      }
    });
  };

  ext.getDistance = function(callback) {
    $.ajax({
      method: "GET",
      url: baseUrl + "/v1/sensors/I2C/distance/distance",
      dataType: "json",
      success: function(data) {
        callback(Math.round(data.distance / 10));
      },
      error: function(jqXHR, textStatus, errorThrown) {
        callback(-1.0);
      }
    });
  };

  // Block and block menu descriptions
  var descriptor = {
    blocks: [
      ["w", "turn %m.blinkers %m.onOff",                         "setBlinkers", "both blinkers", "on" ],
      ["w", "set %m.eyes to red %n % green %n % blue %n %",      "setEyes", "both eyes",  0, 10, 10 ],

      ["w", "drive %m.forwardBackward %n cm at %n % speed",      "drive", "forward", 10, 50 ],
      ["w", "drive %m.forwardBackward at %n % speed",            "driveContiniously", "forward", 50 ],
      ["w", "turn %n degrees to the %m.leftRight at %n % speed", "turn", 90, "left", 30 ],
      ["w", "turn %m.leftRight at %n % speed",                   "turnContiniously", "left", 30 ],
      ["w", "set left motor %m.forwardBackward %n % speed right motor %m.forwardBackward %n % speed",
                                                                 "setMotors", "forward", 50, "forward", 50 ],
      ["w", "stop motors",                                       "stopMotors" ],

      ["w", "set %m.servos to %n degrees",                       "setServo", "Servo 1", "90" ],

      ["R", "distance",                                          "getDistance" ]
    ],
    menus: {
      blinkers:        [ "both blinkers", "left blinker", "right blinker" ],
      onOff:           [ "on", "off" ],
      eyes:            [ "both eyes", "left eye", "right eye" ],
      forwardBackward: [ "forward", "backward" ],
      leftRight:       [ "left", "right"],
      servos:          [ "Servo 1", "Servo 2" ]
    },
    url: "http://{{host_port}}/"
  };

  // Register the extension
  ScratchExtensions.register("GoPiGo3", descriptor, ext);

})({});
