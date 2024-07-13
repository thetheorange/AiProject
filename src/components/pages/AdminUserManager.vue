<template>
    <div style="width: 100%;">
        <!-- 控制面板 -->
        <div class="control-panner">
            <div class="search">
                <i class="el-icon-search"></i>
                <el-input v-model="keyword" size="small" placeholder="输入关键字搜索" />
            </div>
            <div class="gap-horizontal"></div>
            <el-button @click="addAdminDrawerShow = true" size="mini" type="success">添加管理员</el-button>
        </div>
        <!-- 添加管理员子界面 -->
        <el-drawer title="添加一个管理员" :visible.sync="addAdminDrawerShow" :before-close="handleDrawerClose" size="50%">
            <el-form :model="newAdminData" class="modify-admin-view">
                <el-divider content-position="left">管理员基本信息</el-divider>
                <el-form-item>
                    <el-row :gutter="5" type="flex" justify="space-between" align="middle">
                        <el-col>
                            <el-form-item prop="AdminName" :rules="[
                                { required: true, message: '管理员名字不能为空'}
                            ]">
                                <el-input v-model="newAdminData.AdminName" placeholder="管理员姓名" suffix-icon="el-icon-school"
                                    size="small"></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col>
                            <el-form-item prop="Auth" :rules="[
                                { required: true, message: '权限设置不能为空'}
                            ]">
                                <el-input v-model="newAdminData.Auth" placeholder="权限设置" suffix-icon="el-icon-message"
                                    size="small"></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>               
                    <div class="gap-vertical"></div>
                    <el-row :gutter="5" type="flex" justify="space-between" align="middle">
                        <el-col>
                            <el-form-item prop="PassWord" :rules="[
                                { required: true, message: '密码不能为空'}
                            ]">
                                <el-input v-model="newAdminData.PassWord" placeholder="管理员密码" show-password
                                    size="small"></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                </el-form-item>
                <!-- 提交操作 -->
                <el-form-item>
                    <el-button type="primary">提交</el-button>
                    <el-button type="danger">重置</el-button>
                </el-form-item>
            </el-form>
        </el-drawer>
        <!-- 修改管理员信息时的子界面 -->
        <el-drawer title="修改管理员信息" :visible.sync="modifyAdminDrawerShow" :before-close="handleDrawerClose" size="50%">
            <el-form :model="currentAdminData" class="modify-admin-view">
                <el-divider content-position="left">管理员基本信息</el-divider>
                <el-form-item>
                    <el-row :gutter="5" type="flex" justify="space-between" align="middle">
                        <el-col>
                            <el-form-item prop="AdminName" :rules="[
                                { required: true, message: '管理员名字不能为空'}
                            ]">
                                <el-input v-model="currentAdminData.AdminName" placeholder="管理员姓名" suffix-icon="el-icon-school"
                                    size="small"></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col>
                            <el-form-item prop="Auth" :rules="[
                                { required: true, message: '权限设置不能为空'}
                            ]">
                                <el-input v-model="currentAdminData.Auth" placeholder="权限设置" suffix-icon="el-icon-message"
                                    size="small"></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>               
                    <div class="gap-vertical"></div>
                    <el-row :gutter="5" type="flex" justify="space-between" align="middle">
                        <el-col>
                            <el-form-item prop="PassWord" :rules="[
                                { required: true, message: '密码不能为空'}
                            ]">
                                <el-input v-model="currentAdminData.PassWord" placeholder="管理员密码" show-password
                                    size="small"></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                </el-form-item>
                <!-- 提交操作 -->
                <el-form-item>
                    <el-button type="primary">提交</el-button>
                    <el-button type="danger">重置</el-button>
                </el-form-item>
            </el-form>
        </el-drawer>
        <!-- 管理员信息展示列表 -->
        <el-table :data="adminData" class="table" stripe>
            <el-table-column label="Id" prop="Id"></el-table-column>
            <el-table-column label="权限" prop="Auth">
                <template slot-scope="scope">
                    <el-tag :type="scope.row.Auth === 0 ? 'success' : 'danger'">
                        {{ Authorization(scope.row) }}
                    </el-tag>
                </template>
            </el-table-column>
            <el-table-column label="管理员" prop="AdminName"></el-table-column>
            <el-table-column label="密码" prop="PassWord"></el-table-column>
            <el-table-column label="操作">
                <template slot-scope="scope">
                    <el-button @click="modifyAdminData(scope.row)" size=small type="primary">修改</el-button>
                    <el-button size=small type="danger">删除</el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>

<script>
import { MessageBox } from 'element-ui';

export default {
    data() {
        return {
            adminData: [
                {
                    Id: "001",
                    Auth: 0,
                    AdminName: "admin_test",
                    PassWord: "1111"
                },
                {
                    Id: "002",
                    Auth: 1,
                    AdminName: "admin_test",
                    PassWord: "1111"
                },
                {
                    Id: "003",
                    Auth: 0,
                    AdminName: "admin_test",
                    PassWord: "1111"
                },
                {
                    Id: "004",
                    Auth: 0,
                    AdminName: "admin_test",
                    PassWord: "1111"
                },
            ],
            newAdminData: {
                Id: "",
                Auth: 0,
                AdminName: "",
                PassWord: ""
            },
            currentAdminData: {
                Id: "",
                Auth: 0,
                AdminName: "",
                PassWord: ""
            },
            keyword: "",
            addAdminDrawerShow: false,
            modifyAdminDrawerShow: false
        }
    },
    methods: {
        handleDrawerClose(done) {
            MessageBox.confirm("已填入的数据不会保存 确认关闭？")
                // eslint-disable-next-line
                .then(_=> done())
                // eslint-disable-next-line
                .catch(_=> { })
        },
        Authorization(SingleAdminData){
            return SingleAdminData.Auth === 0 ? "普通管理员" : "超级管理员";
        },
        modifyAdminData(adminData) {
            this.modifyAdminDrawerShow = true;
            this.currentAdminData = {...adminData};
        }
    }
}
</script>

<style scoped>
/* 头部控制台 */
.control-panner {
    display: flex;
    justify-content: end;
    align-items: center;
}
.modify-admin-view {
    width: 100%;
    height: 100%;
    padding: 1em;
}
</style>