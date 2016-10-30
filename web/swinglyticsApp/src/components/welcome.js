import React from 'react';
import '../App.css';
import { Grid, Row, Col, Button} from 'react-bootstrap';

import { browserHistory } from 'react-router'

class WelcomePage extends React.Component {


  constructor(props) {
   super(props);
   this.state = {};
 }

  moveToDashboard(){
   console.log("moveToDashboard was called")

   const path = '/dashboard';
   browserHistory.push(path);
 }

  render() {
    return (
      <Grid>
        <Row>
          <Col xs={12} sm={6} smOffset={3} className="loginBody">
            <div className="login-brand">Welcome</div>
              <Button type="button" className="btn-mobile" onClick={this.moveToDashboard}>
                Continue
              </Button>
          </Col>
        </Row>
      </Grid>
    );
  }


}

export default WelcomePage;
