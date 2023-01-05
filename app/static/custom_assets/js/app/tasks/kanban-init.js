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
                fetch(`../task/${el.dataset.eid}`).then(res => res.json())
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
                fetch(`../task/${el.dataset.eid}/comments`,{mode: 'cors'}).then(res => res.json())
                    .then(data => {
                        data.forEach(comment => {
                            addComment(comment);
                        })
                    });
                $("#kt_modal_update_task").modal("show");
            },
        });
        let ktUpdateModalTask = $("#kt_modal_update_task");
        ktUpdateModalTask.on('hidden.bs.modal', function (e) {
            console.log("hide");
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



