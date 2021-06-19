def get_each(sub_url):
    def get_info(each):
        name = each.xpath('@data-itemname')[0]
        itemid = each.xpath('@data-itemid')[0]
        info_url = 'https://www.supremecommunity.com/season/itemdetails/{}/'.format(
            itemid)
        info_req = requests.get(info_url, headers=UA).text
        color_str = re.findall('Colorways: <span>(.*?)</span>', info_req)[0]
        color_list = color_str.split(' ')
        price = 123  # ...
        info = {name: {'item_id': itemid, 'color': color_list,
                       'price': price, 'url': info_url}}
        return info

    week_url = 'https://www.supremecommunity.com' + sub_url
    week_req = requests.get(week_url, headers=UA).text
    document = etree.HTML(week_req)
    week_all_goods = document.xpath(
        '//div[@class="masonry__container masonry--active"]/div/div/div[@class="card-details"]')
    week_info = []
    for i in week_all_goods:
        week_info.append(get_info(i))
    result = {sub_url.split('/')[-1]: week_info}
    return result
