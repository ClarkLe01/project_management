async function deleteComment(id) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let form_data = new FormData();
    form_data.append('comment_id', id);
    const response = await fetch(`../task/comments/delete`,{
        method: 'POST',
        mode: 'same-origin',
        body: form_data,
        headers:{
            'X-CSRFToken': csrftoken
        }
    });
    if(response.status===200){
        console.log("Delete comment id");
        document.getElementById(`comment_${id}`).remove();
    }
    else{
        console.log("Error: " + response.status);
    }
}

function removeAllComment() {
    let parent = document.getElementById("kt_comments");
    let comments = parent.querySelectorAll('.comment-object');
    comments.forEach(comment => comment.remove());
}