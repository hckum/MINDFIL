/*
    Author: Qinbo Li
    Date: 12/22/2017
    Requirement: jquery-3.2.1, clickable.js
    This file is for form submit, and sending user click data
*/

function post(path, params, method) {
    // COPYRIGHT: https://stackoverflow.com/questions/133925/javascript-post-request-like-a-form-submit
    method = method || "post"; // Set method to post by default if not specified.
    var formData = new FormData();
    formData.append("user_data", params);
    var request = new XMLHttpRequest();
    request.open("POST", path);
    request.send(formData);
}

function reset_choice_panel() {
    var $options = $("li.input_radio");

    $options.click(function(e){
        e.preventDefault();
        e.stopPropagation();
        $(this).parent().find("li.input_radio").removeClass("ion-android-radio-button-on");
        $(this).parent().find("li.input_radio").addClass("ion-android-radio-button-off");
        $(this).removeClass("ion-android-radio-button-off");
        $(this).addClass("ion-android-radio-button-on");
        var $selected_id = $(this).attr("id");
        var $diff = $(this).parent().parent().find("li.diff");
        var $same = $(this).parent().parent().find("li.same");
        if($selected_id.indexOf("a1") > 0 || $selected_id.indexOf("a2") > 0 || $selected_id.indexOf("a3") > 0) {
            $diff.css("border-color", "#30819c");
            $same.css("border-color", "transparent");
        }
        else {
            $diff.css("border-color", "transparent");
            $same.css("border-color", "#30819c");
        }

        // save the user click data
        $type = "type:answer";
        $this_click = "value:" + $selected_id;
        var dt = new Date();
        $click_timestamp = "timestamp:" + Math.round(dt.getTime()/1000);
        $url = "url:" + $THIS_URL;
        $data = [$type, $this_click, $click_timestamp, $url].join()
        $user_data += $data + ";";
    });
}

function get_summitted_answers() {
    var c = $(".ion-android-radio-button-on").each(function() {
        $type = "type:final_answer";
        $this_click = "value:" + this.id;
        var dt = new Date();
        $click_timestamp = "timestamp:" + Math.round(dt.getTime()/1000);
        $url = "url:" + $THIS_URL;
        $data = [$type, $this_click, $click_timestamp, $url].join()
        $user_data += $data + ";";
    });
}

function get_responses(){
    i = 0;
    var responses = new Array();
    var ids = new Array();
    var screen_ids = new Array();
    $(".ion-android-radio-button-on").each(function() {
            var screen_id = $(this).parent().parent().parent().parent().children(".table_col1").text();
            var id_ans = this.id;
            var id = id_ans.split("a");
            var response = id[1];
            id = id[0].split("p")[1];
            ids[i] = id;
            responses[i] = response;
            screen_ids[i] = screen_id;
            i += 1;
    })

    results = {
        "responses": responses.join(),
        "ids": ids.join(),
        "screen_ids": screen_ids.join()
    };

    // console.log(results);

    return results;

};


/* 
    This function defines the behavior of the next button 
    1. post the user click data to server.
    2. relocate to the next page.
*/
$(function() {
    $('#button_next').bind('click', function() {
        $('#button_next').attr("disabled", "disabled");
        
        // save this click data
        // $type = "type:jumping";
        // $value = "value:" + $THIS_URL;
        // var dt = new Date();
        // $click_timestamp = "timestamp:" + Math.round(dt.getTime()/1000);
        // $url = "url:" + $THIS_URL;
        // $data = [$type, $value, $click_timestamp, $url].join()
        // $user_data += $data + ";";

        // get_summitted_answers();
        // post($SCRIPT_ROOT+'/save_data', $user_data, "post");
        // $user_data = "";

        $(window).off("beforeunload");
        window.location.href = $NEXT_URL;
    });
});


function all_questions_answered() {
    var i = 0;
    var c = $(".ion-android-radio-button-on").each(function() {
        i += 1;
    });
    //return true; // disable this feature for dev.
    return (i == 6);
}

