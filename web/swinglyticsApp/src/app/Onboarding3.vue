<template>
  <div class="container loginBody">



    <div class="row onboard">
      <div class="onboard-welcome">Quick Guide</div>
      <div class="row">
        <div class="col-xs-10 col-xs-offset-1 text-left quickstart">
          <ol>
              <li>Lorem ipsum dolor sit amet, consectetur adipiscing elit</li>
              <li>Duis et efficitur leo. Vivamus tristique enim ut purus</li>
              <li>In eget dui in urna facilisis congue sed sit amet orci</li>
              <li>Morbi laoreet vitae sapien quis sollicitudin</li>
          </ol>

          <div class="col-sm-12 text-center">
          <form @submit.prevent="next">
            <button type="submit" class="btn btn-default onboard-btn">Confirm</button>
            </form>
          </div>

          <div class="spacing-40"></div>

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

this.$router.replace(this.$route.query.redirect || '/dashboard');

    }


  //end login
  }

  //end method
  }


</script>
