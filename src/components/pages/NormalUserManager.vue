<template>
    <div class="table-container">
        <!-- 控制面板 -->
        <div class="control-panner">
            <div class="search">
                <i class="el-icon-search"></i>
                <el-input v-model="keyword" size="small" placeholder="输入关键字搜索" />
            </div>
            <div class="gap-horizontal"></div>
            <el-button @click="addUserDrawerShow = true" size="mini" type="success">添加用户</el-button>
            <el-button size="mini" type="danger">批量删除</el-button>
        </div>
        <!-- 添加用户时的子界面 -->
        <el-drawer title="添加一个新用户" :visible.sync="addUserDrawerShow" :before-close="handleDrawerClose" size="50%">
            <el-form :model="newUserData" class="add-user-view">
                <!-- 用户基本信息 -->
                <el-divider content-position="left">用户基本信息</el-divider>
                <el-form-item class="base-info">
                    <el-row :gutter="5" type="flex" justify="space-between" align="middle">
                        <el-col>
                            <el-form-item prop="UserName" :rules="[
                                { required: true, message: '用户名不能为空' }
                            ]">
                                <el-input v-model="newUserData.UserName" placeholder="用户名" suffix-icon="el-icon-edit"
                                    size="small"></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col>
                            <el-form-item prop="PassWord" :rules="[
                                { required: true, message: '密码不能为空' }
                            ]">
                                <el-input v-model="newUserData.PassWord" placeholder="用户密码" show-password
                                    size="small"></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <div class="gap-vertical"></div>
                    <el-row :gutter="5" type="flex" justify="space-between" align="middle">
                        <el-col>
                            <el-form-item prop="Academy" :rules="[
                                { required: true, message: '学院不能为空' }
                            ]">
                                <el-input v-model="newUserData.Academy" placeholder="所属学院" suffix-icon="el-icon-school"
                                    size="small"></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col>
                            <el-form-item prop="Email" :rules="[
                                { required: true, message: '邮箱不能为空' }
                            ]">
                                <el-input v-model="newUserData.Email" placeholder="邮箱" suffix-icon="el-icon-message"
                                    size="small"></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                </el-form-item>
                <!-- 用户大模型的可使用量 -->
                <el-divider content-position="left">用户大模型的可使用量</el-divider>
                <el-form-item class="user-model-info">
                    <div>
                        <span class="second-text">文本大模型可使用token数</span>
                        <el-slider v-model="newUserData.Tokens" show-input :max="8192"></el-slider>
                    </div>
                    <div class="gap-vertical"></div>
                    <div>
                        <span class="second-text">用户可上传的图片数</span>
                        <el-slider v-model="newUserData.PicTimes" show-input :max="50"></el-slider>
                    </div>
                </el-form-item>
                <!-- 提交操作 -->
                <el-form-item>
                    <el-button type="primary">提交</el-button>
                    <el-button type="danger">重置</el-button>
                </el-form-item>
            </el-form>
        </el-drawer>
        <!-- 修改用户信息时的子界面 -->
        <el-drawer title="修改一个用户" :visible.sync="modifyUserDrawerShow" :before-close="handleDrawerClose" size="50%">
            <el-form :model="currentUserData" class="add-user-view">
                <!-- 用户基本信息 -->
                <el-divider content-position="left">用户基本信息</el-divider>
                <el-form-item class="base-info">
                    <el-row :gutter="5" type="flex" justify="space-between" align="middle">
                        <el-col>
                            <el-form-item prop="UserName" :rules="[
                                { required: true, message: '用户名不能为空' }
                            ]">
                                <el-input v-model="currentUserData.UserName" placeholder="用户名"
                                    suffix-icon="el-icon-edit" size="small"></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col>
                            <el-form-item prop="PassWord" :rules="[
                                { required: true, message: '密码不能为空' }
                            ]">
                                <el-input v-model="currentUserData.PassWord" placeholder="用户密码" show-password
                                    size="small"></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <div class="gap-vertical"></div>
                    <el-row :gutter="5" type="flex" justify="space-between" align="middle">
                        <el-col>
                            <el-form-item prop="Academy" :rules="[
                                { required: true, message: '学院不能为空' }
                            ]">
                                <el-input v-model="currentUserData.Academy" placeholder="所属学院"
                                    suffix-icon="el-icon-school" size="small"></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col>
                            <el-form-item prop="Email" :rules="[
                                { required: true, message: '邮箱不能为空' }
                            ]">
                                <el-input v-model="currentUserData.Email" placeholder="邮箱" suffix-icon="el-icon-message"
                                    size="small"></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                </el-form-item>
                <!-- 用户大模型的可使用量 -->
                <el-divider content-position="left">用户大模型的可使用量</el-divider>
                <el-form-item class="user-model-info">
                    <div>
                        <span class="second-text">文本大模型可使用token数</span>
                        <el-slider v-model="currentUserData.Tokens" show-input :max="8192"></el-slider>
                    </div>
                    <div class="gap-vertical"></div>
                    <div>
                        <span class="second-text">用户可上传的图片数</span>
                        <el-slider v-model="currentUserData.PicTimes" show-input :max="50"></el-slider>
                    </div>
                </el-form-item>
                <!-- 提交操作 -->
                <el-form-item>
                    <el-button type="primary">提交</el-button>
                    <el-button type="danger">重置</el-button>
                </el-form-item>
            </el-form>
        </el-drawer>
        <!-- 用户数据表 -->
        <el-table :data="userData" class="table" stripe>
            <el-table-column type="selection" width="55">
            </el-table-column>
            <el-table-column label="Id" prop="Id">
            </el-table-column>
            <el-table-column label="UserName" prop="UserName">
            </el-table-column>
            <el-table-column label="PassWord" prop="PassWord">
            </el-table-column>
            <el-table-column label="Tokens" prop="Tokens">
            </el-table-column>
            <el-table-column label="Email" prop="Email">
            </el-table-column>
            <el-table-column label="PicTimes" prop="PicTimes">
            </el-table-column>
            <el-table-column label="Academy" prop="Academy">
            </el-table-column>
            <el-table-column label="操作">
                <template slot-scope="scope">
                    <el-button @click="modifyUserData(scope.row)" size="mini" type="primary">修改</el-button>
                    <el-button size="mini" type="danger">删除</el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-pagination class="container" background layout="prev, pager, next" :total="1000">
        </el-pagination>
    </div>
