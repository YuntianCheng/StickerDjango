/* eslint-disable */
// https://cli.vuejs.org/config/
module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      },
    },
    before: app => {
      // app is an express instance
    },
  },

  lintOnSave: true,
  assetsDir: 'static'
}
