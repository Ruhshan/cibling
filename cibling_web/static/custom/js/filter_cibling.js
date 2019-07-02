Vue.component('v-select', VueSelect.VueSelect);

new Vue({
  el: '#app',
  data: {
      country : "",
      countries :[],
      subjects : [],
      expertises: [],
      institutes: []


  },

  created:function () {
      this.fetchData("countries");
      this.fetchData("subjects");
      this.fetchData("expertises");
  },

  methods:{
      fetchData:function (name, param) {
        var self = this;

        var url = "/api/user/"+name;
        if(param){
            url+="/"+param
        }

        console.log(url)

        axios.get(url).then((response)=>{

        response.data.forEach((item)=>{
            if(name === "countries"){
                self.countries.push(item);

            }
            if(name === "subjects"){
                self.subjects.push(item.subject.trim());

            }
            if(name === "expertises"){
                self.expertises.push(item.expertise.trim());

            }
            if(name === "institute"){
                self.institutes.push(item)
            }

        });

        }).catch((err)=>{
        console.log(err)
        })

      }
  },

  watch:{
      country:function (val) {
          this.institutes = [];
          if(val){

            this.fetchData("institute", val.id)
          }

      }
  }

});