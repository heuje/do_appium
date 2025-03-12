# 选择支持多架构的 Python 基础镜像
FROM --platform=$TARGETPLATFORM public.ecr.aws/docker/library/python:3.10-bookworm

LABEL author="heujeatqq.com"

# 设置环境变量
ENV ALLURE_VERSION=2.31.0
ENV ANDROID_SDK_ROOT=/opt/android-sdk
ENV PATH="${ANDROID_SDK_ROOT}/cmdline-tools/latest/bin:${ANDROID_SDK_ROOT}/platform-tools:${ANDROID_SDK_ROOT}/emulator:${PATH}"

# 安装依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget curl unzip tar \
    openjdk-17-jdk nodejs npm adb git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 下载并安装 Android SDK Command Line Tools
RUN mkdir -p ${ANDROID_SDK_ROOT}/cmdline-tools && \
    cd ${ANDROID_SDK_ROOT}/cmdline-tools && \
    curl -o sdk-tools.zip https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip && \
    unzip sdk-tools.zip -d ${ANDROID_SDK_ROOT}/cmdline-tools && \
    mv ${ANDROID_SDK_ROOT}/cmdline-tools/cmdline-tools ${ANDROID_SDK_ROOT}/cmdline-tools/latest && \
    rm sdk-tools.zip

# 安装 Android SDK 组件（使用国内源）
RUN yes | sdkmanager --sdk_root=${ANDROID_SDK_ROOT} \
        "platform-tools" \
        "platforms;android-33" \
        && sdkmanager --licenses

# 安装 Appium
RUN npm config set registry https://registry.npmmirror.com \
    && npm install -g appium@latest \
    && npm cache clean --force


CMD ["sh", "-c", "appium"]
