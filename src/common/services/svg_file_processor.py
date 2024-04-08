from common.services import BaseService


class SvgFileProcessor(BaseService):
    def __init__(self, instance, svg_field_name):
        super().__init__(instance=instance, svg_field_name=svg_field_name)
        self.instance = instance
        self.svg_field_name = svg_field_name

    def process(self):
        image_content = getattr(self.instance, self.svg_field_name).read()
        image_str = image_content.decode('utf-8')
        svg_data = image_str[image_str.find('<svg'):]
        setattr(self.instance, f'{self.svg_field_name}_text', svg_data)
        self.instance.save(update_fields=[f'{self.svg_field_name}_text'])
