<template>
    <i :class="`iconfont icon-${type}`" :style="styles"></i>

</template>

<script lang="ts">
    import { Component, Vue, Prop } from "vue-property-decorator";

    @Component
    export default class Icons extends Vue {
        @Prop({ type: String, required: true }) private type!: String
        @Prop({ type: String, default: "#5c6b77" }) private color!: String
        @Prop({ type: Number, default: 16 }) private size!: Number

        get styles() {
            return {
                fontSize: `${this.size}px`,
                color: this.color
            }
        }
    }
</script>

<style scoped>

</style>
