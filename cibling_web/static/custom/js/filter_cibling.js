Vue.component('v-select', VueSelect.VueSelect);

new Vue({
    el: '#app',
    data: {
        country: "",
        institute: "",
        subject: "",
        expertise: "",
        countries: [],
        subjects: [],
        expertises: [],
        institutes: [],
        ciblings: []


    },

    created: function () {
        this.fetchData("countries");
        this.fetchData("subjects");
        this.fetchData("expertises");
    },

    methods: {
        fetchData: function (name, param) {
            var self = this;

            var url = "/api/user/" + name;
            if (param) {
                url += "/" + param
            }

            console.log(url)

            axios.get(url).then((response) => {

                response.data.forEach((item) => {
                    if (name === "countries") {
                        self.countries.push(item);

                    }
                    if (name === "subjects") {
                        self.subjects.push(item);

                    }
                    if (name === "expertises") {
                        self.expertises.push(item);

                    }
                    if (name === "institute") {
                        self.institutes.push(item)
                    }

                });

            }).catch((err) => {
                console.log(err)
            })

        },
        search: function () {
            console.log("searching...");
            var csrftoken = this.getCookie('csrftoken');
            var self = this;

            data = {
                country: this.country ? this.country.id : null,
                institute: this.institute ? this.institute.id : null,
                subject: this.subject ? this.subject.id : null,
                expertise: this.expertise ? this.expertise.id : null
            }

            axios.post("/api/user/profiles",
                data,
                {
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    }
                }).then((response) => {
                self.ciblings = response.data
            }).catch((err) => {
                console.log(err)
            })
        },

        getCookie: function (name) {
            var cookieValue = null;

            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }

            return cookieValue;
        }
    },

    watch: {
        country: function (val) {
            this.institutes = [];
            if (val) {

                this.fetchData("institute", val.id)
            }

        }
    }

});