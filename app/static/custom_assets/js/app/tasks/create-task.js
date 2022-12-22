function popup(message, type)   {
    return Swal.fire({
        text: message,
        icon: type,
        buttonsStyling: false,
        confirmButtonText: "Ok, got it!",
        customClass: {
            confirmButton: "btn btn-primary"
        }
    })
}
let postNewTask = async (url) => {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let form_data = new FormData();
    form_data.append('task_title', $("#new_task_title").val());
    form_data.append('task_assign', $('#new_task_assign').val());
    form_data.append('due_date', $('#new_due_date').val());
    form_data.append('task_details', $('#new_task_details').val());
    const response = await fetch(url,{
        method: 'POST',
        mode: 'same-origin',
        body: form_data,
        headers:{
            'X-CSRFToken': csrftoken
        }
    });
    if(response.status===201){
        Swal.fire({
            text: "Created Successful!",
            icon: "success",
            buttonsStyling: false,
            confirmButtonText: "Ok, got it!",
            customClass: {
                confirmButton: "btn btn-primary"
            }
        }).then((result) => {
            window.location.replace(url);
        });
    }
    else{
        Swal.fire({
            text: "Created Failed!",
            icon: "error",
            buttonsStyling: false,
            confirmButtonText: "Ok, got it!",
            customClass: {
                confirmButton: "btn btn-primary"
            }
        });
    }
}
const form =document.querySelector("#kt_modal_new_task_form");
const submitButton = document.querySelector("#kt_modal_new_task_submit");
let validator = FormValidation.formValidation(form,{
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
submitButton.addEventListener('click', function (e) {
    // Prevent default button action
    e.preventDefault();
    // Validate form before submit

    validator.validate().then((status)=>{
        if (status === 'Valid') {

            // Show loading indication
            submitButton.setAttribute('data-kt-indicator', 'on');

            // Disable button to avoid multiple click
            submitButton.disabled = true;

            // Simulate form submission. For more info check the plugin's official documentation: https://sweetalert2.github.io/
            setTimeout((function(){
                submitButton.removeAttribute("data-kt-indicator");
                submitButton.disabled=false;
                postNewTask(window.location.pathname)
                    .then((function(result){
                        if(result.isConfirmed){
                            form.reset();
                        }
                    }))
            }),200);
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