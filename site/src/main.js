import Vue from 'vue'
import App from './App.vue'
import router from './router'
import Buefy from 'buefy'

Vue.config.productionTip = false;
Vue.config.devtools = true;

Vue.use(Buefy, {
    defaultIconPack: 'fas'
});

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
