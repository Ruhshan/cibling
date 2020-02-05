var app = new Vue({
    el: "#new-post",
    data:{
      imageDatas:[]
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
            input.accepts ="image/*";

            input.onchange = e => {

                var reader = new FileReader();
                reader.onload = (e) => {
                    this.imageDatas.push( e.target.result);
                }

                reader.readAsDataURL(input.files[0]);


            }

            input.click();
        },

    }
})