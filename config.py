# -*- coding: UTF-8 -*-

import datetime
import logging.config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s[%(name)s] {%(filename)s:%(lineno)d} -> %(message)s'
)

# 请求头
HEADERS = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/103.0.0.0 Safari/537.36',
    # 填写自己的cookie
    "Cookie": '''bid=RcndmSMtDMM; ll="118159"; _pk_id.100001.8cb4=3774f7de9adaca5d.1712558159.; __yadk_uid=TDacvAjJuBTLhfCLCAQWD9eYwKATynNN; FCNEC=%5B%5B%22AKsRol_216P0IlH6SEerixtH_iE-sXRNcY4wUp5XZx2FTKyJUhyjKTqhXfM-Wk0xNvAgvQeiJdUF4k2eHSpkYzf4ml6gRKuZti-1XldbZeq8DsNtcu1ep7P6sYMPnSU46pxbhpnfvPKh3Mye-xqAHUPjKRnlYEzRrA%3D%3D%22%5D%5D; __gads=ID=9c9fe2f5f6b64891:T=1712558182:RT=1712558182:S=ALNI_MbAJlJnEA5JtY12hIRy92k6uBNLSA; __gpi=UID=00000de3f8c659d9:T=1712558182:RT=1712558182:S=ALNI_Ma5kIunvy_tLXG7dHVomma6lLvwIg; viewed="34450525_20556210"; __utmc=30149280; dbcl2="252140869:Es1MSFuJSZk"; ck=lC-u; push_noty_num=0; push_doumail_num=0; __utmv=30149280.25214; frodotk_db="34a41e1d1ab0d21e9dec5a575012765a"; __utmz=30149280.1728388188.7.4.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1728464515%2C%22https%3A%2F%2Fmovie.douban.com%2F%22%5D; _pk_ses.100001.8cb4=1; ap_v=0,6.0; __utma=30149280.1625006895.1703656513.1728450535.1728464517.11; __utmt=1; ct=y; __utmb=30149280.7.9.1728464535087'''
}

current_time = datetime.datetime.now().time()

# 监控的起始时间(仅在此时间之后发布的帖子才进行监控),默认为今天
START_TIME = datetime.datetime.combine(
    datetime.date.today(), current_time)

# 需要监控的豆瓣小组集合
GROUP_LIST = [
    {"id": "698716", "name": "买组", "start_time": START_TIME},
]

# 匹配规则,符合其中至少一个条件的才进行推送
MATCH_RULES = [
    r"四联|六约北|石芽岭|布吉|罗湖北|黄木岗|岗厦北|老街|红岭|晒布|翠竹|田贝|水贝|草埔|笋岗|洪湖"
]

# 排除规则,此规则中的内容,即便匹配成功了也不进行推送
EXCLUDE_RULES = [
    r"求租|合租",
    r"\d{4}起"
]

# 租金区间限制,(目前只会提取四位数的租金，且有一定概率识别错误)
# 不限制
# RENT_RANGE = ()
# 仅推送1-3k的帖子，最低为1000，最高9999
RENT_RANGE = (1000, 9999)

# 接口请求间隔(秒),默认10-20秒随机
REQUEST_INTERVAL = (3, 5)

# 监控周期(秒),两次循环中间的间隔时长,默认1小时
WATCH_INTERVAL = 5

# 消息通知配置
NOTIFY = {
    # 渠道 feishu:飞书 work.weixin:企业微信 dingtalk:钉钉
    "channel": "feishu",
    # 机器人WebHook地址
    "url": ""
}
