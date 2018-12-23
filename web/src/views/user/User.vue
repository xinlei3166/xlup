<template>
    <Card>
        <Tabs value="userInfo">
            <TabPane label="个人信息" name="userInfo"><UserInfo/></TabPane>
            <TabPane label="修改基本信息" name="changeUserInfo"><ChangeUserInfo/></TabPane>
            <TabPane label="修改密码" name="changePassword"><ChangePassword/></TabPane>
            <TabPane label="修改头像" name="changeHeadimg"><ChangeHeadimg/></TabPane>
            <TabPane label="秘钥管理" name="accessSecret"><UserAccessKey/></TabPane>
        </Tabs>
    </Card>
</template>

<script lang="ts">
    import { Component, Vue } from 'vue-property-decorator'
    import UserInfo from './components/UserInfo.vue'
    import UserAccessKey from './components/UserAccessKey.vue'
    import ChangeUserInfo from './components/ChangeUserInfo.vue'
    import ChangePassword from './components/ChangePassword.vue'
    import ChangeHeadimg from './components/ChangeHeadimg.vue'

    @Component({
        components: {
            UserInfo,
            UserAccessKey,
            ChangeUserInfo,
            ChangePassword,
            ChangeHeadimg
        }
    })
    export default class User extends Vue {

    }
</script>

<style lang="stylus" scoped>
    >>> .ivu-tabs-tab
        font-weight bold
</style>