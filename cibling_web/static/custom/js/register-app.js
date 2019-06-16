//import VueTagInput from 'vue-tag-input'
//import VueTagInput from 'vue-tag-input'

var app = new Vue({
    el: '#app',
    components: { "tags-input": VoerroTagsInput },
    data: {
        message: 'Hello Vue!',
        country: "",
        subject: "",
        institutes: [],
        selectedExpertises:[],
        existingExpertises:{},
        selectedInterests:[],
        existingInterests:{}

    },
    created() {
        var self = this;


        axios.get("/api/user/expertises").then((response)=>{
            response.data.forEach((item)=>{
                self.existingExpertises[item["id"]] = item["expertise"];
            });

        }).catch((err)=>{
            console.log(err);
        });

        axios.get("/api/user/interests").then((response)=>{
            response.data.forEach((item)=>{
                self.existingInterests[item["id"]] = item["interest"];
            });

        }).catch((err)=>{
            console.log(err);
        })
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