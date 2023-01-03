async function updateTaskStatus(id, status) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let form_data = new FormData();
    form_data.append('task_status', status);
    const response = await fetch(`task/${id}/update`,{
        method: 'POST',
        mode: 'same-origin',
        body: form_data,
        headers:{
            'X-CSRFToken': csrftoken
        }
    });
    if(response.status===200){
        console.log("Update status successfully");
    }
    else{
        console.log("Error: " + response.status);
    }
}

async function deleteComment(id) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let form_data = new FormData();
    form_data.append('comment_id', id);
    const response = await fetch(`comments/delete`,{
        method: 'POST',
        mode: 'same-origin',
        body: form_data,
        headers:{
            'X-CSRFToken': csrftoken
        }
    });
    if(response.status===200){
        console.log("Delete comment id");
        document.getElementById(`row_${id}`).remove();
    }
    else{
        console.log("Error: " + response.status);
    }
}

async function createComment(id) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let form_data = new FormData();
    form_data.append('comment_id', id);
    const response = await fetch(`comments/delete`,{
        method: 'POST',
        mode: 'same-origin',
        body: form_data,
        headers:{
            'X-CSRFToken': csrftoken
        }
    });
    if(response.status===200){
        console.log("Update status successfully");
    }
    else{
        console.log("Error: " + response.status);
    }
}

async function updateComment(id) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let form_data = new FormData();
    form_data.append('comment_id', id);
    const response = await fetch(`comments/delete`,{
        method: 'POST',
        mode: 'same-origin',
        body: form_data,
        headers:{
            'X-CSRFToken': csrftoken
        }
    });
    if(response.status===200){
        console.log("Update status successfully");
    }
    else{
        console.log("Error: " + response.status);
    }
}


function addComment(object){
    /*This is Col with class col-md-1*/
    let img = document.createElement("img");
    img.className = "h-30px w-30px symbol-label";
    img.setAttribute("alt", "");
    object.user.avatar!=null
        ? img.setAttribute("src", `${object.user.avatar}`)
        : img.setAttribute("src", "/static/assets/media/avatars/blank.png");
    let divImg = document.createElement("div");
    divImg.className = "symbol symbol-50px symbol-circle";
    divImg.appendChild(img);
    let col1 = document.createElement("div");
    col1.className="col-md-1";
    col1.appendChild(divImg);


    /*This is Col with class col-md-10*/
    // create div name user
    let spanName = document.createElement("span");
    spanName.innerHTML = `${ object.user.first_name } ${ object.user.last_name }`;
    spanName.className = "fs-6 fw-bold";
    let divName = document.createElement("div");
    divName.appendChild(spanName);

    // create div date comment
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

    // create div header comment contains date and username
    let divHeaderComment = document.createElement("div");
    divHeaderComment.className="header-comment d-flex"
    divHeaderComment.appendChild(divName);
    divHeaderComment.appendChild(divDate);

    // create div content comment
    let divComment= document.createElement("div");
    divComment.className="content-comment py-3 row";
    divComment.innerHTML+=object.description;

    // create button delete
    let deleteBtn = document.createElement("button");
    deleteBtn.innerHTML = "Delete";
    deleteBtn.classList.add("btn","btn-link","btn-sm","mx-2","fw-bold","edit-comment");

    // create button edit
    let editBtn = document.createElement("button");
    editBtn.innerHTML = "Edit";
    editBtn.classList.add("btn","btn-link","btn-sm","fw-bold","delete-comment");

    // create div container contains delete and edit button
    let divContainerAction = document.createElement("div");
    divContainerAction.className="action-comment d-flex justify-content-end my-2";
    divContainerAction.appendChild(editBtn);
    divContainerAction.appendChild(deleteBtn);

    // create div container col-md-10 contains header, content and action.
    let col2 = document.createElement("div");
    col2.className="col-md-10";
    col2.appendChild(divHeaderComment);
    col2.appendChild(divComment);
    col2.appendChild(divContainerAction);

    /*This is row for each object*/
    let row = document.createElement("div");
    row.className="row";
    row.appendChild(col1);
    row.appendChild(col2);
    row.setAttribute("id", `row_${object.id}`)
    document.getElementById("kt_comments").appendChild(row);

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
    editBtn.addEventListener('click',(e)=>{
        e.preventDefault();
        console.log(object.id);
    })

}

function removeAllComment() {
    let parent = document.getElementById("kt_comments");
    const comments = parent.querySelectorAll('.comment-object');
    comments.forEach(comment => comment.remove());
}


