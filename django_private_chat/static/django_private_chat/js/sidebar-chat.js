var arr = [];

const worker = new Worker("/chat/worker.js");

// console.log(worker)
//
// worker.port.start();

//worker.port.postMessage({from:"1",sessionId:document.getElementById("requestSessionId").value});



$(document).ready(function () {

    $("#start-chat-btn").bind("click",function () {
        var user={};
        user["id"] = $(this).attr("user-id");
        user["username"] = $(this).attr("user-name");
        user["title"] = $(this).attr("user-title");
        worker.postMessage({type:'new-chat',user:user});
    })



});

var schatApp = new Vue({
    el: "#chat-sidebar-app",
    data: {
        dialogs: [],
        new_chat_users: [],
        loading: false,
        show_suggestion: false,
        chatBoxes: [],
        query : ""
    },
    mounted() {
        this.$root.$on('refetchDialogHistory', () => {
            this.fetchDialogHistory();
        });

        this.$root.$on('clearUnread', (dialogId) => {
            this.clearUnread(dialogId);
        });

        this.$root.$on('closeChatBox', (relId) =>{

           arr.splice($.inArray(relId, arr), 1);

           $('[rel="' + relId + '"]').remove();

           this.displayChatBox();

        });
    },
    created() {
        var baseUrl = document.getElementById('chat_base_url').value
        console.log('chat_server_base_url '+baseUrl)
        this.websocket = new WebSocket('ws://' + baseUrl + this.getRequestSessionId() + '/' + this.getRequestSessionId());
        this.websocket.onopen = this.socketOnOpen;
        this.websocket.onmessage = this.socketOnMessage;

        this.fetchDialogHistory();

        worker.addEventListener('message',this.messageFromWorker)
    },

    methods: {
        messageFromWorker: function(event){

            var dialog = this.retriveDialog(event.data.user)

            if(dialog != null){
                this.showMessageBox(dialog)
            }else{
                this.showNewMessageBox(event.data.user)
            }


        },
        getRequestSessionId: () => {
            return document.getElementById("requestSessionId").value;
        },
        socketOnOpen: (event) => {
            console.log("connection success master!!!")
        },
        socketOnMessage: function (event) {

            var packet;

            try {
                packet = JSON.parse(event.data);
            } catch (e) {
                console.log(e);
            }

            var self = this;

            switch (packet.type) {
                case 'new-message':
                    self.fetchDialogHistory();
                    break;
            }
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
        sendNewMessage: function (chatBoxID, msg, username) {
            var csrftoken = this.getCookie('csrftoken');
            var self = this;

            axios.post("/chat/api/dialog-create/",
                {
                    opponent: username
                },
                {headers: {'Accept': 'application/json', 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken}}
            ).then((response) => {

                console.log(response)
                var dialogId = response.data.id;

                self.dialogs.push(response.data);

                var target_msg_body = $('[rel=' + chatBoxID + ']').find(".msg_body");
                target_msg_body.attr("id", "dialog-" + dialogId);

                var target_msg_input = $('[rel=' + chatBoxID + ']').find(".msg_input_new");

                target_msg_input.removeClass("msg_input_new");
                target_msg_input.addClass("msg_input");

                self.sendMessage(chatBoxID, msg);

            }).catch((err) => {
                console.log(err);
            })
        },


        getRequestUserName: function () {
            return document.getElementById("requestUserName").value
        },
        showNewMessageBox: function (user) {
            userID = user.id;
            opponentUserName = user.username;
            userName = user.title;

            if ($.inArray(userID, arr) != -1) {
                arr.splice($.inArray(userID, arr), 1);
            }

            arr.unshift(userID);

            if ($('[rel="' + userID + '"]').length === 0) {

                var chatBoxObj = {
                    userId: userID,
                    userName: userName,
                    opponentUserName: opponentUserName,
                    chatBoxComp: ChatBox,
                    dialogId: null,
                    requestUserId: this.getRequestUserId()
                }
                //$("body").append(chatPopup);
                this.chatBoxes.push(chatBoxObj);
            }

            this.displayChatBox();


        },
        clearUnread: function (dialogId) {
            this.dialogs.forEach((dialog) => {

                if (dialog.id === parseInt(dialogId)) {
                    dialog.unread = 0;
                }

            });


        },
        showMessageBox: async function (dialog) {
            userID = this.getOpponentIdForDialog(dialog);
            userName = this.getNameForDialog(dialog);
            opponentUserName = this.getOpponentUserNameForDialog(dialog);

            var dialogId = $('input#dialogId-' + userID).val();


            if ($.inArray(userID, arr) != -1) {
                arr.splice($.inArray(userID, arr), 1);
            }

            arr.unshift(userID);


            if ($('[rel="' + userID + '"]').length === 0) {

                var chatBoxObj = {
                    userId: userID,
                    userName: userName,
                    opponentUserName: opponentUserName,
                    chatBoxComp: ChatBox,
                    dialogId: dialogId,
                    requestUserId: this.getRequestUserId()
                }
                //$("body").append(chatPopup);
                this.chatBoxes.push(chatBoxObj);

            }

            this.displayChatBox();
            //this.autoScroll(userID);

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
        getOpponentUserNameForDialog: function (dialog) {
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

            console.log("Fetching history")

            axios.get("/chat/api/dialog-history/").then((result) => {
                self.dialogs = result.data

                console.log("Fetching complete")
            }).catch((err) => {
                console.log(err)
            })
        },
        autoScroll: function (relId) {
            scrollable = $('div[rel=' + relId + ']').find(".msg_body");
            scrollable.scrollTop(scrollable[0].scrollHeight);

        },
        search: function () {

            var query = this.query;
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
                            "username": user.user.username
                        };

                        if (!self.existsInDialog(entry)) {
                            fetched_users.push(entry);
                        }


                    });

                    self.new_chat_users = fetched_users.splice(0, 5);


                    self.loading = false;

                }).catch((err) => {
                    console.log(err);
                    self.loading = false;
                    self.show_suggestion = false;
                })
            } else {
                self.loading = false;
                self.show_suggestion = false;
                self.new_chat_users = [];

            }
        },

        existsInDialog: function (user) {
            var userId = user.id;

            return this.dialogs.some((dialog) => {

                if (parseInt(userId) === parseInt(this.getOpponentIdForDialog(dialog))) {
                    return true;

                }
                return false;

            });


        },
        retriveDialog: function (user) {
            var userId = user.id;
            var result = null;
            this.dialogs.forEach((dialog) => {

                if (parseInt(userId) === parseInt(this.getOpponentIdForDialog(dialog))) {
                    result = dialog;

                }

            });

            return result;
        }
    }
});