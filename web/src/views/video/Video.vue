<template>
    <div>
        <Card>
            <div class="search-con">
                <Input v-model="q" search placeholder="输入关键字搜索" @on-search="onSearch" class="search-input"/>
                <Button class="search-btn" type="primary" @click="onAll">全部</Button>
                <Button class="search-btn-right" type="primary" @click="addVideoModal=true">新增视频</Button>
                <Modal
                        title="新增视频"
                        v-model="addVideoModal"
                        :mask-closable="false"
                        @on-ok="onAddVideo">
                    <Form ref="addVideoForm" :model="form" :rules="rules" :label-width="100" style="margin-top: 16px">
                        <FormItem prop="pic" label="图片">
                            <div class="upload">
                                <input ref="pic_input" type="file" name="pic" @change="changePic($event)"></input>
                                <p>
                                    <img v-if="previewPic !== ''" :src="previewPic" alt="pic" style="width: 100px">
                                </p>
                            </div>
                        </FormItem>
                        <FormItem prop="video" label="视频">
                            <div class="upload">
                                <input ref="video_input" type="file" name="video" @change="changeVideo($event)"></input>
                                <p>
                                    <video v-if="previewVideo !== ''" :src="previewVideo" style="width: 360px" controls></video>
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
    import { getUploadPolicy } from "@/api/user"
    import { getVideoApi, postVideoApi, deleteVideoApi } from "@/api/video"
    import { tooltip, stripSpaceCharacter } from "@/utils/util"

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

        addVideoModal = false
        previewPic = ''
        previewVideo = ''

        form = {
            title: '',
            description: ''
        }

        policy = null

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
            const data = await this._getData(getVideoApi, params)
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

        changeVideo(e) {
            const file = e.target.files[0]
            const reader = new FileReader()
            const self = this
            reader.readAsDataURL(file)
            reader.onload = function (e) {
                self.previewVideo = (this as any).result
            }
        }

        @checkToken()
        async getPolicy(...args) {
            const data = args[0]
            switch (data.code) {
                case 'Success':
                    return data
                default:
                    return
            }
        }

        @checkToken()
        async addVideo(...args) {
            const data = args[0]
            switch (data.code) {
                case 'Success':
                    return data
                default:
                    return
            }
        }

        async onAddVideo() {
            if (this.policy === null){
                const policy = await this.getPolicy(getUploadPolicy)
                if (policy) {
                    this.policy = policy.data
                } else {
                    this.$Notice.error({title: '请在个人信息页面设置Access_key'})
                }
            }
            if ((this.$refs.pic_input as any).files.length > 0 && (this.$refs.video_input as any).files.length > 0) {
                const formData = new FormData()
                const pic = (this.$refs.pic_input as any).files[0]
                const video = (this.$refs.video_input as any).files[0]
                formData.append('pic', pic)
                formData.append('video', video)
                formData.append('title', this.form.title)
                formData.append('description', this.form.description)
                formData.append('access_key_id', this.policy.access_key_id)
                formData.append('policy', this.policy.policy)
                formData.append('sign', this.policy.sign)
                const ret = await this.addVideo(postVideoApi, formData)
                if (ret) {
                    await this.getData()
                    this.$Notice.success({title: '新增视频成功'})
                } else {
                    this.$Notice.error({title: '新增视频失败'})
                }
            } else {
                this.$Notice.warning({title: '图片和视频不存在'})
            }
        }

        showVideo(title: string, path: string): void {
            this.$Modal.info({
                closable: true,
                width: '800px',
                title: title,
                content: `<div style="width: 100%;padding: 12px 20px 0 20px"><video src="${path}" controls></div>`,
                okText: '关闭',
                onOk: () => {
                    this.$Modal.remove()
                }
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
