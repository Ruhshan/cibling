


var app = new Vue({
    el: '#app',
    components: { "tags-input": VoerroTagsInput },
    data: {
        message: 'Hello Vue!',
        country: "",
        subject: "",
        institutes: [],
        selectedExpertises:[],
        existingExpertises:[],
        selectedInterests:[],
        existingInterests:[],

    },
    created() {
        var self = this;

        var previous_expertises = document.getElementById("previous_expertise").value;
        var previous_interests = document.getElementById("previous_interest").value;

        document.getElementById("id_offer").parentNode.innerHTML+='<small class="form-text text-muted" >Adding offers will increase your exposure to ciblings!</small>';


        if(previous_expertises.length !==0 && previous_expertises !== "None"){
        previous_expertises.split(",").forEach((item)=>{
            var kv={key:"", value:item}
            this.selectedExpertises.push(kv);
        });
        }

        if(previous_interests.length !== 0 && previous_interests !== "None"){
        previous_interests.split(",").forEach((item)=>{
            var kv={key:"", value:item}
            this.selectedInterests.push(kv);
        });
        }




        axios.get("/api/user/expertises").then((response)=>{
            response.data.forEach((item)=>{
                var kv = {key:item.id.toString(), value:item.expertise}
                self.existingExpertises.push(kv)
            });

        }).catch((err)=>{
            console.log(err);
        });


        axios.get("/api/user/interests").then((response)=>{
            response.data.forEach((item)=>{
                var kv = {key:item.id.toString(), value: item.interest}
                self.existingInterests.push(kv)
            });

        }).catch((err)=>{
            console.log(err);
        });


    },
    methods: {
        changedTags:function(name, value){
            var current = this.selectedExpertises
            console.log(current)
            current.push(value)
            console.log(current)
            this.selectedExpertises = current


        },
        focused: function () {
            var country = document.getElementById("id_country").value;

            console.log("focused");

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
                this.$refs.country.focus();

            }
        },
        expertise_pressed:function () {
            console.log("expertise pressed")
        }
    }
});

