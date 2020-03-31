

var app = new Vue({
    el: "#all-posts",
    data: {
        iframeWidth: "480px",
        iframeHeight: "320px",
        page: 1,
        posts: [],
        user: "",
        forDelete: ""
    },
    created() {

        this.get_myinfo();
        //this.get_posts()
        var parentWidth = parseInt(document.getElementsByClassName("post-detail")[0].offsetWidth);

        this.iframeWidth = parentWidth+"px";
        this.iframeHeight = (parentWidth / 1.5) + "px";
        window.addEventListener("resize", this.windowResizeHandler);


    },


    filters: {
        formatDate: function (date) {
            var formatted = moment(date).format('MMMM Do YYYY, h:mm:ss a')
            return formatted
        },
        urlize: function (text) {
            u = urlize(text)
            return u
        }

    },

    methods: {
        windowResizeHandler: function (e) {
            var parentWidth = parseInt(document.getElementsByClassName("post-detail")[0].offsetWidth);

            this.iframeWidth = parentWidth+"px";
            this.iframeHeight = (parentWidth / 1.5) + "px";
        },
        getLsbGroup:function(post){
          return "group"+post.id;
        },
        getPhotosSectionId:function(photos){
            return "photos-"+photos.length;
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
        urlize: function (text) {
            u = urlize(text)
            return u
        },
        get_posts: function () {
            var self = this

            axios.get("/api/cibling-web/posts").then((respose) => {
                self.posts = respose.data.results
            }).catch((err) => {
                console.log(err)
            })
        },
        get_myinfo: function () {
            var self = this

            axios.get("/api/user/me").then((respose) => {
                self.user = respose.data
            }).catch((err) => {
                console.log(err)
            })

            console.log(this.user.profile_image)
        },
        get_comment_id: function (id) {
            return "id_comment_" + id
        },
        make_comment: function (id, post) {
            var self = this;
            var comment_id = "id_comment_" + id;
            comment_text = document.getElementById(comment_id).value;

            comment = {
                "author": this.user.id,
                "text": comment_text,
                "post": id
            }

            axios.post("/api/cibling-web/comment",
                comment,
                self.get_csrf_header())
                .then((response) => {
                    comment["author"] = self.user;
                    post.comments.push(comment);
                }).catch((err) => {
                console.log(err);
            });


            document.getElementById(comment_id).value = ""


        },
        post_detail: function (url) {
            location.href = url
        }
        ,
        show_modal: function (index) {
            this.forDelete = index;
            $('#myModal').modal('show');
        },

        get_csrf_header: function () {
            var csrftoken = this.getCookie('csrftoken')

            return {
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json', 'X-CSRFToken': csrftoken
                }
            }
        },
        post_delete: function () {
            var self = this;

            var id = this.posts[this.forDelete].id;

            this.$delete(this.posts, this.forDelete);

            axios.delete("/api/cibling-web/post/" + id,
                self.get_csrf_header()
            ).then((response) => {
                $('#myModal').modal('hide');
            }).catch((err) => {
                console.log(err);
            });

            this.forDelete = ""


        },
        infiniteHandler($state) {
            axios.get("/api/cibling-web/posts", {
                params: {
                    page: this.page,
                },
            }).then(({data}) => {
                if (data.results.length) {
                    this.page += 1;

                    new Promise((resolve, reject)=>{
                         this.posts.push(...data.results);
                         resolve(true);
                    }).then(res=>{
                        $.fn.lightspeedBox();
                         $('.lazy').lazy();
                    })

                    $state.loaded();

                } else {
                    $state.complete();
                }
            }).catch((err) => {

                $state.complete();
            });
        },

    }
});