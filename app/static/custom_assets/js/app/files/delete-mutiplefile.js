const inputCheckbox = document.querySelectorAll('[type="checkbox"]');
const deleteCheckbox = document.querySelectorAll('#kt_file_manager_list_wrapper [type="checkbox"]');
const selectedDeleteCheckbox=document.querySelector('[data-kt-filemanager-table-select="delete_selected"]');
const e=document.querySelector('[data-kt-filemanager-table-toolbar="base"]');
const o=document.querySelector('[data-kt-filemanager-table-toolbar="selected"]');
const n=document.querySelector('[data-kt-filemanager-table-select="selected_count"]');
const r=document.querySelectorAll('tbody [type="checkbox"]');
async function deleteMultipleFile(url, r){
    let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let form_data = new FormData();
    let deleteIdFiles = [];
    r.forEach(t=>{
        if(t.checked){
            deleteIdFiles.unshift(t.closest("tr").querySelectorAll(".sorting_1>div>input")[0].value);
        }
        t.checked&&table.row($(t.closest("tbody tr"))).remove().draw()
    });
    form_data.append("delete_files", deleteIdFiles);
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
let s=()=>{
    let a=!1,l=0;
    r.forEach(e=>{
        if(e.checked){
            a=!0;
            l++;
        }
    });
    if(a){
        n.innerHTML=l.toString();
        e.classList.add("d-none");
        o.classList.remove("d-none");
    }
    else{
        e.classList.remove("d-none");
        o.classList.add("d-none");
    }
}
inputCheckbox.forEach(e=>{
    e.addEventListener("click",(function(){
        setTimeout((function(){
            s()
        }),50);
    }))
})
selectedDeleteCheckbox.addEventListener("click",()=>{
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
    }).then((function(result){
        if(result.isConfirmed) {
            deleteMultipleFile('/project/deletefile/', r).then(r=>{
                inputCheckbox.checked=!1;
                e.classList.remove("d-none");
                o.classList.add("d-none");
            });
        } else {
            popupFileDelete("Selected files or folders was not deleted.","error").then(()=>{
                inputCheckbox.forEach(e=>{
                    e.checked = 0;
                })
                e.classList.remove("d-none");
                o.classList.add("d-none");
            });
        }
    }))
})