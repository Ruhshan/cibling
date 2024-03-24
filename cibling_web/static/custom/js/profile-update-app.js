var profileUpdateApp = new Vue({
    el: "#profileUpdateApp",
    components: {"tags-input": VoerroTagsInput},
    data: {
        selectedExpertises: [],
        existingExpertises: [],
        selectedInterests: [],
        existingInterests: [],
        selectedLanguages: [],
        existingLanguages: [],
        institutes: [],
    },
    created() {
        var self = this;
        var previous_expertises = document.getElementById("previous_expertises").value;
        var previous_interests = document.getElementById("previous_interests").value;
        var previous_languages = document.getElementById("previous_languages").value;


        console.log(previous_languages)


        if (previous_expertises.length !== 0 && previous_expertises !== "None") {
            previous_expertises.split(",").forEach((item) => {
                item = item.includes("Expertise: ") ? item.match(": (.*)>")[1] : item;

                kv={key:"", value:item}

                this.selectedExpertises.push(kv);
            });
        }

        if (previous_interests.length !== 0 && previous_interests !== "None") {
            previous_interests.split(",").forEach((item) => {
                item = item.includes("Interest: ") ? item.match(": (.*)>")[1] : item;

                kv = {key:"", value: item}
                this.selectedInterests.push(kv);
            });
        }

        if (previous_languages.length !== 0 && previous_languages !== "None") {
            previous_languages.split(",").forEach((item) => {
                item = item.includes("Language: ") ? item.match(": (.*)>")[1] : item;
                kv = {key:"",value:item}
                this.selectedLanguages.push(kv);
            });
        }

        axios.get("/api/user/expertises").then((response) => {
            response.data.forEach((item) => {
                var kv = {key:item.id.toString(), value:item.expertise}
                self.existingExpertises.push(kv);
            });

        }).catch((err) => {
            console.log(err);
        });

        axios.get("/api/user/interests").then((response) => {
            response.data.forEach((item) => {

                var kv = {key:item.id.toString(), value: item.interest}
                self.existingInterests.push(kv);
            });

        }).catch((err) => {
            console.log(err);
        });
        axios.get("/api/user/languages").then((response) => {
            response.data.forEach((item) => {
                var kv = {key:item.id.toString(), value:item.language}
                self.existingLanguages.push(kv);
            });

        }).catch((err) => {
            console.log(err);
        });
    },
    methods:{
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
    }
});