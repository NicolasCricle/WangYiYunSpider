from selenium import webdriver
from lxml import etree
from wangyi_spider import WangYiSpider


def get_html():

    browser = webdriver.Chrome()

    browser.get('https://music.163.com/discover/toplist')

    browser.switch_to.frame("contentFrame")

    html = browser.page_source

    browser.close()

    return html


def get_ids(html):

    html_obj = etree.HTML(html)

    divs = html_obj.xpath('//tbody//div[@class="opt hshow"]')

    url_dict = dict()
    for div in divs:
        # print(div.xpath('.//span[@class="icn icn-share"]/@data-res-id')[0])
        # break
        url_dict[div.xpath('.//span[@class="icn icn-share"]/@data-res-name')[0]] = div.xpath('.//span[@class="icn icn-share"]/@data-res-id')[0]

    return url_dict


if __name__ == "__main__":

    spider = WangYiSpider()
    url_dict = get_ids(get_html())

    for key, value in url_dict.items():
        key = key.replace('.', '')
        spider.save_song(key, value)
