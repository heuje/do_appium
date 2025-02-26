from appium import webdriver

# from appium.webdriver.common.touch_action import TouchAction

# 设置desired capabilities
desired_caps = {
    'platformName': 'Android',
    'platformVersion': '11.0',  # 替换为你的设备版本
    'deviceName': 'Pixel_3_API_30',  # 替换为你的设备名称
    'automationName': 'UiAutomator2',
    'appPackage': 'com.android.chrome',  # Chrome 的包名
    'appActivity': 'com.google.android.apps.chrome.Main',  # Chrome 的启动 Activity
    'autoGrantPermissions': True  # 确保这是布尔值
}

# 启动 Appium WebDriver
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

# 在这里，你可以通过 Appium 来与浏览器交互
# 例如，访问一个 URL
driver.get('https://www.google.com')

# 如果你想在操作完成后关闭浏览器
# driver.quit()
