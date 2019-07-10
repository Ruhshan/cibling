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
         console.log(date)
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
             console.log(respose.data)
             self.user = respose.data
         }).catch((err)=>{
             console.log(err)
         })

         console.log(this.user.profile_image)
     }
   }
});