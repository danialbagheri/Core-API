from .contact_us import ContactFormAPIView
from .slider import SliderViewSet
from .instagram_feed import InstagramFeed
from .configuration import ConfigurationView
from .search import Search
from .top_bar import TopBarListAPIView
from .icon_group import IconGroupRetrieveAPIView
from .instagram import InstagramListAPIView
from .top_bar_retrieve import TopBarRetrieveAPIView
from .menu import MenuRetrieveAPIView

from web.tasks import UpdateInstagramPostsTask
