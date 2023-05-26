<template>
    <div class="nav__container" :key="username">
      <nav>
          <div class="left">
              <div class="nav__element">
                  <a class="logo__href__container">
                      <img src="@/assets/logo.svg" alt="" class="logo">
                  </a>
              </div>
              <div class="nav__element">
                  <router-link to="/">
                      <a>Главная</a>
                  </router-link>
              </div>
              <div class="nav__element">
                  <router-link to="/journals/find">
                      <a>Поиск журналов</a>
                  </router-link>
              </div>
              <div class="nav__element"
              v-if="singedIn">
                  <router-link to="/journals/my">
                      <a>Мои журналы</a>
                  </router-link>
              </div>
          </div>
          <div v-if="username === null || username ==='null'" class="right">
              <div class="nav__element">
                  <router-link to="/auth">
                      <a href="/auth">Вход</a>
                  </router-link>
              </div>

              <div class="nav__element highlighted">
                  <router-link to="/register">
                      <a href="/register">Регистрация</a>
                  </router-link>
              </div>
          </div>

          <div v-else class="right">
              <div class="nav__element">
                  <a @click="logout">Выход</a>
              </div>

              <div class="nav__element highlighted">
                  <a>{{ username }}</a>
              </div>

          </div>
      </nav>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: "Header",
    data() {
        return {
            username: 'null',
            singedIn: false
        }
    },
    methods: {
        async logout() {
            await axios.post('/api/logout')
            localStorage.setItem('username', null)
            localStorage.setItem('user_id', null)
            this.username = null
            this.singedIn = false
        },
        usernameUpdate() {
            this.username = localStorage.getItem('username')
        }
    },
    mounted() {
        this.usernameUpdate()
        this.singedIn = localStorage.getItem('username') !== 'null'
    }

}
</script>
<style scoped>
.nav__container {
    min-height: 50px;
    background-color: var(--primary-color);
    min-width: 100vh;
}

nav {
    display: flex;
    flex-direction: row;
    min-width: 1440px;
    max-width: 1440px;
    margin: auto;
    min-height: 50px;
    justify-content: space-between;
}

.left {
    display: flex;
    flex-direction: row;
}

.right {
    display: flex;
    flex-direction: row;
}


.nav__element {
    display: flex;
    justify-content: center;
    align-content: center;
    align-items: center;
    padding-left: 10px;
    padding-right: 10px;
}

.highlighted {
    background-color: var(--button-color);
    border-color: var(--button-color);
    margin: 10px;
    border-radius: 0.2em;
}

.highlighted:hover {
    background-color: var(--button-color-hover);
    border-color: var(--button-color-hover);
}

nav {
    color: white;
}

a:link {
    color: white;
    text-decoration: none;
}

a:visited {
    color: white;
    text-decoration: none;
}

.logo__href__container {
    height: 90%;
}

.logo {
    height: 100%;
}

a {
    font-weight: bold;
}

a:hover {
    text-decoration: underline 1px;
    /*transition: 400ms;*/
}

.highlighted:hover a {
    text-decoration: none;
}
</style>