<template>
    <div>
        <Card>
            <MyTable :columns="columns" :data="data"></MyTable>
        </Card>
        <Paginator ref="paginator" :total="total" :onChange="onChange" :onPageSizeChange="onPageSizeChange"></Paginator>
    </div>
</template>

<script lang="ts">
    import { Component, Vue, Watch } from "vue-property-decorator";
    import MyTable from "@/components/MyTable.vue"
    import Paginator from "@/components/Paginator.vue"
    import { checkToken } from "@/utils/decorators"
    import { getVideoApi, deleteVideoApi } from "@/api/video"

    @Component({
        components: { MyTable, Paginator }
    })
    export default class Video extends Vue {
        columns = [
            {
                title: "#",
                width: 60,
                align: "center",
                render: (h: any, params: any) => {
                    return h("div", [
                        h("span", params.index + 1)
                    ]);
                }
            },
            {
                title: "标题",
                key: "title",
            },
            {
                title: "描述",
                key: "description",
                ellipsis: true
            },
            {
                title: "预览图",
                key: "pic",
                render: (h: any, params: any) => {
                    return h('div', [
                        h('img', {
                            style: {
                                width: "32px",
                                height: "32px",
                            },
                            attrs: {
                                src: params.row.pic
                            }
                        },)
                    ]);
                }
            },
            {
                title: "视频",
                // width: 150,
                render: (h: any, params: any) => {
                    return h('div', [
                        h('Button', {
                            props: {
                                type: 'primary',
                                size: 'small',
                            },
                            on: {
                                click: () => {
                                    this.showVideo(params.row.title, params.row.video)
                                },
                            }
                        }, [
                            h('Icon', {
                                props: {
                                    type: 'ios-play',
                                    size: 14
                                }
                            })
                        ])
                    ]);
                }
            },
            {
                title: "功能",
                key: "action",
                tooltip: true,
                width: 150,
                align: "center",
                render: (h: any, params: any) => {
                    return h("div", [
                        h("Poptip", {
                            props: {
                                confirm: true,
                                transfer: true,
                                placement: 'top',
                                title: "您确认删除这条内容吗？",
                                onText: '确定',
                                canceltext: '取消',
                                type: 'error',
                                size: 'small',
                            },
                            on: {
                                'on-ok': () => {
                                    this.remove(params.row.id)
                                },
                            }
                        }, [
                            h('Button', {
                                props: {
                                    type: "error",
                                    size: "small"
                                }
                            }, '删除')
                        ])
                    ]);
                }
            }
        ]

        currentPage = 1
        pageSize = 10
        data = []
        total = 0

        async created() {
            await this.getData()
        }

        async getData(): Promise<void> {
            const data = await this._getData(getVideoApi, {page: this.currentPage, per_page: this.pageSize})
            if (data) {
                this.data = data.data
                this.total = data.total
            } else {
                this.$Notice.error({'title': '获取数据失败'})
            }
        }

        @checkToken()
        async _getData(...args): Promise<any> {
            const data = args[0]
            switch (data.code) {
                case 'Success':
                    return data
                default:
                    return
            }
        }

        @checkToken()
        async deleteData(...args): Promise<boolean> {
            const data = args[0]
            switch (data.code) {
                case 'Success':
                    return true
                default:
                    return false
            }
        }

        async remove(id: number): Promise<void> {
            const ret = await this.deleteData(deleteVideoApi, id)
            if (ret) {
                await this.getData()
                this.$Notice.success({'title': '删除成功'})
            } else {
                this.$Notice.error({'title': '删除失败'})
            }
        }

        async onChange(currentPage: number): Promise<void> {
            this.currentPage = currentPage
            await this.getData()
        }

        async onPageSizeChange(pageSize: number): Promise<void> {
            this.pageSize = pageSize
            await this.getData()
        }

        showVideo(title: string, path: string): void {
            this.$Modal.success({
                closable: false,
                // @ts-ignore
                maskClosable: false,
                footerHide: true,
                className: 'video-modal',
                width: '800px',
                title: title,
                content: `<div style="width: 100%;padding: 12px 20px 0 20px"><video src="${path}" controls></div>`,
                okText: '关闭',
                onOk: () => {
                    this.$Modal.remove()
                }
            })
        }

        @Watch('data')
        async onDataChanged(val: any): Promise<void> {
            if (val.length === 0 && this.currentPage > 1) {
                this.currentPage -= 1
                await this.getData()
            }
        }
    }
</script>

<style lang="stylus" scoped>
    .ivu-modal-wrap
        .ivu-modal-confirm-footer
                display: none
</style>
