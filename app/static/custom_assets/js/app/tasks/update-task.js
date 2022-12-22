let postUpdateTask = async (url) => {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let form_data = new FormData();
    let status = ["backlog", "todo", "working", "done",]
    form_data.append('task_title', $("#update_task_title").val());
    form_data.append('task_assign', $('#update_task_assign').val());
    form_data.append('due_date', $('#update_due_date').val());
    form_data.append('task_details', $('#update_task_details').val());
    form_data.append('task_status', status[$('#update_task_status').val()]);
    const response = await fetch(url,{
        method: 'POST',
        mode: 'same-origin',
        body: form_data,
        headers:{
            'X-CSRFToken': csrftoken
        }
    });
    if(response.status===200){
        Swal.fire({
            text: "Updated Successful!",
            icon: "success",
            buttonsStyling: false,
            confirmButtonText: "Ok, got it!",
            customClass: {
                confirmButton: "btn btn-primary"
            }
        }).then((result) => {
            window.location.replace(`detail/${$("#project_id").val()}/tasks`);
        });
    }
    else{
        Swal.fire({
            text: "Updated Failed!",
            icon: "error",
            buttonsStyling: false,
            confirmButtonText: "Ok, got it!",
            customClass: {
                confirmButton: "btn btn-primary"
            }
        });
    }
}
const updateTaskForm =document.querySelector("#kt_modal_update_task_form");
const updateTaskSubmitButton = document.querySelector("#kt_modal_update_task_submit");
validator = FormValidation.formValidation(updateTaskForm,{
    fields:{
        "task_title":{
            validators:{
                notEmpty:{
                    message:"Task title is required"
                }
            }
        },
        "due_date":{
            validators: {
                date: {
                    format: 'YYYY-MM-DD',
                    message: 'The value is not a valid date',
                },
                notEmpty: {
                    message: 'Due date input is required'
                }
            }
        },
        "task_assign":{
            validators:{
                notEmpty:{
                    message:"Task assign is required"
                }
            }
        }},
    plugins:{
        trigger:new FormValidation.plugins.Trigger({
            event:{
                password:!1
            }}),
        bootstrap:new FormValidation.plugins.Bootstrap5({
            rowSelector:".fv-row",
            eleValidClass:""
        })
    }
});
updateTaskSubmitButton.addEventListener('click', function (e) {
    // Prevent default button action
    e.preventDefault();
    // Validate form before submit

    validator.validate().then((status)=>{
        if (status === 'Valid') {

            // Show loading indication
            updateTaskSubmitButton.setAttribute('data-kt-indicator', 'on');

            // Disable button to avoid multiple click
            updateTaskSubmitButton.disabled = true;

            // Simulate form submission. For more info check the plugin's official documentation: https://sweetalert2.github.io/
            setTimeout((function(){
                updateTaskSubmitButton.removeAttribute("data-kt-indicator");
                updateTaskSubmitButton.disabled=false;
                let id = $("#selected_task").val();
                postUpdateTask(`task/${id}/update`)
                    .then((function(result){
                        if(result.isConfirmed){
                            updateTaskForm.reset();
                        }
                    }))
            }),300);
        }
        else{
            Swal.fire({
                text: "Sorry, looks like there are some errors detected, please try again.",
                icon:"error",
                buttonsStyling:!1,
                confirmButtonText: "Ok, got it!",
                customClass:{confirmButton:"btn btn-primary"}
            })
        }
    })
});