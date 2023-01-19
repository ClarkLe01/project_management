function popup(message, type){
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

// Post for creating new project
async function postCreatingProject(url) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let form_data = new FormData();
    form_data.append("name", $('#project_name').val());
    form_data.append("description", editor.getData());
    form_data.append("start", $('#start_date').val());
    form_data.append("end", $('#end_date').val());
    form_data.append("cost", $('#cost').val());
    form_data.append("base", $('#base').val());
    let lang_tags = [];
    document.getElementById("project_langs").previousSibling.querySelectorAll('tag').forEach(item => lang_tags.unshift(item.__tagifyTagData))
    form_data.append("langs", JSON.stringify(lang_tags));

    let collaborator_tags = [];
    document.getElementById("project_collaborators").previousSibling.querySelectorAll('tag').forEach(item => collaborator_tags.unshift(item.__tagifyTagData))
    form_data.append("collaborators", JSON.stringify(collaborator_tags));
    const response = await fetch(url, {
        method: 'POST',
        mode: 'same-origin',
        body: form_data,
        headers: {
            'X-CSRFToken': csrftoken
        },
    })
    if(response.status===201){
        popup("Create Successful!","success").then((result) => {
            window.location.replace(url);
        })
    }
    else{
        popup("Create Failed!","error").then((result) => {
            window.location.replace(url);
        })
    }
}
const create_app=document.querySelector("#kt_modal_create_app");
new bootstrap.Modal(create_app)
const app_stepper=document.querySelector("#kt_modal_create_app_stepper");
const app_form=document.querySelector("#kt_modal_create_app_form");
const btn_submit=app_stepper.querySelector('[data-kt-stepper-action="submit"]');
const btn_next=app_stepper.querySelector('[data-kt-stepper-action="next"]');
let validator = []
validator.push(FormValidation.formValidation(app_form,
    {
        fields:
            {
                project_name:
                    {
                        validators:
                            {
                                notEmpty:
                                    {
                                        message:"Project name is required"
                                    }
                            }
                    }
            },
        plugins:
            {
                trigger:new FormValidation.plugins.Trigger,
                bootstrap:new FormValidation.plugins.Bootstrap5(
                    {
                        rowSelector:".fv-row",
                        eleInvalidClass:"",
                        eleValidClass:""
                    }
                )
            }
    }
));
validator.push(FormValidation.formValidation(app_form,
    {
        fields:
            {
                name_example:
                    {
                        validators:
                            {
                                notEmpty:
                                    {
                                        message:"name_example is required"
                                    }
                            }
                    }
            },
        plugins:
            {
                trigger:new FormValidation.plugins.Trigger,
                bootstrap:new FormValidation.plugins.Bootstrap5(
                    {
                        rowSelector:".fv-row",
                        eleInvalidClass:"",
                        eleValidClass:""
                    }
                )
            }
    }
));
validator.push(FormValidation.formValidation(app_form,
    {
        fields:
            {
                start_date:
                    {
                        validators:
                            {
                                notEmpty: {
                                    message:"Start Date is required"
                                }
                            }
                    },
                end_date:
                    {
                        validators:
                            {
                                notEmpty:
                                    {
                                        message:"End Date is required"
                                    }
                            }
                    }
            },
        plugins:
            {
                trigger:new FormValidation.plugins.Trigger,
                bootstrap:new FormValidation.plugins.Bootstrap5(
                    {
                        rowSelector:".fv-row",
                        eleInvalidClass:"",
                        eleValidClass:""
                    }
                )
            }
    }
));
validator.push(FormValidation.formValidation(app_form,
    {
        fields:
            {
                name_example:
                    {
                        validators:
                            {
                                notEmpty:
                                    {
                                        message:"name_example is required"
                                    }
                            }
                    }
            },
        plugins:
            {
                trigger:new FormValidation.plugins.Trigger,
                bootstrap:new FormValidation.plugins.Bootstrap5(
                    {
                        rowSelector:".fv-row",
                        eleInvalidClass:"",
                        eleValidClass:""
                    }
                )
            }
    }
));

