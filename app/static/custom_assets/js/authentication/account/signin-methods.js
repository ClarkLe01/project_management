async function postChangePass(url) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let form_data = new FormData();
    form_data.append('current_password', $('#currentpassword').val());
    form_data.append('new_password', $('#newpassword').val());
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
            text: "Change Successful!",
            icon: "success",
            buttonsStyling: false,
            confirmButtonText: "Ok, got it!",
            customClass: {
                confirmButton: "btn btn-primary"
            }
        }).then((function() {
            c();
        }))
    }
    else{
        Swal.fire({
            text: "Change Failed!",
            icon: "error",
            buttonsStyling: false,
            confirmButtonText: "Ok, got it!",
            customClass: {
                confirmButton: "btn btn-primary"
            }
        });
    }
}
const form_change_pass = document.querySelector("#kt_signin_change_password");
let pass_validator = FormValidation.formValidation(form_change_pass, {
    fields: {
        "currentpassword": {
            validators: {
                notEmpty: {
                    message: "Current Password is required"
                }
            }
        },
        "newpassword": {
            validators: {
                notEmpty: {
                    message: "New Password is required"
                }
            }
        },
        "confirmpassword": {
            validators: {
                notEmpty: {
                    message: "Confirm Password is required"
                },
                identical: {
                    compare: function() {
                        return form_change_pass.querySelector('[name="newpassword"]').value
                    },
                    message: "The password and its confirm are not the same"
                }
            }
        }
    },
    plugins: {
        trigger: new FormValidation.plugins.Trigger,
        bootstrap:new FormValidation.plugins.Bootstrap5({
            rowSelector:".fv-row",
            eleValidClass:""
        })
    }
});
let o = document.getElementById("kt_signin_password");
let a = document.getElementById("kt_signin_password_edit");
let i = document.getElementById("kt_signin_password_button");
let c = function() {
    o.classList.toggle("d-none");
    a.classList.toggle("d-none");
    i.classList.toggle("d-none");
    form_change_pass.reset();
};
i.addEventListener("click", (function() {
    c();
}));
let l = document.getElementById("kt_password_cancel");
l.addEventListener("click", (function() {
    c();
}));
form_change_pass.querySelector("#kt_password_submit").addEventListener("click", (function(e) {
    e.preventDefault();
    if(pass_validator){
        pass_validator.validate().then((status)=> {
            if(status === 'Valid'){
                postChangePass();
            } else{
                swal.fire({
                    text: "Sorry, looks like there are some errors detected, please try again.",
                    icon: "error",
                    buttonsStyling: !1,
                    confirmButtonText: "Ok, got it!",
                    customClass: {
                        confirmButton: "btn font-weight-bold btn-light-primary"
                    }
                })
            }
        })

    }
}));