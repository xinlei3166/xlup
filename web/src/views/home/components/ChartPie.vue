<template>
    <div ref="dom" class="charts chart-pie"></div>
</template>

<script lang="ts">
    import echarts from "echarts"
    import tdTheme from "../theme.json"

    echarts.registerTheme("tdTheme", tdTheme)

    import {Component, Vue, Prop} from "vue-property-decorator";

    @Component
    export default class InfoCard extends Vue {
        @Prop({type: Array}) private value!: any[]
        @Prop({type: String}) private text!: string
        @Prop({type: String}) private subtext!: string

        mounted() {
            this.$nextTick(() => {
                let legend = this.value.map(_ => _.name)
                let option:object = {
                    title: {
                        text: this.text,
                        subtext: this.subtext,
                        x: "center"
                    },
                    tooltip: {
                        trigger: "item",
                        formatter: "{a} <br/>{b} : {c} ({d}%)"
                    },
                    legend: {
                        orient: "vertical",
                        left: "left",
                        data: legend
                    },
                    series: [
                        {
                            type: "pie",
                            radius: "55%",
                            center: ["50%", "60%"],
                            data: this.value,
                            itemStyle: {
                                emphasis: {
                                    shadowBlur: 10,
                                    shadowOffsetX: 0,
                                    shadowColor: "rgba(0, 0, 0, 0.5)"
                                }
                            }
                        }
                    ]
                }
                let dom = echarts.init(this.$refs.dom as HTMLCanvasElement, "tdTheme")
                dom.setOption(option)
            })
        }
    }
</script>

<style scoped>

</style>
