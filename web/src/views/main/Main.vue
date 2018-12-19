<template>
    <Layout class="layout">
        <Sider class="layout-sider" ref="side" hide-trigger collapsible :collapsed-width="78" v-model="isCollapsed">
            <div class="layout-logo">
                <router-link to="/">
                    <h1 v-if="!isCollapsed">仙灵小屋</h1>
                    <img v-else src="../../assets/images/logo.png" alt="logo"/>
                </router-link>
            </div>
            <Menu mode="vertical" active-name="home" theme="dark" width="auto" accordion
                  :class="menuitemClasses">
                <MenuItem name="home" :style="{display: 'none'}" :to="{name: 'home'}">
                    <Icon type="ios-people" :style="{marginTop: '-3px'}"></Icon>
                    <span :style="{marginLeft: '5px'}">首页</span>
                </MenuItem>
                <template v-if="isCollapsed">
                    <template v-for="item in slideMenus">
                        <MenuItem v-if="!item.meta.hidden && checkPermission(item.meta.permission)" :name="item.name">
                            <Dropdown placement="right-start">
                                <Icon class="layout-meun-icon" :type="item.meta.icon"></Icon>
                                <DropdownMenu slot="list" v-for="child in item.children" :key="child.name">
                                    <router-link v-if="!child.meta.hidden && checkPermission(child.meta.permission)" :to="`${item.path}${child.path !== '' ? '/' + child.path : ''}`" exact
                                                 style="text-decoration: none; color: inherit;">
                                        <DropdownItem>
                                            {{ child.meta.title }}
                                        </DropdownItem>
                                    </router-link>
                                </DropdownMenu>
                            </Dropdown>
                        </MenuItem>
                    </template>
                </template>
                <template v-else>
                    <template v-for="item in slideMenus">
                        <Submenu v-if="!item.meta.hidden && checkPermission(item.meta.permission)" :name="item.meta.title">
                            <template slot="title">
                                <Icon class="layout-meun-icon" :type="item.meta.icon"
                                      :style="{marginTop: '-2.5px'}" size="17"></Icon>
                                {{ item.meta.title }}
                            </template>
                            <template v-for="child in item.children">
                                <MenuItem v-if="!child.meta.hidden && checkPermission(child.meta.permission)" :name="child.name"
                                          :to="`${item.path}${child.path !== '' ? '/' + child.path : ''}`" exact
                                          :style="{}">
                                    <Icon class="layout-meun-icon" :type="child.meta.icon"
                                          :style="{marginTop: '-3.0px'}" size="17"></Icon>
                                    {{ child.meta.title }}
                                </MenuItem>
                            </template>
                        </Submenu>
                    </template>
                </template>
            </Menu>
        </Sider>
        <Layout>
            <Header :style="{padding: 0, marginLeft: '0.75px'}" class="layout-header">
                <Icon @click.native="collapsedSider" :class="rotateIcon" :style="{margin: '0 20px'}" type="md-menu"
                      color="#fff" size="24"></Icon>
                <div class="head-bar-content" :style="{float: 'right', paddingRight: '50px'}">
                    <Badge :count="1" type="error" :offset="[13, 0]" :style="{top: '3px', marginRight: '30px'}">
                        <Icon type="ios-notifications-outline" color="white" size="28"></Icon>
                    </Badge>
                    <div class="user-avator-dropdown" :style="{float: 'right'}">
                        <Avatar :src="userInfo.head_img"/>
                        <Dropdown style="margin-left: 3px">
                            <a href="javascript:void(0)">
                                <span :style="{marginLeft: '1px', color: '#fff'}">{{ `${userInfo ? userInfo.nickname : ''}` }}</span>
                                <Icon type="md-arrow-dropdown" :style="{fontSize: '18px', color: '#fff'}"></Icon>
                            </a>
                            <DropdownMenu slot="list">
                                <router-link :to="{name: 'userMe'}" exact>
                                    <DropdownItem>个人信息</DropdownItem>
                                </router-link>
                                <DropdownItem>
                                    <span @click="onLogout">退出登录</span>
                                </DropdownItem>
                            </DropdownMenu>
                        </Dropdown>
                    </div>
                </div>
            </Header>
            <Content class="layout-content">
                <Layout class="layout-content-layout">
                    <Breadcrumb :style="{margin: '24px 0 18px 0'}">
                        <template v-for="item in $route.matched">
                            <BreadcrumbItem>{{ item.meta.title }}</BreadcrumbItem>
                        </template>
                    </Breadcrumb>
                    <Content class="layout-content-content">
                        <router-view/>
                    </Content>
                </Layout>
            </Content>
            <!--<Footer class="layout-footer">&copy; 2018 君惜. All Rights Reserved</Footer>-->
        </Layout>
    </Layout>
