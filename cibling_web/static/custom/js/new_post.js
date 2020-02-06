var app = new Vue({
    el: "#new-post",
    data: {
        imageDatas: []
    },
    created: function () {

    },
    methods: {
        openAddMediaModal: function () {
            $('#addMediaModal').modal('show')
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
        }

    }
})