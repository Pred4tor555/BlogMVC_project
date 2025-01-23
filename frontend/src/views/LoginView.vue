<script setup>
import {RouterLink, useRouter} from "vue-router";
import {useAuthStore} from "@/stores/AuthStore.js";
import VLoader from "@/components/VLoader.vue";
import {LogOut} from "lucide-vue-next";

const authStore = useAuthStore();
const router = useRouter()
const login = async () => {
  await authStore.login()
  if (!authStore.authError) {
    await router.push('/')
    console.log('no error')
  }else {
    console.log('error')
    authStore.logout()
  }
}
</script>

<template>
  <main>
    <div class="header">
      <div class="blog-title">Blog</div>
    </div>
    <div class="auth">
      <h3>Вход</h3>

      <form @keydown.enter.prevent="login" @submit.prevent="login">
        <label>
          <small v-if="authStore.authError">
            {{ authStore.authError.username?.toString() || authStore.authError.detail }}
          </small>

          <input type="text" v-model="authStore.username" placeholder="Логин">
        </label>

        <label>
          <small v-if="authStore.authError">
            {{ authStore.authError.password?.toString() || authStore.authError.detail }}
          </small>

          <input type="password" v-model="authStore.password" placeholder="Пароль">
        </label>

        <button class="button_primary" type="submit" v-if="!authStore.loading">Войти</button>

        <VLoader class="auth-loader" v-else></VLoader>
      </form>

      <p>Нет аккаунта?
        <RouterLink to="/register">Зарегистрироваться</RouterLink>
      </p>
    </div>
    <div class="footer">
      Ⓒ Блог, 2024
    </div>
  </main>
</template>

<style>
.header {
  display: flex;
  justify-content: space-between; /* Размещаем элементы по краям */
  align-items: center; /* Выравниваем по вертикали */
  position: relative;
  margin-bottom: 35px;
}

/* Стили для надписи "Blog" */
.blog-title {
  font-size: 24px;
  font-weight: bold; /* Жирный шрифт */
  color: #000; /* Черный цвет текста */
}

.auth {
  margin: 0 auto;
  max-width: 450px;
}

h3 {
  font-weight: bold;
  font-size: 36px;
}

.button_primary {
  margin-top: 10px;
  width: 100%;
  padding: 10px;
  background-color: #2a4b02;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 18px;
}

.button_primary:hover {
  background-color: #3d6805;
}

.footer {
  position: absolute;
  top: 90%;
  left: 50%;
  transform: translateX(-50%);
  font-size: 16px;
  text-align: center;
}
</style>
