<template>
    <div ref="dom" class="charts chart-bar"></div>
</template>

<script lang="ts">
    import echarts from "echarts"
    import tdTheme from "./theme.json"
    import {Component, Vue, Prop} from "vue-property-decorator"

    @Component
    export default class InfoCard extends Vue {
        @Prop({type: Object}) private value!: object
        @Prop({type: String}) private text!: string
        @Prop({type: String}) private subtext!: string

        mounted() {
            this.$nextTick(() => {
                let xAxisData = Object.keys(this.value)
                let seriesData = Object.values(this.value)
                let option:object = {
                    title: {
                        text: this.text,
                        subtext: this.subtext,
                        x: "center"
                    },
                    xAxis: {
                        type: "category",
                        data: xAxisData
                    },
                    yAxis: {
                        type: "value"
                    },
                    series: [{
                        data: seriesData,
                        type: "bar"
                    }]
                }
                let dom = echarts.init(this.$refs.dom as HTMLCanvasElement, "tdTheme")
                dom.setOption(option)
            })
        }
    }
</script>

<style lang="stylus" scoped>
    .charts {
    }
</style>
