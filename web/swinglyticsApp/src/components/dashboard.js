import React from 'react';
import '../App.css';
import { Grid, Row, Col, Button} from 'react-bootstrap';
import * as firebase from 'firebase';
import { browserHistory } from 'react-router'

class DashboardPage extends React.Component {


  constructor(props) {
   super(props);
   this.state = {};
   this.handleLogout = this.handleLogout.bind(this);
 }



 handleLogout(){
   console.log("handleLogout was called")

   firebase.auth().signOut().then(function() {
  // Sign-out successful.
  const pathlogin = '/login';
  browserHistory.push(pathlogin);
  console.log("logout was successful...")
    }, function(error) {
      // An error happened.
    });
 }

  render() {
    var user = firebase.auth().currentUser;

    return (
      <Grid>
        <Row>
          <Col xs={12} sm={6} smOffset={3} className="loginBody">
            <div className="login-brand">Dashboard</div>
            <div>Email: { user.email }</div>
            <div>ID: { user.uid }</div>
              <Button type="button" className="btn-mobile" onClick={this.handleLogout}>
                Sign Out
              </Button>
          </Col>
        </Row>
      </Grid>
    );
  }


}

export default DashboardPage;
