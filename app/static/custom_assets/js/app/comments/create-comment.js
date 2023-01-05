async function createComment() {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let form_data = new FormData();
    form_data.append('comment', editor.getData());
    const response = await fetch(`../task/${$("#selected_task").val()}/comments/create`,{
        method: 'POST',
        mode: 'same-origin',
        body: form_data,
        headers:{
            'X-CSRFToken': csrftoken
        }
    });
    return await response.json();
}
function addComment(object){
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
    let spanName = document.createElement("span");
    spanName.innerHTML = `${ object.user.first_name } ${ object.user.last_name }`;
    spanName.className = "fs-6 fw-bold";
    let divName = document.createElement("div");
    divName.appendChild(spanName);

    // Create a span element for the date of the comment and add it to a div element
    const dateTimeObject = new Date(object.created);
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
    divHeaderComment.appendChild(divName);
    divHeaderComment.appendChild(divDate);

    // Create a div element for the content of the comment and add the description as its inner HTML. Resize any images within the description if necessary.
    let divComment= document.createElement("div");
    divComment.className="content-comment py-3 row";
    divComment.innerHTML+=object.description;
    let imgS = divComment.querySelectorAll("img");
    imgS.forEach(img => {
        if(img.width > 575){
            let ratio = img.height/img.width;
            img.width = 575;
            img.height = ratio*img.width;
        }
    })
    divComment.addEventListener("resize",()=>{
        imgS.forEach(img => {
            if(img.width > 575){
                let ratio = img.height/img.width;
                img.width = divComment.offsetWidth;
                img.height = ratio*img.width;
            }
        })
    })

    // Create a button element for the delete action
    let deleteBtn = document.createElement("button");
    deleteBtn.innerHTML = "Delete";
    deleteBtn.classList.add("btn","btn-link","btn-sm","mx-2","fw-bold","delete-comment");

    // Create a button element for the edit action
    let editBtn = document.createElement("button");
    editBtn.innerHTML = "Edit";
    editBtn.classList.add("btn","btn-link","btn-sm","fw-bold","edit-comment");

    // Create a div element for the container of the delete and edit buttons
    let divContainerAction = document.createElement("div");
    divContainerAction.className="action-comment d-flex justify-content-end my-2";
    divContainerAction.appendChild(editBtn);
    divContainerAction.appendChild(deleteBtn);

    // Create a div element for the CKEditor instance and add the toolbar and editor div elements to it
    let divContainerCkeditor = document.createElement("div");
    divContainerCkeditor.className="d-none";

    // Create div elements for the toolbar and editor of the CKEditor instance
    let divCkeditorToolbar = document.createElement("div");
    divCkeditorToolbar.setAttribute("id",`edit_ckeditortoolbar_${object.id}`);

    // Add the toolbar and editor div elements to the container
    let divCkeditor = document.createElement("div");
    divCkeditor.setAttribute("id",`edit-ckeditor-${object.id}`);
    divContainerCkeditor.appendChild(divCkeditorToolbar);
    divContainerCkeditor.appendChild(divCkeditor);


    // Create a div element for the container of the save and cancel buttons for the edit action (Comment's Ckeditor)
    let divContainerActionCkeditor = document.createElement("div");
    divContainerActionCkeditor.className = "d-flex justify-content-end my-2 d-none";

    // Create button elements for the save and cancel actions
    let saveBtn = document.createElement("button");
    saveBtn.className = "btn btn-primary btn-sm mx-2";
    saveBtn.setAttribute("id",`save_updateComment_${object.id}`)
    saveBtn.innerHTML = "Save";
    let cancelBtn = document.createElement("button");
    cancelBtn.className = "btn btn-secondary btn-sm ";
    cancelBtn.setAttribute("id",`cancel_updateComment_${object.id}`)
    cancelBtn.innerHTML = "Cancel";

    // Add the save and cancel buttons to the container
    divContainerActionCkeditor.appendChild(saveBtn);
    divContainerActionCkeditor.appendChild(cancelBtn);


    // Create a div element for the entire comment and add all the other div elements as well as the comment object itself to it
    let col2 = document.createElement("div");
    col2.className="col-md-10";
    col2.appendChild(divHeaderComment);
    col2.appendChild(divComment);
    col2.appendChild(divContainerAction);
    col2.appendChild(divContainerCkeditor);
    col2.appendChild(divContainerActionCkeditor);

    // Create row for the comment object
    let row = document.createElement("div");
    row.className="comment-object row";
    // Append the image and content columns to the row
    row.appendChild(col1);
    row.appendChild(col2);
    row.setAttribute("id", `comment_${object.id}`)
    // Insert the row at the beginning of the comments element
    document.getElementById("comments").prepend(row);

    let editor;
    // Create a new CKEditor instance and append its toolbar to the container
    DecoupledEditor
        .create(document.querySelector(`#edit-ckeditor-${object.id}`),{
            ckfinder: {
                uploadUrl: '/ckeditor/upload/'
            },
            filebrowserUpload: function( file ) {
                const maxSize = 500000;

                if (file.data.size > maxSize) {
                    file.preventDefault();
                    alert("The image size is too large.");
                }
            }
        })
        .then(newEditor => {
            editor = newEditor;
            const toolbarContainer = document.querySelector( `#edit_ckeditortoolbar_${object.id}`);
            console.log( 'Editor was initialized', editor );
            toolbarContainer.appendChild( editor.ui.view.toolbar.element );
        })
        .catch(error => {
            console.error(error);
        });

    // Set up the delete button to display a confirmation dialog
    deleteBtn.addEventListener('click',(e)=>{
        e.preventDefault();
        Swal.fire({
            text:"Are you sure you want to delete this comment?",
            icon:"warning",
            showCancelButton:!0,
            buttonsStyling:!1,
            confirmButtonText:"Yes, delete!",
            cancelButtonText:"No, cancel",
            customClass:{
                confirmButton:"btn fw-bold btn-danger",
                cancelButton:"btn fw-bold btn-active-light-primary"
            }
        }).then((result)=>{
            if(result.isConfirmed) {
                deleteComment(object.id).then(r => console.log(r));

            } else {
                console.log(result.isConfirmed)
            }
        });
    });


    // s function shows the CKEditor and hide the comment and action buttons
    const s = (divComment,divContainerAction,divContainerCkeditor,divContainerActionCkeditor,editor,data)=>{
        divComment.classList.add('d-none'); // hide the comment
        divContainerAction.classList.add('d-none'); // hide the action buttons
        divContainerCkeditor.classList.remove('d-none'); // show the CKEditor
        divContainerActionCkeditor.classList.remove('d-none'); // Show the CKEditor action buttons
        editor.setData(data); // set the CKEditor data to the comment text
    }
    const h = (divComment,divContainerAction,divContainerCkeditor,divContainerActionCkeditor,editor,data)=>{
        divComment.classList.remove('d-none');
        divContainerAction.classList.remove('d-none');
        divContainerCkeditor.classList.add('d-none');
        divContainerActionCkeditor.classList.add('d-none');
        editor.setData(data);
    }
    // Set up the save button to save comment's updates
    saveBtn.addEventListener("click",(e)=>{
        e.preventDefault();
        updateComment(object.id, editor.getData()).then(data => {
            // (data!==undefined) && (divComment.innerHTML=editor.getData());
            if (data!==undefined){
                divComment.innerHTML=data.description;
            }
            h(divComment,divContainerAction,divContainerCkeditor,divContainerActionCkeditor,editor,"");
        });

    })
    // When the "Edit" button is clicked, show the CKEditor and hide the comment and action buttons
    editBtn.addEventListener('click',(e)=>{
        e.preventDefault();
        s(divComment,divContainerAction,divContainerCkeditor,divContainerActionCkeditor,editor,object.description);
    })
    // When the "Cancel" button is clicked, hide the CKEditor and show the comment and action buttons
    cancelBtn.addEventListener('click',(e)=>{
        e.preventDefault();
        h(divComment,divContainerAction,divContainerCkeditor,divContainerActionCkeditor,editor,"");
    })

}

const inputElementDiv = document.querySelector('#comment_input').parentNode;
const inputCkEditorDiv = document.querySelector('#kt_docs_ckeditor_document').parentNode;
const btnSaveComment= document.querySelector('#save_comment');
const btnCancelComment = document.querySelector('#cancel_comment');

function showCkeditor(){
    inputElementDiv.classList.add('d-none');
    inputCkEditorDiv.classList.remove('d-none');
    btnSaveComment.parentNode.classList.remove('d-none');
}
function hideCkeditor(){
    inputElementDiv.classList.remove('d-none');
    inputCkEditorDiv.classList.add('d-none');
    btnSaveComment.parentNode.classList.add('d-none');
    editor.setData("");
}
inputElementDiv.addEventListener('click', showCkeditor);
btnCancelComment.addEventListener('click', hideCkeditor);
btnSaveComment.addEventListener('click', ()=>{
    createComment().then(data => addComment(data));
    hideCkeditor();
});