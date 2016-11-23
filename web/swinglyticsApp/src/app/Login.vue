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
    <div class="form-type-highlight"></div>
    <div class="login-body">
      <div class="row">
        <div class="col-xs-12 ">
          <form @submit.prevent="login" class="form-horizontal login-form">
            <div class="form-group">
              <label class="control-label col-xs-12 col-sm-3 login-label" for="username">Username:</label>
              <div class="col-xs-12 col-sm-9">
                <input v-model="user" type="text" id="usernameInput" class="form-control login-form-input" placeholder="">
              </div>
            </div>
            <div class="form-group">
              <label class="control-label col-xs-12 col-sm-3 login-label" for="password">Password:</label>
              <div class="col-xs-12 col-sm-9">
                <input v-model="pass" type="password" id="passwordInput" class="form-control login-form-input" placeholder="">
              </div>
            </div>
            <div class="form-group">
              <div class="col-xs-12 text-center">
                <button type="submit" class="btn btn-default btn-mobile btn-login">Login</button>
                <p v-if="error" class="error">Bad login information</p>
                <p v-if="$route.query.redirect">You need to login first</p>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</div>
</div>

</template>

<script>

var that = this;
export default {
  data () {
    return {
      error: false
    }
  },

  methods: {

    login () {

      var username = document.getElementById("usernameInput").value;
      var password = document.getElementById("passwordInput").value;

      var that = this;
      var url = "/api/v1/user/login";
      var jsonParams = {
        username: username,
        password: password
      };

      console.log(that);
      doRequest(url, "POST", jsonParams, function(http) {
        console.log(http);
        console.log(http.status); //returns 200, 403, etc IF STATUS CHECKEN
        console.log(http.responseText); //returns text if any is returned (see documentation)
        console.log(this);
        console.log(that);
          if(http.status === 200){
            console.log(that);
            that.$router.replace(that.$route.query.redirect || '/dashboard');
          }

      });

    }


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
