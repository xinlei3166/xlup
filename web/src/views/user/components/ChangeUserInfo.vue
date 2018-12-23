<template>
    <Form ref="changeUserInfoForm" :model="form" :rules="rules" :label-width="100" style="margin-top: 16px">
        <FormItem prop="nickname" label="昵称">
            <Input v-model="form.nickname" placeholder="请输入昵称" style="width: 260px"></Input>
        </FormItem>
        <FormItem prop="gender" label="性别">
            <RadioGroup v-model="form.gender">
                <Radio label="male">男</Radio>
                <Radio label="female">女</Radio>
            </RadioGroup>
        </FormItem>
        <FormItem prop="phone" label="手机号">
            <Input v-model="form.phone" placeholder="请输入手机号" style="width: 260px"></Input>
        </FormItem>
        <FormItem prop="email" label="邮箱">
            <Input v-model="form.email" placeholder="请输入邮箱" style="width: 260px"></Input>
        </FormItem>
        <FormItem>
            <Button type="warning" size="default" @click="onReset" >重置</Button>
            <Button class="form-btn" type="primary" size="default" @click="onSubmit">提交</Button>
        </FormItem>
    </Form>
</template>

<script lang="ts">
    import { Component, Vue } from 'vue-property-decorator'
    import { checkToken } from "@/utils/decorators"
    import { getUserMeApi, patchUserMeApi } from "@/api/user"
    import { setUserInfo } from "@/utils/user"

    @Component
    export default class ChangeUserInfo extends Vue {

        form = {
            nickname: this.$store.state.userInfo.nickname,
            gender: this.$store.state.userInfo.gender,
            phone: this.$store.state.userInfo.phone,
            email: this.$store.state.userInfo.email
        }

        rules = {
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

        @checkToken()
        async changeUserInfo(...args): Promise<boolean> {
            const data = args[0]
            switch (data.code) {
                case 'Success':
                    this.$Notice.success({title: '信息修改成功'})
                    return true
                case 'InvalidNickname':
                    this.$Notice.warning({title: '不合法的昵称'})
                    break
                case 'InvalidGender':
                    this.$Notice.warning({title: '不合法的性别'})
                    break
                case 'InvalidPhone':
                    this.$Notice.warning({title: '不合法的手机号'})
                    break
                case 'PhoneExist':
                    this.$Notice.warning({title: '手机号已被使用'})
                    break
                case 'InvalidEmail':
                    this.$Notice.warning({title: '不合法的邮箱'})
                    break
                case 'EmailExist':
                    this.$Notice.warning({title: '邮箱已被使用'})
                    break
                default:
                    this.$Notice.error({title: '信息修改失败'})
                    break
            }
        }

        @checkToken()
        async _getUserInfo(...args): Promise<any> {
            const data = args[0]
            switch (data.code) {
                case 'Success':
                    return data.data
                default:
                    return
            }
        }

        async _setUserInfo(): Promise<void> {
            const userInfo = await this._getUserInfo(getUserMeApi)
            if (userInfo) {
                setUserInfo(userInfo)
            }
        }

        async onSubmit(): Promise<void> {
            (this.$refs.changeUserInfoForm as any).validate(async (valid: any): Promise<void> => {
                if (valid) {
                    const ret = await this.changeUserInfo(patchUserMeApi, this.form)
                    if (ret) {
                        await this._setUserInfo()
                    }
                }
            })
        }

        onReset(): void {
            (this.$refs.changeUserInfoForm as any).resetFields()
        }
    }

</script>

<style lang="stylus" scoped>
    >>> .ivu-form-item
        label
            font-size 15px
            color: #17233d
        .form-btn
            margin-left 50px
</style>