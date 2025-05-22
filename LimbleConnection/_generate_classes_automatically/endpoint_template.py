from jinja2 import Template, BaseLoader, Environment, FileSystemLoader


env = Environment(loader=FileSystemLoader('.'))
 # .compile(filename='jinja_definition_table_macro.j2'))

def render_this(template_str, data):
    template = env.from_string(template_str)
    rendered_output = template.render(**data)
    print(rendered_output)
    with open('_enpoint_development_output.py', 'w') as outfile:
        outfile.write(rendered_output)


template_str = '''from LimbleConnection import LimbleEndpoint
{% from "jinja_definition_table_macro.j2" import definition_list -%}

class {{ class_name }}{% if 'parent_class' is not none %}({{ parent_class}}){% endif %}:
    \"\"\"Auto-generated class for {{ class_name }}.\"\"\"
    {% if children -%}{% for child in children -%}
    {{ child['parent_field_name'] }} = {{ child['class_name'] }}
    {% endfor -%}
    {% endif -%}
    {% if 'GET' in methods -%}
    {% set method_str = "get" -%}
    {% set this_method = methods['GET'] -%}
    def {{ method_str }}(self{{', ' + ', '.join(this_method['kwargs']) if this_method['kwargs'] is not none else '*args, **kwargs' }}):
        \"\"\"{% if this_method is string %}This method "{{ method_str }}" is a string {{ this_method }}{% else %}{{ this_method['description_table']['non_table_before'] }}

{{ definition_list(
this_method['query_dict'].items(),
this_method['description_table']['headers']
) -}}

{% if this_method['description_table']['non_table_after'] -%}
        non_table_after:
        {{ this_method['description_table']['non_table_after'] -}}
        
{% endif -%}
Parameter descriptions:
{{ definition_list(
this_method['description_table']['data_rows'],
this_method['description_table']['headers']
) -}}
{% endif -%}{# if this_method is string #}
        \"\"\"
        return self._get_request(*args, **kwargs)

    {% endif %}
    {% if 'POST' in methods %}
    {% set method_str = "post" -%}
    {% set this_method = methods['POST'] -%}
    def {{ method_str }}(self{{', ' + ', '.join(this_method['kwargs']) if this_method['kwargs'] is not none else '*args, **kwargs' }}):
        \"\"\"{% if this_method is string %}This method "{{ method_str }}" is a string {{ this_method }}{% else %}{{ this_method['description_table']['non_table_before'] }}

{{ definition_list(
this_method['query_dict'].items(),
this_method['description_table']['headers']
) -}}

{% if this_method['description_table']['non_table_after'] -%}
        non_table_after:
        {{ this_method['description_table']['non_table_after'] -}}
        
{% endif -%}
Parameter descriptions:
{{ definition_list(
this_method['description_table']['data_rows'],
this_method['description_table']['headers']
) -}}
{% endif -%}{# if this_method is string #}
        \"\"\"
        pass

    {% endif %}
    {% if 'PUT' in methods %}
    {% set method_str = "put" -%}
    {% set this_method = methods['PUT'] -%}
    def {{ method_str }}(self{{', ' + ', '.join(this_method['kwargs']) if this_method['kwargs'] is not none else '*args, **kwargs' }}):
        \"\"\"{% if this_method is string %}This method "{{ method_str }}" is a string {{ this_method }}{% else %}{{ this_method['description_table']['non_table_before'] }}

{{ definition_list(
this_method['query_dict'].items(),
this_method['description_table']['headers']
) -}}

{% if this_method['description_table']['non_table_after'] -%}
        non_table_after:
        {{ this_method['description_table']['non_table_after'] -}}
        
{% endif -%}
Parameter descriptions:
{{ definition_list(
this_method['description_table']['data_rows'],
this_method['description_table']['headers']
) -}}
{% endif -%}{# if this_method is string #}
        \"\"\"
        pass

    {% endif %}
    {% if 'DELETE' in methods %}
    {% set method_str = "delete" -%}
    {% set this_method = methods['DELETE'] -%}
    def {{ method_str }}(self{{', ' + ', '.join(this_method['kwargs']) if this_method['kwargs'] is not none else '*args, **kwargs' }}):
        \"\"\"{% if this_method is string %}This method "{{ method_str }}" is a string {{ this_method }}{% else %}{{ this_method['description_table']['non_table_before'] }}

{{ definition_list(
this_method['query_dict'].items(),
this_method['description_table']['headers']
) -}}

{% if this_method['description_table']['non_table_after'] -%}
        non_table_after:
        {{ this_method['description_table']['non_table_after'] -}}
        
{% endif -%}
Parameter descriptions:
{{ definition_list(
this_method['description_table']['data_rows'],
this_method['description_table']['headers']
) -}}
{% endif -%}{# if this_method is string #}
        \"\"\"
        pass

    {% endif %}
    {% if 'PATCH' in methods %}
    {% set method_str = "patch" -%}
    {% set this_method = methods['PATCH'] -%}
    def {{ method_str }}(self{{', ' + ', '.join(this_method['kwargs']) if this_method['kwargs'] is not none else '*args, **kwargs' }}):
        \"\"\"{% if this_method is string %}This method "{{ method_str }}" is a string {{ this_method }}{% else %}{{ this_method['description_table']['non_table_before'] }}

{{ definition_list(
this_method['query_dict'].items(),
this_method['description_table']['headers']
) -}}

{% if this_method['description_table']['non_table_after'] -%}
        non_table_after:
        {{ this_method['description_table']['non_table_after'] -}}
        
{% endif -%}
Parameter descriptions:
{{ definition_list(
this_method['description_table']['data_rows'],
this_method['description_table']['headers']
) -}}
{% endif -%}{# if this_method is string #}
        \"\"\"
    pass
    {% endif %}
'''

