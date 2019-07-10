// $(document).ready(function (){
//     $("#all-posts").paginate({
//         perPgae: 15
//     });
// });

var app = new Vue({
   el:"#all-posts",
   data:{
      posts:[],
      user:""
   } ,
   created(){
       console.log("created")
       this.get_myinfo()
       this.get_posts()
   },

   filters:{
     formatDate:function (date) {
         return moment(date).format('MMMM Do YYYY, h:mm:ss a')
     }
   },

   methods:{
     get_posts:function(){
         var self = this

         axios.get("/api/cibling-web/posts").then((respose)=>{
             self.posts = respose.data
         }).catch((err)=>{
             console.log(err)
         })
     },
     get_myinfo:function () {
         var self = this

         axios.get("/api/user/me").then((respose)=>{
             self.user = respose.data
         }).catch((err)=>{
             console.log(err)
         })

         console.log(this.user.profile_image)
     },
     get_comment_id:function (id) {
       return "id_comment_"+id
     },
     make_comment: function (id, post) {
         var comment_id = "id_comment_"+id
         comment_text = document.getElementById(comment_id).value

         comment = {
                "author": this.user,
                "text": comment_text,
                "post": id
            }

         console.log(comment)

         post.comments.push(comment)

         document.getElementById(comment_id).value = ""



     }

   }
});