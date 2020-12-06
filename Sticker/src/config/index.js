/* eslint-disable */
const baseUrl = {
  // dev: 'https://api.escience.org.cn',
  dev: '',
  pro: ''
};
const isDev = process.env.NODE_ENV === 'development'?true:false;
const url = isDev ? baseUrl.dev : baseUrl.pro;
export default {
  projectName: "表情包生成器",
  isDev: isDev,
  /**
   * 暴露一个api 的地址
   */
  url:url,
  /**
   * @description token在Cookie中存储的天数，默认1天
   */
  cookieExpires: 1,
  /**
   * @description 是否使用国际化，默认为false
   *              如果不使用，则需要在路由中给需要在菜单中展示的路由设置meta: {title: 'xxx'}
   *              用来在菜单中显示文字
   */
  useI18n: true,
  /**
   * @description api请求基础路径
   */
  baseUrl: baseUrl,
  /**
   * @description 默认打开的首页的路由name值，默认为home
   */
}
