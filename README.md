# RBAC 权限管理系统

一个基于 FastAPI 和 SQLAlchemy 开发的现代化 RBAC（基于角色的访问控制）权限管理系统，使用异步数据库操作和 JWT 认证。

## 🚀 项目特性

### 核心功能
- **用户管理** - 创建、查询、激活/禁用用户
- **角色管理** - 角色的增删改查和角色权限分配
- **权限管理** - 精细化权限控制和权限描述
- **RBAC 权限控制** - 基于角色的访问控制中间件
- **JWT 身份认证** - 安全的令牌认证机制
- **数据库迁移** - 使用 Alembic 进行版本管理
- **全局异常处理** - 统一的错误响应格式
- **异步数据库操作** - 高性能异步 ORM 操作

### 技术特性
- **异步架构** - 完全异步的 FastAPI 应用
- **现代化开发** - Python 3.12+ 和类型注解
- **配置管理** - 基于环境变量的配置
- **日志系统** - 结构化日志记录
- **SQLAlchemy 2.0** - 最新的 ORM 版本和语法

## 🛠️ 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| **FastAPI** | ≥0.128.0 | Web 框架 |
| **SQLAlchemy** | ≥2.0.45 | 异步 ORM |
| **aiosqlite** | ≥0.22.1 | 异步 SQLite 驱动 |
| **python-jose** | ≥3.5.0 | JWT 令牌处理 |
| **passlib** | ≥1.7.4 | 密码加密 |
| **Alembic** | ≥1.17.2 | 数据库迁移 |
| **Uvicorn** | ≥0.40.0 | ASGI 服务器 |
| **Pydantic** | ≥2.12.5 | 数据验证 |

## 📁 项目架构

### 目录结构

```
rbacscaffold/
├── app/                          # 应用核心代码
│   ├── __init__.py
│   ├── config.py                 # 应用配置
│   ├── auth/                     # 认证模块
│   │   ├── controllers.py        # 认证业务逻辑
│   │   ├── routers.py           # 认证路由
│   │   ├── schemas.py           # 认证数据模型
│   │   └── service.py           # 认证服务
│   ├── core/                     # 核心功能
│   │   ├── apis.py              # API 路由聚合
│   │   ├── database.py          # 数据库配置和会话管理
│   │   ├── exception_handler.py # 全局异常处理
│   │   ├── logging.py           # 日志配置
│   │   ├── logging_config.py    # 日志详细配置
│   │   ├── rbac.py              # RBAC 权限中间件
│   │   └── security.py          # 安全工具（JWT、密码加密）
│   ├── user/                     # 用户模块
│   │   ├── controllers.py       # 用户业务逻辑
│   │   ├── models.py            # 用户数据模型
│   │   ├── routers.py           # 用户路由
│   │   ├── schemas.py           # 用户数据模型
│   │   └── service.py           # 用户服务层
│   ├── role/                     # 角色模块
│   │   ├── controllers.py       # 角色业务逻辑
│   │   ├── models.py            # 角色数据模型
│   │   ├── routers.py           # 角色路由
│   │   └── schemas.py           # 角色数据模型
│   ├── permission/               # 权限模块
│   │   ├── controllers.py       # 权限业务逻辑
│   │   ├── models.py            # 权限数据模型
│   │   ├── routers.py           # 权限路由
│   │   └── schemas.py           # 权限数据模型
│   ├── user_role/                # 用户-角色关联
│   │   └── models.py            # 用户角色关联模型
│   └── role_permission/          # 角色-权限关联
│       └── models.py            # 角色权限关联模型
├── alembic/                      # 数据库迁移
│   ├── versions/                # 迁移文件
│   ├── env.py                   # Alembic 配置
│   ├── script.py.mako           # 迁移脚本模板
│   └── README
├── main.py                       # 应用入口
├── pyproject.toml               # 项目配置和依赖
├── uv.lock                      # 依赖锁定文件
├── .env                         # 环境变量配置
├── .gitignore                   # Git 忽略文件
├── .python-version              # Python 版本指定
├── alembic.ini                  # Alembic 配置
└── README.md                    # 项目文档
```

