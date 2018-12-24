<template>
    <div>
        <Card>
            <div class="search-con">
                <Input v-model="q" search placeholder="输入关键字搜索" @on-search="onSearch" class="search-input"/>
                <Button class="search-btn" type="primary" @click="onAll">全部</Button>
                <Button class="search-btn-right" type="primary" @click="addUserModal=true">新增用户</Button>
                <Modal
                        title="新增用户"
                        v-model="addUserModal"
                        :mask-closable="false"
                        @on-ok="onAddUser"
                        @on-cancel="onCancel">
                    <Form ref="addUserForm" :model="form" :rules="rules" :label-width="100" style="margin-top: 16px">
                        <FormItem prop="username" label="用户名">
                            <Input type="text" v-model="form.username" placeholder="请输入用户名"
                                   style="width: 320px"></Input>
                        </FormItem>
                        <FormItem prop="password" label="密码">
                            <Input type="password" v-model="form.password" placeholder="请输入密码"
                                   style="width: 320px"></Input>
                        </FormItem>
                        <FormItem prop="nickname" label="昵称">
                            <Input v-model="form.nickname" placeholder="请输入昵称" style="width: 320px"></Input>
                        </FormItem>
                        <FormItem prop="gender" label="性别">
                            <RadioGroup v-model="form.gender">
                                <Radio label="male">男</Radio>
                                <Radio label="female">女</Radio>
                            </RadioGroup>
                        </FormItem>
                        <FormItem prop="phone" label="手机号">
                            <Input v-model="form.phone" placeholder="请输入手机号" style="width: 320px"></Input>
                        </FormItem>
                        <FormItem prop="email" label="邮箱">
                            <Input v-model="form.email" placeholder="请输入邮箱" style="width: 320px"></Input>
                        </FormItem>
                    </Form>
                </Modal>
            </div>
            <MyTable ref="table" :height="tableHeight" :columns="columns" :data="data"></MyTable>
        </Card>
        <Paginator ref="paginator" :total="total" :currentPage="currentPage" :pageSize="pageSize" :onChange="onChange"
                   :onPageSizeChange="onPageSizeChange"></Paginator>
    </div>
</template>

