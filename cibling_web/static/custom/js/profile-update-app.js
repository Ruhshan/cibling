var profileUpdateApp = new Vue({
    el: "#profileUpdateApp",
    components: {"tags-input": VoerroTagsInput},
    data: {
        selectedExpertises: [],
        existingExpertises: {},
        selectedInterests: [],
        existingInterests: {},
    },
    created() {
        var self = this;
        var previous_expertises = document.getElementById("previous_expertises").value;
        var previous_interests = document.getElementById("previous_interests").value;


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
    }
});