// const input = document.querySelector('#comment_input');
// const btnCancelComment = document.querySelector('#cancel_comment');
// const btnSaveComment = document.querySelector('#save_comment');
// input.addEventListener('focus', () =>{
//     console.log('click')
// })
const inputElementDiv = document.querySelector('#comment_input').parentNode;
const inputCkEditorDiv = document.querySelector('#kt_docs_ckeditor_document').parentNode;
const btnSaveComment= document.querySelector('#save_comment');
const btnCancelComment = document.querySelector('#cancel_comment');
function showCkeditor(){
    inputElementDiv.classList.add('d-none');
    inputCkEditorDiv.classList.remove('d-none');
    btnSaveComment.parentNode.classList.remove('d-none');
}
function hideCkeditor(){
    inputElementDiv.classList.remove('d-none');
    inputCkEditorDiv.classList.add('d-none');
    btnSaveComment.parentNode.classList.add('d-none');
}
inputElementDiv.addEventListener('click', showCkeditor);
btnCancelComment.addEventListener('click', hideCkeditor);