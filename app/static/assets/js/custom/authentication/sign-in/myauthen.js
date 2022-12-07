// Define form element
const form = document.getElementById('kt_sign_in_form');
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
        username: {
            validators: {
                notEmpty: {
                    message: 'The username is required',
                },
                regexp: {
                    regexp: /^[a-zA-Z0-9_]+$/,
                    message: 'The username can only consist of alphabetical, number and underscore',
                },
            },
        },
        password: {
            validators: {
                notEmpty: {
                    message: 'The password is required',
                },
            },
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
const submitButton = document.getElementById('kt_sign_in_submit');

async function postLogin(url) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const request = new Request(
        url,
        {
            headers:
                {
                    'X-CSRFToken': csrftoken
                }
        }
    );
    const response = await fetch(request,{
        method: 'POST',
        mode: 'same-origin',
        body: JSON.stringify
        ({
            username: $('#id_username').val(),
            email: $('#id_email').val(),
            password: $('#id_password').val(),
        })
    });
    if(response.status===401){
        Swal.fire({
            text: "Login Failed!",
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
            text: "Login Successful!",
            icon: "success",
            buttonsStyling: false,
            confirmButtonText: "Ok, got it!",
            customClass: {
                confirmButton: "btn btn-primary"
            }
        }).then((result) => {
            window.location.replace("/project");
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
                postLogin('',).then(r => console.log(r) ).catch(e=>console.log(e));
            }
        });
    }
});