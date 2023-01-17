async function deleteTask(url, id){
    let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let form_data = new FormData();
    form_data.append("task_id", id);
    const response = await fetch(url, {
        method: 'POST',
        body: form_data,
        headers: {
            'X-CSRFToken': csrftoken
        },
    });
    if(response.status === 200){
        popup("The task deleted successfully.", "success").then((function(){
            location.reload();
        }));
    }
    else{
        popup("Something wrong! Please perform again!","error").then((function(){
            location.reload();
        }));
    }
}

const deleteTaskBtn = document.querySelector("#kt_modal_update_task_delete");
deleteTaskBtn.addEventListener("click", (e)=>{
    e.preventDefault();

    Swal.fire({
        text:"Are you sure you want to delete this task?",
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
            let id = $("#selected_task").val();
            deleteTask(`${window.location.origin}/task/delete`, id).then(r => {console.log(r)});
        } else {
            popup("The task was not deleted.", "error").then(()=>{
                window.location.reload();
            });
        }
    });
})