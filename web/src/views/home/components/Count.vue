<template>
    <div>
        <div class="count-to-wrapper">
            <slot name="left"/>
            <p class="content-outer"><span :class="['count-to-count-text', countClass]"
                                           :id="counterId">{{ init }}</span><i
                    :class="['count-to-unit-text', unitClass]">{{ unitText }}</i></p>
            <slot name="right"/>
        </div>
    </div>
</template>

<script lang="ts">
    import CountUp from "countup"
    import {Component, Vue, Prop, Watch} from "vue-property-decorator";

    @Component
    export default class Count extends Vue {
        @Prop({type: Number, default: 0}) private init!: number
        // 起始值，即动画开始前显示的数值
        @Prop({type: Number, default: 0}) private startVal!: number
        // 结束值，即动画结束后显示的数值
        @Prop({type: Number, required: true}) private end!: number
        // 保留几位小数
        @Prop({type: Number, default: 0}) private decimals!: number
        // 分隔整数和小数的符号，默认是小数点
        @Prop({type: String, default: "."}) private decimal!: string
        // 动画持续的时间，单位是秒
        @Prop({type: Number, default: 2}) private duration!: number
        // 动画延迟开始的时间，单位是秒
        @Prop({type: Number, default: 0}) private delay!: number
        // 是否禁用easing动画效果
        @Prop({type: Boolean, default: false}) private uneasing!: boolean
        // 是否使用分组，分组后每三位会用一个符号分隔
        @Prop({type: Boolean, default: false}) private usegroup!: boolean
        // 用于分组(usegroup)的符号
        @Prop({type: String, default: ","}) private separator!: string
        // 是否简化显示，设为true后会使用unit单位来做相关省略
        @Prop({type: Boolean, default: false}) private simplify!: boolean
        // 自定义单位，如[3, 'K+'], [6, 'M+']即大于3位数小于6位数的用k+来做省略1000即显示为1K+
        @Prop({
            type: Array, default: () => {
                return [[3, "K+"], [6, "M+"], [9, "B+"]]
            }
        }) private unit!: any[]
        @Prop({type: String, default: ""}) private countClass!: String
        @Prop({type: String, default: ""}) private unitClass!: String

        counter: any = null
        unitText = ""

        get counterId() {
            return `count_to_${this["_uid"]}`
        }


        getHandleVal(val: any, len: any) {
            const _endVal = val / Math.pow(10, this.unit[len - 1][0])
            return {
                endVal: typeof _endVal === "string" ? parseInt(_endVal) : _endVal,
                // endVal: _endVal,
                unitText: this.unit[len - 1][1]
            }
        }

        transformValue(val: number) {
            let len = this.unit.length
            let res = {
                endVal: 0,
                unitText: ""
            }
            if (val < Math.pow(10, this.unit[0][0])) res.endVal = val
            else {
                for (let i = 1; i < len; i++) {
                    if (val >= Math.pow(10, this.unit[i - 1][0]) && val < Math.pow(10, this.unit[i][0])) res = this.getHandleVal(val, i)
                }
            }
            if (val > Math.pow(10, this.unit[len - 1][0])) res = this.getHandleVal(val, len)
            return res
        }

        getValue(val: number) {
            let res = 0
            if (this.simplify) {
                let {endVal, unitText} = this.transformValue(val)
                this.unitText = unitText
                res = endVal
            } else {
                res = val
            }
            return res
        }

        mounted() {
            this.$nextTick(() => {
                let endVal = this.getValue(this.end)
                this.counter = new CountUp(this.counterId, this.startVal, endVal, this.decimals, this.duration, {
                    useEasing: !this.uneasing,
                    useGrouping: this["useGroup"],
                    separator: this.separator,
                    decimal: this.decimal
                })
                setTimeout(() => {
                    if (!this.counter.error) this.counter.start()
                }, this.delay)
            })
        }

        @Watch("end")
        onEndChange(newVal) {
            let endVal = this.getValue(newVal)
            this.counter.update(endVal)
        }
    }
</script>

<style lang="stylus" scoped>
    prefix = count-to

    .{prefix}-wrapper
        .content-outer
            display: inline-block

            .{prefix}-unit-text
                font-style: normal

</style>
