from unittest import TestCase

import pytest

from miio import Fan1C, FanMiot, FanZA5
from miio.fan_miot import (
    MODEL_FAN_1C,
    MODEL_FAN_P9,
    MODEL_FAN_P10,
    MODEL_FAN_P11,
    MODEL_FAN_ZA5,
    FanException,
    OperationMode,
    OperationModeFanZA5,
)

from .dummies import DummyMiotDevice


class DummyFanMiot(DummyMiotDevice, FanMiot):
    def __init__(self, *args, **kwargs):
        self.model = MODEL_FAN_P9
        self.state = {
            "power": True,
            "mode": 0,
            "fan_speed": 35,
            "swing_mode": False,
            "swing_mode_angle": 30,
            "power_off_time": 0,
            "light": True,
            "buzzer": False,
            "child_lock": False,
        }
        super().__init__(args, kwargs)


@pytest.fixture(scope="class")
def fanmiot(request):
    request.cls.device = DummyFanMiot()


@pytest.mark.usefixtures("fanmiot")
class TestFanMiot(TestCase):
    def is_on(self):
        return self.device.status().is_on

    def state(self):
        return self.device.status()

    def test_on(self):
        self.device.off()  # ensure off
        assert self.is_on() is False

        self.device.on()
        assert self.is_on() is True

    def test_off(self):
        self.device.on()  # ensure on
        assert self.is_on() is True

        self.device.off()
        assert self.is_on() is False

    def test_set_mode(self):
        def mode():
            return self.device.status().mode

        self.device.set_mode(OperationMode.Normal)
        assert mode() == OperationMode.Normal

        self.device.set_mode(OperationMode.Nature)
        assert mode() == OperationMode.Nature

    def test_set_speed(self):
        def speed():
            return self.device.status().speed

        self.device.set_speed(0)
        assert speed() == 0
        self.device.set_speed(1)
        assert speed() == 1
        self.device.set_speed(100)
        assert speed() == 100

        with pytest.raises(FanException):
            self.device.set_speed(-1)

        with pytest.raises(FanException):
            self.device.set_speed(101)

    def test_set_angle(self):
        def angle():
            return self.device.status().angle

        self.device.set_angle(30)
        assert angle() == 30
        self.device.set_angle(60)
        assert angle() == 60
        self.device.set_angle(90)
        assert angle() == 90
        self.device.set_angle(120)
        assert angle() == 120
        self.device.set_angle(150)
        assert angle() == 150

        with pytest.raises(FanException):
            self.device.set_angle(-1)

        with pytest.raises(FanException):
            self.device.set_angle(1)

        with pytest.raises(FanException):
            self.device.set_angle(31)

        with pytest.raises(FanException):
            self.device.set_angle(140)

        with pytest.raises(FanException):
            self.device.set_angle(151)

    def test_set_oscillate(self):
        def oscillate():
            return self.device.status().oscillate

        self.device.set_oscillate(True)
        assert oscillate() is True

        self.device.set_oscillate(False)
        assert oscillate() is False

    def test_set_led(self):
        def led():
            return self.device.status().led

        self.device.set_led(True)
        assert led() is True

        self.device.set_led(False)
        assert led() is False

    def test_set_buzzer(self):
        def buzzer():
            return self.device.status().buzzer

        self.device.set_buzzer(True)
        assert buzzer() is True

        self.device.set_buzzer(False)
        assert buzzer() is False

    def test_set_child_lock(self):
        def child_lock():
            return self.device.status().child_lock

        self.device.set_child_lock(True)
        assert child_lock() is True

        self.device.set_child_lock(False)
        assert child_lock() is False

    def test_delay_off(self):
        def delay_off_countdown():
            return self.device.status().delay_off_countdown

        self.device.delay_off(0)
        assert delay_off_countdown() == 0
        self.device.delay_off(1)
        assert delay_off_countdown() == 1
        self.device.delay_off(480)
        assert delay_off_countdown() == 480

        with pytest.raises(FanException):
            self.device.delay_off(-1)
        with pytest.raises(FanException):
            self.device.delay_off(481)


