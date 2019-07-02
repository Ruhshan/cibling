Vue.component('v-select', VueSelect.VueSelect);

new Vue({
  el: '#app',
  data: {
      countries :[]
  },

  created:function () {
      var self = this;
      var countries = []
    axios.get("/api/user/countries").then((response)=>{

        response.data.forEach((item)=>{
            countries.push(item.country.trim());
        })

        self.countries = countries;
        //self.countries = ["Bangladesh", "India"]

    }).catch((err)=>{
        console.log(err)
    })
  }

});