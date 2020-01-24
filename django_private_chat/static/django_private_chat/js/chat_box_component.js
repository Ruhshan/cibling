let ChatBox = {
    template: `
    <div class="msg_box" style="right:270px"><input type="hidden" id="opponentName" :value="opponentUserName">
        <div class="msg_head">{{ userName }}
            <div class="close">x</div>
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
        this.fetchMessages(this.dialogId);
    },
    props: {
        relId: String,
        userName: String,
        opponentUserName: String,
        dialogId: String,
        requestUserId: String
    },

    data() {
        return {
            messages: []
        }
    },

    methods: {
        sendMessage: function (e) {

            if (e.key === 'Enter') {
                msg = e.target.value;
                e.target.value = "";
                if (msg.trim().length != 0) {
                    var newMessagePacket = JSON.stringify({
                        type: 'new-message',
                        session_key: this.getRequestSessionId(),
                        username: opponentUserName,
                        message: msg
                    });


                    this.websocket.send(newMessagePacket);

                }
            }

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
        appendNewMessage:function(packet){

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
