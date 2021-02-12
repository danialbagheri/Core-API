import requests
import re
import time
import logging
from datetime import datetime, timezone
from django.core.files import File
from blog.models import BlogPost
from django.conf import settings
import os
logger = logging.getLogger(__name__)

wp_post_url = "https://calypsosun.com/wp-json/wp/v2/posts/?per_page=100"



def import_wp_posts():
    """
        Reads the APIs and populates the database models.
    """
    wp_posts = requests.get(wp_post_url).json()
    post_response = []
    for i in wp_posts:
        title = i['title']['rendered']
        content = i['content']['rendered']
        slug = i['slug']
        date = datetime.strptime(
            i['date'], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc)
        status = i['status']
        image_api = i['_links']['wp:featuredmedia'][0]['href']
        image_data = requests.get(image_api).json()
        alt_text = image_data['alt_text']
        image_link = image_data['media_details']['sizes']['full']['source_url']
        file_name = image_data['media_details']['sizes']['full']['file']
        image_path = save_image(image_link, filename=file_name)
        if status == 'publish':
            post, new = BlogPost.objects.get_or_create(
                title=title,
                slug=slug,
                body=content,
                published=True,
                publish_date=date,
                image_alt_text=alt_text
            )

            if new:
                file = File(open(image_path, 'rb'))
                post.image.save(file_name, file)
                print(post)
                file.close()
                post.save()
                post_response.append(
                    f"Successfully added: {title} \n")
            else:
                post_response.append(f"article already exist: {title}")
            time.sleep(2)

    response = {
        "imported": post_response
    }
    return response




def getFilename_fromCd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]


def save_image(url, filename="filename"):
    r = requests.get(url)
    base_path = settings.MEDIA_ROOT
    try:
        os.mkdir(f'{base_path}/temp/')
    except:
        pass
    # filename = getFilename_fromCd(r.headers.get('content-disposition'))
    path = f'{base_path}/temp/{filename}'
    open(path, 'wb').write(r.content)
    return path


def find_url_in_string(string): 
  
    # findall() has been used  
    # with valid conditions for urls in string 
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)       
    return [x[0] for x in url] 