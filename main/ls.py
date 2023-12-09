# -*- coding: utf-8 -*-
# @Time    : 2023/11/8 16:42
# @Author  : shuai li
# description : 定时发送消息，pc端时间一般有误差。可以进入 https://time.is/zh/，进入后点击左上角 TIME.IS logo，可以查看本机时间差距。
# 慢了就将 delay 设置为负数，快了就设置为正数
import argparse
import uiautomation as uia
import win32clipboard
import win32gui
import win32con
import datetime as dt
from datetime import datetime
import time
import json
import os


def get_parser():
    parser = argparse.ArgumentParser("微信自动发送消息工具")
    parser.add_argument('--r', action='store_true', default=False, help='是否使用上次的记录')
    parser.add_argument('--sr', action='store_true', default=False, help='查看上次的记录')
    parser.add_argument('--time', type=str, default='12:00:00', help='发送时间，格式为: 12:00:00')
    parser.add_argument('--delay', type=float, default=0, help='提前 or 延迟 多少秒发送，满了就减去，快了就加上')
    parser.add_argument('--who', type=str, default='文件传输助手', help='发送给谁，例如 张三')
    parser.add_argument('--msg', type=str, default='今天天气真好', help='消息内容，例如 今天天气真好')
    return parser.parse_args()


def save_file(args):
    with open("D://params.json", mode="w") as f:
        json.dump(args.__dict__, f, indent=4)


def read_file():
    assert os.path.exists("D://params.json"), '历史记录不存在'
    return json.load(open("D://params.json", mode="r"))


class WeChat:
    def __init__(self, args):
        self.args = args
        # 拿到窗口句柄，用于操作
        self.wechat_hw = uia.WindowControl(ClassName='WeChatMainWndForPC', searchDepth=1)

        # 控件注册
        temp_control = [i for i in self.wechat_hw.GetChildren() if not i.ClassName][0]
        temp_control = temp_control.GetChildren()[0]
        self.navigation_box, self.session_box, self.chat_box = temp_control.GetChildren()

        self.search_control = self.session_box.EditControl(Name='搜索')
        self.edit_control = self.chat_box.EditControl()

        self.nickname = self.navigation_box.ButtonControl().Name
        print(f'初始化成功，欢迎您：{self.nickname}')

    def _show(self):
        self.HWND = win32gui.FindWindow('WeChatMainWndForPC', None)
        win32gui.ShowWindow(self.HWND, 1)
        win32gui.SetWindowPos(self.HWND, -1, 0, 0, 0, 0, 3)
        win32gui.SetWindowPos(self.HWND, -2, 0, 0, 0, 0, 3)
        self.wechat_hw.SwitchToThisWindow()

    def _search(self, who):
        self._show()
        self.wechat_hw.SendKeys('{Ctrl}f', waitTime=1)
        self.search_control.SendKeys(who, waitTime=1.5)

        # 目标组件
        aim_control = None

        contact = self.session_box.TextControl(Name='联系人')
        searched_people = contact.GetParentControl().GetParentControl().ListItemControl()
        for i in range(100):
            try:
                if who in searched_people.Name:
                    aim_control = searched_people
                    break
                searched_people = searched_people.GetNextSiblingControl()
            except:
                break
        return aim_control

    def _chat_with(self, who):
        aim_control = self._search(who)
        if aim_control is None:
            print(f'联系人: {who} 不存在')
            return False
        aim_control.Click(simulateMove=False)
        return True

    @staticmethod
    def _set_msg_to_clipboard(msg):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, msg)
        win32clipboard.CloseClipboard()

    def _input_msg(self, msg):
        # 输入内容
        self._set_msg_to_clipboard(msg)
        # 选择输入框
        self.edit_control.Click(simulateMove=False)
        # 粘贴
        self.edit_control.SendKeys('{Ctrl}v')

    def _valid_check(self):
        # 延迟一段时间后执行
        aim_time = datetime.strptime(args.time, '%H:%M:%S')
        cur_time = datetime.now()
        aim_time = aim_time.replace(year=cur_time.year, month=cur_time.month, day=cur_time.day)
        delta = dt.timedelta(microseconds=abs(self.args.delay * 1e6))
        aim_time = aim_time - delta if self.args.delay < 0 else aim_time + delta

        if aim_time <= cur_time:
            print('已超时，设定时间为', aim_time)
            return False
        return True

    def _delay(self):
        aim_time = datetime.strptime(args.time, '%H:%M:%S')
        cur_time = datetime.now()
        aim_time = aim_time.replace(year=cur_time.year, month=cur_time.month, day=cur_time.day)
        delta = dt.timedelta(microseconds=abs(self.args.delay * 1e6) + 100)
        aim_time = aim_time - delta if self.args.delay < 0 else aim_time + delta

        delta = aim_time - cur_time  # 还有多久开始
        if delta.seconds > 5:
            time.sleep(delta.seconds - 5)  # 休眠，减少 cpu 消耗
        self._show()
        # 再次延迟，准备发送了
        delta = aim_time - datetime.now()
        while delta.total_seconds() > 0:
            delta = aim_time - datetime.now()

    def send_msg(self, who, msg):
        if not self._valid_check():
            return
        self._show()
        # 搜索联系人
        if not self._chat_with(who):
            return

        # 输入内容
        self._input_msg(msg)
        # 延迟
        self._delay()

        # 发送
        self.edit_control.SendKeys('{Enter}')
        print('发送完毕')


if __name__ == '__main__':
    args = get_parser()
    if args.sr:
        print(read_file())
    elif args.r:
        obj = read_file()
        args.time = obj['time']
        args.delay = obj['delay']
        args.who = obj['who']
        args.msg = obj['msg']
        wechat = WeChat(args)
        wechat.send_msg(args.who, args.msg)
    else:
        wechat = WeChat(args)
        wechat.send_msg(args.who, args.msg)
        save_file(args)

