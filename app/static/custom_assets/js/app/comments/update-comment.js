async function updateComment(id) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let form_data = new FormData();
    form_data.append('comment_id', id);
    const response = await fetch(`comments/delete`,{
        method: 'POST',
        mode: 'same-origin',
        body: form_data,
        headers:{
            'X-CSRFToken': csrftoken
        }
    });
    if(response.status===200){
        console.log("Update status successfully");
    }
    else{
        console.log("Error: " + response.status);
    }
}

// function showCkeditorCommentObject(){
//
// }
// function hideCkeditorCommentObject(){
//
// }