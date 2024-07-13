<template>
    <el-table :data="serves" class="table" stripe>
        <el-table-column type="expand">
            <template slot-scope="props">
                <div class="detail">
                    <span class="title">服务名称</span>
                    <span>{{props.row.name}}</span>
                </div>
                <div class="detail">
                    <span class="title">状态</span>
                    <span>{{props.row.status}}</span>
                </div>
                <div class="detail">
                    <span class="title">剩余token量</span>
                    <span>{{props.row.token}}</span>
                </div>
            </template>
          </el-table-column>
        <el-table-column label="服务名称" prop="name"></el-table-column>
        <el-table-column label="状态" prop="status">
            <template slot-scope="scope">
                <el-tag>{{ scope.row.status }}</el-tag>
            </template>
        </el-table-column>
        <el-table-column label="剩余token量" prop="status">
            <template slot-scope="scope">
                <el-tag>{{ scope.row.token }}</el-tag>
            </template>
        </el-table-column>
        <el-table-column label="操作" align="right">
            <template slot="header" slot-scope="{}">
                <div class="search">
                    <i class="el-icon-search"></i>
                    <el-input v-model="keyword" size="mini" placeholder="输入关键字搜索"/>
                </div>
            </template>
            <template slot-scope="{}">
                <el-button size="mini" type="primary">测试</el-button>
            </template>
        </el-table-column>
    </el-table>
</template>

<script>
    export default {
        name: "SimpleTest",
        data() {
            return {
                serves: [
                    {
                        name: "文本大模型非流式传输接口", status: "正常", token: 1000
                    },
                    {
                        name: "文本大模型流式传输接口", status: "正常", token: 1000
                    },
                    {
                        name: "语言模型流式传输接口", status: "正常", token: 1000
                    },
                    {
                        name: "图片识别模型流式传输接口", status: "正常", token: 1000
                    },
                ],
                keyword: "",
                isShow: false
            }
        }
    }
</script>

<style scoped>
/* 服务详细信息 */
.detail {
    margin-bottom: 10px;
}
.detail .title {
    text-align: center;
    font-size: 1.2em;
    color: #99a9bf;
    margin-right: 10px;
    font-weight: bold;
}
.detail .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 50%;
  }
</style>