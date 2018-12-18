<template>
    <div class="paginator-style" style="">
        <Page :total="total" :current="currentPage" :page-size="pageSize" @on-change="onChange" @on-page-size-change="onPageSizeChange" :page-size-opts="[10, 20, 30, 50, 100]" show-total show-sizer show-elevator transfer/>
    </div>
</template>

<script lang="ts">
    import { Component, Vue, Prop } from "vue-property-decorator";

    @Component
    export default class Main extends Vue {
        @Prop({type: Number, required: true}) private total!: number
        @Prop({type: Number, default: 1}) private currentPage!: number
        @Prop({type: Number, default: 10}) private pageSize!: number
        @Prop({type: Function, required: true}) private onChange!: Function
        @Prop({type: Function, required: true}) private onPageSizeChange!: Function
    }
</script>

<style lang="stylus" scoped>
    .paginator-style
        margin-top: 18px
        display: flex
        align-items: center
        justify-content: center
</style>
