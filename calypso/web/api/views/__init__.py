from .contact_us import ContactFormAPIView
from .slider import SliderViewSet
from .instagram_feed import InstagramFeed
from .configuration import ConfigurationView
from .search import Search
from .top_bar import TopBarListAPIView
from .instagram import InstagramListAPIView

from web.tasks import UpdateInstagramPostsTask
