"use strict";
function popupFileDelete(message, type){
    return Swal.fire({
        text: message,
        icon: type,
        buttonsStyling: false,
        confirmButtonText: "Ok, got it!",
        customClass: {
            confirmButton: "btn fw-bold btn-primary"
        }
    })
}
async function deleteFile(url, e, n, o){
    let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let form_data = new FormData();
    form_data.append("delete_files", [o.querySelector("input.form-check-input").value].toString());
    const response = await fetch(url, {
        method: 'POST',
        mode: 'same-origin',
        body: form_data,
        headers: {
            'X-CSRFToken': csrftoken
        },
    });
    if(response.status === 200){
        popupFileDelete("You have deleted "+n+"!.","success").then((function(){
            e.row($(o)).remove().draw();
            location.reload();
        }));
    }
    else{
        popupFileDelete("Something wrong! Please perform again!","error").then(()=>{
            location.reload();
        });
    }
}
async function deleteMultipleFile(url, e, o){
    let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let form_data = new FormData();
    let deleteIdFiles = [];
    o.forEach(t=>{
        if(t.checked){
            deleteIdFiles.push(t.closest("tbody tr").querySelector("input.form-check-input").value);
            e.row($(t.closest("tbody tr"))).remove().draw();
        }
    });
    form_data.append("delete_files", deleteIdFiles.toString());
    const response = await fetch(url, {
        method: 'POST',
        mode: 'same-origin',
        body: form_data,
        headers: {
            'X-CSRFToken': csrftoken
        },
    });
    if(response.status === 200){
        popupFileDelete("You have deleted all selected files or folders!.","success").then((function(){
            location.reload();
        }));
    }
    else{
        popupFileDelete("Something wrong! Please perform again!","error").then(()=>{
            location.reload();
        });
    }
}

async function updateFileName(id, newname, e, l) {
    let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let form_data = new FormData();
    form_data.append("file_id", id);
    form_data.append("new_name", newname);
    const response = await fetch('renamefile', {
        method: 'POST',
        mode: 'same-origin',
        body: form_data,
        headers: {
            'X-CSRFToken': csrftoken
        },
    });
    if(response.status === 200){
        Swal.fire({
            text:"You have renamed successfully!.",
            icon:"success",
            buttonsStyling:!1,
            confirmButtonText:"Ok, got it!",
            customClass:{confirmButton:"btn fw-bold btn-primary"}
        }).then((function(){
            location.reload();
            // const t=document.querySelector("#kt_file_manager_rename_input").value;
            // const o=`<div class="d-flex align-items-center">\n                                        ${i.outerHTML}\n                                        <a href="?page=apps/file-manager/files/" class="text-gray-800 text-hover-primary">${t}</a>\n                                    </div>`;
            // e.cell($(l)).data(o).draw();
        }))
    }
    else if(response.status === 400){
        Swal.fire({
            text: " File name existed!!",
            icon:"error",
            buttonsStyling:!1,
            confirmButtonText:"Ok, got it!",
            customClass:{
                confirmButton:"btn fw-bold btn-primary"
            }
        })
    }
    else{
        Swal.fire({
            text: "Something went wrong!",
            icon:"error",
            buttonsStyling:!1,
            confirmButtonText:"Ok, got it!",
            customClass:{
                confirmButton:"btn fw-bold btn-primary"
            }
        })
    }
}

