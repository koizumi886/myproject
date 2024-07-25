const { defineConfig } = require('@vue/cli-service')
// import { defineConfig } from "@vue/cli-service";
module.exports = defineConfig({
  publicPath: "/",
  outputDir: "../dist",
  assetsDir: "static",
  indexPath: "../templates/index.html",
  transpileDependencies: true,

  devServer: {
    host: "localhost",
    hot: "only",
    proxy: {
      "^/api": {
        target: "http://localhost:8080",
        changeOrigin: true,
      },
    },
  },

  chainWebpack: config => {
  config.module
    .rule('vue')
    .use('vue-loader')
    .loader('vue-loader')
    .tap(options => {
      options.compilerOptions = {
        whitespace: 'condense',
        delimiters: ['{{', '}}']
      };
      return options;
    });
  },

  pluginOptions: {
    vuetify: {
			// https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vuetify-loader
		}
  }
})
