import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import './index.css';
import * as firebase from 'firebase';
import { Router, Route, browserHistory } from 'react-router';

import RegisterPage from './components/register.js';
import DashboardPage from './components/dashboard.js';
import AppContainer from './components/appcontainer.js';
import WelcomePage from './components/welcome.js';

var config = {
    apiKey: "AIzaSyDttcy94V8SgDL62BkLizsRpoZXUF487XM",
    authDomain: "swinglyticstest.firebaseapp.com",
    databaseURL: "https://swinglyticstest.firebaseio.com",
    storageBucket: "swinglyticstest.appspot.com",
    messagingSenderId: "49030902296"
  };
firebase.initializeApp(config);


ReactDOM.render(
  <Router history={browserHistory}>
    <Route path="/" component={AppContainer} />
    <Route path="/login" component={App} />
    <Route path="/dashboard" component={DashboardPage} />
    <Route path="/register" component={RegisterPage} />
    <Route path="/welcome" component={WelcomePage} />
  </Router>,
  document.getElementById('root')
);
