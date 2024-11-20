import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import RatesView from '../views/RatesView.vue';
import ExchangeView from '../views/ExchangeView.vue';
import MapView from '../views/MapView.vue';
import CommunityView from '../views/community/CommunityView.vue';
import LoginPage from "@/views/LoginPage.vue";
import RegisterPage from "@/views/RegisterPage.vue";
import ProfileView from '@/views/ProfileView.vue';
import DetailProduct from '@/views/DetailProdoct.vue';
import ArticleForm from '@/views/community/ArticleForm.vue';
import ArticleDetail from '@/views/community/ArticleDetail.vue';

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
    name: "login" 
  },
  { 
    path: "/register",
    component: RegisterPage, 
    name: "register" 
  },
  {
    path: "/profile",
    name: "profile",
    component: ProfileView,
  },
  {
    path: "/details/:id",
    name: "details",
    component: DetailProduct,
    props: true,
  },
  {
    path: "/product/:id",
    name: "DetailProduct",
    component: DetailProduct,
    props: (route) => ({
      product: route.query.data ? JSON.parse(route.query.data) : null,
    }),
  },
  {
    path: '/community/create',
    name: 'articleCreate',
    component: ArticleForm
  },
  {
    path: '/community/:id',
    name: 'articleDetail',
    component: ArticleDetail
  },
  {
    path: '/community/:id/edit',
    name: 'articleEdit',
    component: ArticleForm
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
