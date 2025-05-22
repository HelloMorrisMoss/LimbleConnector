from pprint import pp, pprint
from traceback import format_exc as exc

from bs4 import BeautifulSoup
from postmanparser import Collection


def clean_bs4_text(soup_fragment):
    """Clean <p> and <b> tags and return text with preserved line breaks."""
    for tag in soup_fragment.find_all(['b', 'strong']):
        tag.unwrap()
    for p in soup_fragment.find_all('p'):
        p.insert_after('\n')
        p.unwrap()
    return soup_fragment.get_text()

def get_text_and_table(text: str):
    """Extract a markdown or HTML table from the text, returning uniform dictionary format."""
    # First, let BeautifulSoup try to parse HTML content and extract any <table>
    bs = BeautifulSoup(text, 'html.parser')
    table = bs.find('table')
    if table:
        headers = []
        data_rows = []
        for i, tr in enumerate(table.find_all('tr')):
            cells = tr.find_all(['th', 'td'])
            cell_text = [clean_bs4_text(c) for c in cells]
            if i == 0:
                headers = cell_text
            else:
                data_rows.append(cell_text)
        table.decompose()
        cleaned_text = clean_bs4_text(bs)
        return {
            'headers': headers,
            'data_rows': data_rows,
            'non_table_before': cleaned_text.strip(),
            'non_table_after': ''
        }

    # If no HTML table, attempt markdown table extraction
    table_start = text.find('|')
    table_end = len(text) - text[::-1].find('|')
    if table_start == -1 or table_end == -1:
        return {
            'headers': [],
            'data_rows': [],
            'non_table_before': text,
            'non_table_after': ''
        }

    non_table_before = text[:table_start]
    non_table_after = text[table_end:]
    table_txt = text[table_start:table_end]
    headers = []
    data_rows = []

    for ln, line in enumerate(table_txt.splitlines()):
        line = line.strip()
        if not line or not line.startswith('|'):
            continue
        cells = [x.strip() for x in line[1:-1].split('|')]
        if ln == 0:
            headers = cells
        elif ln == 1:
            continue  # skip the separator line
        else:
            data_rows.append(cells)

    return {
        'non_table_text_before': non_table_before,
        'headers': headers,
        'data_rows': data_rows,
        'non_table_text_after': non_table_after
    }


def get_md_table(text: str):
    """Try to extract a markdown formatted table from the text.

    example this input text:
    '''
    The response of this request is documented as a JSON schema.

    <p><b>Return data description</b></p>
    | **Property** | **Description** |
    | --- | --- |
    | partID | The ID of the part the purchasable belongs to. |
    | name | The name of the purchasable. |
    | size | The size of the purchasable. |
    | orderUnitCode | The unit how the purchasable is ordered. E.g. \"by the box\", or \"by the foot\".|
    | sizeUnitCode | The size of the unit. E.g. whether it is 10 liters, or cans, or feet, etc. |"
    '''

    Would return a dictionary like this:
    {'headers': ['**Property**', '**Description**'],
     'data_rows':[
        ['partID', 'The ID of the part the purchasable belongs to.'],
        ['name', 'The name of the purchasable.'],
        ['size', 'The size of the purchasable.'],
        ['orderUnitCode', 'The unit how the purchasable is ordered. E.g. "by the box", or "by the foot".'],
        ['sizeUnitCode', 'The size of the unit. E.g. whether it is 10 liters, or cans, or feet, etc.']
    ],
    'non_table_before': '    The response of this request is documented as a JSON schema.\n\n'
        '<p><b>Return data description</b></p>',
    'non_table_after': ''
    }
    The whitespace of the non-table text is left as-is.
    """
    table_start: int = text.find('|')  # index in the string of the first pipe character
    table_end: int = len(text) - text[::-1].find('|')  # index in the string of the last pipe character
    non_table_before = text[:table_start]
    non_table_after = text[table_end:]
    table_txt = text[table_start:table_end]
    headers = []
    data_rows = []
    for ln, line in enumerate(table_txt.splitlines()):
        cells = [x.strip() for x in line[1:-2].split('|')]
        if ln == 0:
            headers = cells
        elif ln == 1:
            pass  # don't care about the line break
        else:
            data_rows.append(cells)
    return {'headers': headers, 'data_rows': data_rows, 'non_table_before': non_table_before,
            'non_table_after': non_table_after}


