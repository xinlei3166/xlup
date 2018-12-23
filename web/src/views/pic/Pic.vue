<template>
    <div>
        <Card>
            <div class="search-con">
                <Input v-model="q" search placeholder="输入关键字搜索" @on-search="onSearch" class="search-input"/>
                <Button class="search-btn" type="primary" @click="onAll">全部</Button>
                <Button class="search-btn-right" type="primary" @click="addPicModal=true">新增图片</Button>
                <Modal
                        title="新增图片"
                        v-model="addPicModal"
                        :mask-closable="false"
                        @on-ok="onAddPic">
                    <Form ref="addPicForm" :model="form" :rules="rules" :label-width="100" style="margin-top: 16px">
                        <FormItem prop="pic" label="图片">
                            <div class="upload">
                                <input ref="pic_input" type="file" name="pic" @change="changePic($event)"></input>
                                <p>
                                    <img v-if="previewPic !== ''" :src="previewPic" alt="pic" style="width: 100px">
                                </p>
                            </div>
                        </FormItem>
                        <FormItem prop="title" label="标题">
                            <Input type="text" v-model="form.title" placeholder="请输入标题" style="width: 320px"></Input>
                        </FormItem>
                        <FormItem prop="description" label="描述">
                            <Input type="textarea" v-model="form.description" placeholder="请输入描述" style="width: 320px"></Input>
                        </FormItem>
                    </Form>
                </Modal>
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
    import { getPicApi, postPicApi, deletePicApi } from "@/api/pic"
    import { tooltip, stripSpaceCharacter } from "@/utils/util"

    @Component({
        components: { MyTable, Paginator }
    })
    export default class Pic extends Vue {
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
                title: "图片",
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

        addPicModal = false
        previewPic = ''

        form = {
            title: '',
            description: ''
        }

        rules = {
            title: [
                {type: "string", max: 32, message: "标题最大长度为32", trigger: "blur"}
            ],
            description: [
                {type: "string", max: 64, message: "描述最大长度为64", trigger: "blur"},
            ]
        }

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
            const data = await this._getData(getPicApi, params)
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

        changePic(e) {
            const file = e.target.files[0]
            const reader = new FileReader()
            const self = this
            reader.readAsDataURL(file)
            reader.onload = function (e) {
                self.previewPic = (this as any).result
            }
        }

        @checkToken()
        async addPic(...args) {
            const data = args[0]
            switch (data.code) {
                case 'Success':
                    return data
                default:
                    return
            }
        }

        async onAddPic() {
            if ((this.$refs.pic_input as any).files.length > 0) {
                const formData = new FormData()
                const file = (this.$refs.pic_input as any).files[0]
                formData.append('pic', file)
                formData.append('title', this.form.title)
                formData.append('description', this.form.description)
                const ret = await this.addPic(postPicApi, formData)
                if (ret) {
                    await this.getData()
                    this.$Notice.success({title: '新增图片成功'})
                } else {
                    this.$Notice.error({title: '新增图片失败'})
                }
            }
        }

        // onCancel() {
        //     (this.$refs.addPicForm as any).resetFields()
        // }

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
            const ret = await this.deleteData(deletePicApi, id)
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
    .upload
        p
            padding 15px 0 0 0
</style>
