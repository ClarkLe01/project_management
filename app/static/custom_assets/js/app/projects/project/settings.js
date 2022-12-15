"use strict";
$("#start_date").flatpickr({
    minDate: "today",
    altInput: true,
    altFormat: "d/m/Y",
    dateFormat: "Y-m-d",
});
$("#end_date").flatpickr({
    minDate: "today",
    altInput: true,
    altFormat: "d/m/Y",
    dateFormat: "Y-m-d",
});
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const form =document.querySelector("#kt_project_settings_form");
const submitButton = document.querySelector("#kt_project_settings_submit");
let validator = FormValidation.formValidation(form,{
    fields:{
        name:{
            validators:{
                notEmpty:{
                    message:"Project name is required"
                }
            }
        },
        cost:{
            validators:{
                notEmpty:{
                    message:"Cost is required"
                }
            }
        },
        type:{
            validators:{
                notEmpty:{
                    message:"Project type is required"
                }
            }
        },
        start_date:{
            validators:{
                notEmpty:{
                    message:"Start Date is required"
                }
            }
        },
        end_date:{
            validators:{
                notEmpty:{
                    message:"End Date is required"
                }
            }
        }
    },
    plugins:{
        trigger:new FormValidation.plugins.Trigger,
        submitButton:new FormValidation.plugins.SubmitButton,
        bootstrap:new FormValidation.plugins.Bootstrap5({rowSelector:".fv-row"})
    }
})
async function patchProject(url) {
    let form_data = new FormData();
    form_data.append('name',$('#project_name').val());
    form_data.append('description',editor.getData());
    form_data.append('start',$('#start_date').val());
    form_data.append('end',$('#end_date').val());
    form_data.append('cost',$('#cost').val());
    form_data.append('base',$('#base').val());

    const response = await fetch(url,{
        method: 'POST',
        mode: 'same-origin',
        body: form_data,
        headers: {
            'X-CSRFToken': csrftoken,
        },
    });
    if(response.status===200){
        swal.fire({
            text:"Thank you! You've updated your project settings",
            icon:"success",
            buttonsStyling:!1,
            confirmButtonText:"Ok, got it!",
            customClass:{
                confirmButton:"btn fw-bold btn-light-primary"
            }
        }).then((result) => {
            window.location.replace("/project");
        });;
    }
    else{
        Swal.fire({
            text:"Sorry, looks like there are some errors detected, please try again.",
            icon:"error",
            buttonsStyling:!1,
            confirmButtonText:"Ok, got it!",
            customClass:{
                confirmButton:"btn fw-bold btn-light-primary"
            }
        })
    }
}
submitButton.addEventListener('click', function (e) {
    // Prevent default button action
    e.preventDefault();
    // Validate form before submit
    if (validator) {
        validator.validate().then(function (status) {
            console.log('validated!');

            if (status === 'Valid') {
                let startdate_input = document.querySelector('[name="start_date"]');
                let enddate_input = document.querySelector('[name="end_date"]');
                const start = new Date(startdate_input.value);
                const end = new Date(enddate_input.value);
                if (start.getTime()>end.getTime()){
                    let notify_div = document.getElementById('end_date').parentElement.nextElementSibling;
                    notify_div.innerHTML+='<div data-field="end_date" data-validator="notEmpty">End Date is less than Start Date</div>'
                }
                else{
                    // Show loading indication
                    submitButton.setAttribute('data-kt-indicator', 'on');

                    // Disable button to avoid multiple click
                    submitButton.disabled = true;

                    // Simulate form submission. For more info check the plugin's official documentation: https://sweetalert2.github.io/
                    setTimeout(function () {
                        // Remove loading indication
                        submitButton.removeAttribute('data-kt-indicator');
                        // Enable button
                        submitButton.disabled = false;
                    }, 1000);
                    patchProject(window.location.href).then(r => console.log(r) ).catch(e=>console.log(e));

                }
            }
        });
    }
});



$("#kt_account_deactivate_account_submit").on('click', function(e){
    e.preventDefault();
    Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire(
                'Deleted!',
                'Your files has been deleted.',
                'success'
            ).then(() => {
                $("#delete_form").submit();
            })
        }
    })
})