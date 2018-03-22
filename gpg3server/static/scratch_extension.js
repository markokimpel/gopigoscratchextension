(function(ext) {

  // host_port in double curly brackets is a placeholder that is replaced by
  // the server before sending to the client.
  var baseUrl = "http://{{host_port}}";

  ext._shutdown = function() {};

  ext._getStatus = function() {
    // TODO: do some connection/version tests
    return {status: 2, msg: 'Ready'};
  };

  // async command 'set led'
  ext.setLed = function(ledNo, state, callback) {
    $.ajax({
      method: "POST",
      url: baseUrl + "/v1/led/" + encodeURIComponent(ledNo),
      data: JSON.stringify({state: state}),
      contentType: "application/json; charset=UTF-8",
      complete: function(jqXHR, textStatus) {
        callback();
      }
    });
  };

  // async reporter 'switch X state'
  ext.switchState = function(switchNo, callback) {
    $.ajax({
      method: "GET",
      url: baseUrl + "/v1/switch/" + encodeURIComponent(switchNo),
      dataType: "json",
      success: function(data) {
        callback(data.state == 'closed' ? '1' : '0');
      },
      error: function(jqXHR, textStatus, errorThrown) {
        callback(false);
      }
    });
  };

  // async command 'move'
  ext.move = function(direction, speed, duration, callback) {
    $.ajax({
      method: "POST",
      url: baseUrl + "/v1/move",
      data: JSON.stringify({
        direction: direction,
        speed: speed,
        duration: duration
      }),
      contentType: "application/json; charset=UTF-8",
      complete: function(jqXHR, textStatus) {
        callback();
      }
    });
  };

  // async command 'turn'
  ext.turn = function(direction, speed, duration, callback) {
    // The blocks 'move' and 'turn' share the same implementation. Scratch
    // requires each block to use a dedicated method, otherwise it will it will
    // mix up blocks.
    this.move(direction, speed, duration, callback);
  };

  // async command 'move continously'
  ext.moveContinously = function(direction, speed, callback) {
    // duration '0' means forever
    this.move(direction, speed, 0, callback);
  };

  // async command 'turn continously'
  ext.turnContinously = function(direction, speed, callback) {
    // The blocks 'moveContinously' and 'turnContinously' share the same
    // implementation. Scratch requires each block to use a dedicated method,
    // otherwise it will it will mix up blocks.

    // duration '0' means forever
    this.move(direction, speed, 0, callback);
  };

  // async command 'set motors'
  ext.setMotors = function(leftDirection, leftSpeed, rightDirection, rightSpeed, callback) {
    $.ajax({
      method: "POST",
      url: baseUrl + "/v1/motors",
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

  // async command 'stop motors'
  ext.stopMotors = function(callback) {
    $.ajax({
      method: "POST",
      url: baseUrl + "/v1/stop",
      complete: function(jqXHR, textStatus) {
        callback();
      }
    });
  };

  // async reporter 'distance'
  ext.getDistance = function(callback) {
    $.ajax({
      method: "GET",
      url: baseUrl + "/v1/distance",
      dataType: "json",
      success: function(data) {
        callback(data.distance);
      },
      error: function(jqXHR, textStatus, errorThrown) {
        callback(-1.0);
      }
    });
  };

  // Block and block menu descriptions
  var descriptor = {
    blocks: [
      ['w', 'set led %m.ledNo %m.onOff',                     'setLed', '1', 'on' ],

      // Scratch does not support asynchronous boolean reporters (e.g. to
      // implement 'switch x closed?'). So make it an asynchronous value
      // reporter.
      ['R', 'switch %m.switchNo state',                      'switchState', 1 ],

      ['w', 'move %m.forwardReverse speed %n % for %n secs', 'move', 'forward', 50, 1 ],
      ['w', 'turn %m.rightLeft speed %n % for %n secs',      'turn', 'right', 50, 1 ],

      ['w', 'move %m.forwardReverse speed %n %',             'moveContinously', 'forward', 50 ],
      ['w', 'turn %m.rightLeft speed %n %',                  'turnContinously', 'right', 50 ],
      ['w', 'set motors left %m.forwardReverse speed %n % right %m.forwardReverse speed %n %',
                                                             'setMotors', 'forward', 50, 'forward', 50 ],
      ['w', 'stop motors',                                   'stopMotors' ],

      ['R', 'distance',                                      'getDistance' ]
    ],
    menus: {
      ledNo:          [ '1', '2' ],
      onOff:          [ 'on', 'off' ],
      switchNo:       [ '1', '2' ],
      forwardReverse: [ 'forward', 'reverse' ],
      rightLeft:      [ 'right', 'left']
    },
    url: 'https://github.com/markokimpel/rrbscratchextension'
  };

  // Register the extension
  ScratchExtensions.register('RasPiRobot Board 3', descriptor, ext);

})({});
