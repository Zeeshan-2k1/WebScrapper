from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from . import models


BASE_URL = 'https://newyork.craigslist.org/d/services/search/sss?query='
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search').lower()
    models.Search.objects.create(search=search)
    response = requests.get(BASE_URL, search)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(
                class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)

        else:
            post_image_url = "https://craigslist.org/images/peace.jpg"

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        final_postings.append(
            (post_title, post_url, post_price, post_image_url))

    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)
