<template>
    <div class="login-view">
        <h1>欢迎使用代号: AiProject 后台管理系统</h1>
        <el-form :model="adminData" class="login-form card-float" ref="loginForm">
            <el-form-item label="用户名" prop="name">
                <el-input v-model="adminData.name" placeholder="用户名"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="password">
                <el-input v-model="adminData.password" placeholder="请输入密码" show-password></el-input>
            </el-form-item>
            <el-form-item>
                <el-button @click="login" type="primary">立即登录</el-button>
                <el-button @click="resetForm" type="info">重置</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
import { Notification } from 'element-ui';

export default {
    data() {
        return {
            adminData: {
                name: "",
                password: "",
            }
        }
    },
    methods: {
        login() {
            this.$axios({
                method: "POST",
                url: "http://127.0.0.1:5000/admin/login",
                data: {
                    admin: this.adminData.name,
                    password: this.adminData.password
                }
            }).then(res => {
                let data = res.data;
                if (!data.code) {
                    // 存储jwt秘钥
                    localStorage.setItem("access_token", data.access_token);
                    localStorage.setItem("refresh_token", data.refresh_token);

                    // 存储实例信息状态
                    this.$store.dispatch("APPInfo/app_id", data.app_info);
                    this.$store.dispatch("APPInfo/api_key", data.app_info);
                    this.$store.dispatch("APPInfo/api_secret", data.app_info);

                    // 存储用户信息状态
                    this.$store.commit("AdminInfo/ADMIN_NAME", this.adminData.name);

                    Notification({
                        title: "登录成功",
                        message: data.msg,
                        type: "success"
                    })
                    
                    this.$router.push({
                        path: "/AppInfo"
                    })
                }else {
                    Notification.error({
                        title: "登录错误",
                        message: data.msg
                    })
                }
            }, error => {
                console.log(error);
            })
        },
        resetForm() {
            this.$refs["loginForm"].resetFields();
        }
    }
}
</script>

<style scoped>
.login-view {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
.login-view>h1 {
    margin-bottom: 1em;
}
.login-form {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    border: 1px solid #eeeeee;
    border-radius: 5px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
    padding: 1em;
}
</style>