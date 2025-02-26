import datetime
import os

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
# from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.pointer_input import PointerInput
from typing import Union, Tuple


class AppiumDriver:
    def __init__(self, platform: str, **kwargs):
        """
        初始化Appium驱动
        :param platform: 平台类型 'android' 或 'ios'
        :param kwargs: 自定义能力参数
        """
        self.platform = platform.lower()
        self.driver = None

        # 基础能力配置
        self.capabilities = {
            'platformName': self.platform.capitalize(),
            'automationName': 'Flutter',  # 使用Flutter驱动
            'app': kwargs.get('app_path', ''),
            'deviceName': kwargs.get('device_name', ''),
            'udid': kwargs.get('udid', ''),
            'platformVersion': kwargs.get('platform_version', ''),
            'newCommandTimeout': 600,
            'noReset': kwargs.get('no_reset', True),
            'fullReset': kwargs.get('full_reset', False),
            'flutterWaitTimeout': 30  # Flutter元素等待超时
        }

        # 平台特定配置
        if self.platform == 'android':
            self.capabilities.update({
                'appPackage': kwargs.get('app_package', ''),
                'appActivity': kwargs.get('app_activity', ''),
            })
        elif self.platform == 'ios':
            self.capabilities.update({
                'bundleId': kwargs.get('bundle_id', ''),
                'wdaLocalPort': kwargs.get('wda_port', 8100),
            })
        else:
            raise ValueError(f"Unsupported platform: {self.platform}")

    def start_driver(self, appium_server='http://localhost:4723'):
        """启动Appium驱动"""
        self.driver = webdriver.Remote(
            command_executor=appium_server,
            desired_capabilities=self.capabilities
        )
        return self.driver

    def find_element(self,
                     by: Union[AppiumBy, str] = AppiumBy.ACCESSIBILITY_ID,
                     value: str = None,
                     timeout: int = 10):
        """查找元素（支持Flutter语义化定位）"""
        self.driver.implicitly_wait(timeout)
        try:
            return self.driver.find_element(by, value)
        except Exception as e:
            self.take_screenshot('element_not_found')
            raise Exception(f"Element not found: {value} ({by}), Error: {str(e)}")

    def click_element(self, element=None, by=None, value=None):
        """点击元素"""
        if element is None and (by and value):
            element = self.find_element(by, value)
        element.click()

    def input_text(self, text: str, element=None, by=None, value=None):
        """输入文本"""
        if element is None and (by and value):
            element = self.find_element(by, value)
        element.clear()
        element.send_keys(text)

    # def tap_by_coordinates(self,
    #                        coordinates: Tuple[int, int],
    #                        duration: int = 100):
    #     """通过坐标点击（基于屏幕分辨率）"""
    #     (x, y) = coordinates
    #     action = TouchAction(self.driver)
    #     action.press(x=x, y=y).wait(duration).release().perform()

    def tap_by_coordinates(self, coordinates: Tuple[int, int], duration_ms: int = 100):
        x, y = coordinates
        # 创建指针设备（触摸操作）
        finger = PointerInput(interaction.POINTER_TOUCH, "finger")
        actions = ActionBuilder(self.driver, mouse=finger)

        # 按下 -> 等待 -> 释放
        actions.pointer_action.move_to_location(x, y)
        actions.pointer_action.pointer_down()
        actions.pointer_action.pause(duration_ms / 1000)
        actions.pointer_action.pointer_up()

        # 执行动作链
        actions.perform()

    def take_screenshot(self, name: str = None):
        """屏幕截图并保存"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{name}_{timestamp}.png" if name else f"screenshot_{timestamp}.png"

        if not os.path.exists('screenshots'):
            os.makedirs('screenshots')

        path = os.path.join('screenshots', filename)
        self.driver.save_screenshot(path)
        return path

    def get_window_size(self):
        """获取屏幕尺寸"""
        return self.driver.get_window_size()

    def percentage_tap(self, x_percent: float, y_percent: float):
        """按屏幕百分比点击"""
        size = self.get_window_size()
        x = size['width'] * x_percent
        y = size['height'] * y_percent
        self.tap_by_coordinates((int(x), int(y)))

    def quit(self):
        """关闭驱动"""
        if self.driver:
            self.driver.quit()


# 使用示例
if __name__ == "__main__":
    # Android配置示例
    android_config = {
        'app_path': '/path/to/app.apk',
        'device_name': 'Pixel_5',
        'platform_version': '13.0',
        'app_package': 'com.example.app',
        'app_activity': '.MainActivity'
    }

    # iOS配置示例
    ios_config = {
        'app_path': '/path/to/app.app',
        'device_name': 'iPhone 15',
        'platform_version': '17.0',
        'bundle_id': 'com.example.app'
    }

    # 初始化驱动（根据平台选择配置）
    driver = AppiumDriver('android', **android_config).start_driver()

    try:
        # 示例操作流程
        # 通过accessibility id定位（Flutter推荐方式）
        search_field = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='searchField')
        driver.input_text('Hello Appium!', element=search_field)

        # 通过坐标点击（屏幕右下方10%位置）
        driver.percentage_tap(0.9, 0.9)

        # 截图保存
        driver.take_screenshot('after_search')

    finally:
        driver.quit()