def lucid(obj):
    """Quick "show me what you've got" function for development."""
    items = obj.items() if isinstance(obj, dict) else obj.__dict__.items()
    for k,v in items:
        if not k.startswith('__'):
            print(f'{k} ({type(v)}: {v}')


def get_url_variables(var_url, indent='    ', top_level_indent_count = 1):
    url_data = []
    var_keys = 'id', 'key', 'value', 'variable_type', 'name', 'description', 'system'
    variable_lines = ''
    subind = top_level_indent_count + 1
    for vnum, this_var in enumerate(var_url.variable):
        if vnum > 0:
            variable_lines += '\n\n'  # blank line between variables for readability
        variable_lines += "\n".join([f'{indent * subind}{k}: {getattr(this_var, k)}' for k in var_keys])
    if not variable_lines:
        variable_lines = f'{indent * subind}No variables found.'
    url_data.append(f'{indent * top_level_indent_count}Variables:\n{variable_lines}')
    # pprint(url_data)
    return url_data


def extract_return_data_html_table_to_dict(description_text: str):
    bs = BeautifulSoup(description_text, 'html.parser')
    return_data_desc_items = {}
    table = bs.find('table')
    if table:
        for tr in table.find_all('tr'):
            columns = [c.text for c in tr.find_all('td')]
            if columns:
                # print(columns)
                return_data_desc_items[columns[0]] = columns[1]
        bs.table.decompose()
    non_table_text = bs.text
    return non_table_text, return_data_desc_items


def generate_placeholder_classes(path_dict, indent: str='    '):
    from collections import defaultdict

    # Strip the "Routes/" prefix and sort by depth (deepest first)
    clean_paths = [path[len("Routes/"):].replace(' ', '_') for path in list(path_dict.keys())]
    # print(f'{clean_paths=}')
    clean_paths.sort(key=lambda p: -len(p.split("/")))

    class_defs = {}
    children_map = defaultdict(list)

    # map each path to its class name and track children
    for path in clean_paths:
        parts = path.split("/")
        class_name = "_".join(parts)
        class_defs[path] = class_name

        if len(parts) > 1:
            parent_path = "/".join(parts[:-1])
            children_map[parent_path].append((parts[-1], class_name))

    # output_lines = []
    output_class_data = {}
    written = set()

    # write class definitions with children
    for path in clean_paths:
        if path in written or len(path) == 0:
            continue

        # print(f'Trying to generate documentation for endpoint: {path}')

        class_name = class_defs[path]
        # the keys still have spaces
        endpoint = path_dict.get("Routes/" + path.replace('_', ' '), f"{class_name} description" if class_name else "")
        class_dict = {'class_name': class_name, 'endpoint': endpoint, 'requests': {}, 'path': path, 'children': []}

        try:
            rq_dct = {}
            for rq in endpoint:  # this should be an HTTP method definition
                request_metadata = {}
                if isinstance(rq, str):
                    print(f'rq is string: {rq=}')
                else:
                    # print(f'Processing method: {rq.method=}')
                    if isinstance(rq.url, str):
                        print(f'rq.url is a string: {rq.url}')
                        rq_dct[rq.method] = indent * 2 + rq.url
                    else:
                        query_desc, url_data, extra_params, query_dict = get_url_data(indent, path, rq)
                        url_desc = '\n'.join(url_data)
                        query_desc += f'\n{indent * 2}URL data:\n' + url_desc

                        request_metadata['method'] = rq.method
                        request_metadata['url_data'] = url_data
                        request_metadata['query_desc'] = query_desc
                        request_metadata['query_dict'] = query_dict
                        request_metadata['extra_params'] = extra_params

                        if hasattr(rq, 'name'):  # doesn't seem like postmanparser will include this
                            print(f'rq has a name: {rq.name=}')
                            rq_name = f'\n\n{indent}{rq.name=}\n\n'
                            query_desc += rq_name
                            request_metadata['request_name'] = rq.name

                        if hasattr(rq, 'description'):
                            if rq.description:
                                request_metadata['description_table_processed'] = get_text_and_table(rq.description)
                                pass
                        rq_dct[rq.method] = request_metadata


            class_dict['children'] = sorted(children_map.get(path, []))

            if not rq_dct:
                print(f'No methods in rq_dct found for {path}!')
            else:
                class_dict['requests'] = rq_dct
        except Exception as uhe:
            print(exc())
        written.add(path)
        output_class_data[class_name] = class_dict
        # # url_descriptions = [f'url is a string: {rq.url}' if isinstance(rq.url, str) else x.description for x in rq.url.variable for rq in class_dict['endpoint']]
        # try:
        #     url_descriptions = [
        #                         f'url is a string: {rq.url}' if isinstance(rq.url, str) else var.description
        #                         for rq in class_dict['endpoint']
        #                         for var in rq.url.variable
        #                     ]
        # except AttributeError:
        #     pass
        # if len(set(url_descriptions)) != 1:
        #     pass
        # # for rq in :
        # pp(class_dict)
    metadata = {'clean_paths': clean_paths, 'children_map': children_map, 'class_defs': class_defs}

    # print("\n".join(output_lines))
    return output_class_data, metadata


