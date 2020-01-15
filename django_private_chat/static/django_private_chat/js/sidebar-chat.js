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
        $('[rel="' + chatbox + '"]').hide();
        arr.splice($.inArray(chatbox, arr), 1);
        app.displayChatBox();
        return false;
    });


    $(document).on('keypress', 'textarea', function (e) {
        if (e.keyCode == 13) {
            var msg = $(this).val();
            $(this).val('');
            if (msg.trim().length != 0) {
                var chatbox = $(this).parents().parents().parents().attr("rel");
                $('<div class="msg-right">' + msg + '</div>').insertBefore('[rel="' + chatbox + '"] .msg_push');
                $('.msg_body').scrollTop($('.msg_body')[0].scrollHeight);
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
        this.fetchDialogHistory();
        this.fetchMessagesByDialog(3);
    },
    methods: {
        showMessageBox:async function (userID, userName) {

            var dialogId = $('input#dialogId-' + userID).val();


            if ($.inArray(userID, arr) != -1) {
                arr.splice($.inArray(userID, arr), 1);
            }

            arr.unshift(userID);

            var previous_messages = await this.fetchMessagesByDialog(dialogId.replace("dialogId-",""))


            chatPopup = '<div class="msg_box" style="right:270px" rel="' + userID + '">' +
                '<div class="msg_head">' + userName +
                '<div class="close">x</div> </div>' +
                '<div class="msg_wrap"> <div class="msg_body">' +
                    previous_messages+
                '<div class="msg_push"></div> </div>'+
                '<div class="msg_footer"><textarea class="msg_input" rows="4"></textarea></div> 	</div> 	</div>';


            $("body").append(chatPopup);
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