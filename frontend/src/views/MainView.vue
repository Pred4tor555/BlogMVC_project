<script setup>

import {onMounted, ref} from "vue";

import {LogOut, CircleX, Pencil} from "lucide-vue-next";
import {useAuthStore} from "@/stores/AuthStore.js";
import {useRouter} from "vue-router";
import {createArticle, getArticles, deleteArticle, updateArticle} from "@/api/article.js";
import VLoader from "@/components/VLoader.vue";

// Хранение данных
const authStore = useAuthStore();
const router = useRouter();

let showModal = ref(false);
let editableArticle = ref();
let showLoader = ref(false);
let articles = ref([]);
let title = ref('');  // Используем переменную для хранения значения заголовка
let imgURL = ref(''); // Для хранения URL изображения
let body = ref('');   // Для хранения текста статьи

const logout = () => {
  authStore.logout();
  router.push("/login");
};

const getAllArticles = async () => {
  try {
    showLoader.value = true;
    articles.value = await getArticles();
  } catch (e) {
    console.log(e.response);
  } finally {
    showLoader.value = false;
  }
};

const createArticleItem = async () => {
  try {
    if (title.value.trim() !== "" && body.value.trim() !== "") {
      const article = await createArticle(title.value, imgURL.value, body.value);
      console.log("Создана статья:", article);
      await getAllArticles();
    }
  } catch (e) {
    console.log("Ошибка при создании статьи:", e.response);
  }
};

const deleteArticleItem = async (id) => {
  try {
    const data = await deleteArticle(id);
    console.log(data);
  } catch (e) {
    console.log("Ошибка при удалении статьи:", e.response);
  } finally {
    await getAllArticles();
  }
};

const editBtnHandler = (article) => {
  title.value = article.title;
  imgURL.value = article.imgURL; // Подставляем данные для редактирования
  body.value = article.body;
  editableArticle.value = article;
  router.push({ name: 'edit', params: { id: article.id } });
};

const readArticle = (article) => {
  title.value = article.title;
  imgURL.value = article.imgURL; // Подставляем данные
  body.value = article.body;
  router.push({ name: 'articlePage', params: { id: article.id } });
};

const saveArticleItem = () => {
  if (editableArticle.value) {
    editableArticle.value.title = title.value;
    editableArticle.value.imgURL = imgURL.value;
    editableArticle.value.body = body.value;
    updateArticleItem(editableArticle.value);
    showModal.value = false;
  } else {
    createArticleItem();
  }
};

const updateArticleItem = async (article) => {
  console.log("Обновление статьи:", article);
  try {
    const data = await updateArticle(article);
    console.log(data);
  } catch (e) {
    console.log("Ошибка при обновлении статьи:", e.response);
  } finally {
    await getAllArticles();
  }
};

const getFirstParagraph = (text) => {
  if (!text) return "";
  const paragraphs = text.split("\n").filter(p => p.trim() !== ""); // Разделяем текст на абзацы по символу переноса строки
  return paragraphs.length > 0 ? paragraphs[0] : ""; // Возвращаем первый непустой абзац
};

onMounted(async () => {
  await getAllArticles();
  if (authStore.authError) {
    logout();
  }
});
</script>

<template>
  <transition name="fade" mode="out-in">
    <main class="main" v-if="!showModal">
      <div class="header">
        <div class="blog-title">Blog</div>
        <button class="button_transparent button__logout" @click="logout">
          <LogOut color="#000" :size="27"/>
        </button>
      </div>

      <!-- Форма для создания статьи -->
      <div class="article-form">
        <div class="article-form-title">
          <span>Создание статьи</span>
        </div>

        <!-- Поля для ввода заголовка, URL изображения и тела статьи -->
        <textarea v-model="title" rows="3" placeholder="Заголовок" autofocus />
        <textarea v-model="imgURL" rows="3" placeholder="Ссылка на изображение" />
        <textarea v-model="body" rows="6" placeholder="Текст статьи" />

        <!-- Кнопка для создания статьи -->
        <button class="button_primary button__create" @click="saveArticleItem">
          <span>Создать</span>
        </button>
      </div>

      <VLoader class="article-loader" v-if="showLoader" />

      <template v-else>
        <div v-if="articles.length < 1" class="get-started">
          <p>Статей нет</p>
        </div>

        <template v-else>
          <!-- Список созданных статей -->
          <div class="article-list-title">Подборка статей</div>
          <div class="article-list">
            <div class="article-item" v-for="(article, index) in articles" :key="index">
              <div v-if="article.imgURL">
                <img :src="article.imgURL" alt="Image" class="article-item__image" />
              </div>

              <label class="article-item__group">
                <span class="article-item__title" v-html="article.title"></span>
              </label>

              <label class="article-item__group">
                <span class="article-item__text" v-html="getFirstParagraph(article.body)"></span>
              </label>

              <div class="article-item__group">
                <button class="button button_transparent" @click="editBtnHandler(article)">
                  <Pencil color="black" :size="27" />
                </button>
                <button class="button button_transparent" @click="deleteArticleItem(article.id)">
                  <CircleX color="#F80F0F" :size="29" />
                </button>
                <button class="button_read" @click="readArticle(article)">
                  <span>Читать</span>
                </button>
              </div>
            </div>
          </div>
        </template>
      </template>
    </main>
  </transition>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.23s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

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

.get-started {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 100px;
  margin-bottom: 100px;
  font-size: 24px;
  font-weight: bold;
  color: #251713;
}

/* Стили для формы создания статьи */
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

/* Стили для списка статей */
.article-list {
  margin: 0 auto;
  max-width: 850px;
  display: grid; /* Используем CSS Grid */
  grid-template-columns: repeat(2, 1fr); /* Два столбца */
  gap: 20px; /* Отступы между статьями */
}

.article-list-title {
  margin: 40px auto 20px auto;
  max-width: 850px;
  font-size: 24px;
  font-weight: bold; /* Жирный шрифт */
  color: #000; /* Черный цвет текста */
}

.article-item {
  background-color: white;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

/* Стили для разделения элементов */
.article-item__group {
  margin-bottom: 20px; /* Увеличиваем отступ между заголовком и текстом */
}

/* Жирный шрифт для заголовка */
.article-item__title {
  font-size: 20px;
  font-weight: bold;
  display: block; /* Заголовок будет на новой строке */
  margin-bottom: 10px; /* Добавляем отступ снизу */
}

/* Обычный шрифт для текста статьи */
.article-item__text {
  font-size: 16px;
  line-height: 1.5;
}

/* Изображение статьи */
.article-item__image {
  width: 100%;
  height: auto;
  border-radius: 8px;
}

/* Стили для кнопок */
.button_transparent {
  background: none;
  border: none;
  cursor: pointer;
  padding: 5px;
}

.button_read {
  margin: 0 auto auto 30px;
  width: 50%;
  padding: 10px;
  background-color: #899c38;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 18px;
}
</style>