fetch(`detail/${$("#project_id").val()}/tasklistapi`)
    .then(res => res.json())
    .then(data => {
        let id = '#kt_docs_jkanban_basic';
        const element = document.querySelector("#kt_docs_jkanban_basic")
        const kanbanHeight = element.getAttribute('data-jkanban-height');
        let backlog_data = [], todo_data=[], working_data = [], done_data = [];
        data.forEach(e=>{
            if(e.status === 'backlog') {
                backlog_data.push({'id': e.id, 'title': e.title})
            } else if(e.status === 'todo'){
                todo_data.push({'id': e.id, 'title': e.title})
            } else if(e.status === 'working'){
                working_data.push({'id': e.id, 'title': e.title})
            } else if(e.status === 'done'){
                done_data.push({'id': e.id, 'title': e.title})
            }
        });
        let boards = [
            {
                'id': 'backlog',
                'title': 'BackLog',
                'class': 'card-title, dark',
                'item': backlog_data
            },
            {
                'id': 'todo',
                'title': 'To Do',
                'class': 'card-title, warning',
                'item': todo_data
            },
            {
                'id': 'working',
                'title': 'Working',
                'class': 'card-title, danger',
                'item': working_data
            },
            {
                'id': 'done',
                'title': 'Done',
                'class': 'card-title, success',
                'item': done_data
            }
        ];
        let kanban = new jKanban({
            element: id,
            gutter: '0',
            widthBoard: '270px',
            responsivePercentage: false,
            dragBoards: false,
            boards: boards,
            // Handle item scrolling
            dragEl: function (el, source) {
                document.addEventListener('mousemove', isDragging);
            },

            dragendEl: function (el) {
                console.log('dragendEl')
                updateTaskStatus(el.dataset.eid, kanban.getParentBoardID(el.dataset.eid)).then(r => console.log('r'));
                document.removeEventListener('mousemove', isDragging);
            },

            click: function (el) {
                fetch(`task/${el.dataset.eid}`).then(res => res.json())
                    .then(data => {
                        $("#selected_task").val(data.id);
                        $("#update_task_title").val(data.title);
                        const fp = flatpickr($("#update_due_date"),{});
                        fp.setDate(data.due_date);
                        $("#update_task_details").val(data.task_details);
                        console.log(data.status)
                        let status = {
                            "backlog": 0,
                            "todo": 1,
                            "working": 2,
                            "done": 3,
                        }
                        console.log(status[data.status])
                        $("#update_task_status").select2("val",status[data.status].toString());
                        $("#update_task_assign").select2("val",data.assignee.toString());
                    });
                fetch(`task/${el.dataset.eid}/comments`).then(res => res.json())
                    .then(data => {
                        data.forEach(comment => {
                            addComment(comment);
                        })
                    });
                $("#kt_modal_update_task").modal("show");
            },
        });
        $('#kt_modal_update_task').on('hidden.bs.modal', function (e) {
            $("#selected_task").val('');
            removeAllComment();
        })

        const allBoards = document.querySelectorAll('.kanban-drag');
        allBoards.forEach(board => {
            board.style.maxHeight = kanbanHeight + 'px';
        });

        const isDragging = (e) => {
            const allBoards = document.querySelectorAll('.kanban-drag');
            allBoards.forEach(board => {
                // Get inner item element
                const dragItem = board.querySelector('.gu-transit');

                // Stop drag on inactive board
                if (!dragItem) {
                    return;
                }

                // Get jKanban drag container
                const containerRect = board.getBoundingClientRect();

                // Get inner item size
                const itemSize = dragItem.offsetHeight;

                // Get dragging element position
                const dragMirror = document.querySelector('.gu-mirror');
                const mirrorRect = dragMirror.getBoundingClientRect();

                // Calculate drag element vs jKanban container
                const topDiff = mirrorRect.top - containerRect.top;
                const bottomDiff = containerRect.bottom - mirrorRect.bottom;

                // Scroll container
                if (topDiff <= itemSize) {
                    // Scroll up if item at top of container
                    board.scroll({
                        top: board.scrollTop - 3,
                    });
                } else if (bottomDiff <= itemSize) {
                    // Scroll down if item at bottom of container
                    board.scroll({
                        top: board.scrollTop + 3,
                    });
                } else {
                    // Stop scroll if item in middle of container
                    board.scroll({
                        top: board.scrollTop,
                    });
                }
            });
        }
        let editBtns = document.querySelectorAll(".edit-comment");

        let kanbanBoardTitles = document.querySelectorAll('.kanban-title-board');
        let kanbanBoardMains = document.querySelectorAll('.kanban-drag');
        let kanbanBoardItems = document.querySelectorAll('.kanban-item');
        let kanbanBoardFooters = document.querySelectorAll('.kanban-container>div>footer');
        kanbanBoardTitles.forEach(t=>{
            t.classList.add('d-flex');
            t.classList.add('justify-content-center');
        });
        kanbanBoardMains.forEach(t=>{
            t.classList.add('card');
        });
        kanbanBoardItems.forEach(t=>{
            t.classList.add('fw-bold');
            // t.setAttribute("data-bs-toggle", "modal");
            // t.setAttribute("data-bs-target", `#kt_modal_update_task_${t.dataset.eid}`);
        });
        kanbanBoardFooters.forEach(t=>{
            t.classList.add('d-flex');
            t.classList.add('justify-content-center');
        });
        let createTaskKanbanBtn = document.createElement("button");
        createTaskKanbanBtn.setAttribute("class", "btn btn-primary er w-100 fs-6 px-8 my-4");
        createTaskKanbanBtn.setAttribute("data-bs-toggle", "modal");
        createTaskKanbanBtn.setAttribute("data-bs-target", "#kt_modal_new_task");
        createTaskKanbanBtn.innerHTML += "Create New Task";
        kanbanBoardFooters[0].appendChild(createTaskKanbanBtn)
        createTaskKanbanBtn.addEventListener('click',(e)=>{
            e.preventDefault();
            console.log("Create New Task")
        })

    })
    .catch((error) => {
        console.error('Error:', error);
    });



