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
        expertiseModel:"",
        expertises: ["biman","bala"],

        selectedExpertises:[],
        existingExpertises:{
            1: 'Web Development',
            2: 'PHP',
            3: 'JavaScript',
            4: 'Mysql'
        },

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