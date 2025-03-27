---
parent: Connecting to LLMs
nav_order: 560
---

# Amazon Bedrock

Aider can connect to models provided by Amazon Bedrock.
You will need to have an AWS account with access to the Bedrock service.

To configure Aider to use the Amazon Bedrock API, you need to set up your AWS credentials.
This can be done using the AWS CLI or by setting environment variables.

## 选择Amazon Bedrock模型

在通过Amazon Bedrock使用模型之前，您必须在AWS管理控制台的**模型访问权限**屏幕下"启用"该模型。
要查找`模型ID`，请打开Bedrock控制台中的**模型目录**区域，选择您要使用的模型，
然后在"使用情况"标题下找到`modelId`属性。

### Bedrock推理配置文件

Amazon Bedrock新增了对[跨区域"推理配置文件"](https://aws.amazon.com/about-aws/whats-new/2024/09/amazon-bedrock-knowledge-bases-cross-region-inference/)的支持。
Bedrock中托管的某些模型_仅_支持这些推理配置文件。
如果您使用的是这些模型之一，则需要使用AWS管理控制台**模型目录**屏幕中的`推理配置文件ID`
而不是`模型ID`。
例如，2025年2月发布的Claude Sonnet 3.7模型仅支持通过推理配置文件进行推理。
要使用此模型，您需要使用`us.anthropic.claude-3-7-sonnet-20250219-v1:0`推理配置文件ID。
在Amazon Bedrock控制台中，前往"推理和评估 ➡️ 跨区域推理"以找到`推理配置文件ID`值。

如果您尝试为仅支持推理配置文件功能的模型使用`模型ID`，将收到类似以下的错误消息：

> litellm.BadRequestError: BedrockException - b'{"message":"Invocation of model ID
anthropic.claude-3-7-sonnet-20250219-v1:0 with on-demand throughput isn\xe2\x80\x99t supported. Retry your
request with the ID or ARN of an inference profile that contains this model."}'

## AWS CLI配置

如果您尚未安装，请安装[AWS CLI](https://aws.amazon.com/cli/)并使用您的凭证进行配置：

```bash
aws configure
```

这将提示您输入AWS访问密钥ID、秘密访问密钥和默认区域。

## 环境变量

或者，您可以设置以下环境变量：

```bash
export AWS_REGION=your_preferred_region

# 用于用户身份验证
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key

# 用于配置文件身份验证
export AWS_PROFILE=your-profile
```

您可以将这些添加到您的
[.env文件](/docs/config/dotenv.html)中。

## 安装boto3

AWS Bedrock提供程序需要`boto3`包才能正常工作：

```bash
pip install boto3
```

要通过`pipx`安装的aider使用AWS Bedrock，您必须通过运行以下命令将`boto3`依赖项添加到aider的虚拟环境中

```bash
pipx inject aider-chat boto3
```

您必须通过运行以下命令将`boto3`依赖项安装到通过一键安装或uv安装的aider的虚拟环境中

```bash
uv tool run --from aider-chat pip install boto3
```


## 使用Bedrock运行Aider

设置好AWS凭证后，您可以使用`--model`命令行开关运行Aider，指定要使用的Bedrock模型：

```bash
aider --model bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0
```

有时候在模型名称前加上"us."似乎会有所帮助：

```bash
aider --model bedrock/us.anthropic.claude-3-5-sonnet-20240620-v1:0
```


## 可用模型

要查看通过Bedrock可用的模型，请运行：

```bash
aider --list-models bedrock/
```

在尝试使用这些模型与Aider一起使用之前，请确保您的AWS账户中已启用对这些模型的访问权限。

# 更多信息

有关Amazon Bedrock及其模型的更多信息，请参阅[AWS官方文档](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html)。

另请参阅
[关于Bedrock的litellm文档](https://litellm.vercel.app/docs/providers/bedrock)。
