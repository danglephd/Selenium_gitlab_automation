import shutil
import os
from pathlib import Path
from openpyxl import load_workbook
from datetime import datetime
from ..helper import write_log


def get_testcase_root_path():
    configured_root = os.getenv("TESTCASE_ROOT_PATH", "/media/dango/data1/Testcase/RPA").strip()
    if not configured_root:
        configured_root = "/media/dango/data1/Testcase/RPA"
    return configured_root


def get_template_path(project):
    project_root = Path(__file__).resolve().parents[3]
    candidate_paths = [
        project_root / "TEMPLATE" / f"Testcase-template-{project}.xlsx",
        Path.cwd() / "TEMPLATE" / f"Testcase-template-{project}.xlsx",
        Path("./TEMPLATE") / f"Testcase-template-{project}.xlsx",
    ]

    for candidate in candidate_paths:
        if candidate.exists():
            return candidate

    fallback = candidate_paths[0]
    raise FileNotFoundError(f"Template file not found for project '{project}': {fallback}")


def create_testcase_file(iss_number, project, folder_name, file_name):
    write_log(f"create_testcase_file: {iss_number}, {project}, {folder_name}, {file_name}")

    testcase_root = Path(get_testcase_root_path())
    dest_folder = testcase_root / project / folder_name
    dest_file = dest_folder / f"{file_name}.xlsx"
    template_file = get_template_path(project)

    write_log(f"Source file: {template_file}, Destination file: {dest_file}")

    dest_folder.mkdir(parents=True, exist_ok=True)
    shutil.copy2(str(template_file), str(dest_file))

    return str(dest_file)

def update_file_testcase(path, iss_test_number, issue_desc, test_scenario):
    write_log(f"Update file testcase: {path}")
    #load excel file
    workbook = load_workbook(filename=path)
    
    #open workbook
    sheet = workbook.active
    
    #modify the desired cell
    sheet["C1"] = iss_test_number
    sheet["F1"] = issue_desc
    sheet["B14"] = test_scenario
    
    #save the file
    workbook.save(path)

def update_finish_date_file_testcase(path):
    write_log(f"Update finish date file testcase: {path}")

    #load excel file
    workbook = load_workbook(filename=path)
    
    #open workbook
    sheet = workbook.active

    # Merge cell F6 và F7
    sheet.merge_cells('F6:G6')

    # Gán giá trị ngày hiện tại theo format DD/MM/YYYY
    today_str = datetime.now().strftime("%d/%m/%Y")
    sheet["F6"] = today_str

    # save the file
    workbook.save(path)