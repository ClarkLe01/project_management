const form_update = document.getElementById("kt_account_profile_details_form");
const submitButton = document.getElementById("kt_account_profile_details_submit");
validator = FormValidation.formValidation(form_update,{
    fields:{
        fname:{
            validators:{
                notEmpty:{
                    message:"First name is required"
                }
            }
        },
        lname:{
            validators:{
                notEmpty:{
                    message:"Last name is required"
                }
            }
        },
    },
    plugins:{
        trigger:new FormValidation.plugins.Trigger,
        submitButton:new FormValidation.plugins.SubmitButton,
        bootstrap:new FormValidation.plugins.Bootstrap5({
            rowSelector:".fv-row",eleInvalidClass:"",eleValidClass:""})
    }
});
async function patchProfile(url) {
    let form_data = new FormData();
    let ins = document.getElementById('user_avatar').files.length;
    for (let x = 0; x < ins; x++) {
        form_data.append("files", document.getElementById('user_avatar').files[x]);
    }
    let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let fname = document.getElementById('fname').value;
    let lname = document.getElementById('lname').value;
    form_data.append("csrfmiddlewaretoken", csrftoken);
    form_data.append("fname", fname);
    form_data.append("lname", lname);
    console.log(form_data);
    const response = await fetch(url,{
        method: 'POST',
        mode: 'same-origin',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        body: form_data
    });
    if(response.status===404){
        Swal.fire({
            text: "Update Failed! User Not Found!",
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
            text: "Update Successful!",
            icon: "success",
            buttonsStyling: false,
            confirmButtonText: "Ok, got it!",
            customClass: {
                confirmButton: "btn btn-primary"
            }
        }).then((result) => {
            window.location.replace("/updateprofile");
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
                patchProfile('updateprofile/',).then(r => console.log(r) ).catch(e=>console.log(e));
            }
        });
    }
});


const form_update_pass = document.getElementById("kt_signin_change_password");
const submitChangePassButton = document.getElementById("kt_pass_submit");
validator = FormValidation.formValidation(form_update_pass,{
    fields:{
        current_password:{
            validators:{
                notEmpty:{
                    message:"current password is required"
                }
            }
        },
        new_password:{
            validators:{
                notEmpty:{
                    message:"The password is required"
                },
                callback:{
                    message:"Please enter valid password",
                    callback:
                        function(e){
                            let passwordMeter = KTPasswordMeter.getInstance(passwordMeterElement);
                            if(e.value.length>0) return 100===passwordMeter.getScore();
                        }
                }
            }
        },
        confirm_password:{
            validators:{
                notEmpty:{
                    message:"The password confirmation is required"
                },
                identical:{
                    compare:function(){
                        return form_update_pass.querySelector('[name="new_password"]').value
                    },
                    message:"The password and its confirm are not the same"
                }
            }},
    },
    plugins:{
        trigger:new FormValidation.plugins.Trigger,
        submitButton:new FormValidation.plugins.SubmitButton,
        bootstrap:new FormValidation.plugins.Bootstrap5({
            rowSelector:".fv-row",eleInvalidClass:"",eleValidClass:""})
    }
});
async function patchPass(url) {
    let form_data = new FormData();
    let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let current_password = document.getElementById('current_password').value;
    let new_password = document.getElementById('new_password').value;
    form_data.append("csrfmiddlewaretoken", csrftoken);
    form_data.append("current_password", current_password);
    form_data.append("new_password", new_password);
    const response = await fetch(url,{
        method: 'POST',
        mode: 'same-origin',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        body: form_data
    });
    if(response.status===200){
        Swal.fire({
            text: "Update Successful!",
            icon: "success",
            buttonsStyling: false,
            confirmButtonText: "Ok, got it!",
            customClass: {
                confirmButton: "btn btn-primary"
            }
        }).then((result) => {
            window.location.replace("/updateprofile");
        });
    }
    else{
        Swal.fire({
            text: "Update Failed! User Not Found!",
            icon: "error",
            buttonsStyling: false,
            confirmButtonText: "Ok, got it!",
            customClass: {
                confirmButton: "btn btn-primary"
            }
        });

    }
}
submitChangePassButton.addEventListener('click', function (e) {
    // Prevent default button action
    e.preventDefault();
    // Validate form before submit
    if (validator) {
        validator.validate().then(function (status) {
            console.log('validated!');

            if (status === 'Valid') {
                // Show loading indication
                submitChangePassButton.setAttribute('data-kt-indicator', 'on');

                // Disable button to avoid multiple click
                submitChangePassButton.disabled = true;

                // Simulate form submission. For more info check the plugin's official documentation: https://sweetalert2.github.io/
                setTimeout(function () {
                    // Remove loading indication
                    submitButton.removeAttribute('data-kt-indicator');
                    // Enable button
                    submitButton.disabled = false;
                }, 1000);
                patchPass('updatepass/',).then(r => console.log(r) ).catch(e=>console.log(e));

            }
        });
    }
});