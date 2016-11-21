<template>
<div class="container loginBody">
  <div class="row">
    <div class="login-brand">Swinglytics</div>

    <div class="col-xs-12 col-sm-6 col-sm-offset-3">
      <div class="form-type">
        <div class="row">
          <div class="col-xs-6 text-center">
            <a href="/login"><span class="login-register ">Login</span></a>
          </div>
          <div class="col-xs-6 text-center">
            <a href="/register"><span class="login-register ">Register</span></a>
          </div>
        </div>
      </div>
      <div class="form-type-highlight-reverse"></div>
      <div class="login-body">
        <div class="row">
          <div class="col-xs-12 ">
            <form @submit.prevent="register" class="form-horizontal login-form">
              <div class="form-group">
                <label class="control-label col-sm-3 login-label" for="email">Email:</label>
                <div class="col-sm-9">
                  <input type="email" class="form-control login-form-input" placeholder="">
                </div>
              </div>
              <div class="form-group">
                <label class="control-label col-sm-3 login-label" for="username">Username:</label>
                <div class="col-sm-9">
                  <input type="text" class="form-control login-form-input" placeholder="">
                </div>
              </div>
              <div class="form-group">
                <label class="control-label col-sm-3 login-label" for="password">Password:</label>
                <div class="col-sm-9">
                  <input type="password" class="form-control login-form-input" placeholder="">
                </div>
              </div>
              <div class="form-group">
                <label class="control-label col-sm-3 login-label" for="password"> Confirm:</label>
                <div class="col-sm-9">
                  <input type="password" class="form-control login-form-input" placeholder="">
                </div>
              </div>
              <div class="form-group">
                <div class="col-sm-12 text-center">
                <button type="submit" class="btn btn-default btn-mobile btn-login">Register</button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</div>

</template>

<script>

function doRequest(url, jsonParams, callback) {

  var params = "";
  for (var key in jsonParams) {
    params += key + "=" + jsonParams[key] + '&';
  }
  // remove last "&"
  params = params.substring(0, params.length-1);


  var http = new XMLHttpRequest();
  http.open("POST", url, true);
  http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  http.withCredentials = true;

  http.onreadystatechange = function() {//Call a function when the state changes.
      if(http.readyState == 4) {
        if (typeof callback === "function") {
          callback(http);
        }
      }
  }
  console.log(http);
  http.send(params);

}


export default {
  data () {
    return {
      email: 'kingkuta@example.com',
      pass: '',
      error: false
    }
  },
  methods: {

  register () {

      var url = "http://golf-innovation.com:3000/api/v1/user/register";
      var jsonParams = {
        username: "testUserC",
        password: "test1234C",
        email: "testC@gmail.com",
        firstname: "JohnD",
        lastname: "DoeC"
      };
      doRequest(url, jsonParams, function(http) {
        console.log(http);
        console.log(http.status); //returns 200, 403, etc
        console.log(http.responseText); //returns text if any is returned (see documentation)
      });

    this.$router.replace(this.$route.query.redirect || '/onboarding');

  },

  //end login
  }

  //end method
  }


</script>

<style>
.error {
  color: red;
}
</style>