### 设计细节

#### 项目层级

- 应用内：
    - `models.py` - 数据模型模块, 包含所有数据库模型
    - `schemas.py` - 数据验证模型模块, 包含所有数据验证模型
    - `routers.py` - 路由模块, 包含所有路由定义
    - `controllers.py` - 控制器模块, 包含所有业务逻辑,这里允许schema数据传入
    - `service.py` - 服务层模块, 包含所有服务逻辑,主要负责数据库操作,这里不允许schema数据传入,只允许数据库模型数据

#### 日志

- 使用 Python 标准库 `logging` 模块
- 日志默认输出到 `logs/` 目录下，文件名为 `app.log`
- 日志配置文件为 `logging_config.py`，包含日志级别、格式、输出位置等
  - formatters字段定义了两种日志格式：
    - `access` - 访问日志格式
    - `app` - 应用日志格式
  - handlers字段定义日志处理方式
    - class 字段指定日志处理类，例如`logging.StreamHandler`、`logging.handlers.TimedRotatingFileHandler`等
    - filename 字段指定日志文件路径，例如`logs/app.log`
    - formatter 字段指定日志格式,来自formatters配置，例如`standard`或`access`
    - when 字段指定日志文件分割时间，例如`midnight`表示每天凌晨分割
    - backupCount 字段指定保留的日志文件数量，例如14表示保留14天的日志文件
    - encoding 字段指定日志文件编码，例如`utf-8`
    - level 字段指定日志级别，例如DEBUG、INFO、WARNING、ERROR、CRITICAL等
  - loggers字段定义日志记录器：
    - 可以覆盖默认的日志记录器，例如`uvicorn.access`、`uvicorn.error`以及`sqlalchemy.engine`等
    - 可以通过handlers字段配置日志处理方式，例如文件处理、控制台处理等
    - 可以通过level字段配置日志级别，例如DEBUG、INFO、WARNING、ERROR、CRITICAL等
    - 如果propagate为True, 则会将日志传递给父记录器, 否则不会传递
  - root字段定义了根日志记录器

- 覆盖uvicorn默认日志配置, 使uvicorn日志与应用日志保持一致
- 日志格式有两种：
  - access.log - 访问日志，记录每个请求的详细信息
  - app.log - 应用日志，记录应用运行时的信息
  - 格式化参数：
    - `%(asctime)s` - 日志记录时间
    - `%(levelname)s` - 日志级别
    - `%(module)s` - 记录日志的模块名
    - `%(message)s` - 日志消息
    - `%(name)s` - 日志记录器名称, 即使用`logging.getLogger(__name__)`获取的名称
  
#### 异常处理

- 位于`app.core.exception_handler`模块中
    - 定义了`AppException`基类,可以指定status_code属性, 用于HTTP响应状态码
    - 定义了`generate_exception_handler`函数,用于生成异常处理函数,会将`AppException`的异常处理为HTTP响应, 状态码为`AppException.status_code`; 其他异常会处理为500 Internal Server Error
    - 若需要自定义其他异常的处理, 可以继承`AppException`类, 并指定自定义的status_code属性
    - 自定义异常处理函数的示例：
        ```python
        class CustomException(AppException):
            pass
        ```

### 数据模型关系

```
User (用户) ←→ UserRoleAssignment ←→ Role (角色) ←→ RolePermissionAssignment ←→ Permission (权限)
     ↓                                  ↓                                  ↓
  [多对多关系]                     [多对多关系]                       [多对多关系]
```

- **User** - 用户实体，包含用户名、密码哈希、激活状态
- **Role** - 角色实体，包含角色名称和描述
- **Permission** - 权限实体，包含权限名称和描述
- **UserRoleAssignment** - 用户-角色关联表
- **RolePermissionAssignment** - 角色-权限关联表

## 🔧 快速开始

### 前置要求

- Python 3.12+
- uv（推荐）或 pip

### 1. 克隆项目

