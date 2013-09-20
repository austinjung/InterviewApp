/**
 * Created with PyCharm.
 * User: austin_45B_Kerkhoff
 * Date: 12/07/13
 * Time: 12:36 PM
 * To change this template use File | Settings | File Templates.
 */

function WebServiceErrorHandler(jqXHR, textStatus, errorThrown) {
    var errorMsg = "";
    var errors = JSON.parse(jqXHR.responseText);
    resetInputErrorCss();
    for (var err_key in errors) {
        if (err_key == "errors_html") {
            var err_value = eval("errors." + err_key);
//            errorMsg += err_key + " : <br />";
            errorMsg += err_value + "<br />";
        } else {
//            errorMsg += err_key + " has errors : <br />";
            var err_list = eval("errors." + err_key);
//            for (var i=0; i<err_list.length; i++) {
//                errorMsg += err_list[i] + "<br />&nbsp&nbsp&nbsp&nbsp";
//            }
            var input_id = "#id_" + err_key;
            $("#id_" + err_key).addClass('error');
        }
    }
    $('#dialog-message').title = "textStatus";
    $('#message-header').html(errorThrown);
    $('#message-detail').html(errorMsg);
//    $("#check-circle").css('visibility', 'visible');
    $("#check-circle").show();
    $( "#dialog-message" ).dialog({
      modal: true,
      buttons: {
        Ok: function() {
          $( this ).dialog( "close" );
        }
      }
    });
}

function WebServiceSuccessHandler(response, textStatus, jqXHR) {
    resetInputErrorCss();
    $('#dialog-message').title = "Success";
    $('#message-header').html(textStatus);
    $('#message-detail').html(response.port_name + " is updated successfully.");
//    $("#check-circle").css('visibility', 'visible');
    $("#check-circle").show();
    $( "#dialog-message" ).dialog({
      modal: true,
      buttons: {
        Ok: function() {
          $( this ).dialog( "close" );
        }
      }
    });
}

// variable to hold request
var request;
// bind to the submit event of our form
$("#routerport-update").submit(function(event){
    // abort any pending request
    if (request) {
        request.abort();
    }
    // setup some local variables
    var $form = $(this);
    // let's select and cache all the fields
    var $inputs = $form.find("input, select, button, textarea");
    // serialize the data in the form
    var serializedData = $form.serialize();

    // let's disable the inputs for the duration of the ajax request
    $inputs.prop("disabled", true);

    // fire off the request to /form.php
    request = $.ajax({
        url : "",
        type : "post",
        dataType : 'jsonp', //xml, json, jsonp, html, script, text
        data : serializedData
    });

    // callback handler that will be called on success
    request.done(function (response, textStatus, jqXHR){
        WebServiceSuccessHandler(response, textStatus, jqXHR);
    });

    // callback handler that will be called on failure
    request.fail(function (jqXHR, textStatus, errorThrown){
        WebServiceErrorHandler(jqXHR, textStatus, errorThrown);
    });

    // callback handler that will be called regardless
    // if the request failed or succeeded
    request.always(function () {
        // reenable the inputs
        $inputs.prop("disabled", false);
    });

    // prevent default posting of form
    event.preventDefault();
});