#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/12/11 5:15 PM
# @Author  : w8ay
# @File    : retireJS.py
from W13SCAN.lib.const import Level
from W13SCAN.lib.helper.retireJs import main_scanner, js_extractor
from W13SCAN.lib.output import out
from W13SCAN.lib.plugins import PluginBase


class W13SCAN(PluginBase):
    name = '过时的JS组件检查'
    desc = '''检测到当前页面存在过时的含有漏洞的js组件'''
    level = Level.MIDDLE

    def audit(self):
        method = self.requests.command  # 请求方式 GET or POST
        headers = self.requests.get_headers()  # 请求头 dict类型
        url = self.build_url()  # 请求完整URL
        data = self.requests.get_body_data().decode(self.response.decoding or 'utf-8')

        resp_data = self.response.get_body_data()  # 返回数据 byte类型
        resp_str = self.response.get_body_str()  # 返回数据 str类型 自动解码
        resp_headers = self.response.get_headers()  # 返回头 dict类型

        p = self.requests.urlparse
        params = self.requests.params
        netloc = self.requests.netloc
        js_links = js_extractor(resp_str)
        result = []

        ret = main_scanner(url, resp_str)
        if ret:
            result.append(ret)
        for link in js_links:
            ret2 = main_scanner(link, '')
            if ret2:
                result.append(ret2)
        for res in result:
            out.success(url, self.name, **res)
