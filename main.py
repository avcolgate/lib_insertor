import sys
from classes import Library
from funcs import *

# dest_lib_path = "src/CORELIB8DLL.lib"
# src_lib_path = "src/cmosf8_ssg_1p62v_125c.lib"
# cell_list_to_delete_path = "NR2ALL NR2ALLP NR2ALLX3 NR3ALL NR3ALLP NR3ALLX4"

if len(sys.argv) != 4:
    print('Check args! Exiting...\n \
          arg 1 - destination Liberty\n \
          arg 2 - source Liberty\n \
          arg 3 - file containing cell names to be inserted from the source Liberty\n')
    exit()

dest_lib_path = sys.argv[1]
src_lib_path = sys.argv[2]
cell_list_to_delete_path = sys.argv[3]

check_files([dest_lib_path, src_lib_path, cell_list_to_delete_path])

def main(dest_lib_path: str, src_lib_path: str, cell_list_to_delete_path: str):
    
    cell_list_to_delete = read_cell_file(cell_list_to_delete_path)

    dest_lib = Library(dest_lib_path)
    src_lib = Library(src_lib_path)

    src_lib.templates = parse_tamplates(src_lib.body)
    src_lib.cells = parse_cells(src_lib.body)

    check_cells(src_lib.cells, cell_list_to_delete)

    dest_lib.body = delete_cells(dest_lib.body, cell_list_to_delete)
    dest_lib.body = insert_templates(dest_lib.body, src_lib.templates)
    dest_lib.body = insert_cells(dest_lib.body, src_lib.cells)

    print("Insertion is done!\n")

    write_output(dest_lib.name, dest_lib.body)


if __name__ == "__main__":
    main(dest_lib_path, src_lib_path, cell_list_to_delete_path)