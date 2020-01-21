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

                if(e.target.className === "msg_input"){
                    var chatboxId = $(this).parents().parents().parents().attr("rel");
                    app.sendMessage(chatboxId, msg);
                }

                if(e.target.className === "msg_input_new"){
                    var chatboxId = $(this).parents().parents().parents().attr("rel");
                    var username = $(this).parents().find('.msg_box').find('#opponentName')[0].value

                    app.sendNewMessage(chatboxId, msg, username)
                }

            }
        }
    });




});

var app = new Vue({
    el: "#chat-sidebar",
    data: {
        dialogs: [],
        new_chat_users: [],
        loading: false,
        show_suggestion:false,
    },
    created() {
        this.websocket = new WebSocket('ws://'+location.hostname+':5002/'+this.getRequestSessionId());
        this.websocket.onopen = this.socketOnOpen;
        this.websocket.onmessage = this.socketOnMessage;

        this.fetchDialogHistory();
        this.fetchMessagesByDialog(3);
    },
    methods: {
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
        sendNewMessage:function(chatBoxID, msg,username){
            var csrftoken = this.getCookie('csrftoken');
            var self = this;

            axios.post("/chat/api/dialog-create/",
                {
                    opponent:username
                },
                {headers: {'Accept': 'application/json', 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken}}
            ).then((response) => {

                console.log(response)
                var dialogId = response.data.id;

                self.dialogs.push(response.data);

                var target_msg_body = $('[rel='+chatBoxID+']').find(".msg_body");
                target_msg_body.attr("id", "dialog-"+dialogId);

                var target_msg_input = $('[rel='+chatBoxID+']').find(".msg_input_new");

                target_msg_input.removeClass("msg_input_new");
                target_msg_input.addClass("msg_input");

                self.sendMessage(chatBoxID, msg);

            }).catch((err) => {
                console.log(err);
            })
        },
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
                    this.addMessageInMessageBox(packet);
                    break;
                case "unread-cleared":
                    console.log(packet)
                    break;

            }
        },

        socketOnOpen:(event)=>{
            console.log("connection success!!!")
        },
        addMessageInMessageBox:async function (message) {
            var targetMessageBox = $("#dialog-" + message.dialog_id);
            var rel = targetMessageBox.parent().parent().attr("rel");


            if(targetMessageBox.length === 0){

                this.fetchDialogHistory();

            }

            if(message.sender_name !== this.getRequestUserName()) {
                  $('<div class="msg-left">' + message.message + '</div>').insertBefore('[rel="' + rel + '"] .msg_push');
                  targetMessageBox.scrollTop(targetMessageBox[0].scrollHeight);
                  this.autoScroll(rel);
              }else{
                $('<div class="msg-right">' + message.message + '</div>').insertBefore('[rel="' + rel + '"] .msg_push');
                  targetMessageBox.scrollTop(targetMessageBox[0].scrollHeight);
                  this.autoScroll(rel);
            }
        },
        getRequestSessionId:()=>{
            return document.getElementById("requestSessionId").value;
        },
        getRequestUserName: function () {
          return document.getElementById("requestUserName").value
        },
        showNewMessageBox:function(user){
            userID = user.id;
            opponentUserName = user.username;
            userName = user.title;

            if ($.inArray(userID, arr) != -1) {
                arr.splice($.inArray(userID, arr), 1);
            }

            arr.unshift(userID);

            chatPopup = '<div class="msg_box" style="right:270px" rel="' + userID + '">' +
                '<input type="hidden"'+ ' id="opponentName" value=' + opponentUserName + '>'+
                '<div class="msg_head">' + userName +
                '<div class="close">x</div> </div>' +
                '<div class="msg_wrap"> <div class="msg_body" >' +
                '<div class="msg_push"></div> </div>'+
                '<div class="msg_footer"><textarea class="msg_input_new" rows="4"></textarea></div> 	</div> 	</div>';

            if($('[rel="' + userID + '"]').length === 0){
                $("body").append(chatPopup);
            }

            this.displayChatBox();


        },
        clearUnread:function (dialogId) {
            this.dialogs.forEach((dialog)=>{

                if(dialog.id === parseInt(dialogId)){
                    dialog.unread = 0;
                }

            });

            var newMessagePacket = JSON.stringify({
                    type: 'clear-unread',
                    session_key: this.getRequestSessionId(),
                    dialog: dialogId,
                    username: this.getRequestUserName()
            });

            this.websocket.send(newMessagePacket);


        },
        showMessageBox:async function (userID, userName, opponentUserName) {

            var dialogId = $('input#dialogId-' + userID).val();

            this.clearUnread(dialogId);


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

                console.log("Fetching complete")
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

        },
        openNewChatModal:function(){
            $("#new-chat-modal").modal('show')
        },
        search:function(){
            var query = document.getElementById("search-chat").value;
            var self = this

            if (query.length > 1) {
                self.loading = true
                self.show_suggestion = true
                axios.get("/api/user/profiles?q=" + query).then((response) => {

                    var fetched_users = []

                    response.data.forEach((user) => {

                        var entry = {
                            "title": user.user.first_name + " " + user.user.last_name,
                            "image": user.image,
                            "id": user.user.id,
                            "institute":user.institute.institute,
                            "username":user.user.username
                        };

                        if(!self.existsInDialog(entry)){
                            fetched_users.push(entry);
                        }


                    });

                    self.new_chat_users = fetched_users.splice(0,5);


                    self.loading=false;

                }).catch((err) => {
                    console.log(err);
                    self.loading = false;
                    self.show_suggestion = false;
                })
            } else {
                self.loading=false;
                self.show_suggestion=false
                self.new_chat_users=[]
            }
        },

        existsInDialog:function (user) {
            var userId = user.id;

            return this.dialogs.some((dialog)=>{

                if(parseInt(userId) === parseInt(this.getOpponentIdForDialog(dialog))){
                    return true;

                }
                return false;

            });


        }
    }
});