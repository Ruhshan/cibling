// $(document).ready(function (){
//     $("#all-posts").paginate({
//         perPgae: 15
//     });
// });

var app = new Vue({
   el:"#all-posts",
   data:{
      posts:[]
   } ,
   created(){
       console.log("created")
       this.get_posts()
   },

   methods:{
     get_posts:function(){
         var self = this

         axios.get("/api/cibling-web/posts").then((respose)=>{
             self.posts = respose.data
         }).catch((err)=>{
             console.log(err)
         })
     }
   }
});