<template>
    <div class="console">
        <el-row :gutter="20">
            <el-col :md="10">
                <div class="control-panner">
                    <el-row>
                        <!-- 模型基本信息 -->
                        <div class="info">
                            <div class="model-info">
                                <span>当前模型</span>
                                <el-select v-model="choseModel" placeholder="当前模型" size="mini">
                                    <el-option v-for="item in modelOptions" :key="item.value" :label="item.label"
                                        :value="item.value">
                                    </el-option>
                                </el-select>
                            </div>
                            <div class="token-info">
                                <span>剩余token</span><span class="second-text">{{ $store.state.textModelToken }}</span>
                            </div>
                        </div>
                        <!-- 角色设定 -->
                        <div class="mask-setting">
                            <span>角色设定</span>
                            <div style="margin-bottom: 1em;"></div>
                            <el-input 
                            :autosize="{ minRows: 5, maxRows: 8}"
                            v-model="maskDescription"
                            type="textarea" 
                            maxlength="200"
                            resize="none"
                            placeholder="可选项 这里可以填入对大模型的角色设定信息"
                            show-word-limit></el-input>
                        </div>
                    </el-row>
                    <el-row>
                        <!-- 模型调试参数 -->
                        <div class="slider card-float">
                            <div class="slider-item">
                                <span>回复长度限制</span>
                                <el-slider v-model="modelParams.responseLimit" show-input :max="8192"></el-slider>
                            </div>
                            <div class="slider-item">
                                <span>top-k (灵活度)</span>
                                <el-slider v-model="modelParams.topK" show-input :max="10"></el-slider>
                            </div>
                            <div class="slider-item">
                                <span>temperature (随机性)</span>
                                <el-slider v-model="modelParams.temperature" show-input :max="1" :step="0.1"></el-slider>
                            </div>
                        </div>
                    </el-row>
                </div>
            </el-col>
            <el-col :md="14">
                <!-- 聊天控制台 -->
                <div class="chat-window">
                    <div class="show-msg"></div>
                    <div class="input-msg">
                        <el-input 
                        :autosize="{ minRows: 4, maxRows: 4}"
                        v-model="sendMsg"
                        style="border: none; outline: none; resize: none;"
                        type="textarea"
                        placeholder="按下enter发送调试信息"
                        resize="none"></el-input>
                        <div style="margin-right: 1em;"></div>
                        <el-button type="primary" size="mini"><i class="el-icon-s-promotion"></i>发送</el-button>
                    </div>
                </div>
            </el-col>
        </el-row>
    </div>
</template>

<script>
export default {
    data() {
        return {
            modelParams: {
                responseLimit: 2024, // 回复长度限制
                topK: 4, // 灵活度
                temperature: 0.5 // 随机性
            },
            modelOptions: [
                {
                    value: "星火文本大模型流式传输Api",
                    label: "星火文本大模型 流式传输"
                },
                {
                    value: "星火文本大模型非流式传输Api",
                    label: "星火文本大模型 非流式传输"
                }
            ],
            choseModel: "", // 选择的模型
            sendMsg: "", // 发送的消息
            maskDescription: "" // 面具描述
        }
    },
}
</script>

<style scoped>
.console {
    display: flex;
    align-items: center;
}
.console>.el-row{
    width: 80vw;
    display: flex;
}
/* 左侧控制区 */
.control-panner {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    font-size: 0.8em;
    padding: 1em;
}
/* 模型面具设置 */
.control-panner .mask-setting {
    margin-bottom: 1em;
}
.control-panner .mask-setting > el-button{
    margin-top: 1em;
}
/* 模型基本信息 */
.control-panner .info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1em;
}
.control-panner .info .model-info,
.control-panner .info .token-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.control-panner .info .model-info>span:first-child,
.control-panner .info .token-info>span:first-child {
    margin-right: 1em;
}

/* 模型调试参数 */
.control-panner .slider {
    background-image: linear-gradient(120deg, #a1c4fd 0%, #c2e9fb 100%);
    padding: 1em;
    border-radius: 5px;
}
.control-panner .slider-item:not(.slider-item:last-child) {
    width: 100%;
    margin-bottom: 2em;
}

/* 右侧消息展示区 */
.chat-window {
    width: 100%;
    border: 2px solid #e0e0e1;
    border-radius: 5px;
    overflow: auto;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.chat-window .show-msg {
    height: 20em;
    background-color: #f7f7f9;
}
.chat-window .input-msg {
    width: 100%;
    height: 20%;
    background-color: #f7f7f9;
    padding: 1.2em;
    display: flex;
    justify-content: space-around;
    align-items: self-end;
}
</style>