from jinja2 import Environment, FileSystemLoader

def getTemplate(templatefile,**kwargs):
    TEMPLATE_FILE=templatefile
    templateLoader = FileSystemLoader( searchpath="templates/" )
    templateEnv = Environment( loader=templateLoader )
    template = templateEnv.get_template(TEMPLATE_FILE)
    html = template.render(kwargs)
    return html