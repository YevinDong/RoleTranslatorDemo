# DOC

## 如何运行V0.1

1. 项目使用`uv`进行管理，如果没有全局安装`uv`，请先安装。
2. `uv sync`同步依赖
3. `langgraph dev`启动langsmith的开发服务（后期替换成RESTful api服务）
4. 浏览器中访问`https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024`
5. 在网页中`Input`的`User Input`中输入用户内容，点击`Submit`按钮

