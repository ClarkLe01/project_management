"use strict";
let KTFileManagerList=function(){
    let delete_link = document.querySelectorAll('[data-kt-filemanager-table-filter="delete_row"]');
    delete_link.forEach(t=>{
        t.addEventListener("click", (e) => {
            e.preventDefault();
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
                t.value?Swal.fire({
                        text:"You have deleted "+n+"!.",
                        icon:"success",
                        buttonsStyling:!1,
                        confirmButtonText:"Ok, got it!",
                        customClass:{
                            confirmButton:"btn fw-bold btn-primary"
                        }
                    }).then((function(){
                        e.row($(o)).remove().draw()
                    })):
                    "cancel"===t.dismiss&&Swal.fire({
                        text:customerName+" was not deleted.",
                        icon:"error",
                        buttonsStyling:!1,
                        confirmButtonText:"Ok, got it!",
                        customClass:{
                            confirmButton:"btn fw-bold btn-primary"
                        }
                    })
            }));
        })
    })
}