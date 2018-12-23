<template>
    <div>
        <form ref="changeHeadimgForm">
            <div class="upload">
                <input ref="head_img_input" class="upload-input" type="file" name="head_img" @change="changeImage($event)"></input>
                <img v-if="headimg !== ''" class="upload-img" :src="headimg" alt="headimg">
                <div v-else class="upload-icon">
                    <Icon type="ios-cloud-upload" size="52" style="color: #3399ff"></Icon>
                    <p>上传图片</p>
                </div>
            </div>
            <Button class="upload-btn" type="primary" size="default" @click="onSubmit" long>确认修改</Button>
        </form>
    </div>
</template>

<script lang="ts">
    import { Component, Vue } from "vue-property-decorator"
    import { checkToken } from '@/utils/decorators'
    import { getUserMeApi, postUserMeHeadimgApi } from '@/api/user'
    import { setUserInfo } from "@/utils/user"


    @Component
    export default class ChangeHeadimg extends Vue {
        headimg = ''

        changeImage(e) {
            const file = e.target.files[0]
            const reader = new FileReader()
            const self = this
            reader.readAsDataURL(file)
            reader.onload = function (e) {
                self.headimg = (this as any).result
            }
        }

        @checkToken()
        async changeHeadimg(...args): Promise<boolean> {
            const data = args[0]
            switch (data.code) {
                case 'Success':
                    return true
                default:
                    return false
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

        async onSubmit() {
            if ((this.$refs.head_img_input as any).files.length > 0) {
                const head_img = new FormData()
                const file = (this.$refs.head_img_input as any).files[0]
                head_img.append('head_img', file)
                const ret = await this.changeHeadimg(postUserMeHeadimgApi, head_img)
                if (ret) {
                    await this._setUserInfo()
                    this.$Notice.success({title: '头像修改成功'})
                } else {
                    this.$Notice.error({title: '头像修改失败'})
                }
            }
        }
    }
</script>

<style lang="stylus" scoped>
    .upload
        margin-left 20px
        width 200px
        height 200px
        border 1px dashed #dcdee2
        display flex
        align-items center
        justify-content center
        position: relative
        &-input
            width 100%
            height 100%
            position: absolute
            left: 0
            top: 0
            opacity: 0
        &-img
            width 100%
            height 100%
        &-icon
            text-align: center

    .upload-btn
        width 200px
        margin 20px 20px
</style>