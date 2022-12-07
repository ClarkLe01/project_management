// Define form element
const form = document.getElementById('kt_password_reset_form');
// Init form validation rules. For more info check the FormValidation plugin's official documentation:https://formvalidation.io/
let validator = FormValidation.formValidation(form, {
    fields: {
        'email':{
            validators:{
                regexp:{
                    regexp:/^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                    message:"The value is not a valid email address"
                },
                notEmpty:{
                    message:"Email address is required"
                }
            }
        },
    },
    plugins: {
        trigger: new FormValidation.plugins.Trigger(),
        bootstrap: new FormValidation.plugins.Bootstrap5({
            rowSelector: '.fv-row',
            eleInvalidClass: '',
            eleValidClass: ''
        })
    }
});

// Submit button handler
const submitButton = document.getElementById('kt_password_reset_submit');

async function postReset(url) {
    let form_data = new FormData();
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    form_data.append("email",$('#id_email').val())
    const response = await fetch(url,{
        method: 'POST',
        mode: 'same-origin',
        body: form_data,
        headers: {
            'X-CSRFToken': csrftoken
        }
    });
    if(response.status===400){
        Swal.fire({
            text: 'Account does not exist!',
            icon: "error",
            buttonsStyling: false,
            confirmButtonText: "Ok, got it!",
            customClass: {
                confirmButton: "btn btn-primary"
            }
        });
    }
    else{
        Swal.fire({
            text: 'Password reset email has been sent to your email address.',
            icon: "success",
            buttonsStyling: false,
            confirmButtonText: "Ok, got it!",
            customClass: {
                confirmButton: "btn btn-primary"
            }
        }).then((result) => {
            window.location.replace("/signin");
        });
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
                postReset('',).then(r => console.log(r) ).catch(e=>console.log(e));
            }
        });
    }
});