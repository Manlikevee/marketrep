import re
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template.defaulttags import now
from django.utils import timezone

from .models import market_data


# from mykeycloakdjango.home.models import market_data


# Create your views here.



def home(request):

   return render(request, 'index.html')


@login_required
def testing(request):

   return render(request, 'index2.html')



import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
# from .models import Product

import requests
from bs4 import BeautifulSoup
import re
# from .models import Product


# def scrape_jumia(request):
#     api_endpoint = "https://vee-commerce.cyclic.app/product"
#     base_url = 'https://www.jumia.com.ng/smartphones/?page='
#     page_number = 1
#     iphone_description_template = (
#         "Embark on a delightful journey through the world of beverages with {product_name}. This exceptional drink collection not only sets a new standard but also redefines the very essence of liquid indulgence. Immerse yourself in a diverse array of innovative flavors, each telling its own story and pushing the boundaries of taste and quality. Step into a world where {product_name} transcends the ordinary, introducing you to a realm of drink possibilities previously unexplored. Bid farewell to conventional beverage experiences as this collection weaves together a seamless and boundary-breaking sipping adventure, promising to elevate your every sip and tantalize your taste buds in ways you never thought possible."
#     )
#
#     while True:
#         url = f'{base_url}{page_number}'
#         response = requests.get(url)
#         soup = BeautifulSoup(response.content, 'html.parser')
#         products = soup.find_all('a', class_='core')
#         print(products)
#
#         if not products:
#             break
#
#         for product in products:
#             name_tag = product.find('div', class_='name')
#             image_tag = product.find('img')
#             price_tag = product.find('div', class_='prc')
#
#             if not name_tag or not image_tag or not price_tag:
#                 continue  # Skip this product if any of the required fields are missing
#
#             name = name_tag.text.strip()
#             image = image_tag.get('data-src')
#             price = price_tag.text.strip()
#             print(name)
#             if not name or not image or not price:
#                 continue  # Skip if any of the fields are empty
#
#             price_numeric = int(re.search(r'\d+', price.replace(',', '')).group())
#
#             description = iphone_description_template.format(
#                 product_name=name
#             )
#
#             # Check if the product already exists before creating a new one
#             existing_product = Product.objects.filter(name=name).exists()
#             if not existing_product:
#                 Product.objects.create(name=name, image=image, price=price_numeric)
#                 print(f'{name} added to the database.')
#
#         page_number += 1
#
#     production = Product.objects.all()
#
#     context = {
#         'production': production
#     }
#     return render(request, 'scrape_result.html', context)


# def delete_all_products(request):
#         Product.objects.all().delete()
#         return redirect('scrape_jumia')


from rest_framework.decorators import api_view
from rest_framework.response import Response
BASE_URL = 'https://fmdqgroup.com/exchange/'
BASE_URLs = 'https://ngxgroup.com/exchange/data/equities-price-list/'
topgainers = 'https://doclib.ngxgroup.com/REST/api/statistics/equities/?market=&sector=&orderby=TopGainers&pageSize=300&pageNo=0'
toploosers = 'https://doclib.ngxgroup.com/REST/api/statistics/equities/?market=&sector=&orderby=Losers&pageSize=300&pageNo=0'


def fetch_table_data(table_id):
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        price_list_table = soup.find('table', id=table_id)

        if price_list_table:
            rows = price_list_table.find_all('tr')
            table_data = []
            for row in rows:
                columns = row.find_all('td')
                if columns:
                    if table_id == 'table_7':
                        table_data.append({
                            'description': columns[0].get_text(strip=True),
                            'price': columns[1].get_text(strip=True),
                            'yield': columns[2].get_text(strip=True),
                            'change': columns[3].get_text(strip=True),
                            'date': columns[4].get_text(strip=True) if len(columns) > 4 else None,
                        })
                    elif table_id == 'table_8':
                        table_data.append({
                                'maturity': columns[0].get_text(strip=True),
                                'discount': columns[1].get_text(strip=True),
                                'yield': columns[2].get_text(strip=True),
                                'change': columns[3].get_text(strip=True),
                                'date': columns[4].get_text(strip=True) if len(columns) > 4 else None,
                        })
                    elif table_id == 'table_9':
                        table_data.append({
                                'maturity': columns[0].get_text(strip=True),
                                'discount': columns[1].get_text(strip=True),
                                'yield': columns[2].get_text(strip=True),
                                'change': columns[3].get_text(strip=True),
                                'date': columns[4].get_text(strip=True) if len(columns) > 4 else None,
                        })
                    elif table_id == 'table_12':
                        table_data.append({
                                'contract_code': columns[0].get_text(strip=True),
                                'maturity_date': columns[1].get_text(strip=True),
                                'settlement_price': columns[2].get_text(strip=True),
                                'date': columns[3].get_text(strip=True),
                        })
                    else:
                        table_data.append({
                            'security': columns[0].get_text(strip=True),
                            'issued_shares': columns[1].get_text(strip=True),
                            'wk_high_52': columns[2].get_text(strip=True),
                            'wk_low_52': columns[3].get_text(strip=True),
                            'open_price': columns[4].get_text(strip=True) if len(columns) > 4 else None,
                        })
            return table_data
        else:
            return None
    else:
        return None


