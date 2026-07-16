# 贡献指南 (Contributing Guide)

感谢你对 OpenCode 中文汉化项目的关注和贡献！为了保持项目代码质量和协作效率，请遵守以下规范。

## 核心架构变更说明

从 v7.3 开始，本项目已全面迁移到 **Go 语言** 开发的 CLI 管理工具。旧的 Node.js/JavaScript 脚本 (`scripts/`) 已被标记为过时，并移入 `legacy/` 目录。

新的 CLI 源码位于 `cli-go/` 目录。

---

## 开发环境搭建

### 1. 基础要求
*   **Go**: v1.21+ (推荐 v1.25+)
*   **Git**: 用于版本控制
*   **Node.js 18+** / **Bun 1.3.8+** (可选): 仅当需要编译 OpenCode 源码时需要

### 2. 目录结构

CLI 统一使用 `~/.opencode-i18n/` 目录：

```
~/.opencode-i18n/
├── bin/              # CLI 工具和 OpenCode 可执行文件
├── opencode/         # OpenCode 源码
└── build/            # 编译输出
```

**本地开发时**，可通过环境变量覆盖：
```bash
export OPENCODE_SOURCE_DIR=/path/to/opencode   # 覆盖源码目录
export OPENCODE_BUILD_DIR=/path/to/bin         # 覆盖编译输出
```

汉化配置已内嵌到二进制文件中，无需外部文件。

### 3. 编译 CLI 工具

```bash
cd cli-go

# 编译当前平台版本
go build -o opencode-cli.exe .

# 运行测试
go test ./...
```

### 4. 交叉编译

我们提供了一键编译脚本：

```bash
# Windows
.\build.ps1

# macOS/Linux
./build.sh
```

---

## 汉化指南

从 v8.5+ 开始，汉化资源已内嵌到 CLI 工具中：

*   汉化 JSON 文件位于 `cli-go/internal/core/assets/opencode-i18n/` 目录下
*   修改后需要重新编译 CLI 工具才能生效
*   验证汉化配置：
    ```bash
    opencode-cli verify --detailed
    ```
*   JSON 文件格式要求：无注释，UTF-8 编码

---

## Git 提交规范 (Commit Convention)

我们遵循 [Angular Commit Message Guidelines](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit) 规范。

```
<type>(<scope>): <subject>
```

### Type (类型)
*   **feat**: 新功能 (A new feature)
*   **fix**: 修补 Bug (A bug fix)
*   **docs**: 文档修改 (Documentation only changes)
*   **style**: 代码格式修改 (Changes that do not affect the meaning of the code)
*   **refactor**: 代码重构 (A code change that neither fixes a bug nor adds a feature)
*   **perf**: 性能优化 (A code change that improves performance)
*   **test**: 测试相关 (Adding missing tests or correcting existing tests)
*   **build**: 构建系统或外部依赖变更 (Changes that affect the build system or external dependencies)
*   **ci**: CI 配置文件或脚本修改 (Changes to our CI configuration files and scripts)
*   **chore**: 其他变动 (Other changes that don't modify src or test files)

### Scope (范围)
*   `cli`: Go CLI 工具相关
*   `i18n`: 汉化文件相关
*   `docs`: 文档相关
*   `ci`: GitHub Actions 相关

### 示例
```
feat(cli): add shortcut creation support for deploy command
fix(i18n): correct translation for search panel
docs: update installation guide for go cli
chore: cleanup legacy scripts
```

---

## 版本管理

版本号由 `cli-go/internal/core/version.go` 中的 `VERSION` 常量统一管理：

```go
const VERSION = "8.6.0"
```

发布新版本时：
1. 更新 `cli-go/internal/core/version.go` 中的 `VERSION` 常量
2. 更新 `CHANGELOG.md` 添加版本说明
3. 提交并打上对应的 git tag（如 `v8.2.0`）
4. GitHub Actions 会自动触发构建并发布 Release

---

## CI/CD 工作流

本项目使用 GitHub Actions 实现自动化构建：

### Release (正式发布)

*   **文件**: `.github/workflows/release.yml`
*   **触发条件**:
    *   Schedule: 每 30 分钟检测上游 `anomalyco/opencode` 新 release
    *   Push: 推送 `v*` 格式的 Tag
    *   Workflow Dispatch: 手动指定 `upstream_tag` 和 `release_tag`
*   **产物**: 正式版 Release，包含三平台二进制文件

```bash
# 检测上游最新 release 并构建（默认检测到新版本自动执行）
# 手动触发构建指定版本
gh workflow run release.yml -f upstream_tag=v1.18.2

# 手动触发并指定发布 tag
gh workflow run release.yml -f upstream_tag=v1.18.2 -f release_tag=v1.18.2
```

**构建逻辑：**

1. Schedule 触发时检查 `anomalyco/opencode` 的最新 release tag
2. 与本地记录的 tag 对比，有新 tag 时触发构建
3. 构建完成后：
   - 生成包含上游更新日志的 Release Notes
   - 发布 tag（如 `v1.18.2`）
   - 后续 schedule 检测到更新的 tag 时继续构建

---

再次感谢你的贡献！
