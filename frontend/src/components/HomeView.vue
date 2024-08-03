<script setup lang="ts">
import { AxiosError, AxiosResponse } from "axios";
import { axios, baseURL } from "@/common/api.service";
import { ref, onMounted, defineProps, defineEmits } from "vue";
import RegisterImage from "./RegisterImage.vue";
import { getCookie } from "@/common/csrf_token.js";
// import { useGetCookie } from "@/App.vue";

// const key = Symbol() as InjectionKey<string>
// const loggedIn = useGetCookie();
// const loggedIn = inject("loggedIn");

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const props = defineProps({
  loggedIn: String,
  nickname: String,
  loginUser: String,
});
// const filteredTodos = computed(() => {
//   // props.loginUser ==
//   return "";
// });
type Image = {
  id: number;
  url: string;
  title: string;
  caption: string;
  owner: string;
  nickname: string;
};

const images = ref<Image[]>([]);

function addImage(
  datalist: [
    {
      imageId: number;
      url: string;
      title: string;
      caption: string;
      owner: string;
      nickname: string;
    },
  ]
) {
  images.value = [];
  for (const data of datalist) {
    images.value!.push({
      id: data.imageId,
      url: `${baseURL}${data.url}`,
      title: data.title,
      caption: data.caption,
      owner: data.owner,
      nickname: data.nickname,
    });
  }
}
const timezoneOffset = new Date().getTimezoneOffset() * 60 * 1000;

// console.log("timezoneOffset" + timezoneOffset);
const japanTime1 = new Date(Date.now() - timezoneOffset).toISOString();
console.log(japanTime1);
// const japanStandardTime = new Date().toLocaleString({ 'Asia/Tokyo' });
// console.log(japanStandardTime); // 例: "3/19/2019, 3:29:58 PM"
// let imageData: AxiosResponse | null = null;
const imageData = ref<AxiosResponse>();
// let poemData: AxiosResponse | null = null;

onMounted(() => {
  getImageList();
});

async function getImageList() {
  await axios
    .get("/api/poem/poemSet/list/")
    .then((response: AxiosResponse) => {
      imageData.value = response;
      addImage(response.data);
    })
    .catch((error: AxiosError) => {
      alert("エラーが発生しました\n" + error.message);
      console.log(error.message);
    });
}

const emit = defineEmits(["loginDemand"]);
function logout() {
  emit("loginDemand");
}
async function onDelete(imageId: number) {
  console.log("onDelete");
  // イメージ削除
  await axios
    .delete(`/api/poem/poemSet/${imageId}/`, {
      headers: {
        "X-CSRFTOKEN": getCookie("csrftoken"),
      },
    })
    .then((response: AxiosResponse) => {
      console.log(response.data);
      alert("削除しました!");
      getImageList();
    })
    .catch((error: AxiosError) => {
      console.log(error.message);
      if (error.response?.status == 403) {
        emit("loginDemand");
        alert("タイムアウトのため再ログインを行ってください\n" + error.message);
      } else {
        alert("エラーが発生しました\n" + error.message);
      }
      return;
    });
}
</script>

<template>
  <v-container>
    <!-- <div class="text-left">
      <v-btn color="error" @click="overlay = !overlay"> Show Overlay </v-btn>
      <v-overlay v-model="overlay"></v-overlay>
    </div> -->
    <RegisterImage
      :loggedIn="loggedIn"
      @loginDemand="logout"
      @reacquisition="getImageList"
    />
    <v-row>
      <v-col v-for="image in images" :key="image.id">
        <!-- <div class="d-flex align-center justify-center fill-height 垂直中央"> -->
        <div class="justify-center fill-height">
          <v-card width="360" height="202" class="mx-auto">
            <v-img :src="image.url" width="360" cover>
              <p class="text-h3 ms-7 mt-5 text-white">
                {{ image.title }}
              </p>
            </v-img>
          </v-card>
          <!-- <v-card width="360" height="202"> -->
          <!-- <v-img :src="image.url" width="463" :aspect-ratio="4 / 3" cover /> -->
          <!-- <v-img :src="image.url" class="bg-green-lighten-4" /> -->
          <!-- </v-card> -->

          <v-card
            width="360"
            height="130"
            elevation="10"
            class="mx-auto overflow-y-auto"
          >
            <div class="justify-end">
              <v-card-text class="justify-end">{{ image.caption }}</v-card-text>
            </div>
            <div class="right_h">{{ image.nickname }}</div>
            <div
              v-if="loggedIn && image.owner == loginUser"
              class="d-flex justify-end"
            >
              <v-btn class="me-5" @click="onDelete(image.id)"> 削除 </v-btn>
            </div>
          </v-card>
        </div>
      </v-col>
    </v-row>
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
template {
  /* font-family: "M PLUS Rounded 1c", sans-serif; */
  font-family: "Noto Serif JP", sans-serif;
}
.right_h {
  text-align: right;
  /* border: 1px solid #999; */
  padding: 0px;
  /* background: #f1f1ee; */
  margin: 0px;
}
</style>
