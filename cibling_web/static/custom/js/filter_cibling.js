Vue.component('v-select', VueSelect.VueSelect);

Vue.use(VueSpinners);


new Vue({
    el: '#app',
    data: {
        country: null,
        institute: null,
        subject: null,
        expertise: null,
        offer: null,
        countries: [],
        subjects: [],
        expertises: [],
        institutes: [],
        offers: [],
        ciblings: [],
        searching: false,
        message: ""


    },

    created: function () {
        this.fetchData("countries");
        this.fetchData("subjects");
        this.fetchData("expertises");
        this.fetchData("offers");

        this.checkUrlpath();


    },

    methods: {

        fetchData: function (name, param) {
            var self = this;

            var url = "/api/user/" + name;
            if (param) {
                url += "/" + param
            }


            self.searching = true
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
                    if (name === "ciblings") {
                        self.ciblings.push(item)
                    }
                    if (name == "offers") {
                        self.offers.push(item)
                    }


                });
                self.searching = false
            }).catch((err) => {
                self.searching = false
                console.log(err)
            })

        },
        checkUrlpath: function () {
            var splitted_path = window.location.pathname.split("/");
            target = splitted_path[2];
            id = splitted_path[3];

            if (target === "offer") {
                this.directSearch("offer", parseInt(id));
            }
            else{
                this.fetchData("ciblings")
            }
        },
        directSearch: function (target, value) {
            var csrftoken = this.getCookie('csrftoken');
            var self = this;
            data = {
                country: null,
                institute: null,
                subject: null,
                expertise: null,
                offer: value
            }

            axios.post("/api/user/profiles",
                data,
                {
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    }
                }
            ).then((response) => {
                if (response.status === 204) {

                    self.message = "No one available!"
                } else {
                    console.log(response.data)

                    self.ciblings = response.data


                }
                self.searching = false
            }).catch((err) => {
                self.searching = false
                console.log(err)
            });
        },
        search: function () {
            console.log("searching...");
            var csrftoken = this.getCookie('csrftoken');
            var self = this;

            this.searching = true;
            this.ciblings = []

            data = {
                country: this.country ? this.country.id : null,
                institute: this.institute ? this.institute.id : null,
                subject: this.subject ? this.subject.id : null,
                expertise: this.expertise ? this.expertise.id : null,
                offer: this.offer ? this.offer.id : null
            }

            console.log(this.country || this.institute || this.subject || this.expertise != null);

            if (this.country || this.institute || this.subject || this.expertise != null || this.offer != null) {
                axios.post("/api/user/profiles",
                    data,
                    {
                        headers: {
                            'Accept': 'application/json',
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrftoken
                        }
                    }).then((response) => {

                    console.log(response.data)

                    if (response.status == 204) {

                        self.message = "No one available!"
                    } else {
                        console.log(response.data)
                        self.ciblings = response.data

                    }
                    self.searching = false

                }).catch((err) => {
                    self.searching = false
                    console.log(err)
                })
            } else {
                self.message = "Please select at least one search criteria!"
                self.searching = false
            }

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