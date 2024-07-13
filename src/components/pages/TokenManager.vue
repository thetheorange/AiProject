<template>
    <div style="width: 100%;">
        <!-- 控制面板 -->
        <div class="control-panner">
            <div class="search">
                <i class="el-icon-search"></i>
                <el-input v-model="keyword" size="small" placeholder="输入关键字搜索" />
            </div>
            <div class="gap-horizontal"></div>
            <el-button @click="addTokenDrawerShow = true" size="mini" type="success">添加令牌</el-button>
        </div>
        <!-- 添加令牌子界面 -->
        <el-drawer title="添加一个令牌" :visible.sync="addTokenDrawerShow" :before-close="handleDrawerClose" size="50%">
            <el-form :model="newTokenData" class="add-token-view">
                <el-form-item>
                    <el-row :gutter="5">
                        <el-col :md="12">
                            <el-form-item prop="TokenName" :rules="[
                                { required: true, message: '令牌名不能为空'}
                            ]">
                                <el-input v-model="newTokenData.TokenName" placeholder="令牌名" suffix-icon="el-icon-school"
                                    size="small"></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :md="12">
                            <el-form-item prop="TokenLimit" :rules="[
                                { required: true, message: '令牌额度不能为空'}
                            ]">
                                <el-input v-model="newTokenData.TokenLimit" placeholder="令牌额度" suffix-icon="el-icon-school"
                                    size="small"></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <div class="gap-vertical"></div>
                    <el-row>
                        <el-col>
                            <el-form-item prop="TokenRange" :rules="[
                                { required: true, message: '令牌使用范围不能为空'}
                            ]">
                                <el-input v-model="newTokenData.TokenRange" placeholder="令牌使用范围" suffix-icon="el-icon-school"
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
        <!-- 修改令牌信息子界面 -->
        <el-drawer title="修改一个令牌" :visible.sync="modifyTokenDrawerShow" :before-close="handleDrawerClose" size="50%">
            <el-form :model="currentTokenData" class="modify-token-view">
                <el-form-item>
                    <el-row :gutter="5">
                        <el-col :md="12">
                            <el-form-item prop="TokenName" :rules="[
                                { required: true, message: '令牌名不能为空'}
                            ]">
                                <el-input v-model="currentTokenData.TokenName" placeholder="令牌名" suffix-icon="el-icon-school"
                                    size="small"></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :md="12">
                            <el-form-item prop="TokenLimit" :rules="[
                                { required: true, message: '令牌额度不能为空'}
                            ]">
                                <el-input v-model="currentTokenData.TokenLimit" placeholder="令牌额度" suffix-icon="el-icon-school"
                                    size="small"></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <div class="gap-vertical"></div>
                    <el-row>
                        <el-col>
                            <el-form-item prop="TokenRange" :rules="[
                                { required: true, message: '令牌使用范围不能为空'}
                            ]">
                                <el-input v-model="newTokenData.TokenRange" placeholder="令牌使用范围" suffix-icon="el-icon-school"
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
        <!-- 令牌展示列表 -->
        <el-table :data="tokenData" class="table" stripe>
            <el-table-column label="Id" prop="Id"></el-table-column>
            <el-table-column label="状态" prop="Status">
            </el-table-column>
            <el-table-column label="令牌名" prop="TokenName"></el-table-column>
            <el-table-column label="范围" prop="TokenRange"></el-table-column>
            <el-table-column label="操作">
                <template slot-scope="scope">
                    <el-button @click="modifyTokenInfo(scope.row)" size=small type="primary">修改</el-button>
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
            tokenData: [
                {
                    Id: "001",
                    Status: "available",
                    TokenName: "test",
                    TokenLimit: 1000,
                    TokenRange: "none"
                },
                {
                    Id: "002",
                    Status: "available",
                    TokenName: "test1",
                    TokenLimit: 1000,
                    TokenRange: "none"
                },
                {
                    Id: "003",
                    Status: "available",
                    TokenName: "test2",
                    TokenLimit: 1000,
                    TokenRange: "none"
                },
            ],
            newTokenData: {
                Id: "",
                Status: "",
                TokenName: "",
                TokenLimit: 1000,
                TokenRange: "none"
            },
            currentTokenData: {
                Id: "",
                Status: "",
                TokenName: "",
                TokenLimit: 0,
                TokenRange: ""
            },
            addTokenDrawerShow: false,
            modifyTokenDrawerShow: false,
            keyword: ""
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
        modifyTokenInfo(tokenInfo) {
            this.currentTokenData = {...tokenInfo};
            this.modifyTokenDrawerShow = true;
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
/* 添加令牌子界面 */
.add-token-view,
.modify-token-view{
    width: 100%;
    height: 100%;
    padding: 1em;
}
</style>