let step = new KTStepper(app_stepper);
step.on("kt.stepper.changed",(
    function(e)
    {
        4===step.getCurrentStepIndex()?
            (
                btn_submit.classList.remove("d-none"),
                    btn_submit.classList.add("d-inline-block"),
                    btn_next.classList.add("d-none")
            ):
            5===step.getCurrentStepIndex()?
                (
                    btn_submit.classList.add("d-none"),
                        btn_next.classList.add("d-none")
                ):
                (
                    btn_submit.classList.remove("d-inline-block"),
                        btn_submit.classList.remove("d-none"),
                        btn_next.classList.remove("d-none")
                )
    }
))
step.on("kt.stepper.next",(function(e){
    console.log("stepper.next");
    let tmp_valid = validator[e.getCurrentStepIndex()-1];
    console.log(step)
    tmp_valid?tmp_valid.validate().then((
            function(status)
            {
                console.log("validated!")

                if("Valid"===status){
                    if(e.getCurrentStepIndex()===3){
                        let startdate_input = document.querySelector('[name="start_date"]');
                        let enddate_input = document.querySelector('[name="end_date"]');
                        const start = new Date(startdate_input.value);
                        const end = new Date(enddate_input.value);
                        if (start.getTime()>end.getTime()){
                            let notify_div = document.getElementById('end_date').nextElementSibling.nextElementSibling;
                            notify_div.innerHTML+='<div data-field="end_date" data-validator="notEmpty">End Date is less than Start Date</div>'
                        }else{
                            e.goNext()
                        }
                    }else{
                        e.goNext();
                    }
                }
            })):
        (
            e.goNext(), KTUtil.scrollTop()
        )
}));
step.on("kt.stepper.previous",(
    function(e)
    {
        console.log("stepper.previous"),
            e.goPrevious(),
            KTUtil.scrollTop()
    }
));
// set the dropzone container id
const id = "#kt_dropzonejs_example_1";
const dropzone = document.querySelector(id);
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
// set the preview element template
var previewNode = dropzone.querySelector(".dropzone-item");
previewNode.id = "";
var previewTemplate = previewNode.parentNode.innerHTML;
previewNode.parentNode.removeChild(previewNode);

var myDropzone = new Dropzone(id, { // Make the whole body a dropzone
    url: "/project/", // Set the url for your upload script location
    parallelUploads: 20,
    autoProcessQueue: false,
    uploadMultiple: true,
    maxFiles: 100,
    maxFilesize: 1, // Max filesize in MB
    previewTemplate: previewTemplate,
    previewsContainer: id + " .dropzone-items", // Define the container to display the previews
    clickable: id + " .dropzone-select" // Define the element that should be used as click trigger to select files.
});
btn_submit.addEventListener("click",(
    function(e)
    {
        e.preventDefault();
        e.stopPropagation();
        btn_submit.disabled=!0;
        btn_submit.setAttribute("data-kt-indicator","on");
        setTimeout((function(){
                btn_submit.removeAttribute("data-kt-indicator")
                btn_submit.disabled=!1
            }),2e3)
        if (myDropzone.getQueuedFiles().length > 0) {
            myDropzone.processQueue();
        }
        else {
            postCreatingProject('/project/').then(r => console.log(r));
        }
    }))

$('#filter_form').on('submit',(e)=>{
    e.preventDefault();
    let name = $('#kt_filter_name').val();
    let status = $('#kt_menu_filter_status').val();
    let base = $('#kt_menu_filter_currency').val();
    let start = $('#kt_filter_start_date').val();
    let end = $('#kt_filter_end_date').val();
    let query_string = `?name=${name}&status=${status}&base=${base}&start=${start}&end=${end}`
    window.location.replace(window.location.origin+window.location.pathname+query_string);
})

myDropzone.on("sendingmultiple", function (file, xhr, formData) {
    // Show the total progress bar when upload starts
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    const progressBars = dropzone.querySelectorAll('.progress-bar');
    progressBars.forEach(progressBar => {
        progressBar.style.opacity = "1";
    });
    formData.append("name", $('#project_name').val());
    formData.append("description", editor.getData());
    formData.append("start", $('#start_date').val());
    formData.append("end", $('#end_date').val());
    formData.append("cost", $('#cost').val());
    formData.append("base", $('#base').val());

    let lang_tags = [];
    document.getElementById("project_langs").previousSibling.querySelectorAll('tag').forEach(item => lang_tags.unshift(item.__tagifyTagData))
    formData.append("langs", JSON.stringify(lang_tags));

    let collaborator_tags = [];
    document.getElementById("project_collaborators").previousSibling.querySelectorAll('tag').forEach(item => collaborator_tags.unshift(item.__tagifyTagData))
    formData.append("collaborators", JSON.stringify(collaborator_tags));
});

myDropzone.on("addedfile", function (file) {
    // Hookup the start button
    const dropzoneItems = dropzone.querySelectorAll('.dropzone-item');
    dropzoneItems.forEach(dropzoneItem => {
        dropzoneItem.style.display = '';
    });
});

myDropzone.on('successmultiple', function(files, response) {
    popup("Create Successful!","success").then((result) => {
        window.location.replace("/project");
    })
});
myDropzone.on('errormultiple', function(files, response) {
    popup("Create Failed!","error").then((result) => {
        window.location.replace("/project");
    })
});