let KTFileManagerList=function(){
    let e,t,o,n,r,a;
    // Delete a file
    const l=()=>{
        t.querySelectorAll('[data-kt-filemanager-table-filter="delete_row"]').forEach(
            (t=>{
                t.addEventListener("click",(
                    function(t){
                        t.preventDefault();
                        const o=t.target.closest("tr");
                        const n=o.querySelectorAll("td")[1].innerText;
                        Swal.fire({
                            text:"Are you sure you want to delete "+n+"?",
                            icon:"warning",
                            showCancelButton:!0,
                            buttonsStyling:!1,
                            confirmButtonText:"Yes, delete!",
                            cancelButtonText:"No, cancel",
                            customClass:{
                                confirmButton:"btn fw-bold btn-danger",
                                cancelButton:"btn fw-bold btn-active-light-primary"
                            }
                        }).then((function(t){
                            if(t.isConfirmed){
                                deleteFile('/project/deletefile/',e,n,o).then(r => {console.log(r)});
                            }
                            else{
                                Swal.fire({
                                    text:n+" was not deleted.",
                                    icon:"error",
                                    buttonsStyling:!1,
                                    confirmButtonText:"Ok, got it!",
                                    customClass:{
                                        confirmButton:"btn fw-bold btn-primary"
                                    }
                                })
                            }
                        }))
                    })
                )
            })
        )};
    // Delete multiple file
    const i=()=>{
        let o=t.querySelectorAll('[type="checkbox"]');
        "folders"===t.getAttribute("data-kt-filemanager-table")&&(
            o=document.querySelectorAll('#kt_file_manager_list_wrapper [type="checkbox"]')
        );
        const n=document.querySelector('[data-kt-filemanager-table-select="delete_selected"]');
        o.forEach((e=>{
            e.addEventListener("click",(function(){
                console.log(e);
                setTimeout((function(){
                    s()
                }),50)
            }))
        }));
        n.addEventListener("click",(function(){
            Swal.fire({
                text:"Are you sure you want to delete selected files or folders?",
                icon:"warning",
                showCancelButton:!0,
                buttonsStyling:!1,
                confirmButtonText:"Yes, delete!",
                cancelButtonText:"No, cancel",
                customClass:{
                    confirmButton:"btn fw-bold btn-danger",
                    cancelButton:"btn fw-bold btn-active-light-primary"
                }
            }).then((function(n){
                if(n.isConfirmed){
                    deleteMultipleFile('/project/deletefile/', e, o).then(r => {
                        console.log(r);
                        t.querySelectorAll('[type="checkbox"]')[0].checked=!1;
                    });
                    // Swal.fire({
                    //     text:"You have deleted all selected files or folders!.",
                    //     icon:"success",
                    //     buttonsStyling:!1,
                    //     confirmButtonText:"Ok, got it!",
                    //     customClass:{
                    //         confirmButton:"btn fw-bold btn-primary"
                    //     }
                    // }).then((function(){
                    //     o.forEach((t=>{
                    //         t.checked&&e.row($(t.closest("tbody tr"))).remove().draw()})
                    //     );
                    //     t.querySelectorAll('[type="checkbox"]')[0].checked=!1;
                    // }))
                }else{
                    Swal.fire({
                        text:"Selected files or folders was not deleted.",
                        icon:"error",
                        buttonsStyling:!1,
                        confirmButtonText:"Ok, got it!",
                        customClass:{
                            confirmButton:"btn fw-bold btn-primary"
                        }
                    })
                }
            }))
        }))
    };
    const s=()=>{
        const e=document.querySelector('[data-kt-filemanager-table-toolbar="base"]');
        const o=document.querySelector('[data-kt-filemanager-table-toolbar="selected"]');
        const n=document.querySelector('[data-kt-filemanager-table-select="selected_count"]');
        const r=t.querySelectorAll('tbody [type="checkbox"]');
        let a=!1, l=0;
        r.forEach((e=>{
            if(e.checked){
                a=!0;
                l++;
            }
        }));
        if(a){
            n.innerHTML=l.toString();
            e.classList.add("d-none");
            o.classList.remove("d-none");
        } else {
            e.classList.remove("d-none");
            o.classList.add("d-none")
        }
    };
    const c=()=>{
        const e=t.querySelector("#kt_file_manager_new_folder_row");
        e&&e.parentNode.removeChild(e)
    };
    const d=()=>{
        t.querySelectorAll('[data-kt-filemanager-table="rename"]').forEach((e=>{
            e.addEventListener("click",u)
        }))
    };
    const u=o=>{
        let r;
        o.preventDefault();
        if(t.querySelectorAll("#kt_file_manager_rename_input").length>0)
            return void Swal.fire({
                text:"Unsaved input detected. Please save or cancel the current item",
                icon:"warning",
                buttonsStyling:!1,
                confirmButtonText:"Ok, got it!",
                customClass:{
                    confirmButton:"btn fw-bold btn-danger"
                }
            });
        const a=o.target.closest("tr");
        const l=a.querySelectorAll("td")[1];
        const i=l.querySelector(".svg-icon");
        r=l.innerText;
        const s=n.cloneNode(!0);
        s.querySelector("#kt_file_manager_rename_folder_icon").innerHTML=i.outerHTML;
        l.innerHTML=s.innerHTML;
        a.querySelector("#kt_file_manager_rename_input").value=r;
        let c=FormValidation.formValidation(l,{
            fields:{
                rename_folder_name:{
                    validators:{
                        notEmpty:{message:"Name is required"}
                    }
                }
            },
            plugins:{
                trigger:new FormValidation.plugins.Trigger,
                bootstrap:new FormValidation.plugins.Bootstrap5({
                    rowSelector:".fv-row",eleInvalidClass:"",eleValidClass:""
                })
            }
        });
        document.querySelector("#kt_file_manager_rename_folder").addEventListener("click",(t=>{
            t.preventDefault();
            let bn = document.querySelector("#kt_file_manager_rename_input").value;
            c&&c.validate().then((function(t){
                console.log("validated!");
                "Valid"===t&&Swal.fire({
                    text:"Are you sure you want to rename "+r+"?",
                    icon:"warning",
                    showCancelButton:!0,
                    buttonsStyling:!1,
                    confirmButtonText:"Yes, rename it!",
                    cancelButtonText:"No, cancel",
                    customClass:{
                        confirmButton:"btn fw-bold btn-danger",
                        cancelButton:"btn fw-bold btn-active-light-primary"
                    }
                }).then((function(t){
                    const a=document.querySelector("#kt_file_manager_rename_input").value;
                    const id = document.querySelector("#kt_file_manager_rename_input").parentElement.parentElement.parentElement.getAttribute("data-id");
                    if(t.isConfirmed){
                        updateFileName(id, a, e, l).then(r => console.log(r));
                    } else{
                        Swal.fire({
                            text:r+" was not renamed.",
                            icon:"error",
                            buttonsStyling:!1,
                            confirmButtonText:"Ok, got it!",
                            customClass:{
                                confirmButton:"btn fw-bold btn-primary"
                            }
                        })
                    }
                }))
            }))
        }));
        const d=document.querySelector("#kt_file_manager_rename_folder_cancel");
        d.addEventListener("click",(t=>{
            t.preventDefault();
            d.setAttribute("data-kt-indicator","on");
            setTimeout((function(){
                const t=`<div class="d-flex align-items-center">\n                    ${i.outerHTML}\n                    <a href="?page=apps/file-manager/files/" class="text-gray-800 text-hover-primary">${r}</a>\n                </div>`;
                d.removeAttribute("data-kt-indicator");
                e.cell($(l)).data(t).draw();
                toastr.options={
                    closeButton:!0,
                    debug:!1,
                    newestOnTop:!1,
                    progressBar:!1,
                    positionClass:"toastr-top-right",
                    preventDuplicates:!1,
                    showDuration:"300",
                    hideDuration:"1000",
                    timeOut:"5000",
                    extendedTimeOut:"1000",
                    showEasing:"swing",
                    hideEasing:"linear",
                    showMethod:"fadeIn",
                    hideMethod:"fadeOut"
                };
                toastr.error("Cancelled rename function");
            }),1e3);
        }))
    };
    const m=()=>{
        t.querySelectorAll('[data-kt-filemanger-table="copy_link"]').forEach((e=>{
            const t=e.querySelector("button");
            const o=e.querySelector('[data-kt-filemanger-table="copy_link_generator"]');
            const n=e.querySelector('[data-kt-filemanger-table="copy_link_result"]');
            const r=e.querySelector("input");
            t.addEventListener("click",(e=>{
                let t;
                e.preventDefault();
                o.classList.remove("d-none");
                n.classList.add("d-none");
                clearTimeout(t);
                t=setTimeout((()=>{
                    o.classList.add("d-none");
                    n.classList.remove("d-none");
                    r.select();
                }),2e3);
            }))
        }))
    };
    const f=()=>{
        document.getElementById("kt_file_manager_items_counter").innerText=e.rows().count()+" items"
    };
    return{
        init:function(){
            if(document.querySelector("#kt_file_manager_list")){
                t=document.querySelector("#kt_file_manager_list");
                o=document.querySelector('[data-kt-filemanager-template="upload"]');
                n=document.querySelector('[data-kt-filemanager-template="rename"]');
                r=document.querySelector('[data-kt-filemanager-template="action"]');
                a=document.querySelector('[data-kt-filemanager-template="checkbox"]');
                (
                    ()=>{
                        t.querySelectorAll("tbody tr").forEach((e=>{
                            const t=e.querySelectorAll("td")[3];
                            const o=moment(t.innerHTML,"DD MMM YYYY, LT").format();
                            t.setAttribute("data-order",o);
                        }));
                        const o={
                            info:!1,
                            order:[],
                            scrollY:"700px",
                            scrollCollapse:!0,
                            paging:!1,
                            ordering:!1,
                            columns:[{data:"checkbox"},{data:"name"},{data:"size"},{data:"date"},{data:"action"}],
                            language:{emptyTable:`<div class="d-flex flex-column flex-center">\n                    <img src="${hostUrl}media/illustrations/sketchy-1/5.png" class="mw-400px"  alt=""/>\n                    <div class="fs-1 fw-bolder text-dark">No items found.</div>\n                    <div class="fs-6">Start creating new folders or uploading a new file!</div>\n                </div>`}},n={info:!1,order:[],pageLength:10,lengthChange:!1,ordering:!1,columns:[{data:"checkbox"},{data:"name"},{data:"size"},{data:"date"},{data:"action"}],language:{emptyTable:`<div class="d-flex flex-column flex-center">\n                    <img src="${hostUrl}media/illustrations/sketchy-1/5.png" class="mw-400px"  alt=""/>\n                    <div class="fs-1 fw-bolder text-dark mb-4">No items found.</div>\n                    <div class="fs-6">Start creating new folders or uploading a new file!</div>\n                </div>`},
                            conditionalPaging:!0
                        };
                        let r;
                        if("folders"===t.getAttribute("data-kt-filemanager-table")){
                            r=o;
                        }else{
                            r=n;
                            (e=$(t).DataTable(r)).on("draw",(function(){
                                i();
                                l();
                                s();
                                c();
                                KTMenu.createInstances();
                                m();
                                f();
                                d()
                            }))
                        }
                    }
                )();
                i();
                document.querySelector('[data-kt-filemanager-table-filter="search"]').addEventListener("keyup",(function(t){
                    e.search(t.target.value).draw();
                }));
                l();
                document.getElementById("kt_file_manager_new_folder").addEventListener("click",(n=>{
                    n.preventDefault();
                    if(t.querySelector("#kt_file_manager_new_folder_row"))
                        return;
                    const l=t.querySelector("tbody");
                    const i=o.cloneNode(!0);
                    l.prepend(i);
                    const s=i.querySelector("#kt_file_manager_add_folder_form");
                    const d=i.querySelector("#kt_file_manager_add_folder");
                    const u=i.querySelector("#kt_file_manager_cancel_folder");
                    const m=i.querySelector(".svg-icon-2x");
                    const f=i.querySelector('[name="new_folder_name"]');
                    let g=FormValidation.formValidation(s,{
                        fields:{
                            new_folder_name:{
                                validators:{
                                    notEmpty:{
                                        message:"Folder name is required"
                                    }
                                }
                            }
                        },
                        plugins:{
                            trigger:new FormValidation.plugins.Trigger,
                            bootstrap:new FormValidation.plugins.Bootstrap5({
                                rowSelector:".fv-row",eleInvalidClass:"",eleValidClass:""
                            })
                        }
                    });
                    d.addEventListener("click",(t=>{
                        t.preventDefault();
                        d.setAttribute("data-kt-indicator","on");
                        g&&g.validate().then((function(t){
                            console.log("validated!");
                            "Valid"===t?
                                setTimeout((function(){
                                    const t=document.createElement("a");
                                    t.setAttribute("href","?page=apps/files-manager/blank");
                                    t.classList.add("text-gray-800","text-hover-primary");
                                    t.innerText=f.value;
                                    const o=e.row.add({
                                        checkbox:a.innerHTML,name:m.outerHTML+t.outerHTML,size:"-",date:"-",action:r.innerHTML
                                    }).node();
                                    $(o).find("td").eq(4).attr("data-kt-filemanager-table","action_dropdown");
                                    $(o).find("td").eq(4).addClass("text-end");
                                    for(
                                        let n,l=e.row(0).index(),i=e.data().length-1,s=e.row(i).data(),c=i;c>l;c--
                                    ){}
                                    n=e.row(c-1).data();
                                    e.row(c).data(n);
                                    e.row(c-1).data(s);
                                    toastr.options={
                                        closeButton:!0,
                                        debug:!1,
                                        newestOnTop:!1,
                                        progressBar:!1,
                                        positionClass:"toastr-top-right",
                                        preventDuplicates:!1,
                                        showDuration:"300",
                                        hideDuration:"1000",
                                        timeOut:"5000",
                                        extendedTimeOut:"1000",
                                        showEasing:"swing",
                                        hideEasing:"linear",
                                        showMethod:"fadeIn",
                                        hideMethod:"fadeOut"
                                    };
                                    toastr.success(f.value+" was created!");
                                    d.removeAttribute("data-kt-indicator");
                                    f.value="";
                                    e.draw(!1)
                                }),2e3):
                                d.removeAttribute("data-kt-indicator")
                        }))
                    }));
                    u.addEventListener("click",(e=>{
                        e.preventDefault();
                        u.setAttribute("data-kt-indicator","on");
                        setTimeout((function(){
                            u.removeAttribute("data-kt-indicator");
                            toastr.options={
                                closeButton:!0,
                                debug:!1,
                                newestOnTop:!1,
                                progressBar:!1,
                                positionClass:"toastr-top-right",
                                preventDuplicates:!1,
                                showDuration:"300",
                                hideDuration:"1000",
                                timeOut:"5000",
                                extendedTimeOut:"1000",
                                showEasing:"swing",
                                hideEasing:"linear",
                                showMethod:"fadeIn",
                                hideMethod:"fadeOut"
                            };
                            toastr.error("Cancelled new folder creation");
                            c()
                        }),1e3)
                    }))
                }));
                m();
                d();
                (()=>{
                    const e=document.querySelector("#kt_modal_move_to_folder");
                    const t=e.querySelector("#kt_modal_move_to_folder_form");
                    const o=t.querySelector("#kt_modal_move_to_folder_submit");
                    const n=new bootstrap.Modal(e);
                    let r=FormValidation.formValidation(t, {
                        fields: {
                            move_to_folder:{
                                validators:{
                                    notEmpty:{message:"Please select a folder."}
                                }
                            }
                        },
                        plugins:{
                            trigger:new FormValidation.plugins.Trigger,
                            bootstrap:new FormValidation.plugins.Bootstrap5({
                                rowSelector:".fv-row",
                                eleInvalidClass:"",
                                eleValidClass:""
                            })
                        }
                    });
                    o.addEventListener("click",(e=>{
                        e.preventDefault();
                        o.setAttribute("data-kt-indicator","on");
                        r&&r.validate().then((function(e){
                            console.log("validated!");
                            "Valid"===e
                                ?setTimeout((function(){
                                    Swal.fire({
                                        text:"Are you sure you would like to move to this folder",
                                        icon:"warning",
                                        showCancelButton:!0,
                                        buttonsStyling:!1,
                                        confirmButtonText:"Yes, move it!",
                                        cancelButtonText:"No, return",
                                        customClass:{
                                            confirmButton:"btn btn-primary",
                                            cancelButton:"btn btn-active-light"
                                        }
                                    }).then((function(e){
                                        if(e.isConfirmed){
                                            t.reset();
                                            n.hide();
                                            toastr.options={
                                                closeButton:!0,
                                                debug:!1,
                                                newestOnTop:!1,
                                                progressBar:!1,
                                                positionClass:"toastr-top-right",
                                                preventDuplicates:!1,
                                                showDuration:"300",
                                                hideDuration:"1000",
                                                timeOut:"5000",
                                                extendedTimeOut:"1000",
                                                showEasing:"swing",
                                                hideEasing:"linear",
                                                showMethod:"fadeIn",
                                                hideMethod:"fadeOut"
                                            };
                                            toastr.success("1 item has been moved.");
                                            o.removeAttribute("data-kt-indicator");
                                        }
                                        else{
                                            Swal.fire({
                                                text:"Your action has been cancelled!.",
                                                icon:"error",buttonsStyling:!1,
                                                confirmButtonText:"Ok, got it!",
                                                customClass:{confirmButton:"btn btn-primary"}
                                            });
                                            o.removeAttribute("data-kt-indicator");
                                        }
                                    }))
                                }),500)
                                :o.removeAttribute("data-kt-indicator")
                        }))
                    }))
                })();
                f();
                KTMenu.createInstances();
            }
        }
    }
}();
KTUtil.onDOMContentLoaded((function(){KTFileManagerList.init()}));
