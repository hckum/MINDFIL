/*
    Author: Qinbo Li
    Date: 12/19/2017
    Requirement: jquery-3.2.1
    This file is for practice grading
*/

function get_responses() {

    i = 0;
    var responses = new Array();
    var ids = new Array();
    var html_ids = new Array();
    var screen_ids = new Array();
    // $(".ion-android-radio-button-on").each(function() {
    //         var screen_id = $(this).parent().parent().parent().parent().children(".table_col1").text();
    //         var id_ans = this.id;
    //         var id = id_ans.split("a");
    //         var response = id[1];
    //         id = id[0].split("p")[1];
    //         ids[i] = id;
    //         html_ids[i] = id_ans;
    //         responses[i] = response;
    //         screen_ids[i] = screen_id;
    //         i += 1;
    // })

    $(".ion-android-radio-button-on").each(function() {
        responses[i] = this.id;
        html_ids[i] = this.id;
        var screen_id = $(this).parent().parent().parent().parent().children(".table_col1").text();

        i += 1;
    });


    results = {
        "responses": responses.join(),
        "ids": ids.join(),
        "html_ids": html_ids.join(),
        "screen_ids": screen_ids.join()
    };

    // console.log(results);

    return results;

    
    // var responses = new Array();
    // var i = 0;
    // var c = $(".ion-android-radio-button-on").each(function() {
    //     responses[i] = this.id;
    //     i += 1;
    // });

    // return {
    //     "response": responses.join()
    // };
}


function all_questions_answered_grading() {
    
    var i = 0;
    var c = $(".ion-android-radio-button-on").each(function() {
        i += 1;
    }); 
    console.log(parseInt($(".table_row").length));   
    return (i == parseInt($(".table_row").length));
}


function get_submitted_answers_grading() {
    var c = $(".ion-android-radio-button-on").each(function() {
        $type = "type:practice_answer";
        $this_click = "value:" + this.id;
        var dt = new Date();
        $click_timestamp = "timestamp:" + Math.round(dt.getTime()/1000);
        $url = "url:" + $THIS_URL;
        $data = [$type, $this_click, $click_timestamp, $url].join()
        $user_data += $data + ";";
        post($SCRIPT_ROOT+'/save_data', $user_data, "post");
        $user_data = "";
    });
}

$(function() {
    $('#submit_btn').bind('click', function() {
       
        if(all_questions_answered_grading()){
          // save the click data
          get_submitted_answers_grading();

          $value = "value:" + $THIS_URL;
          $type = "Practice submit and grade";
          var dt = new Date();
          $click_timestamp = "timestamp:" + Math.round(dt.getTime()/1000);
          $url = "url:" + $THIS_URL;
          $data = [$type, $value, $click_timestamp, $url].join()
          $user_data += $data + ";";

          // get_summitted_answers();
          post($SCRIPT_ROOT+'/save_data', $user_data, "post");
          $user_data = "";

          var feedback = $("#feedback");
          $.getJSON($SCRIPT_ROOT + $THIS_URL + '/grading', get_responses(), function(data) {
              var wrong_ids = data.wrong_ids;
              var right_ids = data.right_ids;
              console.log(wrong_ids);
              var responses = get_responses();

              $("#table").html(data.page_content);
              $('#page-number').remove();

              // resuming the choice panel

              var ids = responses["html_ids"].split(",");
              console.log(ids);
              // var ids = data.responses;
              // console.log(ids);
              for(var i = 0; i < ids.length; i++) {
                  var id = ids[i];
                  $("#"+id).removeClass("ion-android-radio-button-off");
                  $("#"+id).addClass("ion-android-radio-button-on");
                  var $diff = $("#"+id).parent().parent().find("li.diff");
                  var $same = $("#"+id).parent().parent().find("li.same");
                  if(id.indexOf("a1") > 0 || id.indexOf("a2") > 0 || id.indexOf("a3") > 0) {
                      $diff.css("border-color", "#30819c");
                      $same.css("border-color", "transparent");
                  }
                  else {
                      $diff.css("border-color", "transparent");
                      $same.css("border-color", "#30819c");
                  }
              }
                

              disable_choice_panel();

              console.log(wrong_ids);

              for(i = 0; i <= wrong_ids.length; i++){
                var id = $("#"+"q"+wrong_ids[i]+"a1");
                var row = id.parent().parent().parent().parent();
                // row.attr("class","table_row table_row_wrong");
                // row.addClass("table_row_wrong");
                console.log(row);
                row.prepend('<img src="/static/images/site/red_cross.png" class="img_wrong_tutorial" />')
              };

              // for(i = 0; i <= right_ids.length; i++){
              //   var id = $("#"+"q"+right_ids[i]+"a1");
              //   var row = id.parent().parent().parent().parent();
              //   // row.attr("class","table_row table_row_right");
              //   // row.addClass("table_row_right");
              //   // row.prepend('<img src="/static/images/site/right.png" class="img_right_wrong" />')
              // };

                        
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
              });
              feedback.fadeIn(250);
              // $("#feedback").html(data.result);
              $("#submit_btn").css({"display": "none"});
              $("#button_next").css({"display": "inline"});

          });

        } else {
          alert("Please answer all questions to continue");
        }


        return false;
    });
});
