from class_search import ASUClassSearch

def seat_check(dept_code: str, class_code: str):
    """
    Determine if there are open seats in a class
    :return bool of if seats are available
    """
    api = ASUClassSearch(dept_code, class_code)
    section_list = api.get_section_list()
    if section_list[0] != "Error":
        for section in section_list:
            if section[1] != "0":
                return True
    return False

def class_list(dept_code: str, class_code: str):
    """
    Determine if there are open seats in a class
    :return str of all class sections
    """
    response = ""
    api = ASUClassSearch(dept_code, class_code)
    response = api.__str__()
    return response

def open_sections(dept_code: str, class_code: str):
    """
    Determine if there are open seats in a class
    :return str of open class sections
    """
    response = ""
    api = ASUClassSearch(dept_code, class_code)
    section_list = api.get_section_list()
    if section_list[0] != "Error":
        for section in section_list:
            if section[1] != "0":
                response += '\t'.join(section) + "\n"
    return response