</template>

<script>
import { MessageBox } from 'element-ui';

export default {
    data() {
        return {
            userData: [
                {
                    Id: "001",
                    UserName: "test",
                    PassWord: "123",
                    Tokens: 1000,
                    Email: "123@test.mail",
                    PicTimes: 5,
                    Academy: "test学院"
                },
                {
                    Id: "002",
                    UserName: "test",
                    PassWord: "123",
                    Tokens: 1000,
                    Email: "123@test.mail",
                    PicTimes: 5,
                    Academy: "test学院"
                },
                {
                    Id: "003",
                    UserName: "test",
                    PassWord: "123",
                    Tokens: 1000,
                    Email: "123@test.mail",
                    PicTimes: 5,
                    Academy: "test学院"
                },
                {
                    Id: "004",
                    UserName: "test",
                    PassWord: "123",
                    Tokens: 1000,
                    Email: "123@test.mail",
                    PicTimes: 5,
                    Academy: "test学院"
                },
            ],
            newUserData: {
                UserName: "",
                PassWord: "",
                Tokens: 0,
                PicTimes: 0,
                Academy: ""
            },
            currentUserData: {
                UserName: "",
                PassWord: "",
                Tokens: 0,
                PicTimes: 0,
                Academy: ""
            },
            keyword: "",
            addUserDrawerShow: false,
            modifyUserDrawerShow: false
        }
    },
    methods: {
        handleDrawerClose(done) {
            MessageBox.confirm("已填入的数据不会保存 确认关闭？")
                // eslint-disable-next-line
                .then(_ => done())
                // eslint-disable-next-line
                .catch(_ => { })
        },
        modifyUserData(userData) {
            this.modifyUserDrawerShow = true;
            this.currentUserData = { ...userData };
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

/* 添加用户界面 */
.add-user-view {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    padding: 1em;
}
</style>