<template>
    <div id="app">
        <router-view/>
    </div>
</template>

<script lang="ts">
    import { Component, Vue } from 'vue-property-decorator';

    @Component
    export default class App extends Vue {
        //
    }
</script>

<style lang="stylus">
    html,body
        width 100%
        height 100%
    #app
        font-family 'Avenir', Helvetica, Arial, sans-serif
        width 100%
        height 100%
</style>

