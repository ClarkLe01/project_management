async function postReNewPass(url) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let form_data = new FormData();
    form_data.append("password",$('#id_password').val())
    form_data.append("confirm_password",$('#id_confirm_password').val())
    const response = await fetch(url,{
        method: 'POST',
        mode: 'same-origin',
        body: form_data,
        headers: {
            'X-CSRFToken': csrftoken
        }
    });
    if(response.status===200){
        Swal.fire({
            text: "Reset Successful!",
            icon: "success",
            buttonsStyling: false,
            confirmButtonText: "Ok, got it!",
            customClass: {
                confirmButton: "btn btn-primary"
            }
        }).then((result) => {
            window.location.replace("/project/");
        });
    }
    else{
        Swal.fire({
            text: "Reset Failed!",
            icon: "error",
            buttonsStyling: false,
            confirmButtonText: "Ok, got it!",
            customClass: {
                confirmButton: "btn btn-primary"
            }
        });
    }
}

const form =document.querySelector("#kt_new_password_form");
const submitButton = document.querySelector("#kt_new_password_submit");
const passwordMeterElement = form.querySelector('[data-kt-password-meter="true"]')
let validator = FormValidation.formValidation(form,{
    fields:{
        'password':{
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
        "confirm_password":{
            validators:{
                notEmpty:{
                    message:"The password confirmation is required"
                },
                identical:{
                    compare:function(){
                        return form.querySelector('[name="password"]').value
                    },
                    message:"The password and its confirm are not the same"
                }
            }},
        toc:{
            validators:{
                notEmpty:{
                    message:"You must accept the terms and conditions"
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

    validator.revalidateField("password");
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
                postReNewPass('')
                    .then((function(result){
                        if(result.isConfirmed){
                            form.reset();
                            KTPasswordMeter.getInstance(passwordMeterElement).reset();
                        }
                    }))
            }),1500);
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
form.querySelector('input[name="password"]').addEventListener("input",(function(){
    this.value.length>0&&validator.updateFieldStatus("password","Valid")
}))