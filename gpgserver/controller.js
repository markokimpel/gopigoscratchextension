/* https://github.com/markokimpel/gopigoscratchextension
 *
 * Controller UI
 *
 * Send commands to GoPiGo3 Server from a webpage.
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

$(document).ready(function() {

  $("#platformInformationSubmit").click(function() {
    $("#platformInformationValue").val("?");
    $.ajax({
      method: "GET",
      url: "/v1/platform/information",
      dataType: "json",
      success: function(data) {
        $("#platformInformationValue").val(
          "Manufacturer: " + data.manufacturer + "\n" +
          "Board name: " + data.board_name + "\n" +
          "Hardware version: " + data.hardware_version + "\n" +
          "Firmware version: " + data.firmware_version + "\n" +
          "Hardware serial number: " + data.hardware_serial_number
          );
      },
      error: function(jqXHR, textStatus, errorThrown) {
        alert("Error: " + errorThrown);
      }
    });
  });

  $("#platformInformationVoltages5VSubmit").click(function() {
    $("#platformInformationVoltages5VValue").val("?");
    $.ajax({
      method: "GET",
      url: "/v1/platform/voltages/5v",
      dataType: "json",
      success: function(data) {
        $("#platformInformationVoltages5VValue").val(data.voltage);
      },
      error: function(jqXHR, textStatus, errorThrown) {
        alert("Error: " + errorThrown);
      }
    });
  });

  $("#platformInformationVoltagesBatterySubmit").click(function() {
    $("#platformInformationVoltagesBatteryValue").val("?");
    $.ajax({
      method: "GET",
      url: "/v1/platform/voltages/battery",
      dataType: "json",
      success: function(data) {
        $("#platformInformationVoltagesBatteryValue").val(data.voltage);
      },
      error: function(jqXHR, textStatus, errorThrown) {
        alert("Error: " + errorThrown);
      }
    });
  });

  $("#blinkersSubmit").click(function() {
    var url = "/v1/blinkers";
    if ($("#blinkersId").val() != "both") {
      url = url + "/" + encodeURIComponent($("#blinkersId").val());
    }
    $.ajax({
      method: "PUT",
      url: url,
      data: JSON.stringify({state: $("#blinkersState").val()}),
      contentType: "application/json; charset=UTF-8",
      error: function(jqXHR, textStatus, errorThrown) {
        alert("Error: " + errorThrown);
      }
    });
  });

  $("#eyesSubmit").click(function() {
    var url = "/v1/eyes";
    if ($("#eyesId").val() != "both") {
      url = url + "/" + encodeURIComponent($("#eyesId").val());
    }
    $.ajax({
      method: "PUT",
      url: url,
      data: JSON.stringify({
        red: $("#eyesRed").val(),
        blue: $("#eyesBlue").val(),
        green: $("#eyesGreen").val()
      }),
      contentType: "application/json; charset=UTF-8",
      error: function(jqXHR, textStatus, errorThrown) {
        alert("Error: " + errorThrown);
      }
    });
  });

  $("#motorsDriveSubmit").click(function() {
    data = {
      direction: $("#motorsDriveDirection").val(),
      speed: $("#motorsDriveSpeed").val()
    }
    if ($("#motorsDriveDistance").val() != "") {
      data.distance = $("#motorsDriveDistance").val();
    }
    $.ajax({
      method: "POST",
      url: "/v1/motors/drive",
      data: JSON.stringify(data),
      contentType: "application/json; charset=UTF-8",
      error: function(jqXHR, textStatus, errorThrown) {
        alert("Error: " + errorThrown);
      }
    });
  });

  $("#motorsTurnSubmit").click(function() {
    data = {
      direction: $("#motorsTurnDirection").val(),
      speed: $("#motorsTurnSpeed").val()
    }
    if ($("#motorsTurnDegrees").val() != "") {
      data.degrees = $("#motorsTurnDegrees").val();
    }
    $.ajax({
      method: "POST",
      url: "/v1/motors/turn",
      data: JSON.stringify(data),
      contentType: "application/json; charset=UTF-8",
      error: function(jqXHR, textStatus, errorThrown) {
        alert("Error: " + errorThrown);
      }
    });
  });

  $("#motorsMoveSubmit").click(function() {
    $.ajax({
      method: "POST",
      url: "/v1/motors/move",
      data: JSON.stringify({
        left_direction: $("#motorsMoveLeftDirection").val(),
        left_speed: $("#motorsMoveLeftSpeed").val(),
        right_direction: $("#motorsMoveRightDirection").val(),
        right_speed: $("#motorsMoveRightSpeed").val(),
      }),
      contentType: "application/json; charset=UTF-8",
      error: function(jqXHR, textStatus, errorThrown) {
        alert("Error: " + errorThrown);
      }
    });
  });

  $("#motorsStopSubmit").click(function() {
    $.ajax({
      method: "POST",
      url: "/v1/motors/stop",
      error: function(jqXHR, textStatus, errorThrown) {
        alert("Error: " + errorThrown);
      }
    });
  });

  $("#motorsStatusSubmit").click(function() {
    $.ajax({
      method: "GET",
      url: "/v1/motors/status",
      dataType: "json",
      success: function(data) {
        $("#motorStatusValue").val(
          $("#motorStatusValue").val() + "\n" +
          data.left.flags.toString().padStart(5) + " " +
          data.left.power.toString().padStart(5) + " " +
          data.left.encoder.toString().padStart(7) + " " +
          data.left.dps.toString().padStart(4) + " | " +
          data.right.flags.toString().padStart(5) + " " +
          data.right.power.toString().padStart(5) + " " +
          data.right.encoder.toString().padStart(7) + " " +
          data.right.dps.toString().padStart(4)
          );
          $('#motorStatusValue').scrollTop($('#motorStatusValue')[0].scrollHeight);
      },
      error: function(jqXHR, textStatus, errorThrown) {
        alert("Error: " + errorThrown);
      }
    });
  });

  var motorStatusValueHeader = "Flags Power Encoder  dps | Flags Power Encoder  dps"

  $("#motorsStatusClear").click(function() {
    $("#motorStatusValue").val(motorStatusValueHeader);
  });

  // initial header
  $("#motorStatusValue").val(motorStatusValueHeader);

  $("#sensorsDistanceSubmit").click(function() {
    $("#sensorsDistanceValue").val("?");
    $.ajax({
      method: "GET",
      url: "/v1/sensors/I2C/distance/distance",
      dataType: "json",
      success: function(data) {
        $("#sensorsDistanceValue").val(data.distance);
      },
      error: function(jqXHR, textStatus, errorThrown) {
        alert("Error: " + errorThrown);
      }
    });
  });

});
