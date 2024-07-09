<template>
  <v-container class="hello">
    <div class="title-color">d [[ text ]] b</div>
    <v-img
      :src="require('../assets/logo.svg')"
      class="my-3"
      contain
      height="200"
    />
    <v-btn @click="submit"> Submit </v-btn>
    {{ message }}
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: "OneView",
  props: {
    msg: String,
  },
  data() {
    return {
      text: null,
      message: "",
    };
  },
  methods: {
    submit() {
      this.message = "submit";
    },
    cancel() {
      this.message = "cancel";
    },
  },
  mounted() {
    axios
      .get("http://localhost:8000/api/v1/sample/")
      .then((response) => (this.text = response.data))
      .then((response) => {
        console.log("status:", response.status);
        console.log("axiosGetData:", response.data);
      })
      .catch((err) => {
        console.log("axiosGetErr", err);
      });
  },
};
</script>

<style scoped>
.title-color {
  color: green;
}
</style>
