import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignupView from '../views/SignupView.vue'
import LoginView from '../views/LoginView.vue'
import FeedView from '../views/FeedView.vue'
import SearchView from '../views/SearchView.vue'
import ProfileView from '../views/ProfileView.vue'
import FriendsView from '../views/FriendsView.vue'
import PostView from '../views/PostView.vue'
import ChatView from '../views/ChatView.vue'
import FollowingView from '../views/FollowingView.vue'
import LikedView from '../views/LikedView.vue'
import CategoryView from '../views/CategoryView.vue'
import EditProfileView from '../views/EditProfileView.vue'
import CertificateView from '../views/CertificateView.vue'
import NotificationView from '../views/NotificationView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/feed',
      name: 'feed',
      component: FeedView,
    },
    {
      path: '/search',
      name: 'search',
      component: SearchView,
    },
    {
      path: '/profile/:id',
      name: 'profile',
      component: ProfileView,
    },
    {
      path: '/profile/:id/friends',
      name: 'friends',
      component: FriendsView,
    },
    {
      path: '/:id',
      name: 'postview',
      component: PostView,
    },
    {
      path: '/chat',
      name: 'chat',
      component: ChatView,
    },
    {
      path: '/following',
      name: 'following',
      component: FollowingView,
    },
    {
      path: '/liked_posts/:id',
      name: 'liked_posts',
      component: LikedView,
    },
    {
      path: '/categories/:id',
      name: 'categories',
      component: CategoryView,
    },
    {
      path: '/profile/edit',
      name: 'edit_profile',
      component: EditProfileView
    },
    {
      path: '/certificate/:id',
      name: 'certificate',
      component: CertificateView
    },
    {
      path: '/notifications',
      name: 'notifications',
      component: NotificationView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    }
  ]
})

export default router
