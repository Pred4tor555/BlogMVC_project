<script setup>

import { ref, onMounted } from "vue";

import { useRouter, useRoute } from "vue-router";
import { getOneArticle, updateArticle } from "@/api/article.js";
import { useAuthStore } from "@/stores/AuthStore.js";
import { LogOut } from "lucide-vue-next";
import VLoader from "@/components/VLoader.vue";

const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();

let showLoader = ref(false);
let title = ref('');
let imgURL = ref('');
let body = ref('');
let articleId = ref(null);

const logout = () => {
  authStore.logout();
  router.push("/login");
};

// Загрузка статьи для редактирования
const getArticleDetails = async (id) => {
  try {
    showLoader.value = true;
    const article = await getOneArticle(id);
    console.log(article);
    title.value = article.title;
    imgURL.value = article.imgURL;
    body.value = article.body;
    articleId.value = article.id;
  } catch (e) {
    console.log("Ошибка при получении статьи:", e.response);
  } finally {
    showLoader.value = false;
  }
};

const saveArticleItem = async () => {
  try {
    const updatedArticle = {
      id: articleId.value,
      title: title.value,
      imgURL: imgURL.value,
      body: body.value
    };
    console.log(updatedArticle);
    await updateArticle(updatedArticle);
    await router.push("/"); // Перенаправление обратно на главную страницу
  } catch (e) {
    console.log("Ошибка при сохранении статьи:", e.response);
  }
};

onMounted(() => {
  const id = route.params.id;
  getArticleDetails(id);
});
</script>

<template>
  <transition name="fade" mode="out-in">
    <main class="main">
      <div class="header">
        <div class="blog-title">Blog</div>
        <button class="button_transparent button__logout" @click="logout">
          <LogOut color="#000" :size="27"/>
        </button>
      </div>

      <!-- Форма для редактирования статьи -->
      <div class="article-form">
        <div class="article-form-title">
          <span>Редактирование статьи</span>
        </div>

        <!-- Поля для редактирования заголовка, URL изображения и текста -->
        <textarea v-model="title" rows="3" placeholder="Заголовок" autofocus />
        <textarea v-model="imgURL" rows="3" placeholder="Ссылка на изображение" />
        <textarea v-model="body" rows="6" placeholder="Текст статьи" />

        <!-- Кнопка для сохранения изменений -->
        <button class="button_primary button__create" @click="saveArticleItem">
          <span>Сохранить</span>
        </button>
      </div>

      <VLoader class="article-loader" v-if="showLoader" />
    </main>
  </transition>
</template>

<style scoped>
.header {
  margin: 0 auto 35px auto;
  max-width: 850px;
  display: flex;
  justify-content: space-between; /* Размещаем элементы по краям */
  align-items: center; /* Выравниваем по вертикали */
  position: relative;
}

/* Стили для надписи "Blog" */
.blog-title {
  font-size: 24px;
  font-weight: bold; /* Жирный шрифт */
  color: #000; /* Черный цвет текста */
}

.article-form {
  margin: 20px auto 20px auto;
  max-width: 850px;
  padding: 20px;
  background: #f4f4f4;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.article-form-title {
  margin-bottom: 15px;
}

.article-form textarea {
  width: 100%;
  margin-bottom: 10px;
  padding: 10px;
  font-size: 16px;
  border-radius: 5px;
  border: 1px solid #ddd;
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
</style>
