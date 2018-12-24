<template>
    <div>
        <Card>
            <div class="search-con">
                <Input v-model="q" search placeholder="输入关键字搜索" @on-search="onSearch" class="search-input"/>
                <Button class="search-btn" type="primary" @click="onAll">全部</Button>
            </div>
            <MyTable ref="table" :height="tableHeight" :columns="columns" :data="data"></MyTable>
        </Card>
        <Paginator ref="paginator" :total="total" :currentPage="currentPage" :pageSize="pageSize" :onChange="onChange" :onPageSizeChange="onPageSizeChange"></Paginator>
    </div>
</template>

<script lang="ts">
    import { Component, Vue, Watch } from "vue-property-decorator";
    import MyTable from "@/components/MyTable.vue"
    import Paginator from "@/components/Paginator.vue"
    import { checkToken } from "@/utils/decorators"
    import { getVideoAdminApi, deleteVideoAdminDetailsoApi } from "@/api/video"
    import { tooltip, stripSpaceCharacter } from "@/utils/util"


    @Component({
        components: { MyTable, Paginator }
    })
    export default class VideoAdmin extends Vue {
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
                render: (h, params) => {
                    return tooltip(h, params.row.title, 16)
                }
            },
            {
                title: "描述",
                key: "description",
                render: (h, params) => {
                    return tooltip(h, params.row.description, 16)
                }
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
                title: "用户",
                key: "user",
                ellipsis: true
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

        tableHeight = 0

        q = ''
        currentPage = 1
        pageSize = 20
        data = []
        total = 0

        async created() {
            await this.getData()
            this.tableHeight = window.innerHeight - (this.$refs.table as any).$el.offsetTop - 250
        }

        async getData(): Promise<void> {
            const params = {page: this.currentPage, per_page: this.pageSize}
            if (this.q !== ''){
                params['q'] = this.q
            }
            const data = await this._getData(getVideoAdminApi, params)
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

        async onSearch(value: string): Promise<void> {
            this.q = stripSpaceCharacter(value)
            this.currentPage = 1
            await this.getData()
        }

        async onAll(): Promise<void> {
            this.q = ''
            this.currentPage = 1
            await this.getData()
        }

        showVideo(title: string, path: string): void {
            this.$Modal.info({
                closable: false,
                width: '800px',
                title: `${title}`,
                content: `<div style="width: 100%;padding: 12px 20px 0 20px"><video src="${path}" controls></div>`,
                okText: '关闭',
                onOk: () => this.$Modal.remove()
            })
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
            const ret = await this.deleteData(deleteVideoAdminDetailsoApi, id)
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
    .search-con
        padding: 0 0 10px 0

        .search

            &-input
                display: inline-block
                width: 300px
                margin-left: 2px

            &-btn
                margin-left: 15px

            &-btn-right
                float right
                margin-right 30px
</style>
