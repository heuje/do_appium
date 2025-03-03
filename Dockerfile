# 使用官方 Python 3.10 Bookworm 作为基础镜像
FROM public.ecr.aws/docker/library/python:3.10-bookworm

LABEL author="heujeatqq.com"

# 设置环境变量
ENV ALLURE_VERSION=2.31.0
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"
ENV ANDROID_SDK_ROOT=/opt/android-sdk
ENV PATH="$ANDROID_SDK_ROOT/emulator:$ANDROID_SDK_ROOT/platform-tools:$ANDROID_SDK_ROOT/cmdline-tools/latest/bin:$PATH"
ENV CHROME_DRIVER_DIR=/usr/local/bin

# 更新系统并安装基本工具
RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-utils \
    wget \
    gnupg \
    curl \
    unzip \
    default-jre \
    libgconf-2-4 \
    libnss3 \
    libxss1 \
    libasound2 \
    fonts-liberation \
    libappindicator3-1 \
    lsb-release \
    xdg-utils \
    openjdk-17-jdk \
    nodejs \
    npm \
    adb && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 添加 Google Chrome 及其 GPG 签名密钥
RUN wget -q -O /usr/share/keyrings/google-chrome.gpg https://dl-ssl.google.com/linux/linux_signing_key.pub && \
    echo "deb [signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list && \
    apt-get update && apt-get install -y google-chrome-stable && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 安装 Chrome Driver（匹配 Chrome 版本）
RUN CHROME_VERSION=$(google-chrome --version | grep -oP '[0-9]+\.[0-9]+\.[0-9]+') && \
    CHROME_DRIVER_VERSION=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION) && \
    wget -q -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d $CHROME_DRIVER_DIR && \
    chmod +x $CHROME_DRIVER_DIR/chromedriver && \
    rm /tmp/chromedriver.zip

# 安装 Allure
RUN wget -q https://github.com/allure-framework/allure2/releases/latest/download/allure-$ALLURE_VERSION.zip -O /tmp/allure.zip && \
    unzip /tmp/allure.zip -d /opt/ && \
    ln -s /opt/allure-$ALLURE_VERSION/bin/allure /usr/local/bin/allure && \
    rm /tmp/allure.zip

# 验证 Python、Chrome 和 Allure 是否安装成功
RUN python --version && google-chrome --version && allure --version

# 安装 Android SDK 命令行工具
RUN mkdir -p $ANDROID_SDK_ROOT/cmdline-tools && \
    cd $ANDROID_SDK_ROOT/cmdline-tools && \
    curl -o sdk-tools.zip https://dl.google.com/android/repository/commandlinetools-linux-latest.zip && \
    unzip sdk-tools.zip -d $ANDROID_SDK_ROOT/cmdline-tools && \
    mv $ANDROID_SDK_ROOT/cmdline-tools/cmdline-tools $ANDROID_SDK_ROOT/cmdline-tools/latest && \
    rm sdk-tools.zip

# 安装 Android SDK 组件
RUN yes | sdkmanager --licenses || true && \
    sdkmanager "platform-tools" "platforms;android-30" "system-images;android-30;google_apis;x86_64" "emulator"

# 创建 Android 虚拟设备 (AVD)
RUN avdmanager create avd -n test_avd -k "system-images;android-30;google_apis;x86_64" -d "pixel"

# 安装 Appium
RUN npm install -g appium@latest

# 启动 Android 模拟器和 Appium
CMD ["sh", "-c", "emulator -avd test_avd -no-window -no-audio & sleep 5 && appium"]
