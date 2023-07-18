from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def base64_to_image(data):
    if '![](data:image/' in data:
        data = data.replace('![]', '')
        
        while data.find('(data:image') != -1:
            start_index = data.find('(data:image')
            end_index = data.find(')', start_index)
            print(start_index, end_index)
            
            data = data[:start_index] + f'<img src="{data[start_index + 1:end_index]}">' + data[end_index + 1:]
        
        return mark_safe(data)
    
    else:
        return mark_safe(data)