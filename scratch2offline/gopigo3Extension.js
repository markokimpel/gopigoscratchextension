// Load and execute scratch extension from local GoPiGo3 Server.
$.ajax({
  url: "http://localhost:8080/scratch_extension.js",
  dataType: 'script',
  cache: true
});
