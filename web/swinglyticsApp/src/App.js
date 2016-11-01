import React, { Component } from 'react';
import './App.css';
import { Grid, Row, Col, FormGroup, ControlLabel, FormControl, Button, Form} from 'react-bootstrap';
import * as firebase from 'firebase';
import { browserHistory } from 'react-router'


class App extends Component {
  constructor(props) {
   super(props);
   this.state = {
     email: '',
     password: ''
   };
   this.handleEmailChange = this.handleEmailChange.bind(this);
   this.handlePasswordChange = this.handlePasswordChange.bind(this);
   this.handleLogin = this.handleLogin.bind(this);
 }

  handleEmailChange(event) {
    this.setState({email: event.target.value});
    //console.log(this.state.email);
  }

  handlePasswordChange(event) {
   this.setState({password: event.target.value});
 }


 handleLogin(){
   console.log("handleLogin was called")

   var email = this.state.email;
   var password = this.state.password;
   console.log("Email: " + email);
   console.log("Password: " + password);

  fetch("server/login", {  
    method: "post",  
    //mode: 'cors', 
    headers: {  
      "Content-type": "application/json"  
    },  
    body: {
      "email": email,
      "password": password
    }
  })
  .then(json)  
  .then(function (data) {  
    console.log('Request succeeded with JSON response', data);  
    //const path = '/dashboard';
    //browserHistory.push(path);
  })  
  .catch(function (error) {  
    console.log('Request failed', error);  
  });

 }

  render() {
    return (
      <Grid>
        <Row>
          <Col xs={12} sm={6} smOffset={3} className="loginBody">
            <div className="login-brand">Swinglytics</div>
            <div className="form-type">
              <Row>
                <Col xs={6} className="text-center">
                  <a href="/login"><span className="login-register ">Login</span></a>
                </Col>
                <Col xs={6} className="text-center">
                  <a href="/register"><span className="login-register ">Register</span></a>
                </Col>
              </Row>
            </div>
            <div className="form-type-highlight"></div>
            <div className="login-body">
              <Row>
                <Col xs={12}>
                  <Form horizontal className="login-form">
                    <FormGroup controlId="formHorizontalEmail">
                      <Col componentClass={ControlLabel} sm={3} xs={12} className="login-label">
                        Email:
                      </Col>
                      <Col sm={9} xs={12}>
                        <FormControl type="text" name="email" className="login-form-input" onChange={this.handleEmailChange} />
                      </Col>
                    </FormGroup>
                    <FormGroup controlId="formHorizontalEmail">
                      <Col componentClass={ControlLabel} sm={3} xs={12} className="login-label">
                        Password:
                      </Col>
                      <Col sm={9} xs={12}>
                        <FormControl type="password" name="password" className="login-form-input"
                          onChange={this.handlePasswordChange} value={this.state.password}/>
                      </Col>
                    </FormGroup>
                    <FormGroup>
                      <Col className="text-center">
                        <Button type="button" className="btn-mobile" onClick={this.handleLogin}>
                          Login
                        </Button>
                      </Col>
                    </FormGroup>
                  </Form>
                </Col>
              </Row>
            </div>
          </Col>
        </Row>
      </Grid>
    );
  }


}

export default App;
