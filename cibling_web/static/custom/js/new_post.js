var app = new Vue({
    el: "#new-post",
    data: {
        imageDatas: [],
        showPhotoBox: false,
        postContent: "",
        postUploadProgress: 0,
        youtubeLink: null,
        ytId: null
    },
    created: function () {
    },
    watch: {
        youtubeLink:function () {
            this.ytId = this.getYtId(this.youtubeLink);
        }
    },
    methods: {
        toggelePhotoBox: function () {
            if (this.showPhotoBox) {
                this.showPhotoBox = false;
            } else {
                this.showPhotoBox = true;
            }
        },
        addPhoto: function () {
            var input = document.createElement('input');
            input.type = 'file';
            input.accepts = "image/*";

            input.onchange = e => {

                var reader = new FileReader();
                reader.onload = (e) => {
                    this.imageDatas.push({id: this.getRandomId(), val: e.target.result});
                }

                reader.readAsDataURL(input.files[0]);


            }

            input.click();
        },

        getRandomId: function () {
            return Math.floor(Math.random() * 1000);
        },

        remove: function (imgId) {
            for (var i = 0; i < this.imageDatas.length; i++) {
                if (this.imageDatas[i].id === imgId) {
                    this.imageDatas.splice(i, 1);
                }
            }
        },
        getYtId: function (url) {
            const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
            const match = url.match(regExp);

            return (match && match[2].length === 11)
                ? match[2]
                : null;
        },
        publish: function () {


            var csrftoken = this.getCookie('csrftoken');
            var headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json', 'X-CSRFToken': csrftoken
            };

            data = {
                content: this.postContent,
                images: this.imageDatas,
                youtubeId: this.ytId
            }
            var self = this;

            if (this.postContent) {
                axios.post("/api/cibling-web/post/create", data, {
                    headers: headers,
                    onUploadProgress: function (progressEvent) {

                        var percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                        self.postUploadProgress = percentCompleted;
                    }
                }).then((res) => {
                    window.location = "/post/" + res.data;
                }).catch((err) => {
                    console.log(JSON.stringify(err))
                })

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

    }
})