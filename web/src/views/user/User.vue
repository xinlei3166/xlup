<template>
    <Card>
        <Tabs value="userInfo">
            <TabPane label="个人信息" name="userInfo">
                <UserInfo/>
            </TabPane>
            <!--<TabPane label="修改基本信息" name="changeUserInfo">标签二的内容</TabPane>-->
            <!--<TabPane label="修改密码" name="changePassword">标签三的内容</TabPane>-->
            <!--<TabPane label="修改头像" name="changeHeadimg">标签三的内容</TabPane>-->
            <TabPane label="秘钥管理" name="accessSecret">
                <UserAccessKey/>
            </TabPane>
        </Tabs>
    </Card>
</template>

<script lang="ts">
    import { Component, Vue } from 'vue-property-decorator'
    import UserInfo from './components/UserInfo.vue'
    import UserAccessKey from './components/UserAccessKey.vue'

    @Component({
        components: {
            UserInfo,
            UserAccessKey
        }
    })
    export default class User extends Vue {

    }
</script>

<style lang="stylus" scoped>
    >>> .ivu-tabs-tab
        font-weight bold
</style>