/*
    This function defines the behavior of the next button in record linkage page:
    1. disable this button
    2. post the user data to server
    3. use ajax to load the next page of data (if any)
    4. if the next page is the last page, change this button to normal next button
    5. enable the button
*/
$(function() {
    $('#submit_grade').bind('click', function() {
        if( !all_questions_answered() ) {
            alert("Please answer all questions to continue.");
        }
        else {
          

            // $('#button_next_rl').attr("disabled", "disabled");
        

            $.getJSON('/feedback_main_section', get_responses(), function(data) {
                var feedback_message = data.result;
                var wrong_ids = data.wrong_ids;
                var right_ids = data.right_ids;
                // console.log(wrong_ids);
                for (var i = 0; i < wrong_ids.length; i++){ 
                    var wrong_id = wrong_ids[i];
                    var row = $("#"+wrong_id+"-1-0").parent().parent();
                    row.attr("class", "table_row table_row_wrong");
                }

                for (var i = 0; i < right_ids.length; i++){ 
                    var right_id = right_ids[i];
                    var row = $("#"+right_id+"-1-0").parent().parent();
                    row.attr("class", "table_row table_row_right");
                }

                var expenditure = $("#privacy-risk-value").text().replace("%","").trim();
                expenditure = parseFloat(expenditure);
                var page = $("#page-number").text().trim();
                var re = /\d+/g; 
                page = parseInt(page.match(re)[0]);
                if(expenditure < 40*page/6){
                    // feedback_message += "You might want to consider opening more relevant information if it would help you get more questions right.";
                } else{
                    // feedback_message += "Consider opening the right cells with relevant information";
                }
                
                $("#feedback").text(feedback_message);
                if(right_ids.length == 6){
                    $("#feedback").css("color","#006606");
                } else {
                    $("#feedback").css("color","#660000");    
                }
                
                $('#submit_grade').attr("disabled", "disabled");
                $('#submit_grade').css("display", "none");
                disable_choice_panel();

                // if not last page
                if(page != 6) {
                    // save this click data
                    $type = "type:next_page";
                    $('#button_next_rl').attr("disabled", false);
                    $('#button_next_rl').css("display", "inline");
                } else { //if last page
                    $type = "type:jumping";
                    $('#button_next_rl').attr("disabled", "disabled");
                    $('#button_next_rl').css("display", "none");
                    $('#button_next').css("display", "inline");
                }

                $value = "value:" + $THIS_URL;
                var dt = new Date();
                $click_timestamp = "timestamp:" + Math.round(dt.getTime()/1000);
                $url = "url:" + $THIS_URL;
                $data = [$type, $value, $click_timestamp, $url].join()
                $user_data += $data + ";";

                get_summitted_answers();
                post($SCRIPT_ROOT+'/save_data', $user_data, "post");
                $user_data = "";
            });
                        
        }
        return false;
    });
});

$(function() {
    $('#button_next_rl').bind('click', function() {
        $('#button_next_rl').attr("disabled", "disabled");
        $('#button_next_rl').css("display", "none");
        $.ajax({
            url: $SCRIPT_ROOT + $THIS_URL + '/next',
            data: {},
            error: function() {},
            dataType: 'json',
            success: function(data) {
                if(data['result'] != 'success') {
                    alert('You have finished this section.');
                    $(window).off("beforeunload");
                    window.location.href = $NEXT_URL;
                }
                // update delta
                $DELTA = data['delta'];
                // update table content
                $("#table_content").html(data['page_content']);
                // update page number
                $("#page-number").html(data['page_number']);
                make_cell_clickable();
                refresh_delta();
                reset_choice_panel();
                $('#feedback').text("");
                $('#submit_grade').attr("disabled", false);
                $('#submit_grade').css("display", "inline");

                // //if not last page
                // if(data['is_last_page'] == 0) {
                //     $('#button_next_rl').attr("disabled", false);
                //      $('#button_next_rl').css("display", "inline");
                // } //else if last page
                // else {
                //     $('#button_next_rl').css("display", "none");
                //     $('#button_next').css("display", "inline");
                // }
            },
            type: 'GET'
        });

    });
});

                