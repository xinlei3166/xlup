export const baseurl = process.env.VUE_APP_DOMAIN

export const loginUrl = `${baseurl}/auth`
export const refreshTokenUrl = `${baseurl}/auth/refresh_token`
export const logoutUrl = `${baseurl}/auth/logout`
export const userMeUrl = `${baseurl}/users/me`
export const userMeAccessKeyUrl = `${baseurl}/users/me/access_key`

export const picUrl = `${baseurl}/pics`
export const videoUrl = `${baseurl}/videos`

export const userAdminUrl = `${baseurl}/admin/users`
export const picAdminUrl = `${baseurl}/admin/pics`
export const videoAdminUrl = `${baseurl}/admin/videos`




