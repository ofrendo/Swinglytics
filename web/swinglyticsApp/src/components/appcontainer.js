import React from 'react';
import '../App.css';
import * as firebase from 'firebase';
import { browserHistory } from 'react-router'

class AppContainer extends React.Component {

  constructor(props) {
   super(props);
   this.state = {};
 }

// This is executed before the Render function
// Checks if a current User exists (meaning the user is logged in)
// if the user is logged in -> send them to the dashboard, if no user exists -> send to login page
 componentWillMount() {
   firebase.auth().onAuthStateChanged(function(user) {
    if (user) {
      console.log("User is already logged in... move to dashboard");
      // User is signed in.
      const pathdashboard = '/dashboard';
      browserHistory.push(pathdashboard);

    } else {
      // No user is signed in.
      console.log("No user is logged in. Send to LoginPage");
      const pathlogin = '/login';
      browserHistory.push(pathlogin);
    }
  });
  }

  render() {
    return null;
  }


}

export default AppContainer;
