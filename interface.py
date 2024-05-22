import requests
from bs4 import BeautifulSoup
from fastapi import HTTPException

'''Prepare the content from the request'''
def prepareContent(response):
    page_content = BeautifulSoup(response.content,'html.parser')
    section_cards = page_content.find('section',class_='PropertiesList_propertiesContainer__Vox4I PropertiesList_listViewGrid__bttyS')
    if not section_cards:
        return []
    
    content_cards = section_cards.find_all('div',class_='BasePropertyCard_propertyCard__N5tuo')
    properties_response = []
    for card in content_cards:
        try:
            broker = card.find('span',class_='BrokerTitle_titleText__RvFV6').text[12:]
            image_element = card.find('img',{'data-testid':'picture-img'})
            image_url = image_element['src'] if image_element else 'NA'
            status = card.find('div',class_='base__StyledType-rui__sc-108xfm0-0 hRTvWe message').text
            price = card.find('div',{'data-testid':'card-price'}).text[1:].replace(',','')
            beds = card.find('li',{'data-testid':'property-meta-beds'}).text[0:1]
            baths = card.find('li',{'data-testid':'property-meta-baths'}).text[0:1]
            sqft = card.find('li',{'data-testid':'property-meta-sqft'}).find('span',{'data-testid':'meta-value'}).text.replace(',','')
            sqft_lot = card.find('li',{'data-testid':'property-meta-lot-size'})
            sqft_lot_value = sqft_lot.find('span', {'data-testid': 'meta-value'}).text.replace(',', '') if sqft_lot else 'NA'
            address = card.find('div',{'data-testid':'card-address-1'}).text

            properties_response.append({
                'broker':broker,
                'image_url':image_url,
                'status':status,
                'price':price,
                'beds':beds,
                'baths':baths,
                'sqft':sqft,
                'sqft_lot_value':sqft_lot_value,
                'address':address
            })
        except AttributeError:
            continue
    return properties_response

'''
Request to realstate.com - Simulate real get request
'''
def pageRequest(zipcode):
    target_url = f'https://www.realtor.com/realestateandhomes-search/{zipcode}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
        'Accept-Language': 'en,es-419;q=0.9,es;q=0.8,es-ES;q=0.7,en-GB;q=0.6,en-US;q=0.5,es-CO;q=0.4,es-MX;q=0.3'
    }
    try:
        response = requests.get(target_url,headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=404,detail=f'Page unavailable')
    except HTTPException as e:
        return HTTPException(status_code=404,detail=f'ERROR:{e}')
    else:
        information = prepareContent(response)
        return information

