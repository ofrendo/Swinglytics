export default {
  login(email, pass, cb) {
    cb = arguments[arguments.length - 1];
    if (localStorage.token) {
      if (cb === true) {
        this.onChange(true);
        return;
      }
    }
    pretendRequest(email, pass, res => {
      if (res.authenticated) {
        localStorage.token = res.token;
        if (cb === true) {
          this.onChange(true);
        }
      } else {
        this.onChange(false);
      }
    });
  },

  getToken() {
    return localStorage.token;
  },

  logout(cb) {
    delete localStorage.token;
    if (cb === true) {
      this.onChange(false);
    }
  },

  loggedIn() {
    return Boolean(localStorage.token);
  },

  onChange() {}
};

function pretendRequest(email, pass, cb) {
  setTimeout(() => {
    if (email === 'joe@example.com' && pass === 'password1') {
      cb({
        authenticated: true,
        token: Math.random().toString(36).substring(7)
      });
    } else {
      cb({authenticated: false});
    }
  }, 0);
}
