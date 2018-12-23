import Vue from 'vue';
import App from '@/App.vue';
import router from '@/router';
import store from '@/store';
import iView from 'iview'
import 'iview/dist/styles/iview.css';

Vue.config.productionTip = false

Vue.use(iView, {
    transfer: true,
    size: 'large'
})

Vue.prototype.$Notice.config({
    // top: 50,
    duration: 1.5
})

new Vue({
    router,
    store,
    render: (h) => h(App),
}).$mount('#app')

