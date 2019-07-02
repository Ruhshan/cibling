Vue.component('v-select', VueSelect.VueSelect);

new Vue({
  el: '#app',
  data: {
      countries :[],
      subjects : [],
      expertises: []

  },

  created:function () {
      this.fetchData("countries");
      this.fetchData("subjects");
      this.fetchData("expertises");
  },

  methods:{
      fetchData:function (name) {
        var self = this;

        axios.get("/api/user/"+name).then((response)=>{

        response.data.forEach((item)=>{
            if(name === "countries"){
                self.countries.push(item.country.trim());

            }
            if(name === "subjects"){
                self.subjects.push(item.subject.trim());

            }
            if(name === "expertises"){
                self.expertises.push(item.expertise.trim());

            }



        });

        //self.countries = countries;
        //self.countries = ["Bangladesh", "India"]

        }).catch((err)=>{
        console.log(err)
        })

      }
  }

});