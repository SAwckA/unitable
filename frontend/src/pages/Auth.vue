<template>
  <Header></Header>
    <div class="form__container">
        <login-form></login-form>
    </div>
</template>

<script>
import Header from "@/components/Header.vue";
import LoginForm from "@/components/LoginForm.vue";

export default {
    name: "Auth",
    components: {LoginForm, Header}
}
</script>

<style scoped>
.form__container {
    min-width: 100vw;
    min-height: 720px;
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>