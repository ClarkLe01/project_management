const socket = new WebSocket(`ws://${window.location.host}/ws/notifications/`);

socket.onopen = function() {
  console.log("WebSocket connection opened");
};

socket.onclose = function() {
  console.log("WebSocket connection closed");
};

socket.onmessage = function(e) {
  let data = JSON.parse(event.data);
  console.log(data)
// displayNotification(*params)
};

// function displayNotification(title, message, user, created) {
//   // check if the notification is for the current user
//   if (user === current_user_id) {
//     // display the notification
//     const notificationDiv = document.createElement("div");
//     notificationDiv.innerHTML = `<strong>${title}</strong>: ${message}`;
//     document.getElementById("notifications").appendChild(notificationDiv);
//   }
//   const notificationContainer = document.getElementById("notification-container");
//   const notification = document.createElement("div");
//   notification.innerHTML = `<h3>${title}</h3><p>${message}</p>`;
//   notificationContainer.appendChild(notification);
// }