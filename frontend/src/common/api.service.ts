import axios from "axios";
// import { CSRF_TOKEN } from "./csrf_token.js";

// axios.defaults.xsrfCookieName = "csrftoken";
// axios.defaults.headers.common['X-CSRFTOKEN'] = CSRF_TOKEN;
axios.defaults.withCredentials = true;
const baseURL = "http://localhost:8000";
axios.defaults.baseURL = baseURL;

export { axios, baseURL };