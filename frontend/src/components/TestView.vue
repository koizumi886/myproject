<script setup lang="ts">
import { ref, reactive } from "vue";
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
console.log(counter.count);
counter.count++;
greeting.value = "Hello from parent Changed";

const increment = () => {
  counter.count++;
};
function onInput(e) {
  text.value = e.target.value;
}
function toggle() {
  awesome.value = !awesome.value;
}
function addTodo() {
  console.log();
  todos.value.push({ id: id++, text: newTodo.value });
  newTodo.value = "";
}
function removeTodo(todo: { id: number; text: string }) {
  todos.value = todos.value.filter((t) => t !== todo);
}
</script>

<template>
  <v-container>
    <v-btn color="primary">default</v-btn>
    <v-btn color="primary" variant="outlined">アウトライン</v-btn>
    <v-btn color="primary" variant="text">テキスト</v-btn>
    <v-btn color="primary" variant="flat">flat</v-btn>
    <v-btn color="primary" icon="mdi-home"></v-btn>
    <h1>Make me dynamic!</h1>
    <p>{{ greeting }}</p>
    <p>Count is: {{ counter.count + 1 }}</p>
    <h1>{{ greeting.split("").reverse().join("") }}</h1>
    <div v-bind:id="dynamicId"></div>
    <!--<h1 :class="titleClass">Make me red</h1>-->
    <h1 :class="titleClass">Make me red</h1>

    <button :disabled="isButtonDisabled">{{ isButtonDisabled }} Button</button
    ><br />
    <button @click="increment">Count is: {{ counter.count }}</button>
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
    </ul>
  </v-container>
</template>

<style>
.title {
  color: red;
}
</style>
: { target: { value: string; }; }: { id: number; text: string; }
