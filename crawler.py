import logging
import random
import re
import sys
import time

import requests
import urllib3

import notify
from config import GROUP_LIST, HEADERS, REQUEST_INTERVAL
from parse import parse_list, parse_detail

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def __get(url):
    response = requests.get(url, headers=HEADERS, verify=False)
    html = response.text
    if response.ok:
        return html
    if response.status_code == 404:
        logging.warning(f'{url}不存在')
        return None
    if '你没有权限访问这个页面' in html:
        logging.warning(f'{url}无权访问')
        return None
    logging.error('request %s is error.\nstatus_code:%s,text:%s',
                  url, response.status_code, html)
    notify.send_msg(f'请求[{url}]({url})失败,状态码:{response.status_code},请修复后继续.')
    logging.info(GROUP_LIST)
    sys.exit()


def crawl_list(group_id, start_time, start=None):
    """获取帖子列表
    :param group_id: 小组ID
    :param start_time: 监控帖子的起始时间
    :param start: 分页参数
    """
    url = f'https://www.douban.com/group/{group_id}/'
    if start:
        url += f'/discussion?start={start}'
    html = __get(url)
    if not html:
        return []
    post_list = parse_list(html)
    posts = [x for x in post_list if x['time'] > start_time]
    if len(post_list) == 0 or len(posts) != len(post_list):
        # 列表没有数据，或者存在时间比start_time小的内容，终止获取帖子列表
        return posts
    time.sleep(random.randint(REQUEST_INTERVAL[0], REQUEST_INTERVAL[1]))
    return post_list + crawl_list(group_id, start_time, start + 25 if start else 50)


def crawl_detail(url, start_id, start_time):
    """
    获取帖子详情
    """
    current_id = extract_id(url)
    if current_id is None or current_id < start_id:
        return {}
    html = __get(url)
    if not html:
        return {}
    post = parse_detail(html)
    post['url'] = url
    post['id'] = current_id
    if notify.meet_condition(post, start_time):
        msg = f'**标题**：[{post["title"]}]({url})\n**租金**：{post["rent"]}\n**发布时间**：{post["create_time"]}\n**作者**：[{post["author"]["name"]}]({post["author"]["url"]})\n**内容**：{post["content"]}\n\n'
        notify.send_msg(msg)
        with open("./test.txt", "a+") as file:
            # 定义要写入的字符串
            file.write(msg)
    return post


def extract_id(url):
    # 使用正则表达式提取 /topic/ 后面的数字串
    match = re.search(r'/topic/(\d+)', url)
    if match:
        return int(match.group(1))  # 返回提取到的数字串
    return None  # 如果没有匹配，返回 None
