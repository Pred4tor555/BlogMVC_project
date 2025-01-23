<script setup>

import { ref, onMounted } from "vue";

import { useRouter, useRoute } from "vue-router";
import { getOneArticle } from "@/api/article.js";
import { useAuthStore } from "@/stores/AuthStore.js";
import { MoveLeft } from "lucide-vue-next";
import VLoader from "@/components/VLoader.vue";

const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();

let showLoader = ref(false);
let title = ref('');
let imgURL = ref('');
let body = ref('');
let articleId = ref(null);

const back = () => {
  router.push("/");
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

// Функция для разделения текста на абзацы
const getParagraphs = (text) => {
  if (!text) return [];
  return text.split("\n");
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
        <button class="button_transparent" @click="back">
          <MoveLeft color="#000" :size="27"/>
        </button>
      </div>

      <VLoader class="article-loader" v-if="showLoader"/>


      <div class="content">
        <div class="article-item__title" v-html="title"></div>

        <div v-if="imgURL">
          <img :src="imgURL" alt="Image" class="article-item__image" />
        </div>

        <div class="article-item__text">
          <p class="text-justify"
            v-for="(paragraph, index) in getParagraphs(body)"
            :key="index"
            :class="{ 'empty-paragraph': paragraph.trim() === '' }"
          >
            {{ paragraph.trim() !== '' ? paragraph : '\u00A0' }}
          </p>
        </div>
      </div>
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

.content {
  margin: 70px auto 20px auto;
  max-width: 850px;
}

/* Жирный шрифт для заголовка */
.article-item__title {
  font-size: 20px;
  font-weight: bold;
  display: block; /* Заголовок будет на новой строке */
  margin-bottom: 50px; /* Добавляем отступ снизу */
}

/* Обычный шрифт для текста статьи */
.article-item__text {
  margin-top: 60px;
  font-size: 16px;
  line-height: 1.5;
}

/* Изображение статьи */
.article-item__image {
  width: 100%;
  height: auto;
  border-radius: 8px;
}

.text-justify {
  text-align: justify;
}

.button_transparent {
  background: none;
  border: none;
  cursor: pointer;
  padding: 5px;
}
</style>
