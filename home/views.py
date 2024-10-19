import json
import re
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template.defaulttags import now
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView

from .models import market_data, pep_data, fx_data


# from .serializer import ProductSerializer


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


class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        # Save the serialized data to a JSON file
        with open('products.json', 'w') as json_file:
            json.dump(serializer.data, json_file, indent=4)

        return Response(serializer.data)




# def scrape_jumia(request):
#     api_endpoint = "https://www.jumia.com.ng/phones-tablets/"
#     base_url = api_endpoint
#     page_number = 1
#
#     while True:
#         url = f'{base_url}?page={page_number}'
#         response = requests.get(url)
#         soup = BeautifulSoup(response.content, 'html.parser')
#         products = soup.find_all('a', class_='core')
#         # print(products)
#
#         if not products:
#             break
#
#         for product in products:
#             name_tag = product.get('data-gtm-name')
#             image_tag = product.find('img')
#             price_tag = product.find('div', class_='prc')
#             category_tag = product.get('data-gtm-category')
#             print(name_tag)
#
#             if not name_tag or not image_tag or not price_tag or not category_tag:
#                 continue  # Skip this product if any of the required fields are missing
#
#             name = name_tag.strip()
#             image = image_tag.get('data-src')
#             price = price_tag.text.strip()
#             category = category_tag
#
#             if not name or not image or not price or not category:
#                 continue  # Skip if any of the fields are empty
#
#             price_numeric = int(re.search(r'\d+', price.replace(',', '')).group())
#
#             # Check if the product already exists before creating a new one
#             existing_product = Product.objects.filter(name=name).exists()
#             if not existing_product:
#                 Product.objects.create(name=name, image=image, price=price_numeric, category=category)
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


class PepDataView(APIView):
    def get(self, request):
        today = timezone.now().date()
        existing_data = pep_data.objects.filter(as_at__date=today)

        if existing_data.exists():
            print("Returning existing data for today.")
            data = existing_data.first().pep_data  # Return the first entry or modify as needed
            return Response(data, status=status.HTTP_200_OK)
        else:
            print("No data found for today. Scraping new data...")
            return self.scrape_and_save_data()

    def scrape_and_save_data(self):
        number = 25
        all_data = []

        for i in range(1, 10000):
            url = f'https://www.opensanctions.org/search/?countries=ng&offset={number}&topics=role.pep'
            number += 25

            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                data_needed = soup.find('ul', class_='Search_resultList___zt_F')

                if data_needed:
                    rows = data_needed.find_all('li')
                    for row in rows:
                        name = row.find('a').get_text(strip=True)
                        person_of_interest = row.find('span', 'bg-warning').get_text(strip=True)
                        all_data.append({'name': name, 'person_of_interest': person_of_interest})
                        print(len(all_data))
                else:
                    print("Information not found.")
            else:
                if all_data:
                    pep_data.objects.create(pep_data=all_data)
                    return Response(all_data, status=status.HTTP_201_CREATED)
                print(f"Failed to retrieve the page status code: {response.status_code}")

        # Save data to the database
        pep_data.objects.create(pep_data=all_data)
        return Response(all_data, status=status.HTTP_201_CREATED)





