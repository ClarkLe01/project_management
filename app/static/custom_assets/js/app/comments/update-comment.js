async function updateComment(id, comment) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let form_data = new FormData();
    form_data.append('comment', comment);
    const response = await fetch(`../task/comments/${id}/update`,{
        method: 'POST',
        mode: 'same-origin',
        body: form_data,
        headers:{
            'X-CSRFToken': csrftoken
        }
    });
    if(response.status===200){
        return await response.json();
    }
    else{
        console.log("Error: " + response.status);
        return undefined;
    }
}
