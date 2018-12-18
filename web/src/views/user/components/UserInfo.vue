<template>
    <Row>
        <Col span="24" class="userinfo-item"><span class="userinfo-item-key">头像：</span><span class="userinfo-item-value"><Avatar class="avator-circle" :src="userInfo.head_img" size="large"/></span></Col>
        <Col span="24" class="userinfo-item"><span class="userinfo-item-key">昵称：</span><span class="userinfo-item-value">{{ userInfo.nickname }}</span></Col>
        <Col span="24" class="userinfo-item"><span class="userinfo-item-key">性别：</span><span class="userinfo-item-value">{{ userInfo.gender | formatGender }}</span></Col>
        <Col span="24" class="userinfo-item"><span class="userinfo-item-key">手机号：</span><span class="userinfo-item-value">{{ userInfo.phone }}</span></Col>
        <Col span="24" class="userinfo-item"><span class="userinfo-item-key">邮箱：</span><span class="userinfo-item-value">{{ userInfo.email }}</span></Col>
        <Col span="24" class="userinfo-item"><span class="userinfo-item-key">身份：</span><span class="userinfo-item-value">{{ userInfo.role_name }}</span></Col>
    </Row>
</template>

<script lang="ts">
    import { Component, Vue } from 'vue-property-decorator'
    import { State } from 'vuex-class'

    @Component({
        filters: {
            formatGender: (gender: string): string => {
                switch (gender) {
                    case 'male':
                        return '男'
                    case 'female':
                        return '女'
                    default:
                        return '未知'
                }
            }
        }
    })
    export default class UserInfo extends Vue {
        @State userInfo: object

    }
</script>

<style lang="stylus" scoped>
    .userinfo-item
        font-size 16px
        padding 20px
        .userinfo-item-key
            color #17233d
            display inline-block
            width 80px
        .userinfo-item-value
            color #17233d
        .avator-circle
            width: 120px
            height: 120px
            line-height: 40px
            border-radius: 120px
</style>