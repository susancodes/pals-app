var WebSocketServer = require("ws").Server;
var http = require("http");
var express = require("express");
var app = express();
var port = process.env.PORT || 5000;

app.use(express.static(__dirname + "/"));

var server = http.createServer(app);
server.listen(port);

console.log("http server listening on %d", port);

var wss = new WebSocketServer({server: server});
console.log("websocket server created");

var users = 0;
// 0 is on; 1 is off
var switch1 = 0;
var switch2 = 0;
var switch3 = 0;

wss.on("connection", function(ws) {
  users++;
  var obj = {users: users, switch1: switch1, switch2: switch2, switch3: switch3};
  wss.broadcast(JSON.stringify(obj));

  console.log("websocket connection open");
  ws.on("close", function() {
    console.log("websocket connection close");
    users--;
    obj.users = users;
    wss.broadcast(JSON.stringify(obj));

  })

  ws.on("message", function (message) {
	wss.broadcast(message);
	var messageobj = JSON.parse(message);
	switch1 = messageobj.switch1;
	switch2 = messageobj.switch2;
	switch3 = messageobj.switch3;
  })

})


wss.broadcast = function broadcast(data) {
	wss.clients.forEach(function each(client) {
		client.send(data);
	});
};