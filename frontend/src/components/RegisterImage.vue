<script setup lang="ts">
import { AxiosError, AxiosResponse } from "axios";
import { ref, watch, defineProps, defineEmits } from "vue";
import { axios, baseURL } from "@/common/api.service";
import { getCookie } from "@/common/csrf_token.js";
// import { require_rule, maxLength_rule } from "@/common/validation_rules";
import * as validation_rules from "@/common/validation_rules";

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const props = defineProps({
  loggedIn: String,
});
type File = {
  files: string[] | null;
};
const file = ref<File>();
// const form = reactive({
// count: 0,
// });
/** 入力フォームバリデーション用定数 */
const form = ref();
const updated = ref(false);
// const caption = ref();
let imgData: string | Blob | undefined = undefined;
let imgUrl: string | undefined = undefined;
let imageId: string | undefined = undefined;
let selectedFile = ref(false);
let dialog = ref(false);
const title = ref("");
const caption = ref("");
// let captionId: string | undefined = undefined;
const emit = defineEmits(["loginDemand", "reacquisition"]);

watch(file, () => {
  if (file == null) {
    selectedFile.value = false;
    imgData = undefined;
  }
});

// バリデーションルール
const title_rules = [
  validation_rules.require_rule,
  validation_rules.maxLength_rule(25),
];
const caption_rules = [
  validation_rules.require_rule,
  validation_rules.maxLength_rule(1000),
];
const resetValidation = () => {
  console.log("resetValidation");
  form.value.resetValidation();
};

function selectFile() {
  if (file.value!.files![0]) {
    console.log("selectFile");
    imgData = file.value!.files![0];
    selectedFile.value = true;
  } else {
    selectedFile.value = false;
  }
}

const onClick = () => {
  console.log("onclick");
  // e.target!.value = "";
  file.value!.files = null;
  imgData = undefined;
  selectedFile.value = false;
};

const onCancel = () => {
  console.log("onCancel");
  // onClick(); bug修正済み
  imgData = undefined;
  selectedFile.value = false;
  dialog.value = false;
  updated.value = false;
  emit("reacquisition");
};

// 投稿
async function onSubmit() {
  console.log("onSubmit");
  const { valid } = await form.value.validate();
  console.log("valid", valid);
  if (valid) {
    const formData = new FormData();
    formData.append("img_subject", "1");
    const timezoneOffset = new Date().getTimezoneOffset() * 60 * 1000;
    const datetime = new Date(Date.now() - timezoneOffset).toISOString();
    // "YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ] format."
    formData.append("img_created_datetime", datetime);
    formData.append("img_updated_datetime", datetime);
    formData.append("img_imageData", imgData!);

    formData.append("title", title.value);
    formData.append("caption", caption.value);
    formData.append("classification", "1");
    formData.append("font", "2");
    formData.append("created_datetime", datetime);
    formData.append("updated_datetime", datetime);

    await axios
      .post("/api/poem/poemSet/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
          "X-CSRFTOKEN": getCookie("csrftoken"),
        },
      })
      .then((response: AxiosResponse) => {
        console.log(response.data);
        imgUrl = `${baseURL}${response.data.image_url}`;
        imageId = response.data.image_id;
        // poemId = response.data.poem_id;
        updated.value = true;
        // イメージ選択リセット
        imgData = undefined;
        alert("登録しました!");
      })
      .catch((error: AxiosError) => {
        console.log(error.message);
        if (error.response?.status == 403) {
          emit("loginDemand");
          alert(
            "タイムアウトのため再ログインを行ってください\n" + error.message
          );
          onCancel();
        } else {
          alert("エラーが発生しました\n" + error.message);
        }
      });
  } else {
    // validationエラー
    return;
  }
}

// 投稿削除
async function onDelete() {
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
      imgUrl = undefined;
      imageId = undefined;
      alert("削除しました!");
    })
    .catch((error: AxiosError) => {
      console.log(error.message);
      if (error.response?.status == 403) {
        emit("loginDemand");
        alert("タイムアウトのため再ログインを行ってください\n" + error.message);
        onCancel();
      } else {
        alert("エラーが発生しました\n" + error.message);
      }
      return;
    });
}
</script>

<template>
  <v-container>
    <div class="text-left">
      <v-btn :disabled="!loggedIn" class="my-5" color="primary">
        {{ loggedIn ? "投稿する" : "投稿する（ログインしてください）" }}
        <v-dialog
          v-model="dialog"
          activator="parent"
          max-width="600"
          persistent
        >
          <v-sheet>
            <v-sheet class="my-4 mx-5">
              <h3>コンテンツを作成</h3>
              <div>
                <v-form
                  ref="form"
                  validate-on="submit"
                  @submit.prevent="onSubmit"
                >
                  <!-- <label for="img-upload">Choose a profile picture:</label> -->
                  <div class="mt-5">
                    <label for="img-upload">{{
                      !selectedFile ? "Choose a picture" : ""
                    }}</label>
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
                  <div class="mt-5">
                    <v-textarea
                      v-model="title"
                      :readonly="updated"
                      :clearable="!updated"
                      rows="2"
                      bg-color="transparent"
                      label="タイトル"
                      :rules="title_rules"
                      auto-grow
                      variant="outlined"
                      counter
                      placeholder="25文字"
                      maxlength="25"
                      @click="resetValidation"
                      height="20"
                    ></v-textarea>
                    <v-textarea
                      v-model="caption"
                      :readonly="updated"
                      :clearable="!updated"
                      bg-color="transparent"
                      label="投稿文"
                      :rules="caption_rules"
                      auto-grow
                      variant="outlined"
                      counter
                      placeholder="1000文字"
                      maxlength="1000"
                      @click="resetValidation"
                    ></v-textarea>
                  </div>
                  <v-btn
                    v-if="selectedFile && !updated"
                    type="submit"
                    class="mt-5"
                    text="登録"
                    color="primary"
                    block
                  ></v-btn>
                </v-form>
                <!-- プレビュー表示 -->
                <img :src="imgUrl" class="example2" />
                <v-btn
                  v-if="updated"
                  @click="onDelete"
                  text="削除する"
                  color="error"
                  block
                ></v-btn>
              </div>
              <!-- <div @click="onClick"> -->
              <v-btn class="text-right" text="Cancel" @click="onCancel"></v-btn>
              <!-- </div> -->
            </v-sheet>
          </v-sheet>
        </v-dialog>
      </v-btn>
    </div>
  </v-container>
</template>

<style type="text/css">
.v-container {
  padding: 0px;
}
img.example2 {
  zoom: 10%;
}
input[type="file"] {
  color: rgb(31, 41, 55);
  cursor: pointer;
  border: 1px solid rgb(191, 194, 199);
  border-radius: 0.375rem;
  padding-right: 0.5rem;
  width: 24rem;
}

::file-selector-button,
::-webkit-file-upload-button {
  background-color: rgb(209, 213, 219);
  color: rgb(31, 41, 55);
  border: none;
  cursor: pointer;
  border-right: 1px solid rgb(191, 194, 199);
  padding: 0.25rem 1rem;
  margin-right: 1rem;
}
</style>
