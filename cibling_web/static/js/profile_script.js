var profileImageApp = new Vue({
    el: "#profileApp",
    data: {
        imageData: "",
        coverimageData: "",
        imageUploadProgress: 0,
        profileImageUploadProgress: 0,
        imageUpdated: false
    },
    created() {
    },
    methods: {
        showModal: function (name) {
            if (name === 'profile') {
                $("#profileImageChangeModal").modal('show');
            }
            if (name === 'cover') {
                $("#coverImageChangeModal").modal('show');
            }


        },
        closeModal: function (name) {
            if (name === 'profile') {
                $("#profileImageChangeModal").modal('hide');
            }
            if (name === 'cover') {
                $("#coverImageChangeModal").modal('hide');
            }


            if (this.imageUpdated) {
                window.location.reload();
            }

        },
        previewImage: function (event) {
            $("#id_profile_preview").cropper('destroy');
            this.imageUploadProgress = 0;
            this.imageUpdated = false;
            var input = event.target;


            if (input.files && input.files[0]) {
                var reader = new FileReader();
                reader.onload = (e) => {
                    this.imageData = e.target.result;
                }
                reader.readAsDataURL(input.files[0]);

            }
        },
        previewImageCover: function (event) {
            var input = event.target;
            if (input.files && input.files[0]) {
                var reader = new FileReader();
                reader.onload = (e) => {
                    this.coverimageData = e.target.result;
                }
                reader.readAsDataURL(input.files[0]);
            }
        },
        uploadProfileImg: function () {

            var blob = this.b64ToBlob("#id_profile_preview");

            var formData = new FormData();

            formData.append("image", blob,this.getProfileImageName());

            axios.put("/api/user/update-profile-img/" + document.getElementById("user_pk").value,
                formData, this.get_axios_config("profileImage")).then((response) => {
                console.log("Done");
                this.imageUpdated = true;
            }).catch((e) => {
                console.log(e);
            });

        },
        uploadCoverImg: function () {
            var input = document.getElementById("coverImageInput");
            var formData = new FormData();
            formData.append("cover_image", input.files[0]);
            var self = this;

            axios.put("/api/user/update-cover-pic/" + document.getElementById("user_pk").value,
                formData, this.get_axios_config('coverImage')).then((response) => {
                console.log("Done");
                this.imageUpdated = true;
            }).catch((e) => {
                console.log(e);
            })


        },
        getIdFromPath() {
            var splitted = document.URL.split("/");
            return splitted[splitted.length - 2];
        },
        get_axios_config: function (progressName) {
            var csrftoken = this.getCookie('csrftoken');
            var self = this;

            return {
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'multipart/form-data', 'X-CSRFToken': csrftoken
                },
                onUploadProgress: function (progressEvent) {

                    var percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                    console.log(percentCompleted);
                    self.update_progress_bar(progressName, percentCompleted);
                }

            }
        },
        update_progress_bar: function (progressName, value) {
            if (progressName === "profileImage") {
                this.imageUploadProgress = value
            }
            if (progressName === "coverImage") {
                this.profileImageUploadProgress = value
            }
        },
        getCookie: function (name) {
            var cookieValue = null;

            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }

            return cookieValue;
        },
        enableCropper: function (id) {
            $(id).cropper({
                aspectRatio: 1
            });
        },
        b64ToBlob: function (id) {
            var imageURL = $(id).cropper('getCroppedCanvas').toDataURL("image/png");
            var block = imageURL.split(";");
            // Get the content type of the image
            var contentType = block[0].split(":")[1];// In this case "image/gif"
            // get the real base64 content of the file
            var b64Data = block[1].split(",")[1];// In this case "R0lGODlhPQBEAPeoAJosM...."


            contentType = contentType || '';
            sliceSize = 512;

            var byteCharacters = atob(b64Data);
            var byteArrays = [];

            for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) {
                var slice = byteCharacters.slice(offset, offset + sliceSize);

                var byteNumbers = new Array(slice.length);
                for (var i = 0; i < slice.length; i++) {
                    byteNumbers[i] = slice.charCodeAt(i);
                }

                var byteArray = new Uint8Array(byteNumbers);

                byteArrays.push(byteArray);
            }

            var blob = new Blob(byteArrays, {type: contentType});
            return blob;
        },
        getProfileImageName(){
            var name = "profile_"+document.getElementById("user_pk").value+".png";
            return name;
        }

    },
    watch: {
        imageData: function (val) {
            // this.enableCropper("#id_profile_preview");
            var self = this;
            setTimeout(function () {
                self.enableCropper("#id_profile_preview");
            }, 1000);
        }
    }

});