def get_url_data(indent, path, rq):
    # look for url fields
    url_data = []
    # todo: just pass back the dict and do the formatting in here?
    extra_params_list,  extra_params_dict = get_extra_parameters(indent, rq)
    url_data += extra_params_list

    # try to add url query data
    query_desc = '\n'.join([f'{indent * 2}{q.key}: {q.description}' for q in rq.url.query])
    query_dict = {q.key: q.description for q in rq.url.query}
    if not query_desc:  # if that's empty
        if hasattr(rq.url, 'description'):
            print(f'rq.url has a description!')
            query_desc = f'{indent * 2}URL-desc: {rq.url.description=}'
        else:
            query_desc = f'{indent * 2}No query or url description found for {path}-{rq.method}'
    if hasattr(rq.url, 'variable'):
        url_data.append('')  # blank line
        url_data += get_url_variables(rq.url, indent=indent, top_level_indent_count=3)
    return query_desc, url_data, extra_params_dict, query_dict


def get_extra_parameters(indent, rq):
    found_url_data = []
    extra_parameters = {}
    for key in dir(rq.url):
        if key.startswith('__') or (key in ('parse', 'variable', 'query')):
            pass
        else:
            value = getattr(rq.url, key)
            # if value:
            found_url_data.append(f'{indent * 3}{key}: {value}')
            extra_parameters[key] = value
        # extra_parameters['url_variables'] = [{key: value for key, value in url_var.__dict__.items()
        #                                       if not key.startswith('__')}
        #                  for url_var in rq.url.variable] if not isinstance(rq.url, str) else []
        if not isinstance(rq.url, str):
            extra_parameters['variable'] = [{key: value for key, value in url_var.__dict__.items()
                                              if not key.startswith('__')}
                         for url_var in rq.url.variable]
        else:
            extra_parameters['variable'] = []

    return found_url_data, extra_parameters



# get the data from the file
collection = Collection()
collection.parse_from_file(r"C:\Users\lmcglaughlin_local\Downloads\Limble API V2.postman_collection.json")
path_dict = collection.get_requests_map()

result, mtadata = generate_placeholder_classes(path_dict, '    ')

from end_point_dataclass import *
endpoints = {}
for path, details in result.items():
    try:
        endpoints[path] = EndPoint(name=path, path=path,
                               methods={k: UrlInfo(**(v['extra_params'] | {'description': v['query_desc'],
                                   'description_table': DescriptionTable(**v['description_table_processed'],),
                                   'query_dict': v['query_dict'],})) if not isinstance(v, str) else v for k, v in
                                        result['Assets']['requests'].items()},
                               children=[endpoints[child[1]] for child in details['children']],
                               )
    except Exception as uhe:
        print(uhe)
        pass

from endpoint_template import template_str, Template, render_this

# def render_this(template_str, data):
#     template = Template(template_str)
#     rendered_output = template.render(**data)
#     print(rendered_output)



# import json
# with open(r"./LimbleConnection/result_data.py", "w") as f:
#     # f.write(result)
#     json.dump(result, f, indent=4)
render_this(data=endpoints['Assets'].dictification(), template_str=template_str)
pass
"        assets:             This parameter is used to only get specific Assets. This parameter expects a"
# pp({k: UrlInfo(**v['extra_params']) if not isinstance(v, str) else v for k,v in result['Assets']['requests'].items()})
