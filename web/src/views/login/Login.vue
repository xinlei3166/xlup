<template>
    <div class="login">
        <div class="login-content">
            <Card title="欢迎登录" :bordered="false">
                <div class="form-content">
                    <Form ref="loginForm" :model="form" :rules="rules">
                        <FormItem prop="username">
                            <Input type="text" v-model="form.username" clearable>
                                <Icon type="ios-person" slot="prepend"></Icon>
                            </Input>
                        </FormItem>
                        <FormItem prop="password">
                            <Input type="password" v-model="form.password" clearable>
                                <Icon type="md-lock" slot="prepend"></Icon>
                            </Input>
                        </FormItem>
                        <FormItem>
                            <Button type="primary" long @click="onSubmit">登录</Button>
                        </FormItem>
                    </Form>
                    <p class="login-tip">账号获取，请联系我们</p>
                </div>
            </Card>
        </div>
    </div>
</template>

<script lang="ts">
    import { Component, Vue, Prop } from "vue-property-decorator"
    import { loginApi, getUserMeApi } from "@/api/user"
    import { setToken } from "@/utils/token"
    import { setUserInfo } from "@/utils/user"
    import { checkToken } from '@/utils/decorators'

    @Component
    export default class Login extends Vue {

        form = {
            username: "",
            password: "",
        }

        rules = {
            username: [
                {required: true, message: "用户名不能为空", trigger: "blur"},
                {type: "string", min: 2, message: "用户名无效", trigger: "blur"}
            ],
            password: [
                {required: true, message: "密码不能为空", trigger: "blur"},
                {type: "string", min: 6, message: "密码最少6位", trigger: "blur"}
            ]
        }

        validatePassword(rule, value, callback) {
            if (value === "") {
                callback(new Error("Please enter your password"));
            } else {
                if (this.form.password !== "") {
                    // 对第二个密码框单独验证
                    console.log(this.$refs.loginForm);
                }
                callback();
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

        async _login(): Promise<void> {
            const ret = await loginApi(this.form)
            if (ret) {
                switch (ret.code) {
                    case "Success":
                        setToken(ret.data)
                        const userInfo = await this._getUserInfo(getUserMeApi)
                        if (userInfo) {
                            setUserInfo(userInfo)
                            this.$Message.success("登录成功")
                            this.$router.push('/home')
                        } else {
                            this.$Message.error("获取用户信息失败")
                        }
                        break
                    case "InvalidParams":
                        this.$Message.error("用户名或密码不能为空")
                        break
                    case "UsernameNotExist":
                        this.$Message.error("用户名无效")
                        break
                    case "IncorrectPassword":
                        this.$Message.error("密码错误")
                        break
                    default:
                        this.$Message.error("未知错误")
                }
            }
        }

        onSubmit(): void {
            (this.$refs.loginForm as any).validate(async (valid: any): Promise<void> => {
                if (valid) {
                    await this._login()
                }
            })
        }
    }
</script>

<style lang="stylus" scoped>
    .login
        width: 100%
        height: 100%
        background-image: url('../../assets/images/logo-bg.jpeg')
        background-size: cover
        background-position: center
        position: relative

        &-content
            position: absolute
            right: 50%
            top: 50%
            margin 0 -180px
            transform: translateY(-60%)
            width: 360px

            >>> .ivu-card
                background: rgba(0, 0, 0, .3);

                span
                    color: #fff;

        &-header
            font-size: 16px
            font-weight: 300
            text-align: center
            padding: 30px 0

        .form-content
            padding: 10px 0 0

        .login-tip
            font-size: 10px
            text-align: center
            color: #c3c3c3
</style>