<script lang="ts">
    import { Component, Vue, Watch } from "vue-property-decorator"
    import MyTable from "@/components/MyTable.vue"
    import Paginator from "@/components/Paginator.vue"
    import { checkToken } from "@/utils/decorators"
    import { tooltip, stripSpaceCharacter } from "@/utils/util"
    import { getUserAdminApi, postUserAdminApi, patchUserDetailsAdminApi, deleteUserDetailsAdminApi } from "@/api/user"


    @Component({
        components: {MyTable, Paginator}
    })
    export default class UserAdmin extends Vue {
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
                title: "用户名",
                key: "username",
            },
            {
                title: "昵称",
                key: "nickname",
            },
            {
                title: "性别",
                key: "gender",
                render: (h, params) => {
                    return h("span", this.formatGender(params.row.gender))
                }
            },
            {
                title: "邮箱",
                key: "email",
                render: (h, params) => {
                    return tooltip(h, params.row.email)
                }
            },
            {
                title: "手机号",
                key: "phone",
            },
            {
                title: "创建时间",
                key: "create_time",
                // ellipsis: true,
                // tooltip: true
                render: (h, params) => {
                    return tooltip(h, params.row.create_time, 16)
                }
            },
            {
                title: "功能",
                key: "action",
                width: 150,
                align: "center",
                render: (h: any, params: any) => {
                    return h("div", [
                        h("Button", {
                            props: {
                                type: "warning",
                                size: "small"
                            },
                            style: {
                                marginRight: "5px"
                            },
                            on: {
                                click: () => {
                                    this.onChangePassword(h, params.row.nickname, params.row.id)
                                },
                            }
                        }, "密码"),
                        h("Poptip", {
                            props: {
                                confirm: true,
                                transfer: true,
                                placement: "top",
                                title: "您确认删除这条内容吗？",
                                onText: "确定",
                                canceltext: "取消",
                                type: "error",
                                size: "small",
                            },
                            style: {
                                marginRight: "5px"
                            },
                            on: {
                                "on-ok": () => {
                                    this.onRemove(params.row.id)
                                },
                            }
                        }, [
                            h("Button", {
                                props: {
                                    type: "error",
                                    size: "small"
                                }
                            }, "删除")
                        ])
                    ]);
                }
            }
        ]

        addUserModal = false

        form = {
            username: "",
            password: "",
            nickname: "",
            gender: "female",
            phone: "",
            email: ""
        }

        rules = {
            username: [
                {required: true, message: "用户名不能为空", trigger: "blur"},
                {type: "string", min: 2, max: 20, message: "用户名最小长度为2, 最大长度为20", trigger: "blur"}
            ],
            password: [
                {required: true, message: "密码不能为空", trigger: "blur"},
                {type: "string", min: 6, max: 20, message: "密码最小长度为6, 最大长度为20", trigger: "blur"},
            ],
            nickname: [
                {required: true, message: "昵称不能为空", trigger: "blur"},
                {type: "string", min: 2, max: 32, message: "密码最小长度为2, 最大长度为32", trigger: "blur"},
            ],
            gender: [
                {required: true, message: "性别不能为空", trigger: "blur"},
            ],
            phone: [
                {
                    validator: (rule, value, callback) => {
                        if (value !== "") {
                            const reg = /^1[356789]\d{9}/
                            if (!reg.test(value)) {
                                callback(new Error("请输入11位合法手机号"));
                            }
                            callback()
                        } else {
                            callback();
                        }
                    },
                    trigger: "blur"
                }
            ],
            email: [
                {
                    validator: (rule, value, callback) => {
                        if (value !== "") {
                            const reg = /[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/
                            if (!reg.test(value)) {
                                callback(new Error("请输入正确的邮箱地址"));
                            }
                            callback()
                        } else {
                            callback();
                        }
                    },
                    trigger: "blur"
                }
            ]
        }

        newPassword = ''

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
            const data = await this._getData(getUserAdminApi, params)
            if (data) {
                this.data = data.data
                this.total = data.total
            } else {
                this.$Notice.error({"title": "获取数据失败"})
            }
        }

        @checkToken()
        async _getData(...args): Promise<any> {
            const data = args[0]
            switch (data.code) {
                case "Success":
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

        @checkToken()
        async addUser(...args) {
            const data = args[0]
            switch (data.code) {
                case "Success":
                    return true
                default:
                    return false
            }
        }

        onAddUser(): void {
            (this.$refs.addUserForm as any).validate(async (valid: any): Promise<void> => {
                if (valid) {
                    const ret = await this.addUser(postUserAdminApi, this.form)
                    if (ret) {
                        (this.$refs.addUserForm as any).resetFields()
                        await this.getData()
                        this.$Notice.success({"title": "新增用户成功"})
                    } else {
                        this.$Notice.error({"title": "新增用户失败"})
                    }
                }
            })
        }

        onCancel() {
            (this.$refs.addUserForm as any).resetFields()
        }

        formatGender(gender: string): string {
            switch (gender) {
                case "male":
                    return "男"
                case "female":
                    return "女"
                default:
                    return "未知"
            }
        }

        @checkToken()
        async changePassword(...args): Promise<boolean> {
            const data = args[0]
            switch (data.code) {
                case "Success":
                    return true
                default:
                    return false
            }
        }

        onChangePassword(h: any, nickname: string, user_id: number) {
            this.$Modal.confirm({
                title: `正在为${nickname}重置密码`,
                width: 360,
                onOk: async (): Promise<void> => {
                    const data = {'password': this.newPassword}
                    const ret = await this.changePassword(patchUserDetailsAdminApi, user_id, data)
                    if (ret) {
                        this.$Notice.success({title: '重置密码成功'})
                    } else {
                        this.$Notice.error({title: '重置密码失败'})
                    }
                },
                onCancel: () => {
                    this.newPassword = ''
                },
                render: () => {
                    return h("Input", {
                        props: {
                            size: "large",
                            type: "password",
                            maxlength: 20,
                            autofocus: true,
                            clearable: true,
                            placeholder: "请输入新密码"
                        },
                        style: {
                            marginTop: "10px",
                        },
                        on: {
                            'on-blur': (event: any): void => {
                                this.newPassword = event.target.value
                            }
                        }
                    })
                }
            })
        }

        @checkToken()
        async deleteData(...args): Promise<boolean> {
            const data = args[0]
            switch (data.code) {
                case "Success":
                    return true
                default:
                    return false
            }
        }

        async onRemove(id: number): Promise<void> {
            const ret = await this.deleteData(deleteUserDetailsAdminApi, id)
            if (ret) {
                await this.getData()
                this.$Notice.success({"title": "删除成功"})
            } else {
                this.$Notice.error({"title": "删除失败"})
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

        @Watch("data")
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
