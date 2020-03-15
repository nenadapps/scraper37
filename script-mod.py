from bs4 import BeautifulSoup
import datetime
from random import shuffle
import requests
from time import sleep
from random import randint
from fake_useragent import UserAgent

'''import os
import sqlite3
import shutil
from stem import Signal
from stem.control import Controller
import socket
import socks

controller = Controller.from_port(port=9051)
controller.authenticate()



def connectTor():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5 , "127.0.0.1", 9050)
    socket.socket = socks.socksocket

def renew_tor():
    controller.signal(Signal.NEWNYM)
    
UA = UserAgent(fallback='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2')
hdr = {'User-Agent': UA.random}'''
req = requests.Session()
hdr = {'User-Agent': 'Mozilla/5.0'}

def get_html(url):
    
    html_content = ''
    try:
        page = req.get(url, headers=hdr, timeout=120)
        html_content = BeautifulSoup(page.content, "html.parser")
    except: 
        print('Trouble with html_content')
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
        else:
             stamp['condition']=NoneCanada
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
        for img_item in html.select('.item-img a'):
            img_src = img_item.get('href')
            img = 'https://www.arpinphilately.com' + img_src
            if img not in images:
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
'''
def file_names(stamp):
    file_name = []
    rand_string = "RAND_"+str(randint(0,100000000))
    file_name = [rand_string+"-" + str(i) + ".png" for i in range(len(stamp['image_urls']))]
    print (file_name)
    return(file_name)

def query_for_previous(stamp):
    # CHECKING IF Stamp IN DB
    os.chdir("/Volumes/Stamps/")
    conn1 = sqlite3.connect('Reference_data.db')
    c = conn1.cursor()
    col_nm = 'url'
    col_nm2 = 'raw_text'
    unique = stamp['url']
    unique2 = stamp['raw_text']
    c.execute('SELECT * FROM arpin WHERE {cn} == "{un}" AND {cn2} == "{un2}"'.format(cn=col_nm, cn2=col_nm2, un=unique, un2=unique2))
    all_rows = c.fetchall()
    conn1.close()
    price_update=[]
    price_update.append((stamp['url'],
    stamp['raw_text'],
    stamp['scrape_date'], 
    stamp['price'], 
    stamp['currency'],
    stamp['number']))
    
    if len(all_rows) > 0:
        print ("This is in the database already")
        conn1 = sqlite3.connect('Reference_data.db')
        c = conn1.cursor()
        c.executemany("""INSERT INTO price_list (url, raw_text, scrape_date, price, currency, number) VALUES(?,?,?,?,?,?)""", price_update)
        try:
            conn1.commit()
            conn1.close()
        except:
            conn1.commit()
            conn1.close()
        print (" ")
        sleep(randint(10,45))
        next_step = 'continue'
    else:
        os.chdir("/Volumes/Stamps/")
        conn2 = sqlite3.connect('Reference_data.db')
        c2 = conn2.cursor()
        c2.executemany("""INSERT INTO price_list (url, raw_text, scrape_date, price, currency, number) VALUES(?,?,?,?,?,?)""", price_update)
        try:
            conn2.commit()
            conn2.close()
        except:
            conn2.commit()
            conn2.close()
        next_step = 'pass'
    print("Price Updated")
    return(next_step)

def db_update_image_download(stamp): 
    directory = "/Volumes/Stamps/stamps/arpin/" + str(datetime.datetime.today().strftime('%Y-%m-%d')) +"/"
    image_paths = []
    names = file_names(stamp)
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.chdir(directory)
    image_paths = [directory + names[i] for i in range(len(names))]
    for item in range(0,len(names)):
        print (stamp['image_urls'][item])
        try:
            imgRequest1=req.get(stamp['image_urls'][item],headers=hdr, timeout=120, stream=True)
        except:
            print ("waiting...")
            sleep(randint(3000,6000))
            print ("...")
            imgRequest1=req.get(stamp['image_urls'][item], headers=hdr, timeout=120, stream=True)
        if imgRequest1.status_code==200:
            with open(names[item],'wb') as localFile:
                imgRequest1.raw.decode_content = True
                shutil.copyfileobj(imgRequest1.raw, localFile)
                sleep(randint(18,30))
    stamp['image_paths']=", ".join(image_paths)
    database_update =[]
    # PUTTING NEW STAMPS IN DB
    database_update.append((
        stamp['url'],
        stamp['raw_text'],
        stamp['category'],
        stamp['country'],
        stamp['scott_num'],
        stamp['condition'],
        stamp['image_type'],
        stamp['monarch'],
        stamp['name'],
        stamp['face_value'],
        stamp['year'],
        stamp['variety'],
        stamp['color'],
        stamp['perfs'],
        stamp['printer'],
        stamp['scrape_date'],
        stamp['image_paths']))
    os.chdir("/Volumes/Stamps/")
    conn = sqlite3.connect('Reference_data.db')
    conn.text_factory = str
    cur = conn.cursor()
    cur.executemany("""INSERT INTO arpin ('url','raw_text', 'category','country',
    'scott_num','condition','image_type','monarch','name','face_value','year','variety','color','perfs',
    'printer','scrape_date','image_paths') 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", database_update)
    try:
        conn.commit()
        conn.close()
    except:
        conn.commit()
        conn.close()
    print ("all updated")
    print ("++++++++++++")
    print (" ")
    sleep(randint(60,160)) 



count = 0'''

categories = get_categories()

for category_name in categories:
    print(category_name + ': ' + categories[category_name])  

selected_category_name = input('Choose category: ')
category = categories[selected_category_name]
#connectTor()
while(category):
    page_items, category = get_page_items(category)
    for page_item in page_items:
        '''
        count += 1
        if count > randint(100, 256):
            print('Sleeping...')
            sleep(randint(600, 4000))
            hdr['User-Agent'] = UA.random
            renew_tor()
            connectTor()
            count = 0
        else:
            pass'''
        stamp = get_details(page_item, selected_category_name)
        '''if stamp['price']==None or stamp['price']=='':
            sleep(randint(500,700))
            continue
        next_step = query_for_previous(stamp)
        if next_step == 'continue':
            print('Only updating price')
            continue
        elif next_step == 'pass':
            print('Inserting the item')
            pass
        else:
            break
        db_update_image_download(stamp)'''
print('Scrape Complete')

    

