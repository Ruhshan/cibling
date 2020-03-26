function getBgUrl(image){
    return 'url(' + image.image + ')'
}

let OneImage ={
    template:`
    <section :id="sectionId">
        <a :href="image0.image" class="lsb-preview" :data-lsb-group="lsbGroup">
            <div v-bind:style="{ 'background': image0.background }" v-bind:class="[gridBase, photoClass]"></div>
        </a>
    </section>
    `,
    created:function () {
        this.image0=this.images[0]
        this.image0['background'] = getBgUrl(this.image0)

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
        lsbGroup:String,
        sectionId:String
    }
}

let TwoImages ={
    template:`
    <section :id="sectionId">
    <div style="display: flex; flex-direction: row">
        <div>
                <a :href="image0.image" class="lsb-preview" :data-lsb-group="lsbGroup">
                    <div v-bind:style="{ 'background' : image0.background }" class="photo20 gridbase"></div>
                </a>
        </div>
        <div>    
                <a :href="image1.image" class="lsb-preview" :data-lsb-group="lsbGroup">
                    <div v-bind:style="{ 'background' : image1.background }" class="photo21 gridbase"></div>
                </a>
        </div>
    </div>
    </section>
    `,
    created:function () {
        this.image0=this.images[0]
        this.image0['background'] = getBgUrl(this.image0)
        this.image1=this.images[1]
        this.image1['background'] = getBgUrl(this.image1)
    },
    data(){
    return {
      image0:[],
      image1:[]
    }},
    props:{
        images:Array,
        lsbGroup:String,
        sectionId:String
    }
}

let ThreeImages = {
    template: `
    <section :id="sectionId">
    <div>
        <a :href="image0.image" class="lsb-preview" :data-lsb-group="lsbGroup">
            <div v-bind:style="{ 'background' : image0.background }" class="photo30 gridbase"></div>
        </a>
    </div>
    <div style="display: flex; flex-direction: row">
        <div>
            <a :href="image1.image" class="lsb-preview" :data-lsb-group="lsbGroup">
                <div v-bind:style="{ 'background' : image1.background }" class="photo31 gridbase"></div>
            </a>
        </div>
        <div>    
            <a :href="image2.image" class="lsb-preview" :data-lsb-group="lsbGroup">
                <div v-bind:style="{ 'background' : image2.background }" class="photo32 gridbase"></div>
            </a>
        </div>
    </div>
    </section>
    `,
    created: function () {
        this.image0 = this.images[0]
        this.image0['background'] = getBgUrl(this.image0)
        this.image1 = this.images[1]
        this.image1['background'] = getBgUrl(this.image1)
        this.image2 = this.images[2]
        this.image2['background'] = getBgUrl(this.image2)
    },
    data() {
        return {
            image0: [],
            image1: [],
            image2: []
        }
    },
    props: {
        images: Array,
        lsbGroup: String,
        sectionId:String
    }
}

let FourImages = {
    template: `
    <section :id="sectionId">
    
    <div style="display: flex; flex-direction: row">
        <div>
            <div>
                <a :href="image0.image" class="lsb-preview" :data-lsb-group="lsbGroup">
                    <div v-bind:style="{ 'background' : image0.background }" class="photo40 gridbase"></div>
                </a>
            </div>
            <div>    
                <a :href="image1.image" class="lsb-preview" :data-lsb-group="lsbGroup">
                    <div v-bind:style="{ 'background' : image1.background }" class="photo41 gridbase"></div>
                </a>
            </div>
        </div>
        <div>
            <div>
                <a :href="image2.image" class="lsb-preview" :data-lsb-group="lsbGroup">
                    <div v-bind:style="{ 'background' : image2.background }" class="photo42 gridbase"></div>
                </a>
            </div>
            <div>    
                <a :href="image3.image" class="lsb-preview" :data-lsb-group="lsbGroup">
                    <div v-bind:style="{ 'background' : image3.background }" class="photo43 gridbase"></div>
                </a>
            </div>
        </div>
    </div>
    </section>
    `,
    created: function () {
        this.image0 = this.images[0]
        this.image0['background'] = getBgUrl(this.image0)
        this.image1 = this.images[1]
        this.image1['background'] = getBgUrl(this.image1)
        this.image2 = this.images[2]
        this.image2['background'] = getBgUrl(this.image2)
        this.image3 = this.images[3]
        this.image3['background'] = getBgUrl(this.image3)
    },
    data() {
        return {
            image0: [],
            image1: [],
            image2: [],
            image3: []
        }
    },
    props: {
        images: Array,
        lsbGroup: String,
        sectionId:String
    }
}

let FiveImages = {
    template: `
    <section :id="sectionId">
    
    <div style="display: flex; flex-direction: row">
        <div>
            <div>
                <a :href="image0.image" class="lsb-preview" :data-lsb-group="lsbGroup">
                    <div v-bind:style="{ 'background' : image0.background }" class="photo50 gridbase"></div>
                </a>
            </div>
            <div>    
                <a :href="image1.image" class="lsb-preview" :data-lsb-group="lsbGroup">
                    <div v-bind:style="{ 'background' : image1.background }" class="photo51 gridbase"></div>
                </a>
            </div>
        </div>
        <div>
            <div>
                <a :href="image2.image" class="lsb-preview" :data-lsb-group="lsbGroup">
                    <div v-bind:style="{ 'background' : image2.background }" class="photo52 gridbase"></div>
                </a>
            </div>
            <div>    
                <a :href="image3.image" class="lsb-preview" :data-lsb-group="lsbGroup">
                    <div v-bind:style="{ 'background' : image3.background }" class="photo53 gridbase"></div>
                </a>
            </div>
            <div>    
                <a :href="image4.image" class="lsb-preview" :data-lsb-group="lsbGroup">
                    <div v-bind:style="{ 'background' : image4.background }" class="photo54 gridbase"></div>
                </a>
            </div>
        </div>
    </div>
    </section>
    `,
    created: function () {
        this.image0 = this.images[0]
        this.image0['background'] = getBgUrl(this.image0)
        this.image1 = this.images[1]
        this.image1['background'] = getBgUrl(this.image1)
        this.image2 = this.images[2]
        this.image2['background'] = getBgUrl(this.image2)
        this.image3 = this.images[3]
        this.image3['background'] = getBgUrl(this.image3)
        this.image4 = this.images[4]
        this.image4['background'] = getBgUrl(this.image4)
    },
    data() {
        return {
            image0: [],
            image1: [],
            image2: [],
            image3: [],
            image4: []
        }
    },
    props: {
        images: Array,
        lsbGroup: String,
        sectionId:String
    }
}