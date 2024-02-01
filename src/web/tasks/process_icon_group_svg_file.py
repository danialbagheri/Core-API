from celery import Task, current_app

from common.services import SvgFileProcessor
from web.models import IconGroupItem


class ProcessIconGroupSvgFileTask(Task):
    name = 'web.tasks.ProcessIconGroupSvgFileTask'

    def run(self, icon_group_item_id, svg_field_name):
        icon_group_item = IconGroupItem.objects.get(id=icon_group_item_id)
        SvgFileProcessor(icon_group_item, 'svg_icon').process()


current_app.register_task(ProcessIconGroupSvgFileTask())
