<script setup lang="ts">
import { AxiosError, AxiosResponse } from "axios";
import { ref, onMounted, watch } from "vue";
import { axios, baseURL } from "@/common/api.service";
// import { VueCookies } from "vue-cookies";

// let $cookies = inject("$cookies");
// const sessionId = Symbol() as InjectionKey<string>;

const drawer = ref(true);
type User = {
  message: string | null;
  token: string | null;
  username: string | null;
};
type LoginParam = {
  username: string | null;
  password: string | null;
};
type UserProfile = {
  id: string | null;
  username: string | null;
  nickname: string | null;
  email: string | null;
  comment: string | null;
};
const loginUser = ref<User>();
const loggedIn = ref(false);
// const loginParam = ref({ username: "", password: "" });
const loginParam = ref<LoginParam>({ username: null, password: null });
const userProfile = ref<UserProfile>({
  id: null,
  username: null,
  nickname: null,
  email: null,
  comment: null,
});

onMounted(() => {
  // ログイン状態取得
});

watch(loggedIn, () => {
  if (loggedIn.value) {
    sessionStorage.setItem("loggedIn", "true");
    console.log("in" + loggedIn.value);
    sessionStorage.setItem("token", loginUser.value!.token!);
    sessionStorage.setItem("username", loginUser.value!.username!);
  } else {
    sessionStorage.removeItem("loggedIn");
    loginUser.value = undefined;
    console.log("out" + loggedIn.value);
  }
});

// const useGetCookie = () => {
//   // const $cookies = inject<VueCookies>("$cookies");
//   if ($cookies !== null && $cookies !== undefined) {
//     if ($cookies.get("sessionid")) {
//       loggedIn.value = true;
//       return true;
//     }
//     console.log("keys ", $cookies.keys());
//     // provide("loggedIn", $cookies);
//   }
//   console.log("sessionid false" + $cookies);
//   loggedIn.value = false;
//   return false;
// };
if (sessionStorage.getItem("loggedIn")) {
  loginUser.value = {
    message: "",
    token: sessionStorage.getItem("token"),
    username: sessionStorage.getItem("username"),
  };
  userProfile.value = {
    id: null,
    username: null,
    nickname: sessionStorage.getItem("nickname"),
    email: null,
    comment: null,
  };
  loggedIn.value = true;
  console.log("初期 in");
} else {
  loggedIn.value = false;
  console.log("初期 out");
}

let meta = document.createElement("meta");
meta.name = "description";
meta.content =
  "<meta> 要素は、名前と値のペアで文書のメタデータを提供するのに使用できます。name 属性はメタデータの名前を与え、content 属性は値を与えます。";
// document.head.appendChild(meta);
// meta.name = "login";
// meta.content = loggedIn.value ? "Yes" : "No";
// document.head.appendChild(meta);

// CSRFトークンをmetaタグから取得
// console.log(window.document.querySelector);
// const csrfToken = document.querySelector!('meta[name="csrf-token"]').getAttribute('content');
// console.log("csrfToken: " + csrfToken)
// axios.defaults.headers.common["X-CSRFToken"] =
//   "H9gUwclzvtuWmkOdWs4XPGVPjgE8A2E3";
// インスタンス作成する場合
// const baseURL =  'https://jsonplaceholder.typicode.com';
// const headers = {
//    Authorization: `Bearer ${token_id}`
// }
// const axiosInstance = axios.create({
//   baseURL,
//   headers,
// });

// ログイン
async function login(isActive: { value: boolean }) {
  console.log("login" + isActive.value);
  await axios
    .post("/api/accounts/login/", {
      username: loginParam.value!.username,
      password: loginParam.value!.password,
    })
    .then((response: AxiosResponse<User>) => {
      loginUser.value = response.data;
      console.log("Set-Cookie:" + response.headers["content-type"]);
      console.log("Set-Cookie:" + response.headers["Set-Cookie"]);
      // axios.defaults.headers.common["X-CSRFToken"] =
      //   response.headers["Set-Cookie"];
      loginParam.value = { username: null, password: null };

      loggedIn.value = true;
      // ユーザー情報取得
      getUserInfo();
    })
    .catch((error: AxiosError) => {
      alert("ログインでエラーが発生しました\n" + error.message);
      console.log(error.message);
      return;
    });

  isActive.value = !isActive.value;
}

// ログアウト
function logout(isActive: { value: boolean }) {
  console.log("logout");
  const headers = {
    Authorization: `token ${loginUser.value?.token}`,
  };
  const axiosInstance = axios.create({
    baseURL,
    headers,
  });
  axiosInstance
    .post("/api/accounts/logout/", {})
    .then((response: AxiosResponse) => {
      let text = response.data;
      console.log(text);
      loggedIn.value = false;
    })
    .catch((error: AxiosError) => {
      alert("エラーが発生しました\n" + error.message);
      console.log(error.message);
    });
  isActive.value = !isActive.value;
}

