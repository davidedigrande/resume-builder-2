import yaml
from jinja2 import Template, Environment, FileSystemLoader


def boldify(obj):
    if isinstance(obj, dict):
        return {k: boldify(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [boldify(elem) for elem in obj]
    elif isinstance(obj, str):
        while "*" in obj:
            obj = obj.replace("*", "<strong>", 1).replace("*", "</strong>", 1)
        return obj
    else:
        return obj


def replace_newlines(obj):
    if isinstance(obj, dict):
        return {k: replace_newlines(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_newlines(elem) for elem in obj]
    elif isinstance(obj, str):
        obj = obj.replace("\n\n", '<br><br style="line-height: 50%">')
        obj = obj.replace('\n', '<br>')
        return obj
    else:
        return obj


with open('resume.yml') as file:
    resume_yml_text = file.read()
    resume_data = yaml.load(resume_yml_text, Loader=yaml.FullLoader)
    resume_data = replace_newlines(resume_data)
    resume_data = boldify(resume_data)


with open('template.html') as f:
    environment = Environment(loader=FileSystemLoader('.'))
    template = environment.from_string(f.read())
    html = template.render(resume_data)

with open('resume.html', "w+") as f:
    f.write(html)