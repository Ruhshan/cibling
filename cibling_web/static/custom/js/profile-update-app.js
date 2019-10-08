var profileUpdateApp = new Vue({
    el: "#profileUpdateApp",
    components: {"tags-input": VoerroTagsInput},
    data: {
        selectedExpertises: [],
        existingExpertises: {},
        selectedInterests: [],
        existingInterests: {},
        selectedLanguages: [],
        existingLanguages: {},
        institutes: [],
    },
    created() {
        var self = this;
        var previous_expertises = document.getElementById("previous_expertises").value;
        var previous_interests = document.getElementById("previous_interests").value;
        var previous_languages = document.getElementById("previous_languages").value;



        if (previous_expertises.length !== 0 && previous_expertises !== "None") {
            previous_expertises.split(",").forEach((item) => {
                item = item.includes("Expertise: ") ? item.match(": (.*)>")[1] : item;
                this.selectedExpertises.push(item);
            });
        }

        if (previous_interests.length !== 0 && previous_interests !== "None") {
            previous_interests.split(",").forEach((item) => {
                item = item.includes("Interest: ") ? item.match(": (.*)>")[1] : item;
                this.selectedInterests.push(item);
            });
        }

        if (previous_languages.length !== 0 && previous_languages !== "None") {
            previous_languages.split(",").forEach((item) => {
                item = item.includes("Language: ") ? item.match(": (.*)>")[1] : item;
                this.selectedLanguages.push(item);
            });
        }

        axios.get("/api/user/expertises").then((response) => {
            response.data.forEach((item) => {
                self.existingExpertises[item["expertise"]] = item["expertise"];
            });

        }).catch((err) => {
            console.log(err);
        });

        axios.get("/api/user/interests").then((response) => {
            response.data.forEach((item) => {
                self.existingInterests[item["interest"]] = item["interest"];
            });

        }).catch((err) => {
            console.log(err);
        });
        axios.get("/api/user/languages").then((response) => {
            response.data.forEach((item) => {
                self.existingLanguages[item["language"]] = item["language"];
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