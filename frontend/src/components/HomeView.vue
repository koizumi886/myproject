<script setup lang="ts">
import { AxiosError, AxiosResponse } from "axios";
import { axios } from "@/common/api.service";
import { ref, reactive, onMounted } from "vue";
import RegisterImage from "./RegisterImage.vue";
// import { useGetCookie } from "@/App.vue";

// const key = Symbol() as InjectionKey<string>
// const loggedIn = useGetCookie();
// const loggedIn = inject("loggedIn");
let overlay = ref(false);
const isButtonDisabled = true;
const dynamicId = "dy";
const titleClass = ref("title");
const greeting = ref("Hello from parent");
const text = ref("");
const awesome = ref(true);
let id = 0;
const newTodo = ref("");
const todos = ref([
  { id: id++, text: "Learn Html" },
  { id: id++, text: "Learn Vue" },
]);

const counter = reactive({
  count: 0,
});
// console.log(counter.count);
counter.count++;
greeting.value = "Hello from parent Changed";

// const increment = () => {
//   counter.count++;
// };
// function login(isActive: boolean) {
//   console.log("login" + isActive);
//   // isActive.value = !isActive.value;
// }
const timezoneOffset = new Date().getTimezoneOffset() * 60 * 1000;

// console.log("timezoneOffset" + timezoneOffset);
const japanTime1 = new Date(Date.now() - timezoneOffset).toISOString();
console.log(japanTime1);
// const japanStandardTime = new Date().toLocaleString({ 'Asia/Tokyo' });
// console.log(japanStandardTime); // 例: "3/19/2019, 3:29:58 PM"

function onInput(e: { target: { value: string } }) {
  text.value = e.target.value;
}
function toggle() {
  awesome.value = !awesome.value;
  console.log("toggle");
}
function addTodo() {
  console.log();
  todos.value.push({ id: id++, text: newTodo.value });
  newTodo.value = "";
}
function removeTodo(todo: { id: number; text: string }) {
  todos.value = todos.value.filter((t) => t !== todo);
}

onMounted(() => {
  axios
    .get("/api/poem/image/")
    .then((response: AxiosResponse) => {
      console.log(response.data);
      addImage(response.data);
      // imgUrl = `http://localhost:8000${response.data.url}`;
      // sessionStorage.setItem("nickname", userProfile.value!.nickname!);
    })
    .catch((error: AxiosError) => {
      alert("エラーが発生しました\n" + error.message);
      console.log(error.message);
    });
});
type Image = {
  id: number;
  url: string;
};
// const newTodo = ref("");
const images = ref<Image[]>([]);
function addImage(datalist: [{ id: number; subject: string; image: string }]) {
  for (const data of datalist) {
    images.value!.push({ id: data.id, url: data.image });
  }
  // newTodo.value = ''
}
</script>

<template>
  <v-container>
    <div class="text-left">
      <v-btn color="error" @click="overlay = !overlay"> Show Overlay </v-btn>
      <v-overlay v-model="overlay"></v-overlay>
    </div>

    <RegisterImage />
    <v-row>
      <!-- <v-col v-for="n in 24" :key="n" cols="4"> -->
      <v-col v-for="image in images" :key="image.id">
        <v-card width="360" height="260">
          <img :src="image.url" class="example2" width="auto" height="100%" />
        </v-card>
        <v-card width="360" height="200"></v-card>
      </v-col>
    </v-row>

    <v-container>
      <h1>Make me dynamic!</h1>
      <p>loggedIn</p>
      <p>Count is: {{ counter.count + 1 }}</p>
      <h1>{{ greeting.split("").reverse().join("") }}</h1>
      <div v-bind:id="dynamicId"></div>
      <!--<h1 :class="titleClass">Make me red</h1>-->
      <h1 :class="titleClass">Make me red</h1>

      <v-btn :disabled="isButtonDisabled">{{ isButtonDisabled }} Button</v-btn
      ><br />
      <div>
        <input :value="text" @input="onInput" placeholder="Type here" />
      </div>
      <input v-model="text" placeholder="Type here" />
      <p>{{ text }}</p>
      <button @click="toggle">Toggle</button>
      <h1 v-if="awesome">Vue is awesome!</h1>
      <h1 v-else>Oh no 😢</h1>

      <form @submit.prevent="addTodo">
        <input v-model="newTodo" required placeholder="new todo" />
        <button>Add Todo</button>
      </form>
      <ul>
        <li v-for="todo in todos" :key="todo.id">
          {{ todo.text }}
          <button @click="removeTodo(todo)">delete</button>
        </li>
      </ul></v-container
    >
  </v-container>
</template>

<style>
.title {
  color: red;
}
.imgSize {
  /* width: ""; */
  height: "300";
}
</style>
