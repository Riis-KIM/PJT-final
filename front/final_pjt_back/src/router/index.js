import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import RatesView from '../views/RatesView.vue';
import ExchangeView from '../views/ExchangeView.vue';
import MapView from '../views/MapView.vue';
import CommunityView from '../views/CommunityView.vue';
import LoginPage from "@/views/LoginPage.vue";
import RegisterPage from "@/views/RegisterPage.vue";

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/rates',
    name: 'rates',
    component: RatesView,
  },
  {
    path: '/exchange',
    name: 'exchange',
    component: ExchangeView,
  },
  {
    path: '/map',
    name: 'map',
    component: MapView,
  },
  {
    path: '/community',
    name: 'community',
    component: CommunityView,
  },
  { 
    path: "/login", 
    component: LoginPage, 
    name: "Login" 
  },
  { 
    path: "/register",
    component: RegisterPage, 
    name: "Register" 
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
