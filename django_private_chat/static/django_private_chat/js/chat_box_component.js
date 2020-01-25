let ChatBox = {
    template: `
    <div class="msg_box" style="right:270px"><input type="hidden" id="opponentName" :value="opponentUserName">
        <div class="msg_head">{{ userName }}
            <div class="close" @click="close">x</div>
        </div>
        <div class="msg_wrap">
            <div class="msg_body" id="dialog-{{ dialogId }}">
                <div><p class="msg-right pull-right "></p></div>
                <div v-for="message in messages">
                    <p :class="getMessageClass(message)"> {{ message.text }} </p>
                </div>
                <div class="msg_push"></div>
            </div>
            <div class="msg_footer"><textarea class="msg_input" rows="4" v-on:keyup="sendMessage"></textarea></div>
        </div>
    </div>
  `,
    created: function () {
        this.websocket = new WebSocket('ws://' + location.hostname + ':5002/' + this.getRequestSessionId() + '/' + this.opponentUserName);
        this.websocket.onopen = this.socketOnOpen;
        this.websocket.onmessage = this.socketOnMessage;

        this.websocket.onclose = this.socketOnClose;


        if(this.dialogId){
            this.fetchMessages(this.dialogId);
        }else{
            this.hasDialogId = false
        }

    },
    props: {
        relId: String,
        userName: String,
        opponentUserName: String,
        dialogId: String,
        requestUserId: String,

    },

    data() {
        return {
            messages: [],
            hasDialogId : true
        }
    },

    methods: {
        close:function(){
            this.websocket.close();

        },
        clearUnreadParent:function(){
            this.$root.$emit('clearUnread', this.dialogId);

            var newMessagePacket = JSON.stringify({
                    type: 'clear-unread',
                    session_key: this.getRequestSessionId(),
                    dialog: this.dialogId,
                    username: this.getRequestUserName()
            });

            this.websocket.send(newMessagePacket);
        },
        getRequestUserName: function () {
          return document.getElementById("requestUserName").value
        },
        getCookie: function (name) {
            var cookieValue = null;

            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }

            return cookieValue;
        },
        sendMessage: function (e) {

            if (e.key === 'Enter') {
                msg = e.target.value;
                e.target.value = "";
                if (msg.trim().length != 0) {
                    var newMessagePacket = JSON.stringify({
                        type: 'new-message',
                        session_key: this.getRequestSessionId(),
                        username: this.opponentUserName,
                        message: msg
                    });

                    if(this.hasDialogId){

                        this.websocket.send(newMessagePacket);
                    }else{
                        this.createDialogThenSend(newMessagePacket);
                    }



                }
            }

        },
        createDialogThenSend:function(newMessagePacket){
            var csrftoken = this.getCookie('csrftoken');
            var self = this;


            axios.post("/chat/api/dialog-create/",
                {
                    opponent:self.opponentUserName
                },
                {headers: {'Accept': 'application/json', 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken}}
            ).then((response) => {
                    self.hasDialogId = true;
                    self.websocket.send(newMessagePacket);
                    self.refetchDialogHistory();


            })
        },
        refetchDialogHistory:function(){
          this.$root.$emit('refetchDialogHistory')
        },
        getRequestSessionId: () => {
            return document.getElementById("requestSessionId").value;
        },
        socketOnOpen: (event) => {
            console.log("connection success!!!")
        },
        socketOnMessage:function(event){

            var packet;

            try {
                packet = JSON.parse(event.data);
            } catch (e) {
                console.log(e);
            }

            var self = this;


            switch (packet.type) {
                case 'new-message':
                    this.appendNewMessage(packet);
                    break;
            }
        },
        socketOnClose: function(){
          this.$root.$emit('closeChatBox', this.relId);
        },
        appendNewMessage:function(packet){

            if(this.dialogId === null){
                this.dialogId = packet.dialog.id;
            }


            new Promise((resolve, reject)=>{
                        this.messages.push(packet);
                        resolve(1);
                    }).then((res)=>{
                        this.autoScroll();
                    })
        },
        fetchMessages: async function () {
            var self = this;
            await axios.get("/chat/api/message-in-dialog/" + this.dialogId).then((result => {
                self.messages = result.data;
                self.clearUnreadParent();
            })).catch((err) => {
                console.log(err)
            });

            this.autoScroll();
        },
        getMessageClass: function (message) {

            if (message.sender.id === this.requestUserId) {
                return "msg-right pull-right"
            } else {
                return "msg-left"
            }
        },
        autoScroll: function () {
            scrollable = $('div[rel=' + this.relId + ']').find(".msg_body");
            scrollable.scrollTop(scrollable[0].scrollHeight);

        },
    }
}
