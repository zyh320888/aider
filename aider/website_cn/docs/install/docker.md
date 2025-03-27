---
parent: 安装
nav_order: 100
---

# 使用Docker的Aider

Aider提供了2个docker镜像：

- `paulgauthier/aider` 安装aider核心版，这是一个较小的镜像，适合快速开始使用。
- `paulgauthier/aider-full` 安装带有所有可选附加功能的aider完整版。

完整版镜像支持交互式帮助、浏览器GUI和使用Playwright抓取网页等功能。
核心版镜像也可以使用这些功能，但需要在首次访问时进行安装。
由于容器是临时的，下次启动aider核心版容器时，这些附加功能需要重新安装。

### Aider核心版

```
docker pull paulgauthier/aider
docker run -it --user $(id -u):$(id -g) --volume $(pwd):/app paulgauthier/aider --openai-api-key $OPENAI_API_KEY [...其他aider参数...]
```

### 完整版

```
docker pull paulgauthier/aider-full
docker run -it --user $(id -u):$(id -g) --volume $(pwd):/app paulgauthier/aider-full --openai-api-key $OPENAI_API_KEY [...其他aider参数...]
```

## 如何使用

你应该在git仓库的根目录下运行上述命令，因为`--volume`参数将你当前的目录映射到docker容器中。
因此，你需要在git仓库的根目录下运行，这样aider才能看到仓库及其所有文件。

你应该确保你的git仓库配置包含你的用户名和邮箱，因为docker容器不会有你的全局git配置。
在执行`docker run`命令之前，在你的git仓库中运行以下命令：

```
git config user.email "you@example.com"
git config user.name "Your Name"
```


## 限制

- 当你使用聊天中的`/run`命令时，它将在docker容器内部运行shell命令。所以这些命令不会在你的本地环境中运行，这可能会使为你的项目`/run`测试等操作变得复杂。
- 除非你能想办法让docker容器访问你的主机音频设备，否则`/voice`命令将无法工作。容器已安装libportaudio2，所以如果你能实现这一点，它应该可以工作。
