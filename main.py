#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
import random
import sys
import time

from config import GROUP_LIST, START_TIME, REQUEST_INTERVAL, WATCH_INTERVAL
from crawler import crawl_list, crawl_detail
from notify import send_msg

start_id = 0


def crawl(group):
    global start_id
    start_time = group.get('start_time', START_TIME)
    logging.info('开始抓取[%s]小组[%s]之后发布的新帖子,id:[%d]', group['name'], start_time, start_id)
    try:
        post_list = crawl_list(group['id'], start_time)
        max_time = start_time
        for post in post_list:
            logging.debug(post)
            detail = crawl_detail(post['url'], start_id, start_time)
            if detail:
                time.sleep(random.randint(REQUEST_INTERVAL[0], REQUEST_INTERVAL[1]))
                logging.info(detail)
            if "create_time" in detail and detail["create_time"] > max_time:
                max_time = detail["create_time"]
            if "id" in detail and detail["id"] > start_id:
                start_id = detail["id"]

        group["start_time"] = max_time
        logging.info('[%s]小组的新帖子抓取完成,最新一篇帖子发布时间为[%s]', group['name'], max_time)
    except Exception as e:
        logging.error("%s的数据获取失败.", group, exc_info=e)
        send_msg(
            f'获取[{group["name"]}](https://www.douban.com/group/{group["id"]}/)小组的数据时出现异常.\nerror:{e.args}')
        logging.info(GROUP_LIST)
        sys.exit()


if __name__ == "__main__":
    while True:
        for g_info in GROUP_LIST:
            crawl(g_info)
        logging.info('本轮抓取已完成,开始休眠...')
        logging.info(GROUP_LIST)
        time.sleep(WATCH_INTERVAL)
