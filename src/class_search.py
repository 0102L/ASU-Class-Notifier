from lxml import etree
from class_section import Section
import re
import requests

class ASUSearch:
    """
    ASUSearch returns class sections for a specific class
    """
    def __init__(self, major, code):
        """
        :param major: str, user input for major code. Such as "CSE"
        :param code: str, user input for class code. Such as "110"
        """
        self.major = major
        self.code = code

        # Headers to include with the https request
        self.headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/75.0.3770.142 Safari/537.36"
        }

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
        result = requests.get(self.base_url, headers=self.headers)
        return result

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
        if self.total_result > 0:
            for sect_info in self.get_section_list():
                response += sect_info.sect_num + '\t' + sect_info.seats + '\t' + sect_info.instructor + '\n'
        else:
            response = "Error"

        return response

    def get_section_list(self):
        """
        Generate response string by page.
        :return: list of all class sections
        """
        response = list()
        document = etree.HTML(self.page.text)
        if self.total_result > 0:
            for count in range(0, self.total_result):
                response.append(self.analyze_url(count, document))

        else:
            response.append("Error")

        return response

    def any_space(self):
        if self.open_sections():
            return True
        return False

    def open_sections(self):
        """
        Generate response of open sections
        :return list of open class sections
        """
        response = list()
        section_list = self.get_section_list()
        if section_list[0] != "Error":
            for section in section_list:
                if section.is_open():
                    response.append(section.__str__())
        return response

    def analyze_url(self, count: int, available):
        """
        Analyze the document node.
        :param count: int, the current page count.
        :param available: documentNode, a document node to parse into etree.
        :return: Section object for each section found
        """
        if count == 0:
            # Find attributes through regex
            class_node = available.xpath('//*[@id="Any_13"]/text()')
            class_number = re.findall(r'\d+', class_node[0])[0]

            seats_node = available.xpath('//*[@id="informal"]/td[11]/div/span[1]/text()')
            seats_open = re.findall(r'\d+', seats_node[0])[0]

            instructor_node = re.findall(
                r'<a id="DirectLink" title="Instructor\|(.*?)"',
                self.page.text
            )

            # Set instructor
            if instructor_node:
                instructor = instructor_node[0]
            else:
                instructor = "staff"
            
            # Return Section object
            response = Section(class_number, seats_open, instructor)

        else:
            # Find attributes through regex
            class_node = available.xpath(f'//*[@id="Any_13_{str(count - 1)}"]/text()')
            class_number = re.findall(r'\d+', class_node[0])[0]

            seats_node = available.xpath(f'//*[@id="informal_{str(count - 1)}"]/td[11]/div/span[1]/text()')
            seats_open = re.findall(r'\d+', seats_node[0])[0]

            instructor_node = re.findall(
                fr'<a id="DirectLink_{str(count - 1)}" title="Instructor\|(.*?)"',
                self.page.text
            )

            # Set instructor
            if instructor_node:
                instructor = instructor_node[0]
            else:
                instructor = "staff"

            # Return Section object
            response = Section(class_number, seats_open, instructor)

        return response