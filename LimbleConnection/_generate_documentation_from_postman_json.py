from pprint import pp, pprint
from traceback import format_exc as exc

from bs4 import BeautifulSoup
from postmanparser import Collection


def get_md_table(text: str):
    table_start = text.find('|')
    table_end = len(text) - text[::-1].find('|')
    non_table_before = text[:table_start]
    non_table_after = text[table_end:]
    table_txt = text[table_start:table_end]
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
    for k,v in obj.__dict__.items():
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
    print(f'{clean_paths=}')
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

    output_lines = []
    written = set()

    # write class definitions with children
    for path in clean_paths:
        if path in written or len(path) == 0:
            continue

        print(f'Trying to generate documentation for endpoint: {path}')

        class_name = class_defs[path]
        # the keys still have spaces
        endpoint = path_dict.get("Routes/" + path.replace('_', ' '), f"{class_name} description" if class_name else "")

        try:
            rq_dct = {}
            for rq in endpoint:  # this should be an HTTP method definition
                if isinstance(rq, str):
                    print(f'rq is string: {rq=}')
                else:
                    print(f'Processing method: {rq.method=}')
                    if isinstance(rq.url, str):
                        print(f'rq.url is a string: {rq.url}')
                        rq_dct[rq.method] = indent * 2 + rq.url
                    else:
                        # look for url fields
                        url_data = []
                        for key in dir(rq.url):
                            if key.startswith('__') or (key in ('parse', 'variable', 'query')):
                                pass
                            else:
                                value = getattr(rq.url, key)
                                # if value:
                                url_data.append(f'{indent * 3}{key}: {value}')

                        # try to add url query data
                        query_desc = '\n'.join([f'{indent * 2}{q.key}: {q.description}' for q in rq.url.query])
                        if not query_desc:  # if that's empty
                            if hasattr(rq.url, 'description'):
                                print(f'rq.url has a description!')
                                query_desc = f'{indent * 2}URL-desc: {rq.url.description=}'
                            else:
                                query_desc = f'{indent * 2}No query or url description found for {path}-{rq.method}'

                        if hasattr(rq.url, 'variable'):
                            url_data.append('')  # blank line
                            url_data += get_url_variables(rq.url, indent=indent, top_level_indent_count=3)
                        url_desc = '\n'.join(url_data)
                        query_desc += f'\n{indent * 2}URL data:\n' + url_desc

                        # pprint(f'after initial url.description: {query_desc=}', width=120)

                        if hasattr(rq, 'name'):  # doesn't seem like postmanparser will include this
                            print(f'rq has a name: {rq.name=}')
                            rq_name = f'\n\n{indent}{rq.name=}\n\n'
                            query_desc += rq_name

                        if hasattr(rq, 'description'):
                            # print(f'rq has a description: {rq.description=}')
                            if rq.description:
                                if '|' in rq.description:
                                    # todo: this should maybe be reworked to only tear up the md table after bs4 has had its try
                                    table_data: dict = get_md_table(rq.description)
                                    # {'headers': headers, 'data_rows': data_rows, 'non_table_before': non_table_before,
                                    #  'non_table_after': non_table_after}
                                    rq_desc = ''
                                    if table_data['non_table_before']:
                                        rq_desc += f'''{indent * 2}{table_data['non_table_before']}\n'''
                                    # if any(table_data['headers']):
                                    #     rq_desc += f'''{indent * 2}{table_data['headers']}\n'''
                                    if any(table_data['data_rows']):
                                        for dr in table_data['data_rows']:
                                            rq_desc += f'''{indent * 2}{dr[0]}: {dr[1]}\n'''
                                    if table_data['non_table_after']:
                                        # while not rq_desc.endswith('\n\n'):  # make sure there's some space
                                        #     rq_desc += '\n'
                                        rq_desc += f'''{indent * 2}{table_data['non_table_after']}\n'''
                                else:
                                    non_table_text, return_data_desc_items = extract_return_data_html_table_to_dict(rq.description)
                                    rq_desc = f'\n\n'  # space before the description
                                    for rd_Line in non_table_text.splitlines():
                                        rq_desc += f'{indent * 2}{rd_Line}\n'
                                    rq_desc += f'\n'  # space between 'Return data description' and the data from the table
                                    for k,v in return_data_desc_items.items():
                                        rq_desc += f'{indent * 2}{k}: {v}\n'
                                    # rq_desc += '\n\n'  # space after the table
                                    # pp(rq_desc, width=120)
                                query_desc += rq_desc
                        # pprint(f'after rq.description: {query_desc=}', width=120)

                        rq_dct[rq.method] = query_desc
                        # pprint(f'after appending url.description: {query_desc=}', width=120)
            if not rq_dct:
                print(f'No methods in rq_dct found for {path}!')
            docstring = '\n\n'.join(
                [f'{indent}{k}:\n{desc}' if len(desc) else "" for k, desc in rq_dct.items()]).strip()

            lines = [f"class {class_name.replace(' ', '_')}:",
                     f'{indent}"""Automatically extracted documentation for {class_name}.\n\n    {docstring}\n"""']

            for attr, child_class in sorted(children_map.get(path, [])):
                lines.append(f"{indent}{attr.lower()} = {child_class}")

            output_lines.extend(lines)
            output_lines.append("\n\n")  # blank lines between classes
        except Exception as uhe:
            print(exc())
        written.add(path)

    metadata = {'clean_paths': clean_paths, 'children_map': children_map}

    # print("\n".join(output_lines))
    return "\n".join(output_lines), metadata


# get the data from the file
collection = Collection()
collection.parse_from_file(r"C:\Users\lmcglaughlin_local\Downloads\Limble API V2.postman_collection.json")
path_dict = collection.get_requests_map()

result, mtadata = generate_placeholder_classes(path_dict, '    ')

with open(r"C:\Users\lmcglaughlin_local\PycharmProjects\LimbleConnector\LimbleConnection\placeholder_classes.py",
          "w") as f:
    f.write(result)

pass
