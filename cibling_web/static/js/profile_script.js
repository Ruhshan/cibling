var profileImageApp = new Vue({
    el: "#profileApp",
    data: {
        imageData: "",
        imageUploadProgress : 0,
        imageUpdated: false
    },
    created() {
    },
    methods: {
        profileImageChangeModal: function () {
            $("#profileImageChangeModal").modal('show');

        },
        closeModal: function(name){
            console.log("Closing modal");
            $("#profileImageChangeModal").modal('hide');

            if(this.imageUpdated){
                window.location.reload();
            }

        },
        previewImage: function (event) {
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
        uploadProfileImg: function () {
            var input = document.getElementById("profileImageInput");

            var formData = new FormData();
            formData.append("image", input.files[0]);
            var url = document.URL;
            var id = url.substr(url.lastIndexOf('/') + 1);
            var self=this;

            axios.put("/api/user/update-profile-img/14" + id,
                formData, this.get_axios_config("profileImage")).then((response) => {
                console.log("Done");
                this.imageUpdated=true;
            });
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
        update_progress_bar:function(progressName, value){
            if(progressName === "profileImage"){
                this.imageUploadProgress = value
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
        }

    }

});