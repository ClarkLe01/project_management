function addNotification(data){
  let img = document.createElement("img");
  data.changed_by.avatar != null
      ? img.setAttribute("src", `${data.changed_by.avatar}`)
      : img.setAttribute("src", "/static/assets/media/avatars/blank.png");
  let notification = document.createElement("div");
  notification.className = "d-flex flex-stack py-4";
  notification.innerHTML = `
            <div class="d-flex align-items-center">
                <div class="symbol symbol-35px me-4">
                    <span class="symbol-label bg-light-primary">
                        <span class="svg-icon svg-icon-2 svg-icon-primary">
                            <img src="${data.changed_by.avatar}" width="30" height="30">
                        </span>
                    </span>
                </div>
                <div class="mb-0 me-2">
                    <a href="#" >
                        <span class="fs-6 text-gray-800 text-hover-primary fw-bold">${data.changed_by.first_name} ${data.changed_by.last_name}</span>
                        <span class="fs-6 text-gray-800">${data.message}</span>
                    </a>
                </div>
            </div>
        `;
  let created_time_element = document.createElement("span");
  created_time_element.classList.add("badge", "badge-light", "fs-8");
  created_time_element.setAttribute("data-created-time", data.created);
  created_time_element.innerHTML = moment(data.created).fromNow();
  notification.appendChild(created_time_element);
  document.getElementById("notification-container").insertBefore(notification, document.getElementById("notification-container").firstChild);
}

const socket = new WebSocket(`ws://${window.location.host}/ws/notifications/`);
socket.onopen = function() {
  console.log("WebSocket connection opened");
};
socket.onclose = function() {
  console.log("WebSocket connection closed");
};
socket.onmessage = function(e) {
  let data = JSON.parse(event.data);
  console.log(data);
  console.log("data" in data);
  if ("data" in data){
    data = JSON.parse(data.data.value);
    let notHasNotificationReport = document.getElementById("no-notification");
    if (notHasNotificationReport != null){
      notHasNotificationReport.remove();
    }
    addNotification(data)
  }
// displayNotification(*params)
};

setInterval(() => {
  let time_elements = document.querySelectorAll("[data-created-time]");
  time_elements.forEach(element => {
    let time = element.getAttribute("data-created-time");
    element.innerHTML = moment(time).fromNow();
  });
}, 60000);


fetch(`${window.location.origin}/notification`,{mode: 'cors'}).then(res => res.json())
    .then(data => {
      console.log(data.length);
      if(data.length > 0){
        data.forEach(notification => {addNotification(notification)});
      }
      else {
        let notification = document.createElement("div");
        notification.className = "d-flex flex-stack py-4";
        notification.innerHTML = `
                <div class="d-flex align-items-center" id="no-notification">
                    You dont have any notifications
                </div>
        `;
        document.getElementById("notification-container").insertBefore(notification, document.getElementById("notification-container").firstChild);
      }
    });