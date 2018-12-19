<template>
    <Table :height="height" :highlight-row="highlightRow" :no-data-text="noDataText" :no-filtered-data-text="noFilteredDataText"
           :columns="columns" :data="data"></Table>
</template>

<script lang="ts">
    import { Component, Vue, Prop } from "vue-property-decorator";

    @Component
    export default class MyTable extends Vue {
        @Prop({type: [Number, String], default: 520}) private height!: number|string
        @Prop({type: Boolean, default: true}) private highlightRow!: boolean
        @Prop({type: String, default: '暂无数据'}) private noDataText!: string
        @Prop({type: String, default: '没有找到你要搜索的数据'}) private noFilteredDataText!: string
        @Prop({type: Array, required: true}) private columns!: object[]
        @Prop({type: Array, required: true}) private data!: object[]
    }
</script>

<style lang="stylus" scoped>

</style>
