
var app = new Vue({
    el: "#chat-app",
    data:{
      messages:[],
      dialogs:[],
      new_message:true

    },
    created(){
        this.fetchDialogHistory();
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
        addNewMessageIndialogPreview:function (packet) {
            var opponent = ""

            if(packet.username === this.getRequestUserName()){
                opponent = packet.sender_name;
            }else{
                opponent = packet.username;
            }

            this.dialogs.forEach((obj)=>{
                if(obj.opponent.username === this.getRequestUserName() && obj.owner.username === opponent){
                    obj.last_message = packet.message
                }
                if(obj.owner.username === this.getRequestUserName() && obj.opponent.username === opponent){
                    obj.last_message = packet.message
                }

            })
        },
        getRequestUserId:function () {
          return parseInt(document.getElementById("requestUserId").value);
        },
        getRequestUserName: function () {
          return document.getElementById("requestUserName").value
        },
        openDetails:function (dialog) {
            if(dialog.owner.id === this.getRequestUserId()){
                window.location = "/chat/dialogs-new/" + dialog.opponent.username
            }else{
                window.location = "/chat/dialogs-new/" + dialog.owner.username
            }
        },
        getActiveDialogId:function () {
            return parseInt(document.getElementById("activeDialogId").value);
        },
        getIconForDialog:function (dialog) {

            if(dialog.owner.id === this.getRequestUserId()){
                return dialog.opponent.profile_image;
            }else{
                return dialog.owner.profile_image;
            }

        },
        getNameForDialog:function(dialog){
            if(dialog.owner.id === this.getRequestUserId()){
                return dialog.opponent.first_name+" "+dialog.opponent.last_name;
            }else{
                return dialog.owner.first_name+" "+dialog.owner.last_name;
            }
        },

        fetchDialogHistory:function () {
          var self = this;

            axios.get("/chat/api/dialog-history/").then((result)=>{
                self.dialogs=result.data
            }).catch((err)=>{
                console.log(err)
            })
        },
        sendMessage:function () {

            var newMessagePacket = JSON.stringify({
                    type: 'new-message',
                    session_key: this.getRequestSessionId(),
                    username: this.getOpponentUserName(),
                    message: document.getElementById("newMessageTextBox").value
            });

            this.websocket.send(newMessagePacket);

            document.getElementById("newMessageTextBox").value=""

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
                    this.addNewMessageIndialogPreview(packet)
                    break;
            }
        }
    }
});

