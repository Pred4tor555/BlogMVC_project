import {$authHost} from "@/api/index.js";

export const getArticles = async () => {
  const articles = await $authHost.get('articles')
  return articles.data
}

export const getOneArticle = async (id) => {
  const article = await $authHost.get(`articles/${id}`)
  return article.data
}

export const createArticle = async (title, imgURL, body) => {
  const {article} = await $authHost.post('articles', {
    title, imgURL, body
  })
  return {article}
}

export const updateArticle = async ({id, title, imgURL, body}) => {
  const {data} = await $authHost.put(`articles/${id}`, {
    title, imgURL, body
  })
  return {data}
}

export const deleteArticle = async (id) => {
  return await $authHost.delete(`articles/${id}`)
}
