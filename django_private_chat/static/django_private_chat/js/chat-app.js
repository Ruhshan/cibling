
var app = new Vue({
    el: "#chat-app",
    data:{
      messages:[]
    },
    created(){
        this.websocket = new WebSocket('ws://localhost:5002/'+this.getRequestSessionId()+'/'+this.getOpponentUserName());

        this.websocket.onopen = this.socketOnOpen;
        this.websocket.onmessage = this.socketOnMessage;

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
        },
        addNewMessage:function (packet) {
          this.messages.push(packet);
        },
        socketOnMessage:function(event){

            var packet;

            try {
                packet = JSON.parse(event.data);
            } catch (e) {
                console.log(e);
            }

            switch (packet.type) {
                case "new-message":
                    this.addNewMessage(packet);
                    break;
            }
        }
    }
});

