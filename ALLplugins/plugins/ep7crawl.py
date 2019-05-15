import datetime, json, math, pytz, re, time, requests

# 获取首页的文章响应
import os


def e7_mainpage_crawl(board_key='e7tw002'):
    mainpage_header = {
        'Host': 'api.onstove.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'http://page.onstove.com/epicseven/tw/main?listType=2&searchBoardKey=e7tw001',
        'Content-Type': 'application/json;charset=utf-8',
        'X-Device-Type': 'P01',
        'X-Client-Lang': 'EN',
        'X-Nation': 'CN',
        'X-Timezone': 'Asia/Shanghai',
        'X-Utc-Offset': '480',
        'X-Lang': 'EN',
        'X-UUID': '67482891-d182-4f1c-93cf-8ebfeaddf4ba',
        'Content-Length': '584',
        'Origin': 'http://page.onstove.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'TE': 'Trailers',
    }
    mainpage_form_data = {"board_key": "e7tw002",
                          "direction": "latest",
                          "list_type": "3",
                          "display_opt": "usertag_on,html_remove",
                          "notice_type": "A",
                          "page": 1,
                          "size": 15,
                          "not_headline_nos": [],
                          "access_token": None,
                          "cafe_key": "epicseven",
                          "channel_key": "tw"}
    print('开始获取首页文章接口')
    nocache = math.floor(time.time() * 1000)
    mainpage_url = f'https://api.onstove.com/cafe/v1/ArticleList?nocache={nocache}'
    try:
        mainpage_form_data['board_key'] = board_key
        main_page_response = requests.post(url=mainpage_url, data=json.dumps(mainpage_form_data),
                                           headers=mainpage_header)
        artic_list = json.loads(main_page_response.text)['context']['article_list']
        print('首页文章获取结束')
        article_id_list = []
        article_title_list = []
        for article_id in artic_list:
            article_id_list.append(article_id['card_no'])
            article_title_list.append(article_id['title'])
        article_id_list.sort(reverse=True)
        article_id_list = article_id_list[:10]
        return article_id_list
    except:
        print('连接超时')
        return None


# 根据文章id获取文章正文,返回标题和响应
def e7ArticleCrawl(new_article_id):
    artic_data = {
        "access_token": None,
        "cafe_key": "epicseven",
        "card_no": "3093109",
        "channel_key": "tw",
        "display_opt": "usertag_on,html_escape",
        "game_id": "141",
        "more_card_type": "normal",
        "not_headline_nos": [],
        "show_like_yn": "Y",
    }
    artic_head = {
        'Host': 'api.onstove.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'Referer: http://page.onstove.com/epicseven/tw/main/view/3167984?listType=2',
        'Content-Type': 'application/json;charset=utf-8',
        'X-Device-Type': 'P01',
        'X-Client-Lang': 'EN',
        'X-Nation': 'CN',
        'X-Timezone': 'Asia/Shanghai',
        'X-Utc-Offset': '480',
        'X-Lang': 'EN',
        'X-UUID': '67482891-d182-4f1c-93cf-8ebfeaddf4ba',
        'Content-Length': '559',
        'Origin': 'http://page.onstove.com',
        'Connection': 'keep-alive',
        'TE': 'Trailers'
    }
    nocache = math.floor(time.time() * 1000)
    artic_url = f'https://api.onstove.com/cafe/v1/ArticleInfo?nocache={nocache}'

    all_articl_response = []
    all_articl_title = []
    print('开始解析新闻内容')
    for card_id in new_article_id:
        print(f'开始解析{card_id}的内容')
        artic_data['card_no'] = card_id
        artic_response = requests.post(url=artic_url, data=json.dumps(artic_data), headers=artic_head)
        try:
            res = json.loads(artic_response.text)['context']
            all_articl_response.append(
                res['content'] + f'\n本文详细地址\nhttp://page.onstove.com/epicseven/tw/board/list/e7tw001/view/{card_id}')
            all_articl_title.append(res['title'])
            print(f'{card_id}解析结束')
            # time.sleep(10)
        except:
            print('解析失败，请检查')
            continue
    return all_articl_title, all_articl_response


# 获取最新文章，得到标题和清洗后的正文
def new_article(E7news_set):
    res = E7news_set
    local_article_id = []
    local_article_title = []
    # 获取本地数据
    for i in res:
        local_article_id.append(i['article_id'])
        local_article_title.append(i['article_title'])
    local_article_id = local_article_id[:10]
    e7tw001_id_list = e7_mainpage_crawl(board_key='e7tw001')
    e7tw002_id_list = e7_mainpage_crawl(board_key='e7tw002')
    if e7tw001_id_list:
        try:
            new_artic_id, all_article_title, all_article = re_news(e7tw001_id_list, local_article_id)
        except:
            return None
        return new_artic_id, all_article_title, all_article
    elif e7tw002_id_list:
        try:
            new_artic_id, all_article_title, all_article = re_news(e7tw002_id_list, local_article_id)
        except:
            return None
        return new_artic_id, all_article_title, all_article
    return None


# 解析最新文章
def re_news(article_id_list, local_article_id):
    article_id_list.sort(reverse=True)
    article_id_list = article_id_list[:10]
    if article_id_list != local_article_id:
        new_artic_id = set(article_id_list) - set(local_article_id)
        print('开始爬取最新新闻')
        all_article_title, all_article_list = e7ArticleCrawl(new_artic_id)
        all_article = []
        for i in all_article_list:
            b = re.sub('</tr>|■', '\n', i)
            c = re.sub('</td>|&nbsp', '\t', b)
            d = re.sub('<.*?>', '', c)
            all_article.append(d)
        return new_artic_id, all_article_title, all_article
    else:
        return None


# 整合文章id，标题，正文
def zip_article(article_id_list, all_article_title, all_article):
    complete = zip(article_id_list, all_article_title, all_article)
    e7_news = []
    print('开始整理文章')
    for i in complete:
        now = datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai'))
        e7_news.append({'article_id': i[0], 'article_title': i[1], 'article': i[2],
                        'up_time': now.strftime('%m-%d %H:%M')})
    print('整理结束')
    return e7_news


# 推送最新文章
def push_article(E7news_set):
    article_list = new_article(E7news_set)
    if article_list:
        new_artic_id, all_article_title, all_article = article_list
        latest_news = zip_article(new_artic_id, all_article_title, all_article)
        return latest_news
    print(f'{datetime.datetime.now(tz=pytz.timezone("Asia/Shanghai"))}\ne7tw002没有最新文章\n')
    print(f'{datetime.datetime.now(tz=pytz.timezone("Asia/Shanghai"))}\ne7tw001没有最新文章\n')
    return None

if __name__ == '__main__':
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = curPath[:curPath.find("qqbot\\") + len("qqbot\\")]

    noticePath = os.path.abspath(rootPath + '\\notice.json')
    notice = json.load(open(noticePath, 'r'))
    mes = push_article(notice)
    if mes:
        for i in reversed(mes):
            notice.insert(0, i)
    json.dump(notice, open(noticePath, 'w'))