```bash
git clone <repository-url>
cd rbacscaffold
```

### 2. 安装 uv（推荐）

```bash
# macOS
brew install uv

# 或者使用 pip 安装
pip install uv
```

### 3. 创建虚拟环境并安装依赖

```bash
# 使用 uv（推荐）
uv venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate  # Windows

uv sync
```

或者使用传统的 Python venv：

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### 4. 环境配置

复制环境变量模板：

```bash
cp .env.example .env
```

或者直接使用现有的 `.env` 文件：

```bash
# .env 文件内容
APP_NAME=RBAC Demo
DATABASE_URL=sqlite+aiosqlite:///./rbac.db
SECRET_KEY=super-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 5. 初始化数据库

```bash
# 运行数据库迁移
alembic upgrade head
```

### 6. 启动应用

```bash
# 开发模式
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 或者直接运行
python main.py
```

访问 http://localhost:8000 查看 API 文档。

## 📚 API 文档

启动应用后，可以访问以下端点：

- **Swagger UI** - http://localhost:8000/docs
- **ReDoc** - http://localhost:8000/redoc

### 主要 API 端点

| 模块 | 端点 | 方法 | 描述 |
|------|------|------|------|
| 认证 | `/auth/login` | POST | 用户登录 |
| 认证 | `/auth/register` | POST | 用户注册 |
| 用户 | `/users` | GET | 获取用户列表 |
| 用户 | `/users` | POST | 创建用户 |
| 角色 | `/roles` | GET | 获取角色列表 |
| 角色 | `/roles` | POST | 创建角色 |
| 权限 | `/permissions` | GET | 获取权限列表 |
| 权限 | `/permissions` | POST | 创建权限 |

## 🔐 认证和授权

### JWT 认证流程

1. **注册/登录** - 用户提供用户名和密码
2. **获取令牌** - 服务器返回 JWT 访问令牌
3. **令牌使用** - 在请求头中包含 `Authorization: Bearer <token>`
4. **权限验证** - 服务器验证令牌和用户权限

### 权限控制

```python
# 示例：需要特定权限的端点
@router.post("/", response_model=UserResponse)
async def create_user(
    user_in: UserCreate,
    current_user: User = Depends(get_current_active_user),
    _: bool = Depends(verify_permission("create_user"))
):
    return await controllers.create_user(db, user_in)
```

## 🗄️ 数据库迁移

### 创建新迁移

```bash
alembic revision --autogenerate -m "描述变更"
```

### 应用迁移

```bash
alembic upgrade head
```

### 回滚迁移

```bash
alembic downgrade -1
```

## 📊 日志配置

项目使用结构化日志系统：

- **应用日志** - 记录到 `logs/app.log`
- **访问日志** - 记录到 `logs/access.log`
- **错误日志** - 记录到 `logs/error.log`

日志级别可以通过环境变量配置。

## 🧪 测试

```bash
# 运行测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=app
```

## 🚀 部署

### Docker 部署

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 生产环境配置

```bash
# 使用 Gunicorn 部署
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 📝 开发规范

### 代码风格

- 遵循 PEP 8 代码规范
- 使用 Black 进行代码格式化
- 使用 isort 进行导入排序
- 使用 mypy 进行类型检查

### 提交规范

- 使用 Conventional Commits 规范
- feat: 新功能
- fix: 修复
- docs: 文档更新
- style: 代码格式
- refactor: 重构
- test: 测试
- chore: 构建/工具相关

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🆘 支持

如果您在使用过程中遇到问题，请：

1. 查看 [FAQ](docs/FAQ.md)
2. 搜索现有的 [Issues](../../issues)
3. 创建新的 [Issue](../../issues/new)

## 🎯 路线图

- [ ] Redis 缓存支持
- [ ] 微服务架构改造
- [ ] 单元测试覆盖
- [ ] API 限流功能
- [ ] 多租户支持
- [ ] 审计日志功能

---

**注意**: 这是一个演示项目，仅用于学习和参考目的。在生产环境中使用前，请确保进行充分的安全评估和测试。