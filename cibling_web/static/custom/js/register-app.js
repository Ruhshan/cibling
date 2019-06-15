var app = new Vue({
  el: '#app',
  data: {
    message: 'Hello Vue!',
    country:"",
    institutes:["SUST","JUST"]
  },
  created(){
      console.log("App created");
  },
  methods:{
      focused:function(){
          if(this.country){
              this.institutes = ["BUST","TUST"]
          }else{
              alert("Enter country first!");
          }
      }
  }
});