<template>
    <Card :shadow="shadow" class="info-card-wrapper" :padding="0">
        <div class="content-con">
            <div class="left-area" :style="{background: color, width: leftWidth}">
                <CommonIcon class="icon" :type="icon" :size="iconSize" color="#fff"/>
            </div>
            <div class="right-area" :style="{width: rightWidth}">
                <div>
                    <slot></slot>
                </div>
            </div>
        </div>
    </Card>
</template>

<script lang="ts">
    import {Component, Vue, Prop} from "vue-property-decorator";
    import CommonIcon from './CommonIcon.vue'

    @Component({
        components: {
            CommonIcon
        }
    })
    export default class InfoCard extends Vue {
        @Prop({ type: Number, default: 36 }) private left!: number
        @Prop({ type: String, default: '#2d8cf0' }) private color!: string
        @Prop({ type: String, default: '' }) private icon!: string
        @Prop({ type: Number, default: 20 }) private iconSize!: number
        @Prop({ type: Boolean, default: false }) private shadow!: boolean

        get leftWidth() {
            return `${this.left}%`
        }

        get rightWidth() {
            return `${100 - this.left}%`
        }
    }
</script>

<style lang="stylus" scoped>
    common()
        float left
        height 100%
        display table
        text-align center

    size()
        width 100%
        height 100%

    middle-center()
        display table-cell
        vertical-align middle

    .info-card-wrapper
        overflow: hidden
        size()
        & >>> .ivu-card-body
            size()
        .content-con
            position relative
            size()
            .left-area
                common()
                &  > .icon
                    middle-center()
            .right-area
                common()
                &  > div
                    middle-center()
</style>
