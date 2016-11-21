import Vue from 'vue';
import Dashboard from './app/Dashboard.vue';
import Login from './app/Login.vue';
import Register from './app/Register.vue';
import Onboarding from './app/Onboarding.vue';
import Onboarding2 from './app/Onboarding2.vue';
import Onboarding3 from './app/Onboarding3.vue';
import Profile from './app/Profile.vue';
import Sessions from './app/Sessions.vue';
import Swing from './app/Swing.vue';
import StationScan from './app/StationScan.vue';
import './index.scss';
import VueRouter from 'vue-router';

Vue.use(VueRouter);

const router = new VueRouter({
  mode: 'history',
  routes: [
    {
      path: '/',
      components: {
        default: Login
      }
    },
    {path: '/dashboard', component: Dashboard},
    {path: '/login', component: Login},
    {path: '/register', component: Register},
    {path: '/onboarding', component: Onboarding},
    {path: '/onboarding2', component: Onboarding2},
    {path: '/onboarding3', component: Onboarding3},
    {path: '/profile', component: Profile},
    {path: '/sessions', component: Sessions},
    {path: '/stationscan', component: StationScan},
    {path: '/swing', component: Swing}
  ]
});

export default new Vue({
  el: '#root',
  router,
  render: h => h('router-view')
});
