<template>
  <div>
    <h2>Profile</h2>

    <nav class="navbar navbar-default navbar-fixed-bottom text-center footer">
      <div class="container">

  <button v-on:click="navSessions" class="col-xs-4"><i class="fa fa-check fa-2x"></i><br/>Sessions</button>
  <button v-on:click="navDashboard" class="col-xs-4"><i class="fa fa-dashcube fa-2x"></i><br/>Dashboard</button>
  <button v-on:click="navProfile" class="col-xs-4"><i class="fa fa-user fa-2x"></i><br/>Profile</button>

      </div>
    </nav>


  </div>



</template>


<script>

export default {
  data () {
    return {
      email: 'kingkuta@example.com',
      pass: '',
      error: false
    }
  },

  methods: {

  navSessions: function (event) {
    this.$router.replace(this.$route.query.redirect || '/sessions');
  },

  navDashboard: function (event) {
    this.$router.replace(this.$route.query.redirect || '/dashboard');
  },

  navProfile: function (event) {
    this.$router.replace(this.$route.query.redirect || '/profile');
  },

  //end login
  }

  //end method
  }

</script>