</template>

<script lang="ts">
    import { Component, Vue } from "vue-property-decorator";
    import { State } from "vuex-class"
    import { logoutApi } from "@/api/user"
    import { setToken } from "@/utils/token"
    import { checkPermission as _checkPermission } from "@/utils/user"

    // const someModule = namespace('path/to/module')

    @Component
    export default class Main extends Vue {
        isCollapsed = false

        @State slideMenus: object[]
        @State userInfo: object
        @State token: object

        get rotateIcon() {
            return [
                "menu-icon",
                this.isCollapsed ? "rotate-icon" : ""
            ];
        }

        get menuitemClasses() {
            return this.isCollapsed ? ["menu-item", this.isCollapsed ? "collapsed-menu" : ""] : []
        }

        checkPermission(item: boolean): boolean {
            return _checkPermission(item)
        }

        collapsedSider() {
            this.isCollapsed = !this.isCollapsed
        }

        async logout() {
            await logoutApi(this.token)
            setToken(null)
            this.$router.push('/login')
        }

        onLogout() {
            this.$Modal.confirm({
                title: '退出登录',
                content: '<p>确定要退出吗</p>',
                okText: '确定',
                cancelText: '取消',
                onOk: this.logout
            });
        }
    }
</script>

<style lang="stylus" scoped>
    bg-color = #001529
    menu-bg-color = #000c17

    .layout
        background: #f5f7f9;
        position: relative;
        overflow: hidden;
        height 100%

        .layout-sider
            height 100%
            background bg-color

            .ivu-menu-dark, .ivu-menu-vertical
                background bg-color

            .ivu-menu-opened
                >>> .ivu-menu-submenu-title
                    background bg-color!important
                    color #fff

                >>> .ivu-menu
                    background menu-bg-color


    .layout-logo
        width 100%
        height: 64px
        color: white
        background bg-color
        display flex
        align-items center
        justify-content center

        h1
            color #fff

        img
            height 48px

    .layout-meun
        margin-top 15px

    .ivu-menu-item
        a
            color rgba(255, 255, 255, .7)

            &:hover
                color #fff

        .ivu-dropdown
            width 100%

    .ivu-menu-item-active
        a
            color: #fff

    .menu-icon
        // transition: all .1s
    .rotate-icon
        transform: rotate(-90deg)

    .menu-item
        span
            display: inline-block
            overflow: hidden
            width: 69px
            text-overflow: ellipsis
            white-space: nowrap
            vertical-align: bottom

        // transition: width .1s ease .1s

        i
            // transform: translateX(0px)
            // transition: font-size .1s ease, transform .1s ease
            vertical-align: middle
            font-size: 16px

    .collapsed-menu
        span
            width: 0

        /*transition: width .1s ease*/

        i
            // transform: translateX(5px)
            // transition: font-size .1s ease .1s, transform .1s ease .1s
            vertical-align: middle;
            font-size: 21px;

    .layout-header
        background bg-color
        box-shadow: 0 1px 1px rgba(0, 0, 0, .1)

    .layout-content
        height calc(100% - 60px)
        overflow hidden
        padding 0 24px 0 24px

        .layout-content-layout
            height 100%
            overflow hidden

        .layout-content-content
            padding 5px 20px 20px 0
            height calc(100% - 80px)
            overflow auto
            &::-webkit-scrollbar
                display none

    .layout-footer
        margin-top 10px
        text-align center
</style>