// ユーザー情報取得
async function getUserInfo() {
  console.log("getUserInfo");
  await axios
    .get("/api/accounts/profile/", { withCredentials: true })
    .then((response: AxiosResponse<UserProfile>) => {
      userProfile.value = response.data;
      sessionStorage.setItem("nickname", userProfile.value!.nickname!);
      console.log("userProfile:" + userProfile.value);
    })
    .catch((error: AxiosError) => {
      alert("ユーザー情報取得でエラーが発生しました\n" + error.message);
      console.log(error.message);
    });
}
</script>

<template>
  <v-app>
    <v-system-bar color="grey-lighten-4"> System Bar </v-system-bar>
    <v-app-bar color="teal-accent-1" dark app>
      <template v-slot:prepend>
        <v-app-bar-nav-icon
          variant="text"
          @click.stop="drawer = !drawer"
        ></v-app-bar-nav-icon>
      </template>
      <v-app-bar-title>Application</v-app-bar-title>
      <v-spacer></v-spacer>
      <template v-slot:append>
        <v-btn text to="/"><v-icon>mdi-home</v-icon>Home</v-btn>
        <v-btn text to="/test">test</v-btn>
        <v-dialog max-width="420">
          <template v-slot:activator="{ props: activatorProps }">
            <v-btn
              v-bind="activatorProps"
              color="surface-variant"
              variant="flat"
              >{{ loggedIn ? "Sign out" : "Sign in" }}</v-btn
            >
          </template>
          <template v-slot:default="{ isActive }">
            <v-sheet>
              <v-sheet class="my-2 mx-5">
                <!-- <div class="form-example"></div> -->
                <br />
                <h2>
                  {{ loggedIn ? "サインアウトします" : "サインイン" }}
                </h2>
                <br />
                <!-- <v-spacer></v-spacer> -->
                <form
                  class="my-4"
                  v-if="!loggedIn"
                  @submit.prevent="login(isActive)"
                >
                  <div class="form-example">
                    <label for="name">user ID</label>
                    <v-text-field
                      id="userId"
                      required
                      placeholder="半角英数字"
                      v-model="loginParam.username"
                    />
                    <label for="name">password</label>
                    <v-text-field
                      id="password"
                      required
                      placeholder="半角英数字・記号"
                      v-model="loginParam.password"
                    />
                  </div>
                  <div class="text-center">
                    <v-btn
                      type="submit"
                      color="primary"
                      block
                      text="送信"
                    ></v-btn>
                  </div>
                  <!-- <v-text-field
                    v-model="loginParam.username"
                    required
                    placeholder="ユーザーID"
                  /> -->
                  <!-- <v-spacer></v-spacer> -->
                  <!-- <v-text-field
                    v-model="loginParam.password"
                    required
                    placeholder="半角英数字・半角記号で入力"
                  /> -->
                  <!-- <div class="text-center"> -->
                  <!-- <v-btn
                      color="primary"
                      block
                      text="Enter"
                      @click="login(isActive)"
                    ></v-btn> -->
                  <!-- </div> -->
                </form>
                <v-spacer></v-spacer>
                <div class="text-center">
                  <v-btn
                    v-if="loggedIn"
                    color="primary"
                    block
                    text="OK"
                    @click.prevent="logout(isActive)"
                  ></v-btn>
                </div>
                <br />
                <div class="text-center">
                  <!-- <v-btn text="取得" @click.prevent="getUserInfo"></v-btn> -->
                </div>
                <v-btn
                  text="Cancel"
                  @click.prevent="isActive.value = !isActive.value"
                ></v-btn>
              </v-sheet>
            </v-sheet>
          </template>
        </v-dialog>
        <v-avatar v-if="loggedIn" color="secondary">
          {{ userProfile.nickname }}
        </v-avatar>
      </template>
    </v-app-bar>
    <v-navigation-drawer v-model="drawer" permanent>
      <!-- <v-list @click:select="login(true)"> -->
      <v-list>
        <v-list-item
          prepend-icon="mdi-view-dashboard"
          title="Home"
          value="home"
          to="/"
        ></v-list-item>
        <v-list-item
          prepend-icon="mdi-forum"
          title="About"
          value="about"
        ></v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-main>
      <router-view />
    </v-main>
    <v-footer color="grey" dark app class="justify-center">
      Django Startup - Step3
    </v-footer>
  </v-app>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
