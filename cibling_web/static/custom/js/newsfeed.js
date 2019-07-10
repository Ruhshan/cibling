// $(document).ready(function (){
//     $("#all-posts").paginate({
//         perPgae: 15
//     });
// });

var app = new Vue({
    el: "#all-posts",
    data: {
        page: 1,
        posts: [],
        user: ""
    },
    created() {
        console.log("created")
        this.get_myinfo()
        //this.get_posts()
    },

    filters: {
        formatDate: function (date) {
            return moment(date).format('MMMM Do YYYY, h:mm:ss a')
        },
        urlize: function(text){
            u = urlize(text)
            return u
        }

    },

    methods: {
        urlize: function(text){
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
            var comment_id = "id_comment_" + id
            comment_text = document.getElementById(comment_id).value

            comment = {
                "author": this.user,
                "text": comment_text,
                "post": id
            }

            console.log(comment)

            post.comments.push(comment)

            document.getElementById(comment_id).value = ""


        },
        post_detail:function (url) {
            location.href = url
        }
        ,
        infiniteHandler($state) {
            axios.get("/api/cibling-web/posts", {
                params: {
                    page: this.page,
                },
            }).then(({data}) => {
                console.log(data)
                if (data.results.length) {
                    this.page += 1;
                    this.posts.push(...data.results);
                    $state.loaded();
                } else {
                    $state.complete();
                }
            });
        },

    }
});