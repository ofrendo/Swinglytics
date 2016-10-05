// just kinda need this here
BlazeLayout.setRoot('body');

// imports
import '../ui/layouts/layout.html';
import '../ui/pages/root.html';
import '../ui/pages/dashboard.html';
import '../ui/components/navbar.html';

// routes

FlowRouter.route('/', {
  name: "Initial",
  action() {
    BlazeLayout.render('LayoutTmpl', {main: 'dashboardTemplate'})
  }
})

FlowRouter.route('/test', {
  name: "Initial",
  action() {
    BlazeLayout.render('LayoutTmpl',  {main: 'testTemplate2'} )
  }
})