@api_view(['GET'])
def get_table_9a_datagain(request):
    today = timezone.now().date()

    # Check if today's data for Top Gainers is already saved
    top_gainers_data = market_data.objects.filter(product_class='Top_Gainers', as_at__date=today).order_by('-id').first()
    if top_gainers_data:
        print('Top Gainers data already saved')
    else:
        # Fetch data from the Top Gainers external API
        response_gainers = requests.get(
            'https://doclib.ngxgroup.com/REST/api/statistics/equities/?market=&sector=&orderby=TopGainers&pageSize=300&pageNo=0')
        if response_gainers.status_code == 200:
            data_gainers = response_gainers.json()
            print('Fetched Top Gainers data')

            # Save the fetched data to the database
            market_data.objects.create(product_class='Top_Gainers', product_data=data_gainers)
            print('Top Gainers data saved')
        else:
            return Response({'error': 'Failed to retrieve data from the Top Gainers API'}, status=404)

    # Check if today's data for Top Losers is already saved
    top_losers_data = market_data.objects.filter(product_class='Top_Losers', as_at__date=today).order_by('-id').first()
    if top_losers_data:
        print('Top Losers data already saved')
    else:
        # Fetch data from the Top Losers external API
        response_losers = requests.get(
            'https://doclib.ngxgroup.com/REST/api/statistics/equities/?market=&sector=&orderby=Losers&pageSize=300&pageNo=0')
        if response_losers.status_code == 200:
            data_losers = response_losers.json()
            print('Fetched Top Losers data')

            # Save the fetched data to the database
            market_data.objects.create(product_class='Top_Losers', product_data=data_losers)
            print('Top Losers data saved')
        else:
            return Response({'error': 'Failed to retrieve data from the Top Losers API'}, status=404)

    # Combine both Top Gainers and Top Losers data into a single response
    response_data = {
        'top_gainers': top_gainers_data.product_data if top_gainers_data else data_gainers,
        'top_losers': top_losers_data.product_data if top_losers_data else data_losers
    }

    return Response(response_data)

@api_view(['GET'])
def scrapengx(request):
    response = requests.get(BASE_URLs)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        print(soup)
        return Response(soup)


@api_view(['GET'])
def getngx(request):
    data = fetch_table_data('table_7')

@api_view(['GET'])
def get_table_7_data(request):
    today = timezone.now().date()
    mymarketdata = market_data.objects.filter(product_class='Bonds').filter(as_at__date=today).order_by('-id').first()
    if mymarketdata:
        print('already saved')
        return Response(mymarketdata.product_data)


    data = fetch_table_data('table_7')
    print('still ran')
    if data is not None:
        market_data.objects.create(product_class='Bonds' , product_data=data)
        print('created')
        return Response(data)
    else:
        return Response({'error': 'Failed to retrieve table data or table not found'}, status=404)


@api_view(['GET'])
def get_table_9a_data(request):
    today = timezone.now().date()

    # Check if today's data is already saved
    mymarketdata = market_data.objects.filter(product_class='Equities_Price_List', as_at__date=today).order_by('-id').first()
    if mymarketdata:
        print('already savedaaaaaaaa')
        return Response(mymarketdata.product_data)

    # Fetch data from the external API
    response = requests.get(
        'https://doclib.ngxgroup.com/REST/api/statistics/equities/?market=&sector=&orderby=&pageSize=1900&pageNo=0')
    if response.status_code == 200:
        data = response.json()
        print('still ran')

        # Save the fetched data to the database
        market_data.objects.create(product_class='Equities_Price_List', product_data=data)
        print('created')
        return Response(data)
    else:
        return Response({'error': 'Failed to retrieve data from the external API'}, status=404)


