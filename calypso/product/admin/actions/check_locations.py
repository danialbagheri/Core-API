import requests

from product.models import WhereToBuy


def check_locations(modeladmin, request, queryset):
    amazon_headers = {
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,'
                  'image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }
    for location in WhereToBuy.objects.filter(url__isnull=False).exclude(url='').all():
        kwargs = {}
        if location.stockist.name == 'Amazon':
            kwargs['headers'] = amazon_headers
        resp = requests.get(location.url, **kwargs)
        if resp.status_code == 404 or 'Sorry about that...' in resp.text:
            location.url = ''
            location.save()


check_locations.short_description = 'Check buying urls'
check_locations.dependant_action = True
