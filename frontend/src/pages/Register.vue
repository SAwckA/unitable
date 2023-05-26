<template>
    <Header></Header>
    <div class="form__container">
        <register-form></register-form>
    </div>
</template>

<script>
import Header from "@/components/Header.vue";
import RegisterForm from '@/components/RegisterForm.vue'
export default {
    components: {
        Header,
        RegisterForm
    },
    name: "Register"
}
</script>

<style scoped>

.form__container {
    max-width: 1440px;
    min-width: 1440px;
    margin: auto;
    display: flex;
    justify-content: center;
    align-items: center;

    min-height: 720px;
}

</style>