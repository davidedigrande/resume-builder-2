import yaml
from jinja2 import Template


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
        return obj.replace('\n', '<br>')
    else:
        return obj


with open('resume.yml') as file:
    resume_yml_text = file.read()
    resume_data = yaml.load(resume_yml_text, Loader=yaml.FullLoader)
    resume_data = replace_newlines(resume_data)
    resume_data = boldify(resume_data)


with open('template.html') as f:
    template = Template(f.read())

html = template.render(resume_data)

with open('resume.html', "w+") as f:
    f.write(html)