from bs4 import BeautifulSoup
import datetime
from random import shuffle
import requests
from time import sleep
from random import randint

def get_html(url):
    
    html_content = ''
    try:
        page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_content = BeautifulSoup(page.content, "html.parser")
    except: 
        pass
    
    return html_content

def get_value(html, info_name):
    
    info_value = ''
    
    items = html.select('#main .table td')
    for item in items:
        item_heading = item.get_text().strip()
        try:
            item_next = item.find_next().get_text().strip()
            if info_name == item_heading:
                info_value = item_next
                break
        except:
            pass
      
    return info_value 

def get_details(url, category):
    
    stamp = {}
    
    try:
        html = get_html(url)
    except:
        return stamp
    
    try:
        raw_text = html.select('#item-title')[0].get_text().strip()
        stamp['raw_text'] = raw_text.replace("\n"," ").replace('"',"'")
    except:
        stamp['raw_text'] = None 
        
    try:
        image_type = html.select('#item-image-tooltip')[0].get_text().strip()
        stamp['image_type'] = image_type
    except:
        stamp['image_type'] = None     

    try:
        condition_cont = html.select('.item-variation-description')
        if condition_cont:
             condition = condition_cont.parent.get_text().strip()
             stamp['condition'] = condition
    except:
        stamp['condition'] = None
        
    try:
        number_cont = html.select('.fa-check-circle-o')[0]
        if number_cont:
             number = number_cont.parent.get_text().strip()
             number = number.replace('(', '').replace(')', '')
             stamp['number'] = number
    except:
        stamp['number'] = None        
    
    
    try:
        price_temp = html.select('#item-variations td')[0].get_text().strip()
        if not 'CAD $' in price_temp:
            price_temp = html.select('#item-variations td')[1].get_text().strip()
        if 'CAD $' in price_temp:
            price = price_temp.replace('CAD $', '')
            stamp['price'] = price
    except:
        stamp['price'] = None  
        
    stamp['category'] = category   

    stamp['currency'] = "CAD"

    # image_urls should be a list
    images = []                    
    try:
        img_src = html.select('.item-img a')[0].get('href')
        img = 'https://www.arpinphilately.com' + img_src
        images.append(img)
    except:
        pass
    
    stamp['image_urls'] = images 
    
    stamp['country'] = get_value(html, 'Country')
    stamp['scott_num'] = get_value(html, '#Scott')
    stamp['monarch'] = get_value(html, 'Issue')
    stamp['name'] = get_value(html, 'Name')
    stamp['face_value'] = get_value(html, 'Face Value')
    stamp['year'] = get_value(html, 'Date')
    stamp['variety'] = get_value(html, 'Variety')
    stamp['color'] = get_value(html, 'Color')
    stamp['perfs'] = get_value(html, 'Perforation')
    stamp['printer'] = get_value(html, 'Printer')
        
    # scrape date in format YYYY-MM-DD
    scrape_date = datetime.date.today().strftime('%Y-%m-%d')
    stamp['scrape_date'] = scrape_date
    
    stamp['url'] = url

    print(stamp)
    print('+++++++++++++')
    sleep(randint(25, 65))
           
    return stamp

def get_page_items(url):
    
    items = []
    next_url = ''

    try:
        html = get_html(url)
    except:
        return items, next_url

    try:
        for item in html.select('a.item-desc'):
            item_href = item.get('href')
            item_link = 'https://www.arpinphilately.com' + item_href
            if item_link not in items:
                items.append(item_link)
    except:
        pass
    
    try:
        next_items = html.select('.pagination a')
        for next_item in next_items:
            next_text = next_item.get_text().strip()
            next_href = next_item.get('href')
            if(next_text == '>'):
                 next_url = 'https://www.arpinphilately.com' + next_href
    except:
        pass 
    
    shuffle(list(set(items)))
    
    return items, next_url

def get_categories():
    
    url = 'https://www.arpinphilately.com/'
    
    items = {}

    try:
        html = get_html(url)
    except:
        return items

    try:
        for cat_heading_item in html.select('#sidebar-categories > li > a'):
            cat_heading = cat_heading_item.get_text().strip()
            if (cat_heading == 'Canadian Stamps & Collections') or (cat_heading == 'World Stamps & Collections'):
                item_cont = cat_heading_item.parent.select('ul')[0]
                if item_cont:
                    for item in item_cont.select('li > a'):
                        item_link = 'https://www.arpinphilately.com'  + item.get('href')
                        item_text = item.get_text().strip()
                        if item_link not in items:
                            items[item_text] = item_link

    except:
        pass
    
    shuffle(list(set(items)))
    
    return items

categories = get_categories()

for category_name in categories:
    print(category_name + ': ' + categories[category_name])  

selected_category_name = input('Choose category: ')
category = categories[selected_category_name]

while(category):
    page_items, category = get_page_items(category)
    for page_item in page_items:
        stamp = get_details(page_item, selected_category_name)
    

