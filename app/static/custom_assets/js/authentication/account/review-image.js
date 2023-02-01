let imageInputElement = document.querySelector("#kt_image_input_control");
let imageInput = new KTImageInput(imageInputElement);
let actionChangeDiv = document.querySelector('[data-kt-image-input-action=change]')
actionChangeDiv.addEventListener("click", function() {
    console.log("click");
});
actionChangeDiv.addEventListener("change", function(e) {
    let reader = new FileReader();
    reader.onload = function(e) {
        let imageInnputWrapper = document.querySelector(".image-input-wrapper")
        if (document.getElementById('user_avatar').files[0].type.split('/')[0]==="image") {
            imageInnputWrapper.setAttribute("style",`background-image: url(${e.target.result})`)
        } else {
            Swal.fire({
                text: "Something went wrong!",
                icon: "error",
                buttonsStyling: false,
                confirmButtonText: "Ok, got it!",
                customClass: {
                    confirmButton: "btn btn-primary"
                }
            }).then((result) => {
                window.location.replace("/updateprofile");
            });
        }
    }
    reader.readAsDataURL(e.target.files[0]);
});