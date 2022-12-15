const id = "#kt_modal_upload_dropzone";
const dropzone = document.querySelector(id);
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
// set the preview element template
let previewNode = dropzone.querySelector(".dropzone-item");
previewNode.id = "";
let previewTemplate = previewNode.parentNode.innerHTML;
previewNode.parentNode.removeChild(previewNode);
let myDropzone = new Dropzone(id, { // Make the whole body a dropzone
    url: "/abc/", // Set the url for your upload script location
    parallelUploads: 20,
    autoProcessQueue: false,
    uploadMultiple: true,
    maxFiles: 100,
    maxFilesize: 1, // Max filesize in MB
    previewTemplate: previewTemplate,
    previewsContainer: id + " .dropzone-items", // Define the container to display the previews
    clickable: id + " .dropzone-select" // Define the element that should be used as click trigger to select files.
});