var arr = [];
$(document).ready(function () {

    // List of users

    $(document).on('click', '.msg_head', function () {
        var chatbox = $(this).parents().attr("rel");
        $('[rel="' + chatbox + '"] .msg_wrap').slideToggle('slow');
        return false;
    });


    $(document).on('click', '.close', function () {
        var chatbox = $(this).parents().parents().attr("rel");
        $('[rel="' + chatbox + '"]').remove();
        arr.splice($.inArray(chatbox, arr), 1);
        app.displayChatBox();
        return false;
    });


    $(document).on('keypress', 'textarea', function (e) {
        if (e.keyCode == 13) {
            var msg = $(this).val();
            $(this).val('');
            if (msg.trim().length != 0) {
                var chatboxId = $(this).parents().parents().parents().attr("rel");
                app.sendMessage(chatboxId, msg);
            }
        }
    });


});

var app = new Vue({
    el: "#chat-sidebar",
    data: {
        dialogs: [],
    },
    created() {
        this.websocket = new WebSocket('ws://'+location.hostname+':5002/'+this.getRequestSessionId());
        this.websocket.onopen = this.socketOnOpen;
        this.websocket.onmessage = this.socketOnMessage;

        this.fetchDialogHistory();
        this.fetchMessagesByDialog(3);
    },
    methods: {
        sendMessage:function(chatboxID, msg){
            var username = $('[rel='+chatboxID+']').find('#opponentName')[0].value

            var newMessagePacket = JSON.stringify({
                    type: 'new-message',
                    session_key: this.getRequestSessionId(),
                    username: username,
                    message: msg
            });

            this.websocket.send(newMessagePacket);
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
                    this.addMessageInMessageBox(packet)
            }
        },

        socketOnOpen:(event)=>{
            console.log("connection success!!!")
        },
        addMessageInMessageBox:function (message) {
            var targetMessageBox = $("#dialog-" + message.dialog_id);
            var rel = targetMessageBox.parent().parent().attr("rel");

            if(message.sender_name !== this.getRequestUserName()) {
                  $('<div class="msg-left">' + message.message + '</div>').insertBefore('[rel="' + rel + '"] .msg_push');
                  targetMessageBox.scrollTop(targetMessageBox[0].scrollHeight);
                  this.autoScroll(rel);
              }else{
                $('<div class="msg-right">' + message.message + '</div>').insertBefore('[rel="' + rel + '"] .msg_push');
                  targetMessageBox.scrollTop(targetMessageBox[0].scrollHeight);
                  this.autoScroll(rel);
            }
        }
        ,
        getRequestSessionId:()=>{
            return document.getElementById("requestSessionId").value;
        },
        getRequestUserName: function () {
          return document.getElementById("requestUserName").value
        },
        showMessageBox:async function (userID, userName, opponentUserName) {

            var dialogId = $('input#dialogId-' + userID).val();


            if ($.inArray(userID, arr) != -1) {
                arr.splice($.inArray(userID, arr), 1);
            }

            arr.unshift(userID);

            var previous_messages = await this.fetchMessagesByDialog(dialogId.replace("dialogId-",""))


            chatPopup = '<div class="msg_box" style="right:270px" rel="' + userID + '">' +
                '<input type="hidden"'+ ' id="opponentName" value=' + opponentUserName + '>'+
                '<div class="msg_head">' + userName +
                '<div class="close">x</div> </div>' +
                '<div class="msg_wrap"> <div class="msg_body"' + ' id = ' + "dialog-"+dialogId + '>' +
                    previous_messages+
                '<div class="msg_push"></div> </div>'+
                '<div class="msg_footer"><textarea class="msg_input" rows="4"></textarea></div> 	</div> 	</div>';

            if($('[rel="' + userID + '"]').length === 0){
                $("body").append(chatPopup);
            }

            this.displayChatBox();
            this.autoScroll(userID);

        },
        displayChatBox: function () {
            i = 270; // start position
            j = 260;  //next position

            $.each(arr, function (index, value) {
                if (index < 4) {
                    $('[rel="' + value + '"]').css("right", i);
                    $('[rel="' + value + '"]').show();
                    i = i + j;
                } else {
                    $('[rel="' + value + '"]').hide();
                }
            });
        },
        getRequestUserId: function () {
            return parseInt(document.getElementById("requestUserId").value);
        },
        getIconForDialog: function (dialog) {

            if (dialog.owner.id === this.getRequestUserId()) {
                return dialog.opponent.profile_image;
            } else {
                return dialog.owner.profile_image;
            }

        },
        getNameForDialog: function (dialog) {
            if (dialog.owner.id === this.getRequestUserId()) {
                return dialog.opponent.first_name + " " + dialog.opponent.last_name;
            } else {
                return dialog.owner.first_name + " " + dialog.owner.last_name;
            }
        },
        getOpponentIdForDialog: function (dialog) {
            if (dialog.owner.id === this.getRequestUserId()) {
                return dialog.opponent.id.toString();
            } else {
                return dialog.owner.id.toString();
            }
        },
        getOpponentUserNameForDialog: function(dialog){
            if (dialog.owner.id === this.getRequestUserId()) {
                return dialog.opponent.username;
            } else {
                return dialog.owner.username;
            }
        },
        setDialogId: function (dialog) {
            return "dialogId-" + this.getOpponentIdForDialog(dialog);
        },
        fetchDialogHistory: function () {
            var self = this;

            axios.get("/chat/api/dialog-history/").then((result) => {
                self.dialogs = result.data
            }).catch((err) => {
                console.log(err)
            })
        },
        fetchMessagesByDialog:async function (dialog_id) {
            //<div class="msg-right">asdf</div>


            var previousMessages = ""


            let resp = await axios.get("/chat/api/message-in-dialog/"+dialog_id);

            resp.data.forEach((message)=>{

                if(parseInt(message.sender.id)== this.getRequestUserId()){
                    previousMessages+= `<div class="msg-right">${message.text}</div>`
                }else{
                    previousMessages+= `<div class="msg-left">${message.text}</div>`
                }


            })

            return previousMessages

        },
        autoScroll:function (relId) {
            scrollable = $('div[rel='+relId+']').find(".msg_body");
            scrollable.scrollTop(scrollable[0].scrollHeight);

        }
    }
});