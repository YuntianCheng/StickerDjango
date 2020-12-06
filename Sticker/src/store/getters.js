/* eslint-disable */
const getters = {
  errorCount: state => state.log.errorList.length,
  messageUnreadCount: state => state.message.unreadCount,
  messageReadedCount: state => state.message.readCount,
  messageTrashCount: state => state.message.trashCount,
  uvo: state => state.user.uvo,
  orgName: state => state.org.orgName,
  userId: state => state.user.userId,
  roleId: state => state.user.roleId,
  defaultAvatar: state => state.user.defaultAvatar,
  avatar: state => state.user.avatar,
  access: state => state.user.access,
  menu: state => state.user.menu,
  footerShow: state => state.setting.footerShow,
  token: state => state.user.token,
  refresh_token: state => state.user.refresh_token,
  screenWidth: state => state.app.screenWidth,
  widthThreshold: state => state.app.widthThreshold,
  siteId: state =>state.setting.siteId,
  startDate: state => state.setting.startDate,
  endDate: state => state.setting.endDate,
  hasResetPass: state => state.user.hasResetPass,
  infoReload: state => state.info.infoReload,
  platCenterDeptAccess: state => state.platcenter.platCenterDeptAccess,
  collapsed: state => state.setting.collapsed,
  categoryCode: state=> state.org.categoryCode,
  cstrId: state => state.org.cstrId,
  orgInfo:state=> state.org.org
};
export default getters

