
var app = new Vue({
    el: "#chat-app",
    created(){
        this.websocket = new WebSocket('ws://localhost:5002/'+this.getRequestSessionId()+'/'+this.getOpponentUserName());

        this.websocket.onopen = this.socketOnOpen;

    },
    methods:{
        getRequestSessionId:()=>{
            return document.getElementById("requestSessionId").value;
        },
        getOpponentUserName:()=>{
            return document.getElementById("opponentUserName").value;
        },
        socketOnOpen:(event)=>{
            console.log("connection success!!!")
        }
    }
});

