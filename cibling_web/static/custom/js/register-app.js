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

        var previous_expertises = document.getElementById("previous_expertise").value;
        var previous_interests = document.getElementById("previous_interest").value;


        if(previous_expertises.length !==0 && previous_expertises !== "None"){
        previous_expertises.split(",").forEach((item)=>{
            this.selectedExpertises.push(item);
        });
        }

        if(previous_interests.length !== 0 && previous_interests !== "None"){
        previous_interests.split(",").forEach((item)=>{
            this.selectedInterests.push(item);
        });
        }



        axios.get("/api/user/expertises").then((response)=>{
            response.data.forEach((item)=>{
                self.existingExpertises[item["expertise"]] = item["expertise"];
            });

        }).catch((err)=>{
            console.log(err);
        });

        axios.get("/api/user/interests").then((response)=>{
            response.data.forEach((item)=>{
                self.existingInterests[item["interest"]] = item["interest"];
            });

        }).catch((err)=>{
            console.log(err);
        })
    },
    methods: {
        focused: function () {
            var country = document.getElementById("id_country").value;

            if (country) {
                this.institutes = [];
                var self = this;
                axios.get("/api/user/institute/" + country).then((response) => {

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