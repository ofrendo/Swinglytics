<template>
  <div class="container loginBody">



    <div class="row onboard">
      <div class="onboard-welcome">Preferences</div>

      <h2 class="onboard">set your prferences below</h2>

      <div class="row">
        <div class="col-sm-6 col-sm-offset-3 col-xs-8 col-xs-offset-2 text-center">
          <h2 class="custom"><i>Any preferences that could be set would be listed here</i></h2>
          <form @submit.prevent="next">
        <button type="submit" class="btn btn-default onboard-btn">Confirm</button>
        </form>
        </div>
      </div>

    </div>


    </div>


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

    next () {

this.$router.replace(this.$route.query.redirect || '/onboarding3');

    }


  //end login
  }

  //end method
  }


</script>
