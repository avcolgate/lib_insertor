import os
from classes import *
from typing import List

def check_files(files: list):
    for file in files:
        if not os.path.exists(file):
            print(f"File {file} not found! Exiting...\n")
            exit()


def read_cell_file(path: str) -> List[str]:
    with open(file=path, mode='rt') as file:
        cells = file.read().split()
    return cells


def parse_tamplates(lines: list) -> list:
    template_list = list()
    template_section = False

    for line_num, line in enumerate(lines):
            if (line.strip().startswith("lu_table_template") or line.strip().startswith("power_lut_template")) and \
                line.endswith('{') and not template_section:
                template_section = True
                template = Template()
                template.name = line[line.find('(')+1:line.find(')')].replace('"', '').strip()

            if line.endswith('}') and template_section:
                template.body.append(line)
                template_list.append(template)
                template_section = False
                del template

            if template_section:
                template.body.append(line)

            if line.replace(' ', '').startswith("cell(") and line.strip().endswith('{'):
                break
    return template_list


def parse_cells(lines: list) -> list:
    cell_list = list()
    cell_section = False

    for line_num, line in enumerate(lines):
            if line.replace(' ', '').startswith("cell(") and line.strip().endswith('{') and not cell_section:
                cell_section = True
                cell = Cell()
                open_curly_bracket = 0
                close_curly_bracket = 0
                cell.name = line[line.find('(')+1:line.find(')')].replace('"', '').strip()

            if ('}') in line and cell_section and open_curly_bracket == close_curly_bracket + 1:
                cell.body.append(line)
                cell_list.append(cell)
                cell_section = False
                del cell

            if cell_section:
                if '{' in line:
                    open_curly_bracket += 1
                if '}' in line:
                    close_curly_bracket += 1

                cell.body.append(line)
    return cell_list


def delete_cells(lines: list, cell_name_list: list) -> list:
    # output_name = 'deletion.lib'
    # output = open(output_name , 'w')

    cell_section = False

    for cell_name in cell_name_list:
        start_cell_line = -1
        end_cell_line = -1
        open_curly_bracket = 0
        close_curly_bracket = 0
        for line_num, line in enumerate(lines):
            if line.replace(' ', '').startswith(f"cell({cell_name})") and line.strip().endswith('{'):
                cell_section = True
                start_cell_line = line_num
            if ('}') in line and cell_section and open_curly_bracket == close_curly_bracket + 1:
                cell_section = False
                end_cell_line = line_num
            if cell_section:
                if '{' in line:
                    open_curly_bracket += 1
                if '}' in line:
                    close_curly_bracket += 1
        
        # print(start_cell_line, end_cell_line)
        if start_cell_line != -1 and end_cell_line != 1:
            lines = lines[0:start_cell_line] + lines[end_cell_line + 1:]
    
    # for line in lines:
    #     output.write("%s\n" % line)

    return lines


def insert_cells(lines: list, cells: list, cell_list: list) -> list:
    # output_name = 'cell_insertion.lib'
    # output = open(output_name , 'w')
    start_insert_line = 0

    for line_num, line in enumerate(lines):
        if '}' in line:
            start_insert_line = line_num - 1
    # print(start_insert_line)

    for line_num, line in enumerate(lines):
        if line_num > start_insert_line:
            for cell in cells[::-1]:
                if cell.name in cell_list:
                    for cell_line in cell.body[::-1]:
                        lines.insert(line_num, cell_line)
            break

    # for line in lines:
    #     output.write("%s\n" % line)

    return lines


def insert_templates(lines: list, template_list: list) -> list:
    # output_name = 'template_insertion.lib'
    # output = open(output_name , 'w')
    start_insert_line = 0

    for line_num, line in enumerate(lines):
        if line.strip().startswith("lu_table_template") and line.endswith('{'):
            start_insert_line = line_num - 1
            break
    # print(start_insert_line)

    for line_num, line in enumerate(lines):
        if line_num > start_insert_line:
            for template in template_list[::-1]:
                if not template.name in lines:
                    for template_line in template.body[::-1]:
                        if template_line.startswith("    "):  # deletion 2 spaces in the beginning of line
                            template_line =  template_line[2:]
                        lines.insert(line_num, template_line)
            break

    # for line in lines:
    #     output.write("%s\n" % line)

    return lines


def check_cells(lib_cells: list, user_cells: list) -> list:
    lib_cells_string = ""
    for cell in lib_cells:
        lib_cells_string += cell.name

    for cell in user_cells:
        if cell not in lib_cells_string:
            print(f"Warning: cell {cell} not found in source Liberty! It will be skipped...\n")


def write_output(name: str, lines: list) -> None:
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    with open(file=f"{output_dir}/{name}_upd.lib", mode='w') as output:
        for line in lines:
            output.write("%s\n" % line)