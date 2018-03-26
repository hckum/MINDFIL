/*
    Author: Qinbo Li
    Date: 12/19/2017
    Requirement: jquery-3.2.1
    This file is for practice grading
*/

function get_responses() {
    
    var responses = new Array();
    var i = 0;
    var c = $(".ion-android-radio-button-on").each(function() {
        responses[i] = this.id;
        i += 1;
    });

    return {
        "response": responses.join()
    };
}

$(function() {
    $('#submit_btn').bind('click', function() {
        // save the click data
        
        $this_click = "user click: Attemp";
        var dt = new Date();
        $click_time = "click time: " + dt.getHours() + "h" + dt.getMinutes() + "m" + dt.getSeconds() + "s";
        $click_timestamp = "click timestamp: " + dt.getTime();
        $data = [$this_click, $click_time, $click_timestamp].join()
        $user_data += $data + ";";
        var feedback = $("#feedback");
        $.getJSON($SCRIPT_ROOT + $THIS_URL + '/grading', get_responses(), function(data) {
            feedback.fadeOut(250, function(){
              feedback.html(data.result);  
              feedback.css("color","#660000");
              if($("#clickable_practice").length == 1) {
                  var expenditure = $("#privacy-risk-value").text().replace("%","").trim();
                  expenditure = parseFloat(expenditure);

                  // if(expenditure > 10.0){
                  //     feedback.prepend("<h5>" + "You have used more than half your budget! Did you need to see all this information?" + "</h5>");
                  // } else 
                  if((feedback.html().match(/review/g) || []).length > 0){
                    if(expenditure >= 13.0){
                        feedback.prepend("<h5>" + "Consider opening cells with more relevant information.</br></br>" + "</h5>");
                    } else{
                        feedback.prepend("<h5>" + "Maybe you should open some more cells to get more information.</br></br>" + "</h5>");
                    }
                  }
              }
            })
            feedback.fadeIn(250);
            // $("#feedback").html(data.result);
            $("#submit_btn").css({"display": "none"});
            $("#button_next").css({"display": "inline"})

        });

        return false;
    });
});
