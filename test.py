from WLedController.WLedController import WLedController

wled = WLedController("192.168.178.42")

wled.deactivate_log()
wled.activate_log()


