<template>
    <footer>      
        <div class="description">
            <div class="highlight-text">POWER BY VUE2</div>
        </div>
        <div class="links">
            <a href="#">
                <font-awesome-icon :icon="['fab', 'github']" />
            </a>
            <a href="#">
                <font-awesome-icon :icon="['fab', 'vuejs']" />
            </a>
            <a href="#">
                <font-awesome-icon :icon="['fas', 'flask']" />
            </a>
            <a href="#">
                <font-awesome-icon :icon="['fab', 'python']" />
            </a>
        </div>
    </footer>
</template>

<script>
    export default {
        
    }
</script>

<style scoped>
/* 基础设置 */
a, a:active {
    text-decoration: none;
    color: #8cc5ff;
}
footer {
    display: flex;
    justify-content: space-around;
    align-items: center;
    padding-top: 1em;
    padding-bottom: 1em;
}
/* 项目描述 */
.description {
    text-align: center;
}
/* 链接区 */
.links a {
    color: #303133;
}
.links a:not(a:last-child) {
    margin-right: 10px;
}
</style>