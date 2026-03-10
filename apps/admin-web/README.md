# Admin Web 目录说明

`apps/admin-web/` 是基于 `Vue3 + Vite + TDesign Vue Next` 的管理端。当前已做一轮结构收敛，重点是减少配置分散、页面平铺和历史示例文件残留带来的混乱感。

## 当前技术栈

- `Vue 3`
- `Vite`
- `Vue Router`
- `TDesign Vue Next`

## 当前结构说明

- `src/api/`
  - 负责真实接口请求封装
  - `request.js`：统一请求入口
  - `platform.js`：平台接口方法集合

- `src/app/`
  - 负责应用级配置
  - `config/route-map.js`：页面路由与菜单来源配置
  - `config/navigation.js`：从路由映射派生出的导航结构
  - `router/`：前端路由实例

- `src/layouts/`
  - 放布局级组件
  - 当前主布局：`AdminLayout.vue`

- `src/pages/`
  - 按页面职责拆分页面目录
  - 当前包含：
    - `dashboard/`
    - `datasets/`
    - `training/`
    - `models/`
    - `testing/`
    - `settings/`

- `src/shared/`
  - 放通用复用能力
  - `components/common/`：通用展示组件
  - `utils/`：格式化与辅助函数

- `src/assets/`
  - 存放全局样式与静态资源

## 当前结构优化点

- 页面组件统一使用动态导入，确保懒加载
- 菜单结构从路由配置派生，避免两套配置重复维护
- 页面通过真实后端接口渲染，不再依赖原先的本地 mock 主流程
- 旧的 `views/`、零散 `config/`、历史 `mock.js` 已退出主结构

## 当前已搭建页面

- `登录页`
- `工作台`
- `数据集管理`
- `模型训练`
- `模型管理`
- `推理测试`
- `客户端接入管理`
- `文件资产`
- `审计日志`
- `系统设置`

## 启动方式

先在 `apps/admin-web/` 目录安装依赖：

```bash
npm install
```

说明：若遇到旧缓存或依赖残留问题，可删除当前目录下 `node_modules/` 与 Vite 缓存后重新执行 `npm install`。

然后启动开发环境：

```bash
npm run dev
```

默认开发端口：`5500`

当前默认登录账号：`admin / 1234`

环境变量模板：`apps/admin-web/.env.example`

## 后端联调说明

- 当前前端已接入 FastAPI 真实接口
- 开发环境默认通过 Vite 代理访问：`/api`
- Vite 代理实际转发到：`http://127.0.0.1:2048`
- 管理端接口统一走 `/api/admin/*`
- 鉴权接口统一走 `/api/auth/*`
- 系统接口统一走 `/api/overview`、`/api/settings`、`/api/health`
- 客户端接入管理页会调用 `/api/client/access/*`
- 配置文件：`apps/admin-web/.env.development`
- 若修改了 `apps/admin-web/.env.development`，需要重启前端开发服务才能生效

推荐顺序：

```bash
cd apps/api-server
python -m app.db.init_db
uvicorn app.main:app --host 127.0.0.1 --port 2048 --reload
cd ../admin-web
npm run dev
```

若从项目根目录直接启动后端，推荐使用：

```bash
.venv311\Scripts\python.exe -m uvicorn app.main:app --app-dir apps/api-server --host 127.0.0.1 --port 2048 --reload
```

## 当前定位

当前前端的重点是先把后台管理系统的基础链路跑通，后续继续补：

1. 数据集导入接口
2. 训练任务启动与日志接口
3. 模型列表与默认模型切换接口
4. 推理测试执行与结果详情接口

## 构建与部署

- 当前生产构建命令：`npm run build`
- Dockerfile：`apps/admin-web/Dockerfile`
- 若云上通过独立域名部署，可在构建前调整 `VITE_API_BASE_URL`