class DummyFanMiotP10(DummyFanMiot, FanMiot):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.model = MODEL_FAN_P10


@pytest.fixture(scope="class")
def fanmiotp10(request):
    request.cls.device = DummyFanMiotP10()


@pytest.mark.usefixtures("fanmiotp10")
class TestFanMiotP10(TestCase):
    def test_set_angle(self):
        def angle():
            return self.device.status().angle

        self.device.set_angle(30)
        assert angle() == 30
        self.device.set_angle(60)
        assert angle() == 60
        self.device.set_angle(90)
        assert angle() == 90
        self.device.set_angle(120)
        assert angle() == 120
        self.device.set_angle(140)
        assert angle() == 140

        with pytest.raises(FanException):
            self.device.set_angle(-1)

        with pytest.raises(FanException):
            self.device.set_angle(1)

        with pytest.raises(FanException):
            self.device.set_angle(31)

        with pytest.raises(FanException):
            self.device.set_angle(150)

        with pytest.raises(FanException):
            self.device.set_angle(141)


class DummyFanMiotP11(DummyFanMiot, FanMiot):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.model = MODEL_FAN_P11


@pytest.fixture(scope="class")
def fanmiotp11(request):
    request.cls.device = DummyFanMiotP11()


@pytest.mark.usefixtures("fanmiotp11")
class TestFanMiotP11(TestFanMiotP10, TestCase):
    pass


class DummyFan1C(DummyMiotDevice, Fan1C):
    def __init__(self, *args, **kwargs):
        self.model = MODEL_FAN_1C
        self.state = {
            "power": True,
            "mode": 0,
            "fan_level": 1,
            "swing_mode": False,
            "power_off_time": 0,
            "light": True,
            "buzzer": False,
            "child_lock": False,
        }
        super().__init__(args, kwargs)


@pytest.fixture(scope="class")
def fan1c(request):
    request.cls.device = DummyFan1C()


@pytest.mark.usefixtures("fan1c")
class TestFan1C(TestCase):
    def is_on(self):
        return self.device.status().is_on

    def state(self):
        return self.device.status()

    def test_on(self):
        self.device.off()  # ensure off
        assert self.is_on() is False

        self.device.on()
        assert self.is_on() is True

    def test_off(self):
        self.device.on()  # ensure on
        assert self.is_on() is True

        self.device.off()
        assert self.is_on() is False

    def test_set_mode(self):
        def mode():
            return self.device.status().mode

        self.device.set_mode(OperationMode.Normal)
        assert mode() == OperationMode.Normal

        self.device.set_mode(OperationMode.Nature)
        assert mode() == OperationMode.Nature

    def test_set_speed(self):
        def speed():
            return self.device.status().speed

        self.device.set_speed(1)
        assert speed() == 1
        self.device.set_speed(2)
        assert speed() == 2
        self.device.set_speed(3)
        assert speed() == 3

        with pytest.raises(FanException):
            self.device.set_speed(0)

        with pytest.raises(FanException):
            self.device.set_speed(4)

    def test_set_oscillate(self):
        def oscillate():
            return self.device.status().oscillate

        self.device.set_oscillate(True)
        assert oscillate() is True

        self.device.set_oscillate(False)
        assert oscillate() is False

    def test_set_led(self):
        def led():
            return self.device.status().led

        self.device.set_led(True)
        assert led() is True

        self.device.set_led(False)
        assert led() is False

    def test_set_buzzer(self):
        def buzzer():
            return self.device.status().buzzer

        self.device.set_buzzer(True)
        assert buzzer() is True

        self.device.set_buzzer(False)
        assert buzzer() is False

    def test_set_child_lock(self):
        def child_lock():
            return self.device.status().child_lock

        self.device.set_child_lock(True)
        assert child_lock() is True

        self.device.set_child_lock(False)
        assert child_lock() is False

    def test_delay_off(self):
        def delay_off_countdown():
            return self.device.status().delay_off_countdown

        self.device.delay_off(0)
        assert delay_off_countdown() == 0
        self.device.delay_off(1)
        assert delay_off_countdown() == 1
        self.device.delay_off(480)
        assert delay_off_countdown() == 480

        with pytest.raises(FanException):
            self.device.delay_off(-1)
        with pytest.raises(FanException):
            self.device.delay_off(481)


