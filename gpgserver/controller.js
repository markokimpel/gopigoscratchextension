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

  $("#switchSubmit").click(function() {
    $("#switchState").val("?");
    $.ajax({
      method: "GET",
      url: "/v1/switch/" + encodeURIComponent($("#switchNo").val()),
      dataType: "json",
      success: function(data) {
        $("#switchState").val(data.state);
      },
      error: function(jqXHR, textStatus, errorThrown) {
        alert("Error: " + errorThrown);
      }
    });
  });

  $("#moveSubmit").click(function() {
    $.ajax({
      method: "POST",
      url: "/v1/move",
      data: JSON.stringify({
        direction: $("#moveDirection").val(),
        speed: $("#moveSpeed").val(),
        duration: $("#moveDuration").val()
      }),
      contentType: "application/json; charset=UTF-8",
      error: function(jqXHR, textStatus, errorThrown) {
        alert("Error: " + errorThrown);
      }
    });
  });

  $("#motorsSubmit").click(function() {
    $.ajax({
      method: "POST",
      url: "/v1/motors",
      data: JSON.stringify({
        left_direction: $("#motorsLeftDirection").val(),
        left_speed: $("#motorsLeftSpeed").val(),
        right_direction: $("#motorsRightDirection").val(),
        right_speed: $("#motorsRightSpeed").val(),
      }),
      contentType: "application/json; charset=UTF-8",
      error: function(jqXHR, textStatus, errorThrown) {
        alert("Error: " + errorThrown);
      }
    });
  });

  $("#stopSubmit").click(function() {
    $.ajax({
      method: "POST",
      url: "/v1/stop",
      error: function(jqXHR, textStatus, errorThrown) {
        alert("Error: " + errorThrown);
      }
    });
  });

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
