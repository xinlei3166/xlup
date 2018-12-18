<template>
    <Row>
        <Col span="24" class="userinfo-item"><span class="userinfo-item-key">AccessKeyID：</span><span class="userinfo-item-value">{{ accessKey.access_key_id }}</span></Col>
        <Col span="24" class="userinfo-item"><span class="userinfo-item-key">AccessKeySecret：</span><span class="userinfo-item-value">{{ accessKey.access_key_secret }}</span></Col>
    </Row>
</template>

<script lang="ts">
    import { Component, Vue } from 'vue-property-decorator'
    import { checkToken } from '@/utils/decorators'
    import { getUserMeAccessKeyApi, postUserMeAccessKeyApi } from '@/api/user'

    @Component
    export default class UserAccessKey extends Vue {
        accessKey = {}

        async mounted() {
            this.accessKey = await this.getAccessKey()
        }

        async getAccessKey() {
            const data = await this._getAccessKey(getUserMeAccessKeyApi)
            if (data) {
                return data
            } else {
                this.$Notice.error({
                    title: '获取访问秘钥失败，请稍后重试。'
                })
                return
            }
        }

        @checkToken()
        async _getAccessKey(...args) {
            const data = args[0]
            switch (data.code) {
                case 'Success':
                    return data.data
                case 'AccessKeyNotExist':
                    return await this._postAccessKey(postUserMeAccessKeyApi)
                default:
                    return
            }
        }

        @checkToken()
        async _postAccessKey(...args) {
            const data = args[0]
            switch (data.code) {
                case 'Success':
                    return data.data
                default:
                    return
            }
        }
    }
</script>

<style lang="stylus" scoped>
    .userinfo-item
        font-size 16px
        padding 20px
        .userinfo-item-key
            color #17233d
        .userinfo-item-value
            color #17233d
            margin-left 16px
</style>