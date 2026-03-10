# Client Web 目录说明

`apps/client-web/` 当前已升级为标准前端项目结构（Vue + Vite），用于演示“客户端本地调用模型后回传结果”的接入链路。当前阶段仍以接入验证为主，后续再扩展上传、任务列表、结果详情与报告下载。

## 当前能力

- 读取客户端接入配置：`GET /api/client/access/profile`
- 查看可用模型清单（后端下发）
- 回传本地推理结果摘要：`POST /api/client/access/reports`

## 启动方式

在 `apps/client-web/` 目录下执行：

```bash
npm install
npm run dev
```

默认端口：`5180`

环境变量模板：`apps/client-web/.env.example`

访问地址：

```text
http://127.0.0.1:5180
```

说明：当前已采用 `src/ + api/ + assets/` 的标准前端结构，后续可继续扩展登录、任务列表、结果查看与报告下载能力。

## 构建与部署

- 当前生产构建命令：`npm run build`
- Dockerfile：`apps/client-web/Dockerfile`
- 若客户端独立域名部署，可在构建前调整 `VITE_API_BASE_URL`