## attempted to do a loop for methods, but that may not be a great idea
# template_str = '''from LimbleConnection import LimbleEndpoint
# {% from "jinja_definition_table_macro.j2" import definition_list -%}
#
# class {{ class_name }}{% if 'parent_class' is not none %}({{ parent_class}}){% endif %}:
#     \"\"\"Auto-generated class for {{ class_name }}.\"\"\"
#     {% if children -%}{% for child in children -%}
#     {{ child['parent_field_name'] }} = {{ child['class_name'] }}
#     {% endfor -%}
#     {% endif -%}
#     {# this line intentionally left blank #}
#     {% for method_str in methods -%}
#     {% set this_method = methods[method_str] -%}
#     {% if this_method is string -%}
#     this_method "{{ method_str }}" is a string: {{ this_method }}
#     {% else -%}
#     def {{ method_str }}(self{{', ' + ', '.join(this_method['kwargs']) if this_method['kwargs'] is not none else '*args, **kwargs' }}):
#         \"\"\"        non_table_before:
#         {{ this_method['description_table']['non_table_before'] }}
#     Return data descriptions table:
# {{ definition_list(
# this_method['query_dict'].items(),
# this_method['description_table']['headers']
# ) -}}
#
# Parameter descriptions:
# {{ definition_list(
# this_method['description_table']['data_rows'],
# this_method['description_table']['headers']
# ) -}}
#
#         non_table_after:
#         {{ this_method['description_table']['non_table_after'] -}}
#         \"\"\"
#         return self._get_request(*args, **kwargs)
#
#     {% endif -%}
#     {% endfor -%}
# '''


# {{"%-30s" | format(row[0]) -}}{{row[1][:100] -}}{{"\nNEWLINE" + row[1][100:] if row[1] | length > 100 else none -}}  # CUTS WORDS IN HALF, NO INDENTATION

# {#        {{ "%-30s %s"|format(row[0]+':', row[1][:100 - row[1][100::-1].index(' ')]) }}
#         {{row[1][100 - row[1][100::-1].index(' '):] | indent(width=38) }}  -#}
# {{"%-30s %s" | format(row[0] + ':', row[1] | wordwrap(width=70))}}

if __name__ == '__main__':
    data = {
        'class_name': 'Users',
        'methods': {"GET": {'docstring': 'dummy docstring',
                            'kwargs': ['users', 'name', 'roles', 'teams', 'cursor', 'limit'],
                            },
                    "POST": {},
                    "PUT": {},
                    },
        'parent_class': 'LimbleEndpoint',
        'children': [...]
        # ''
    }


    render_this(template_str, data)
    pass