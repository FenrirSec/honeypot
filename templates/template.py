import json

class Template():
    def __init__(self, template_file):
        self.json_content = json.load(open(template_file))
        self.banner = json_content.get('banner')
        self.name = json_content.get('name')
        self.port = json_content.get('port')
