# 基础镜像：使用 Python 3.10 Bookworm
FROM public.ecr.aws/docker/library/python:3.10-bookworm

LABEL author="heujeatqq.com"

# 设置环境变量
ENV ALLURE_VERSION=2.31.0
# 使用 Debian Bookworm 推荐的 OpenJDK 版本
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV ANDROID_SDK_ROOT=/opt/android-sdk
# 合并 JAVA 和 Android SDK 路径到 PATH
ENV PATH="${JAVA_HOME}/bin:${ANDROID_SDK_ROOT}/emulator:${ANDROID_SDK_ROOT}/platform-tools:${ANDROID_SDK_ROOT}/cmdline-tools/latest/bin:${PATH}"

# ==================== 1. 设置 APT 源（使用国内镜像，加速更新和安装） ====================
RUN echo "deb http://mirrors.aliyun.com/debian bookworm main contrib non-free" > /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian bookworm-updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian-security bookworm-security main contrib non-free" >> /etc/apt/sources.list

# ==================== 2. 添加 Google Chrome 仓库 ====================
# 使用 curl 下载 Google 的 GPG 签名公钥，转换为 gpg 格式后保存到 /usr/share/keyrings
RUN curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list

# ==================== 3. 安装基础依赖 ====================
RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-utils \
    wget \
    gnupg \
    curl \
    unzip \
    libnss3 \
    libxss1 \
    libasound2 \
    fonts-liberation \
    libappindicator3-1 \
    lsb-release \
    xdg-utils \
    google-chrome-stable \
    openjdk-17-jdk \
    nodejs \
    npm \
    adb \
    awscli \
    git \
    qemu-system-aarch64 \
    libvirt-daemon-system \
    libvirt-clients \
    bridge-utils \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# ==================== 4. 安装 Chrome Driver ====================
RUN CHROME_DRIVER_VERSION=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget -q -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm /tmp/chromedriver.zip

# ==================== 5. 安装 Allure ====================
RUN wget -q -O /tmp/allure.zip https://github.com/allure-framework/allure2/releases/download/${ALLURE_VERSION}/allure-${ALLURE_VERSION}.zip && \
    unzip /tmp/allure.zip -d /opt/ && \
    ln -s /opt/allure-${ALLURE_VERSION}/bin/allure /usr/local/bin/allure && \
    rm /tmp/allure.zip

# ==================== 6. 验证 Python、Chrome 与 Allure ====================
RUN python --version && google-chrome --version && allure --version

# ==================== 7. 安装 Android SDK 命令行工具 ====================
RUN mkdir -p ${ANDROID_SDK_ROOT}/cmdline-tools && \
    cd ${ANDROID_SDK_ROOT}/cmdline-tools && \
    curl -o sdk-tools.zip https://googledownloads.cn/android/repository/commandlinetools-linux-11076708_latest.zip && \
    unzip sdk-tools.zip -d ${ANDROID_SDK_ROOT}/cmdline-tools && \
    mv ${ANDROID_SDK_ROOT}/cmdline-tools/cmdline-tools ${ANDROID_SDK_ROOT}/cmdline-tools/latest && \
    rm sdk-tools.zip

# 安装 Android SDK 组件（包括平台工具、Android 30 SDK、系统映像和模拟器）
RUN yes | sdkmanager --sdk_root=${ANDROID_SDK_ROOT} \
    "platform-tools" \
    "platforms;android-33" \
    "system-images;android-33;google_apis;arm64-v8a" \
    "emulator" \
    "cmdline-tools;latest" \
    && sdkmanager --licenses

# ==================== 8. 创建 Android 虚拟设备 (AVD) ====================
RUN echo "no" | avdmanager create avd -n test_avd -k "system-images;android-33;google_apis;arm64-v8a" --device "pixel_4"

# ==================== 9. 安装 Appium ====================
RUN npm config set registry https://registry.npmmirror.com && npm install -g appium@latest

# ==================== 10. 启动 Android 模拟器和 Appium ====================
# 使用 sh -c 启动 Android 模拟器（后台运行）并延时启动 Appium
CMD ["sh", "-c", "emulator -avd test_avd -no-window -no-audio & sleep 10 && appium &"]
