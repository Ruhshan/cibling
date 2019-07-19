Vue.component('v-select', VueSelect.VueSelect);

Vue.use(VueSpinners);

var app = new Vue({
    el: '#app',
    data: {
        recipient: {},
        subject: "",
        body: "",
        users: [],
        error: {subject: "", recipient: "", body: ""},
        delivering:false,
        successMessage:""


    },
    created() {
        this.check_recepient_in_urlpath()
    },
    methods: {
        check_recepient_in_urlpath: function () {
            var self = this
            var name = window.location.pathname.split("/")[3];

            if(name){
                axios.get("/api/user/profile/"+name).then((response)=>{

                    var entry = {
                            "title": response.data.first_name + " " + response.data.last_name,
                            "image": response.data.profile_image,
                            "id": response.data.id
                        };

                    self.recipient = entry
                }).catch((err)=>{
                    console.log(err)
                })
            }
        }
        ,
        onSearch: function (search, loading) {

            loading(true);

            this.search(loading, search);


        },
        search: function (loading, search) {

            var self = this;


            if (search.length != 0) {

                axios.get("/api/user/profiles?q=" + search).then((response) => {
                    var fetched_users = [];

                    response.data.forEach((user) => {

                        var entry = {
                            "title": user.user.first_name + " " + user.user.last_name,
                            "image": user.image,
                            "id": user.user.id
                        };
                        //console.log(entry);
                        fetched_users.push(entry);
                    });
                    console.log(fetched_users);

                    self.users = fetched_users;

                    loading(false);


                }).catch((err) => {
                    console.log(err);
                })
            } else {
                loading(false)
            }

        },
        onSend: function () {
            var recipient = this.recipient;
            var subject = this.subject;
            var body = this.body;

            var has_error = 0;

            if (recipient == null || recipient.id == null) {
                document.getElementById("div_id_recipients").classList.add("has-error");
                this.error.recipient = "Please select a recipient."
                has_error += 1
            } else {
                document.getElementById("div_id_recipients").classList.remove("has-error");
                this.error.recipient = ""
            }

            // if (subject.trim().length === 0) {
            //     document.getElementById("div_id_subject").classList.add("has-error");
            //     this.error.subject = "Subject cannot be empty."
            //     has_error += 1
            // } else {
            //     this.error.subject = ""
            //     document.getElementById("div_id_subject").classList.remove("has-error");
            // }
            if (body.trim().length === 0) {
                document.getElementById("div_id_body").classList.add("has-error");
                this.error.body = "Body cannot be empty."
                has_error += 1
            } else {
                this.error.body = ""
                document.getElementById("div_id_body").classList.remove("has-error");
            }


            if (has_error == 0) {
                this.send()
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
        },
        send: function () {
            var csrftoken = this.getCookie('csrftoken');
            var self = this;

            self.delivering = true;

            console.log(self.delivering);

            axios.post("/api/user/send-message",
                {
                    recipient: this.recipient.id,
                    subject: this.subject,
                    body:this.body
                },
                {headers: {'Accept': 'application/json', 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken}}
            ).then((response) => {
                console.log(response);
                self.delivering = false

                self.successMessage = "Message delivered"
                self.clear()

            }).catch((err) => {
                console.log(err);
            })

        },
        clear:function () {
            this.recipient = ""
            this.subject=""
            this.body = ""
            var self = this

            setTimeout(function(){
                self.successMessage=""
            }, 3000);

        }

    },


});