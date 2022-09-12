import axios from "axios";

axios.defaults.withCredentials = true; // withCredentials 전역 설정

export default axios.create({
  baseURL: "https://cjfghk5697-classification-site-5764gqr4w724pp7-8000.githubpreview.dev",
  headers: {
    'Accept': 'application/json',
    "Content-type": "application/json"
  }
});