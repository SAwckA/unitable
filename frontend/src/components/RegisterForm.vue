<template>
    <div class="container">
        <form @submit.prevent>
            <h1>Регистрация</h1>
            <input v-model="username" type="text" placeholder="Username">
            <input v-model="email" type="text" placeholder="Email">
            <input v-model="password1" type="password" placeholder="Password">
            <input v-model="password2" type="password" placeholder="Повторите пароль">
            <div class="link__list">
                <router-link to="/auth">
                    <a>Уже зарегистрированы?</a>
                </router-link>
                <a>Забыл пароль</a>
            </div>
            <button @click="register">Зарегистрироваться</button>
        </form>
    </div>
</template>

<script>
import axios from "axios";
import router from "@/router";

export default {
    name: "LoginForm",
    data() {
        return {
            username: '',
            email: '',
            password1: '',
            password2: ''
        }
    },
    methods: {
        async register() {
            if (this.password1 !== this.password2) {
                return;
            }
            const resp = await axios.post('/api/register', {
                'username': this.username,
                'email': this.email,
                'password': this.password1
            })
            await router.push('/auth')
        }
    }
}
</script>

<style scoped>
.container {
    max-width: 480px;
    min-width: 480px;
}

form {
    margin: 10px;
    display: flex;
    flex-direction: column;
}

form * {
    margin-bottom: 10px;
}

input {
    border: 1px solid;
    border-radius: 0.25rem;
    transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
    padding: 5px 15px;
}

input:focus {
    color: #212529;
    background-color: #fff;
    border-color: var(--primary-color);
    outline: 0;
    box-shadow: 0 0 0 0.2rem rgba(158, 158, 158, 1);
}

.link__list {
    display: flex;
    justify-content: space-between;
    margin-bottom: 5px;
}

.link__list a {
    color: rgb(128, 128, 128);
    margin-top: 10px;
    margin-bottom: 0;
}

button {
    padding: 8px 0;
    font-weight: bold;
    font-size: 1.1rem;
    background-color: var(--primary-color);
    color: white;
    border-radius: 0.25rem;
    border-color: var(--primary-color);
    transition: 125ms;
    cursor: pointer;
}

button:hover {
    background-color: var(--button-color);
    border-color: var(--button-color);
    transition: 125ms;
}

button:active {
    background-color: var(--button-color-hover);
    border-color: var(--button-color-hover);
    transition: 125ms;
}

h1 {
    text-align: center;
}
</style>