let id = '#kt_docs_jkanban_basic';
const element = document.querySelector("#kt_docs_jkanban_basic")

// Get kanban height value
const kanbanHeight = element.getAttribute('data-jkanban-height');

let kanban = new jKanban({
    element: id,
    gutter: '0',
    widthBoard: '270px',
    responsivePercentage: false,
    dragBoards: false,
    boards: [
        {
            'id': 'backlog',
            'title': 'BackLog',
            'class': 'card-title, dark',
            'item': [
                {
                    "id": 1,
                    'title': 'I am 1'
                },
                {
                    "id": 2,
                    'title': 'I am 2'
                }
            ]
        },
        {
            'id': 'inprocess',
            'title': 'In Process',
            'class': 'card-title, warning',
            'item': [
                {
                    "id": 3,
                    'title': 'I am 3'
                },
                {
                    "id": 4,
                    'title': 'I am 4'
                }
            ]
        },
        {
            'id': 'working',
            'title': 'Working',
            'class': 'card-title, danger',
            'item': [
                {
                    "id": 5,
                    'title': 'I am 5'
                },
                {
                    "id": 6,
                    'title': 'I am 6'
                }
            ]
        },
        {
            'id': 'done',
            'title': 'Done',
            'class': 'card-title, success',
            'item': [
                {
                    "id": 7,
                    'title': 'I am 7'
                },
                {
                    "id": 8,
                    'title': 'I am 8'
                }
            ]
        }
    ],
    // Handle item scrolling
    dragEl: function (el, source) {
        console.log("Drag up", el);
        console.log(source);
        document.addEventListener('mousemove', isDragging);
    },

    dragendEl: function (el) {
        console.log("Drag Down", el);
        console.log(kanban.getParentBoardID(el.dataset.eid))
        document.removeEventListener('mousemove', isDragging);
    },

    click: function (el) {
        console.log("Click", el.dataset.eid);
    },
});
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
    console.log(t.dataset.eid)
    t.setAttribute("data-bs-toggle", "modal");
    t.setAttribute("data-bs-target", "#kt_modal_new_task");
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