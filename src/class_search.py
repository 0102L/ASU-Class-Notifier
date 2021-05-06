import re
import requests
from lxml import etree

# Headers to include with the https request
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/75.0.3770.142 Safari/537.36"
}

def generate_response(instructor_full_node: list, class_number: str, seats_open: str):
    """
    Generate response from input.
    :param instructor_full_node: list, the full node is generated from etree.HTML() function.
    :param class_number: str, user stored class number.
    :param seats_open: str, how many seats are left.

    :return list() of params for the class section.
    """
    response = list()
    if instructor_full_node:
        instructor_full = instructor_full_node[0]
    else:
        instructor_full = "staff"

    # Add attributes to class section
    response.append(class_number)
    response.append(seats_open)
    response.append(instructor_full)

    return response

class ASUClassSearch:
    """
    ASU class finder class for searching in ASU website for courses.
    """

    def __init__(self, major, code):
        """
        :param major: str, user input for major code. Such as "CSE"
        :param code: str, user input for class code. Such as "110"
        """
        self.major = major
        self.code = code

        # Fall 2021 catalog URL format
        self.base_url = f"https://webapp4.asu.edu/catalog/myclasslistresults?t=2217" \
                        f"&s={major}&n={code}&hon=F&promod=F&e=all&page=1"

        self.page = self._get_page()
        self.total_result = self.get_page_count()

    def _get_page(self):
        """
        Helper method to get response text.
        :return: HTTPRequest.
        """
        res = requests.get(self.base_url, headers=headers)
        return res

    def get_page_count(self):
        """
        Get page count total
        :return: int, page count total.
        """
        result_node = re.findall(r'.*?of (\d+)', self.page.text)
        if result_node:
            total_result = int(result_node[0])
        else:
            total_result = 0

        return total_result

    def __str__(self):
        """
        Generate response string by page.
        :return: str, full response of the search result.
        """
        response = ""
        document = etree.HTML(self.page.text)
        if self.total_result > 0:
            for count in range(0, self.total_result):
                response += '\t'.join(''.join(class_info) for class_info in self.analyze_url(count, document)) + '\n'

        else:
            response = "Error. No response."

        return response

    def get_seat_count(self):
        """
        Generate response string by page.
        :return: str, seat counts of the results.
        """
        response = ""
        document = etree.HTML(self.page.text)
        if self.total_result > 0:
            for count in range(0, self.total_result):
                if count == 0:
                    seats_open_string = document.xpath('//*[@id="informal"]/td[11]/div/span[1]/text()')
                    seats_open = re.findall(r'\d+', seats_open_string[0])[0]
                    response += seats_open
                else:
                    seats_open_string = document.xpath(f'//*[@id="informal_{str(count - 1)}"]'
                                                        f'/td[11]/div/span[1]/text()')
                    seats_open = re.findall(r'\d+', seats_open_string[0])[0]
                    response += seats_open
        else:
            response = "Error. No response."
        return response

    def get_section_list(self):
        """
        Generate response string by page.
        :return: list of each section details
        """
        response = list()
        document = etree.HTML(self.page.text)
        if self.total_result > 0:
            for count in range(0, self.total_result):
                response.append(self.analyze_url(count, document))

        else:
            response.append("Error")

        return response

    def analyze_url(self, count: int, available):
        """
        Analyze the document node.
        :param count: int, the current page count.
        :param available: documentNode, a document node to parse into etree.
        :return: list() response for one page that depends on the page number.
        """
        if count == 0:
            class_number_string = available.xpath('//*[@id="Any_13"]/text()')
            class_number = re.findall(r'\d+', class_number_string[0])[0]

            seats_open_string = available.xpath('//*[@id="informal"]/td[11]/div/span[1]/text()')
            seats_open = re.findall(r'\d+', seats_open_string[0])[0]

            instructor_full_string = re.findall(
                r'<a id="DirectLink" title="Instructor\|(.*?)"',
                self.page.text
            )

            response = generate_response(instructor_full_string, class_number, seats_open)

        else:
            class_number_string = available.xpath(f'//*[@id="Any_13_{str(count - 1)}"]/text()')
            class_number = re.findall(r'\d+', class_number_string[0])[0]

            seats_open_string = available.xpath(f'//*[@id="informal_{str(count - 1)}"]'
                                                f'/td[11]/div/span[1]/text()')

            seats_open = re.findall(r'\d+', seats_open_string[0])[0]

            instructor_full_string = re.findall(
                fr'<a id="DirectLink_{str(count - 1)}" title="Instructor\|(.*?)"',
                self.page.text
            )

            response = generate_response(instructor_full_string, class_number, seats_open)

        return response