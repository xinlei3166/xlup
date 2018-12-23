<template>
    <Form ref="changePasswordForm" :model="form" :rules="rules" :label-width="100" style="margin-top: 16px">
        <FormItem prop="oldPassword" label="原密码: ">
            <Input type="password" v-model="form.oldPassword" placeholder="请输入原密码" style="width: 260px"></Input>
        </FormItem>
        <FormItem prop="newPassword" label="新密码: ">
            <Input type="password" v-model="form.newPassword" placeholder="请输入新密码" style="width: 260px"></Input>
        </FormItem>
        <FormItem prop="confirmPassword" label="确认密码: ">
            <Input type="password" v-model="form.confirmPassword" placeholder="再次输入新密码" style="width: 260px"></Input>
        </FormItem>
        <FormItem>
            <Button type="warning" @click="onReset">清空</Button>
            <Button type="primary" @click="onSubmit" style="margin-left: 50px">修改</Button>
        </FormItem>
    </Form>
</template>

<script lang="ts">
    import { Component, Vue } from 'vue-property-decorator'
    import { checkToken } from "@/utils/decorators"
    import { putUserMePasswordApi } from "@/api/user"

    @Component
    export default class ChangePassword extends Vue {

        form = {
            oldPassword: '',
            newPassword: '',
            confirmPassword: ''
        }

        rules = {
            oldPassword: [
                {required: true, message: "原密码不能为空", trigger: "blur"},
                {type: "string", min: 6, max: 20, message: "密码最小长度为6, 最大长度为20", trigger: "blur"},
            ],
            newPassword: [
                {required: true, message: "新密码不能为空", trigger: "blur"},
                {type: "string", min: 6, max: 20, message: "密码最小长度为6, 最大长度为20", trigger: "blur"},
                {
                    validator: (rule, value, callback) => {
                        if (value === '') {
                            callback(new Error('新密码不能为空'));
                        } else {
                            if (this.form.confirmPassword !== '') {
                                // 对第二个密码框单独验证
                                (this.$refs.changePasswordForm as any).validateField('confirmPassword')
                            }
                            callback()
                        }
                    },
                    trigger: "blur"
                }
            ],
            confirmPassword: [
                {required: true, message: "确认密码不能为空", trigger: "blur"},
                {type: "string", min: 6, max: 20, message: "密码最小长度为6, 最大长度为20", trigger: "blur"},
                {
                    validator: (rule, value, callback) => {
                        if (value === '') {
                            callback(new Error('确认密码不能为空'));
                        } else if (value !== this.form.newPassword) {
                            callback(new Error('两次新密码输入不一致'));
                        } else {
                            callback();
                        }
                    },
                    trigger: "blur"
                }
            ]
        }

        @checkToken()
        async changePassword(...args): Promise<any> {
            const data = args[0]
            switch (data.code) {
                case 'Success':
                    this.$Notice.success({title: '密码修改成功'})
                    break
                case 'IncorrectOldPassword':
                    this.$Notice.error({title: '原密码不正确'})
                    break
                default:
                    this.$Notice.error({title: '密码修改失败'})
                    break
            }
        }

        async onSubmit(): Promise<void> {
            (this.$refs.changePasswordForm as any).validate(async (valid: any): Promise<void> => {
                if (valid) {
                    const data = {old_password: this.form.oldPassword, new_password: this.form.newPassword}
                    await this.changePassword(putUserMePasswordApi, data)
                }
            })
        }

        onReset(): void {
            (this.$refs.changePasswordForm as any).resetFields()
        }
    }

</script>

<style lang="stylus" scoped>
    >>> .ivu-form-item
        label
            font-size 15px
            color: #17233d
</style>