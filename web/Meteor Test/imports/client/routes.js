// just kinda need this here
BlazeLayout.setRoot('body');

// imports
import '../ui/layouts/layout.html';
import '../ui/pages/root.html';
import '../ui/pages/dashboard.html';
import '../ui/components/navbar.html';
import '../ui/components/returnHome.html';
import '../ui/components/footer.html';
import '../ui/pages/login.html';
import '../ui/pages/register.html';
import '../ui/pages/navigationDemo.html';

import '../ui/pages/onboarding1.html';
import '../ui/pages/onboarding2.html';
import '../ui/pages/onboarding3.html';

// routes

FlowRouter.route('/', {
  name: "Initial",
  action() {
    BlazeLayout.render('LayoutTmpl', {main: 'navigationDemoTemplate'})
  }
})

FlowRouter.route('/test', {
  name: "Initial",
  action() {
    BlazeLayout.render('LayoutTmpl',  {main: 'testTemplate2'} )
  }
})

FlowRouter.route('/login', {
  name: "Initial",
  action() {
    BlazeLayout.render('LayoutTmpl',  {main: 'loginTemplate'} )
  }
})

FlowRouter.route('/register', {
  name: "Initial",
  action() {
    BlazeLayout.render('LayoutTmpl',  {main: 'registerTemplate'} )
  }
})

FlowRouter.route('/onboarding1', {
  name: "Initial",
  action() {
    BlazeLayout.render('LayoutTmpl',  {main: 'onboarding1Template'} )
  }
})

FlowRouter.route('/onboardingAlt', {
  name: "Initial",
  action() {
    BlazeLayout.render('LayoutTmpl',  {main: 'onboardingAltTemplate'} )
  }
})

FlowRouter.route('/onboarding2', {
  name: "Initial",
  action() {
    BlazeLayout.render('LayoutTmpl',  {main: 'onboarding2Template'} )
  }
})

FlowRouter.route('/onboarding3', {
  name: "Initial",
  action() {
    BlazeLayout.render('LayoutTmpl',  {main: 'onboarding3Template'} )
  }
})

FlowRouter.route('/dashboard', {
  name: "Initial",
  action() {
    BlazeLayout.render('LayoutTmpl',  {main: 'dashboardTemplate'} )
  }
})