# API_ID = 25801134  # Your API ID
# API_HASH = '2057aa75a2c3fe58cc8910709b33e5cb'  # Your API hash
# PHONE_NUMBER = '+2348165201384'
# import asyncio
# from telethon.sync import TelegramClient
# class SendMessageView(APIView):
#     """
#     API View to send a message via Telegram using Telethon.
#     """
#
#     def send_telegram_message_sync(self, recipient, message):
#         async def send_message():
#             client = TelegramClient('session_name', API_ID, API_HASH)
#             await client.start(phone=PHONE_NUMBER)
#
#             try:
#                 await client.send_message(recipient, message)
#             finally:
#                 await client.disconnect()
#
#         # Run the async function using asyncio.run()
#         asyncio.run(send_message())
#
#     def post(self, request):
#         recipient = request.data.get('recipient')
#         message = request.data.get('message')
#
#         if not recipient or not message:
#             return Response({"error": "Recipient and message are required."}, status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             # Call the synchronous wrapper for the async function
#             self.send_telegram_message_sync(recipient, message)
#
#             return Response({"status": "Message sent successfully"}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#
# import csv
# import os
# import io
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# import dns.resolver
# from validate_email_address import validate_email
#
#
# class EmailValidationView(APIView):
#     """
#     API View to validate email addresses and return active/inactive lists, and save a CSV file locally.
#     """
#
#     def get_mx_record(self, domain):
#         """Check if a domain has MX records (i.e., can receive emails) using dnspython."""
#         try:
#             records = dns.resolver.resolve(domain, 'MX')
#             return bool(records)
#         except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout):
#             return False
#
#     def validate_email_address(self, email):
#         """Check if the email address format is valid and if the domain has MX records."""
#         is_valid_format = validate_email(email)  # Checks email format
#
#         if is_valid_format:
#             domain = email.split('@')[-1]
#             has_mx_record = self.get_mx_record(domain)
#             return has_mx_record
#
#         return False
#
#     def create_csv(self, active_emails, inactive_emails):
#         """Create a CSV file containing active and inactive emails and save it to the current directory."""
#         # Define the CSV filename and path
#         csv_filename = 'email_validation_results.csv'
#         csv_filepath = os.path.join(os.getcwd(), csv_filename)
#
#         # Open the file and write the CSV content
#         with open(csv_filepath, mode='w', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow(['Active Emails', 'Inactive Emails'])
#
#             # Write rows for both active and inactive emails
#             max_len = max(len(active_emails), len(inactive_emails))
#             for i in range(max_len):
#                 active = active_emails[i] if i < len(active_emails) else ''
#                 inactive = inactive_emails[i] if i < len(inactive_emails) else ''
#                 writer.writerow([active, inactive])
#
#         return csv_filepath
#
#     def post(self, request):
#         """
#         Validate a list of email addresses, return active and inactive lists,
#         and save the CSV file to the current directory.
#         """
#         email_list = request.data.get('emails', [])
#         if not isinstance(email_list, list):
#             return Response({"detail": "Invalid data. Expected a list of emails."}, status=status.HTTP_400_BAD_REQUEST)
#
#         active_emails = []
#         inactive_emails = []
#
#         for email in email_list:
#             print(email)
#             if self.validate_email_address(email):
#                 active_emails.append(email)
#             else:
#                 inactive_emails.append(email)
#
#         # Create and save the CSV file in the current directory
#         csv_filepath = self.create_csv(active_emails, inactive_emails)
#
#         return Response({
#             'active_emails': active_emails,
#             'inactive_emails': inactive_emails,
#             'csv_file_path': csv_filepath  # Path to the saved CSV file
#         }, status=status.HTTP_200_OK)


def scrape_closing_rate():
    today = timezone.now().date()
    # Define the URL to scrape
    url = 'https://fmdqgroup.com/exchange/'

    # Make an HTTP GET request to fetch the HTML content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Search for text containing "NAFEM Closing rate"
    text = soup.find(text=lambda t: 'NAFEM Closing rate' in t)

    if text:
        # Assuming the format is "NAFEM Closing rate $/₦1600.78", we extract the rate
        closing_rate_text = text.strip()

        # Extract the numeric value, splitting by "$" and "₦"
        closing_rate = closing_rate_text.split('$')[1].split('₦')[1].strip()

        # Convert to a float for easier processing
        closing_rate = float(closing_rate)

        # Get today's date (without time)

        # Check if the data for today already exists
        existing_record = fx_data.objects.filter(as_at__date=today).first()

        if existing_record:
            # If a record for today exists, update it
            existing_record.closingrate = closing_rate
            existing_record.save()
            message = "Updated today's NAFEM closing rate."
        else:
            # If no record for today, create a new one
            fx_data.objects.create(closingrate=closing_rate, as_at=today)
            message = "Created new record for today's NAFEM closing rate."

        # Return response with the updated or created data
        return Response({
            'message': message,
            'closing_rate': closing_rate,
            'as_at': today
        })
    else:
        return Response({'error': 'Could not find the NAFEM Closing rate on the page.'}, status=404)


@api_view(['GET'])
def get_nafem_closing_rate(request):
    return scrape_closing_rate()