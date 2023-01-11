function addHistory(object){
    // Create and set up the element for displaying the avatar of the user who made the comment
    let img = document.createElement("img");
    img.className = "h-30px w-30px symbol-label";
    img.setAttribute("alt", "");
    object.user.avatar!=null
        ? img.setAttribute("src", `${object.user.avatar}`) // Set the src attribute to the user's avatar if it exists
        : img.setAttribute("src", "/static/assets/media/avatars/blank.png"); // Set the src attribute to a default image if the user doesn't have an avatar
    let divImg = document.createElement("div");
    divImg.className = "symbol symbol-50px symbol-circle";
    divImg.appendChild(img);
    let col1 = document.createElement("div");
    col1.className="col-md-1";
    col1.appendChild(divImg);

    // Create a span element for the user's name and add it to a div element
    let spanContent = document.createElement("span");
    spanContent.innerHTML = `<b>${ object.user.first_name } ${ object.user.last_name }</b> ${object.action} <b>${ object.object}`;
    spanContent.className = "fs-6";
    let divContent = document.createElement("div");
    divContent.appendChild(spanContent);

    // Create a span element for the date of the comment and add it to a div element
    const dateTimeObject = new Date(object.date);
    const options = {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "numeric",
        minute: "numeric",
        hour12: true
    };
    const formattedDate = new Intl.DateTimeFormat("en-US", options).format(dateTimeObject);
    let spanDate = document.createElement("span");
    spanDate.className="fs-6 text-gray-400";
    spanDate.innerHTML = formattedDate;
    let divDate = document.createElement("div");
    divDate.className="time-comment mx-3";
    divDate.appendChild(spanDate);

    // Create a div element for the header of the comment and add the div elements for the user's name and the date to it
    let divHeaderComment = document.createElement("div");
    divHeaderComment.className="header-comment d-flex"
    divHeaderComment.appendChild(divContent);
    divHeaderComment.appendChild(divDate);

    // Create a div element for the entire comment and add all the other div elements as well as the comment object itself to it
    let col2 = document.createElement("div");
    col2.className="col-md-10";
    col2.appendChild(divHeaderComment);

    // Create row for the comment object
    let row = document.createElement("div");
    row.className="history-object row";
    // Append the image and content columns to the row
    row.appendChild(col1);
    row.appendChild(col2);
    row.setAttribute("id", `history_${object.id}`)
    // Insert the row at the beginning of the comments element
    document.getElementById("histories").prepend(row);
}