class DummyFanZA5(DummyMiotDevice, FanZA5):
    def __init__(self, *args, **kwargs):
        self.model = MODEL_FAN_ZA5
        self.state = {
            "anion": True,
            "buzzer": False,
            "child_lock": False,
            "fan_speed": 42,
            "light": 44,
            "mode": OperationModeFanZA5.Normal.value,
            "power": True,
            "power_off_time": 0,
            "swing_mode": True,
            "swing_mode_angle": 60,
        }
        super().__init__(args, kwargs)


@pytest.fixture(scope="class")
def fanza5(request):
    request.cls.device = DummyFanZA5()


@pytest.mark.usefixtures("fanza5")
class TestFanZA5(TestCase):
    def is_on(self):
        return self.device.status().is_on

    def is_ionizer_enabled(self):
        return self.device.status().is_ionizer_enabled

    def state(self):
        return self.device.status()

    def test_on(self):
        self.device.off()  # ensure off
        assert self.is_on() is False

        self.device.on()
        assert self.is_on() is True

    def test_off(self):
        self.device.on()  # ensure on
        assert self.is_on() is True

        self.device.off()
        assert self.is_on() is False

    def test_ionizer(self):
        def ionizer():
            return self.device.status().ionizer

        self.device.set_ionizer(True)
        assert ionizer() is True

        self.device.set_ionizer(False)
        assert ionizer() is False

    def test_set_mode(self):
        def mode():
            return self.device.status().mode

        self.device.set_mode(OperationModeFanZA5.Normal)
        assert mode() == OperationMode.Normal

        self.device.set_mode(OperationModeFanZA5.Nature)
        assert mode() == OperationMode.Nature

    def test_set_speed(self):
        def speed():
            return self.device.status().fan_speed

        for s in range(1, 101):
            self.device.set_speed(s)
            assert speed() == s

        for s in (-1, 0, 101):
            with pytest.raises(FanException):
                self.device.set_speed(s)

    def test_set_angle(self):
        def angle():
            return self.device.status().angle

        for a in (30, 60, 90, 120):
            self.device.set_angle(a)
            assert angle() == a

        for a in (0, 45, 140):
            with pytest.raises(FanException):
                self.device.set_angle(a)

    def test_set_oscillate(self):
        def oscillate():
            return self.device.status().oscillate

        self.device.set_oscillate(True)
        assert oscillate() is True

        self.device.set_oscillate(False)
        assert oscillate() is False

    def test_set_buzzer(self):
        def buzzer():
            return self.device.status().buzzer

        self.device.set_buzzer(True)
        assert buzzer() is True

        self.device.set_buzzer(False)
        assert buzzer() is False

    def test_set_child_lock(self):
        def child_lock():
            return self.device.status().child_lock

        self.device.set_child_lock(True)
        assert child_lock() is True

        self.device.set_child_lock(False)
        assert child_lock() is False

    def test_set_led_brightness(self):
        def led_brightness():
            return self.device.status().led_brightness

        for brightness in range(101):
            self.device.set_led_brightness(brightness)
            assert led_brightness() == brightness

        for brightness in (-1, 101):
            with pytest.raises(FanException):
                self.device.set_led_brightness(brightness)

    def test_delay_off(self):
        def delay_off_countdown():
            return self.device.status().delay_off_countdown

        for delay in (0, 1, 36000):
            self.device.delay_off(delay)
            assert delay_off_countdown() == delay

        for delay in (-1, 36001):
            with pytest.raises(FanException):
                self.device.delay_off(delay)
