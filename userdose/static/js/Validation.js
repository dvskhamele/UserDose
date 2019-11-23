function validateUsername() {
    console.log("data");           
  var form = $(this).closest("form");
        var username = $("#username").val();

 var pattern = new RegExp(/^[a-z][a-z0-9_.-]{1,19}$/); 

 if(!pattern.test(username)) {    
         $("#already_exist_user").text("username must be simple to memorise :)");
$("#already_exist_user").css("display", "block");
        $("#signup").attr("disabled", true);
$('#password').attr("disabled", true);
$('#confirmpassword').attr("disabled", true);
$('#email').attr("disabled", true);
         return false;
}else{
$("#already_exist_user").css("display", "none");
}

  $.ajax({
    url: "/api/v1/users/check_if_exists/",
    data: {
          'username': username
        },
    dataType: 'json',
    success: function (data) {
    console.log("data",data);           
      if (data.message) {
$("#already_exist_user").css("display", "block");
$("#already_exist_user").text(data.error_message);
        $("#signup").attr("disabled", true);
$('#password').attr("disabled", true);
$('#confirmpassword').attr("disabled", true);
$('#email').attr("disabled", true);
 return false;
      }else{
        $("#already_exist_user").css("display", "none");
$('#password').removeAttr("disabled");
$('#confirmpassword').removeAttr("disabled");
$('#email').removeAttr("disabled");
        $("#signup").removeAttr("disabled");
    }
    },
    error: function (jqXHR, textStatus, errorThrown) {
    console.log(jqXHR);
    console.log(textStatus);
    console.log(errorThrown);
}
  });

}

function validateEmail() {
    console.log("data");           
  var form = $(this).closest("form");
        var email = $("#email").val();
              if (email.length!=0) {

  $.ajax({
    url: "/api/v1/users/check_if_exists/",
    data: {
          'email': email
        },
    dataType: 'json',
    success: function (data, status, xhr) {
      if (data.message) {
        alert("Sorry, its only one time list viewing site, and You have already been listed and reviewed list. Our paid plans are coming soon for reviewing more times. thanks :)");
         return false;
      }else{
        $("#already_exist_email").css("display", "none");
        $("#signup").removeAttr("disabled");
    }
    },
    error: function (jqXHR, textStatus, errorThrown) {
    console.log(jqXHR);
    console.log(textStatus);
    console.log(errorThrown);
}
  });
}
}

function validatePassword(e) {
        var validator = $("#regForm").validate({
            rules: {
                password: {
                    required: true,
                    minlength: 8,
                    maxlength:20
                },
                confirmpassword: {
                    required: true,
                    equalTo: "#password"
                }
            }

        })

        if (validator.form()) {
        var email = $("#email").val();
        var username = $("#username").val();
        var password = $("#password").val();
    console.log("data to signup", email,username,password);           
  $.ajax({
    url: "/api/v1/accounts/register/",
          type: 'POST',
    data: {
          'email': email,
          'username': username,
          'password': password,
        },
    dataType: 'json',
    success: function (data, status, xhr) {
        console.log("Content-Type",xhr.getAllResponseHeaders("Content-Type"));
    console.log("data from signup",data);           
            $("#myModal").modal();
    },
    error: function (jqXHR, textStatus, errorThrown) {
    console.log("jqXHR.responseText",jqXHR.responseText);
    console.log("textStatus",textStatus);
    console.log('errorThrown',errorThrown);
}
            });
            return false;
        }
        else{
            return false;
        }
    }