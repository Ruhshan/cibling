let OneImage ={
    template:`
    <a :href="image0.image" class="lsb-preview" :data-lsb-group="lsbGroup">
    <div v-bind:style="{ 'background': 'url(' + image0.image + ')' }" v-bind:class="[gridBase, photoClass]"></div>
    </a>
    `,
    created:function () {
        this.image0=this.images[0]

        if(this.image0.height / this.image0.width > 1){
            this.photoClass = 'photo10portrait'
        }else{
            this.photoClass = 'photo10landscape'
        }
    },
    data(){
    return {
      gridBase: 'gridbase',
      photoClass: 'photo10landscape',
      image0:[]
    }},
    props:{
        images:Array,
        lsbGroup:String
    }
}