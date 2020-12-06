import axios from 'axios'

class HttpRequest {
	constructor (baseUrl = baseURL) {
		this.baseUrl = baseUrl
        this.queue = {}
	}

	getInsideConfig () {
		const config = {
			baseURL: this.baseUrl,
			headers: {}
		}
		return config
	}

	destroy (url) {
		delete this.queue[url]
		// if (!Object.keys(this.queue).length) {
		//   Spin.hide()
		// }
	}

	interceptors (instance, url) {
		// 请求拦截
		instance.interceptors.request.use(config => {
			// 添加全局的loading...
			// if (!Object.keys(this.queue).length) {
			// Spin.show() // 不建议开启，因为界面不友好
			// }
			// const isToken = (config.headers || {}).isToken === false;
			// /* let token = store.getters.token; */
			// let token = Cookie.get('token')
			// if (token && !isToken) {
			// 	config.headers['Authorization'] = 'Bearer ' + token// token
			// }
			this.queue[url] = true;
			return config

		}, error => {
			return Promise.reject(error)
		})
		// 响应拦截
		instance.interceptors.response.use(res => {
			this.destroy(url)
			const {data, status, headers} = res
			return {data, status, headers}
		}, error => {
			this.destroy(url)
			let errorInfo = error.response;
			/* if (!errorInfo) {
				const {
				  request: {statusText, status},
          config
				} = JSON.parse(JSON.stringify(error));
				errorInfo = {
					statusText,
					status,
          data: {
            msg: statusText,
          },
          config: config,
					request: {responseURL: config.url}
				}
			} */
			// addErrorLog(errorInfo)
      if(status === 401) {
        window.location.reload();
      }
			return Promise.reject(error)
		})
	}

	request (options) {
		const instance = axios.create({
            //withCredentials: true
        })
		let insideConfig = this.getInsideConfig();
		options = Object.assign(insideConfig, options)
		this.interceptors(instance, options.url)
		return instance(options);
	}
}

export default HttpRequest
