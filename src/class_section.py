class Section:
    """
    Section class for storing a section's information
    """
    def __init__(self, sect_num, seats_open, instructor):
        """
        :param sect_num: str, unique code that ASU provides for each section
        :param seats_open: str, remaining available seats in a section
        :param instructor: str, full name of assigned instructor
        """
        self.sect_num = sect_num
        self.seats = seats_open
        self.instructor = instructor

    def is_open(self):
        """
        Determine if the section has room for students
        :return: bool, if there is available space in the section
        """
        if int(self.seats) > 0:
            return True
        return False

    def __str__(self):
        """
        Generate string of section info
        :return: str, full information of section
        """
        return self.sect_num + '\t' + self.seats + '\t' + self.instructor