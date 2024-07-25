<script setup lang="ts">
import { AxiosError, AxiosResponse } from "axios";
import { ref, onMounted } from "vue";
import { axios } from "@/common/api.service";
import { getCookie } from "@/common/csrf_token.js";

type File = {
  files: string[] | null;
};
const file = ref<File>();
const updated = ref(false);
let imgData: string | Blob | undefined = undefined;
let imgUrl: string | undefined = undefined;
let imageId: string | undefined = undefined;
let selectedFile = ref(false);
let dialog = ref(false);
// watch(imgData, () => {
//   if (typeof imgData === "undefined") {
//     selectedFile = false;
//   } else {
//     selectedFile = true;
//   }
// });
onMounted(() => {
  // ログイン状態取得
  // if (sessionStorage.getItem("loggedIn")) {
  //   loginUser.value = {
  //     message: "",
  //     token: sessionStorage.getItem("token"),
  //     username: sessionStorage.getItem("username"),
  //   };
  //   userProfile.value = {
  //     id: null,
  //     username: null,
  //     nickname: sessionStorage.getItem("nickname"),
  //     email: null,
  //     comment: null,
  //   };
  //   loggedIn.value = true;
  //   console.log("初期 in");
  // } else {
  //   loggedIn.value = false;
  //   console.log("初期 out");
  // }
});

function selectFile() {
  if (file.value!.files![0]) {
    imgData = file.value!.files![0];
    console.log("selectFile");
    selectedFile.value = true;
  } else {
    selectedFile.value = false;
  }
}

const onClick = (e) => {
  console.log("onclick" + imgData !== undefined);
  e.target!.value = "";
  imgData = undefined;
  selectedFile.value = false;
};

async function onSubmit() {
  console.log("onSubmit");
  const formData = new FormData();
  formData.append("subject", "1");
  const timezoneOffset = new Date().getTimezoneOffset() * 60 * 1000;
  const datetime = new Date(Date.now() - timezoneOffset).toISOString();
  // "YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ] format."
  formData.append("created_datetime", datetime);
  formData.append("updated_datetime", datetime);
  formData.append("imageData", imgData!);

  await axios
    .post("/api/poem/image/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
        "X-CSRFTOKEN": getCookie("csrftoken"),
      },
    })
    .then((response: AxiosResponse) => {
      console.log(response.data);
      imgUrl = `http://localhost:8000${response.data.url}`;
      imageId = response.data.id;
      updated.value = true;
      alert("Success!");
    })
    .catch((error: AxiosError) => {
      alert("エラーが発生しました\n" + error.message);
      console.log(error.message);
    });
  imgData = undefined;
}

async function onDelete() {
  console.log("onDelete");
  await axios
    .delete(`/api/poem/image/${imageId}/`, {
      headers: {
        "X-CSRFTOKEN": getCookie("csrftoken"),
      },
    })
    .then((response: AxiosResponse) => {
      console.log(response.data);
      updated.value = false;
      alert("delete Success!");
      imgUrl = undefined;
      imageId = undefined;
    })
    .catch((error: AxiosError) => {
      alert("エラーが発生しました\n" + error.message);
      console.log(error.message);
    });
}
</script>

<template>
  <v-container>
    <div>
      <v-btn color="primary">
        Open Dialog
        <v-dialog v-model="dialog" activator="parent" max-width="520">
          <v-sheet>
            <v-sheet class="my-2 mx-5">
              <h2>Dialog</h2>

              <p class="my-4">Please confirm information!</p>

              <v-btn color="primary" block @click="dialog = false">Close</v-btn>
            </v-sheet>
          </v-sheet>
        </v-dialog>
      </v-btn>
    </div>
    <div>
      <form @submit.prevent="onSubmit">
        <label for="img-upload">Choose a profile picture:</label>
        <div>
          <!-- <input type="text" name="subject"/> -->
          <input
            v-if="!updated"
            type="file"
            name=""
            id="img-upload"
            ref="file"
            accept="image/*"
            required
            @change="selectFile"
            @click="onClick"
          />
        </div>
        <div v-if="!updated">
          <button v-if="selectedFile">登録</button>
        </div>
      </form>
      <button v-if="updated" @click="onDelete">削除</button>
      <!-- プレビュー表示 -->
      <img :src="imgUrl" class="example2" />
    </div>
  </v-container>
</template>

<style type="text/css">
img.example2 {
  zoom: 10%;
}
</style>