def run_table_7_data_check():
    today = timezone.now().date()
    mymarketdata = market_data.objects.filter(product_class='Bonds').filter(as_at__date=today).order_by('-id').first()
    if mymarketdata:
        print('Table 7 already saved')
        return mymarketdata.product_data

    data = fetch_table_data('table_7')
    print('Table 7 running')
    if data is not None:
        market_data.objects.create(product_class='Bonds', product_data=data)
        print('Table 7 created')
        return data
    else:
        print('Failed to retrieve table 7 data')
        return None

def run_table_8_data_check():
    today = timezone.now().date()
    mymarketdata = market_data.objects.filter(product_class='Bills').filter(as_at__date=today).order_by('-id').first()
    if mymarketdata:
        print('Table 8 already saved')
        return mymarketdata.product_data

    data = fetch_table_data('table_8')
    print('Table 8 running')
    if data is not None:
        market_data.objects.create(product_class='Bills', product_data=data)
        print('Table 8 created')
        return data
    else:
        print('Failed to retrieve table 8 data')
        return None

def run_table_9_data_check():
    today = timezone.now().date()
    mymarketdata = market_data.objects.filter(product_class='Cps').filter(as_at__date=today).order_by('-id').first()
    if mymarketdata:
        print('Table 9 already saved')
        return mymarketdata.product_data

    data = fetch_table_data('table_9')
    print('Table 9 running')
    if data is not None:
        market_data.objects.create(product_class='Cps', product_data=data)
        print('Table 9 created')
        return data
    else:
        print('Failed to retrieve table 9 data')
        return None

def run_table_12_data_check():
    today = timezone.now().date()
    mymarketdata = market_data.objects.filter(product_class='FGN_BOND_FUTURES').filter(as_at__date=today).order_by('-id').first()
    if mymarketdata:
        print('Table 12 already saved')
        return mymarketdata.product_data

    data = fetch_table_data('table_12')
    print('Table 12 running')
    if data is not None:
        market_data.objects.create(product_class='FGN_BOND_FUTURES', product_data=data)
        print('Table 12 created')
        return data
    else:
        print('Failed to retrieve table 12 data')
        return None


@api_view(['GET'])
def get_table_8_data(request):
    today = timezone.now().date()
    mymarketdata = market_data.objects.filter(product_class='Bills').filter(as_at__date=today).order_by('-id').first()
    if mymarketdata:
        print('already saved')
        return Response(mymarketdata.product_data)
    print('running')
    data = fetch_table_data('table_8')
    if data is not None:
        market_data.objects.create(product_class='Bills', product_data=data)
        print('created')
        return Response(data)
    else:
        return Response({'error': 'Failed to retrieve table data or table not found'}, status=404)


@api_view(['GET'])
def get_table_9_data(request):
    today = timezone.now().date()
    mymarketdata = market_data.objects.filter(product_class='Cps').filter(as_at__date=today).order_by('-id').first()
    if mymarketdata:
        print('already saved')
        return Response(mymarketdata.product_data)
    print('running')
    data = fetch_table_data('table_9')
    if data is not None:
        market_data.objects.create(product_class='Cps', product_data=data)
        print('created')
        return Response(data)
    else:
        return Response({'error': 'Failed to retrieve table data or table not found'}, status=404)


@api_view(['GET'])
def get_table_12_data(request):
    today = timezone.now().date()
    mymarketdata = market_data.objects.filter(product_class='FGN_BOND_FUTURES').filter(as_at__date=today).order_by('-id').first()
    if mymarketdata:
        print('already saved')
        return Response(mymarketdata.product_data)

    print('running')
    data = fetch_table_data('table_12')
    if data is not None:
        market_data.objects.create(product_class='FGN_BOND_FUTURES', product_data=data)
        print('created')
        return Response(data)
    else:
        return Response({'error': 'Failed to retrieve table data or table not found'}, status=404)