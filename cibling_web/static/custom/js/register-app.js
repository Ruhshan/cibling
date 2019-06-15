var app = new Vue({
    el: '#app',
    data: {
        message: 'Hello Vue!',
        country: "",
        subject: "",
        institutes: [],
        expertiseModel:"",
        expertises: ["biman","bala"]
    },
    created() {
        console.log("App created");
    },
    methods: {
        focused: function () {
            if (this.country) {
                this.institutes = [];
                var self = this;
                axios.get("/api/user/institute/" + this.country).then((response) => {

                    response.data.forEach((item)=>{
                        self.institutes.push(item.institute);
                    });

                }).catch((err) => console.log(err));


            } else {
                alert("Enter country first!");
            }
        },
        expertise_pressed:function () {
            console.log("expertise pressed")
        }
    }
});