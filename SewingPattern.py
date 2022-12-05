import math
from abc import ABC, abstractmethod

import pandas as pd
from PIL import Image, ImageDraw

IMAGE_MARGIN = 50
IMAGE_CM = 100
CM_SQUARE_POS = 120
SMALL_PATTERN_MARGIN = 2
MEDIUME_PATTERN_MARGIN = 2
LARGE_PATTERN_MARGIN = 5


class SewingPattern(ABC):
    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError("Pattern Name Must Be String")
        self.pattern_name = name
        self.size = None

    def get_known_size(self, size, file_name):
        """
        Reads size information from csv file and returns the data for the relevant size.
        :param size: str, the wanted size.
        :param file_name: str, the name of the csv file with the size's data.
        :return: dict, the data for the relevant size.
        """

        def df_line_to_dict(df, size):
            """
            Gets the wanted line from the data frame and returns it as a dictionary.
            :param df: dataframe, measurements for patterns by size.
            :param size: str, the wanted size.
            :return: dictionary, measurements for the wanted size.
            """
            return df.loc[df['size'] == int(size)].to_dict(orient='records')[0]

        if not isinstance(file_name, str):
            raise TypeError("File Name Must Be String")
        try:
            df = pd.read_csv(file_name)
            self.size = df_line_to_dict(df, size)
        except:
            print(f'{file_name} Not Found')

    @abstractmethod
    def get_size_by_measurements(self):
        pass

    @abstractmethod
    def draw_pattern(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass


class PantsSewingPattern(SewingPattern):
    def __init__(self, name, size=None):
        SewingPattern.__init__(self, name)
        self.size = None

    def get_size_by_measurements(self):
        """
        Gets from the user the relevant measurements to build the pattern.
        :return: dict, the data for the relevant pattern and size.
        """
        # Get measurements
        length_of_pants = float(input("Enter the length of the pants:"))
        crotch_line = float(input("Enter the distance of the crotch line from the navel:"))
        thigh_scope = float(input("Enter thigh scope:"))
        waist_scope = float(input("Enter waist scope:"))
        ankle_scope = float(input("Enter ankle scope:"))
        lower_center = float(input(
            "Enter by how much would you like to lower the center of the pant relative to the side of the waist:"))

        # Fit measurements where needed
        thigh_scope = 1 / 4 * thigh_scope + LARGE_PATTERN_MARGIN
        waist_scope = 1 / 4 * waist_scope
        ankle_scope = 1 / 2 * ankle_scope + SMALL_PATTERN_MARGIN

        # Set size
        self.size = {
            'length_of_pants': length_of_pants,
            'crotch_line': crotch_line,
            'thigh_scope': thigh_scope,
            'waist_scope': waist_scope,
            'ankle_scope': ankle_scope,
            'lower_center': lower_center
        }

    def draw_pattern(self):
        """
        Draws pants pattern and saves it as a .png file.
        """
        # convert measurements to cm
        self.size.update((x, y * IMAGE_CM) for x, y in self.size.items())

        # size of image
        w = math.ceil(self.size['length_of_pants'] + IMAGE_MARGIN)
        h = math.ceil(self.size['thigh_scope'] + IMAGE_MARGIN)

        # init canvas
        image = Image.new("RGB", (w, h), color="white")
        draw = ImageDraw.Draw(image)

        # Draw cm Square
        cm_square = ((w - IMAGE_CM + IMAGE_MARGIN, h - IMAGE_CM + IMAGE_MARGIN),
                     (w - IMAGE_MARGIN, h - IMAGE_MARGIN))
        draw.rectangle(cm_square, fill="blue", outline="blue")
        draw.text((w - CM_SQUARE_POS, h - CM_SQUARE_POS), "cm\nSquare")

        # Draw pattern
        # draw length of pants line
        draw.line(
            xy=(
                (0, 0),
                (self.size['length_of_pants'], 0)
            ),
            fill="blue",
            width=5
        )
        # drae crotch line
        draw.line(
            xy=(
                (self.size['crotch_line'], 0),
                (self.size['crotch_line'], self.size['thigh_scope'])
            ),
            fill="blue",
            width=5
        )
        # lower the center on the waist scope
        draw.line(
            xy=(
                (self.size['lower_center'], 0),
                (0, self.size['waist_scope'])
            ),
            fill="blue",
            width=5
        )
        # draw ankle line
        draw.line(
            xy=(
                (self.size['length_of_pants'], 0),
                (self.size['length_of_pants'], self.size['ankle_scope'])
            ),
            fill="blue",
            width=5
        )
        # draw line from waist to crotch
        draw.line(
            xy=(
                (0, self.size['waist_scope']),
                (self.size['crotch_line'], self.size['waist_scope'])
            ),
            fill="blue",
            width=5
        )
        # draw curve from waist to crotch
        draw.arc(
            xy=(
                (self.size['crotch_line'] - (self.size['thigh_scope'] - self.size['waist_scope']),
                 self.size['waist_scope']),
                (self.size['crotch_line'], self.size['thigh_scope'])
            ),
            start=270,
            end=0,
            fill="blue",
            width=5
        )
        # draw line from crotch to ankle
        draw.line(
            xy=(
                (self.size['crotch_line'], self.size['thigh_scope']),
                (self.size['length_of_pants'], self.size['ankle_scope'])
            ),
            fill="blue",
            width=5
        )

        # Show pattern
        image.show()

        # Save pattern
        file_name = self.pattern_name + '.png'
        image.save(file_name)

    def __str__(self):
        return f'Pants Pattern: {self.pattern_name}'

    def __repr__(self):
        return self.__str__()


class TShirtSewingPattern(SewingPattern):
    def __init__(self, name, size=None):
        SewingPattern.__init__(self, name)
        self.size = None

    def get_size_by_measurements(self):
        """
        Gets the relevant measurements to build the pattern from the user.
        :return: dict, the data for the relevant pattern and size.
        """
        # Get measurements for T-Shirt
        length_of_shirt = float(input("Enter the length of the shirt:"))
        armpit_height = float(input("Enter the armpit height:"))
        stomach_scope = float(input("Enter the stomach scope:"))
        neck_key = float(input("Enter the neck key:"))
        distance_neck_to_shoulder = float(input("Enter the distance from the neck to the shoulder:"))
        neck_depth = float(input("Enter the neck depth:"))
        lower_shoulder_line = float(input("Enter how much you want to lower the shoulder line:"))

        # Fit measurements where needed for T-Shirt
        stomach_scope = 1 / 4 * stomach_scope + LARGE_PATTERN_MARGIN
        neck_key = 1 / 4 * neck_key + SMALL_PATTERN_MARGIN
        distance_neck_to_shoulder = distance_neck_to_shoulder + neck_key + 3

        # Get measurements for sleeve
        sleeve_length = float(input("Enter the sleeve length:"))
        distance_shoulder_to_armpit = float(input("Enter the distance from the shoulder to the armpit:"))
        arm_scope = float(input("Enter the arm scope:"))
        wrist_scope = float(input("Enter the wrist scope:"))
        expand_at_shoulder = float(input("Enter how much you want to expand the sleeve at the shoulder:"))

        # Fit measurements where needed for sleeve
        distance_shoulder_to_armpit = distance_shoulder_to_armpit + SMALL_PATTERN_MARGIN
        arm_scope = 1 / 2 * arm_scope + MEDIUME_PATTERN_MARGIN
        wrist_scope = 1 / 2 * wrist_scope + MEDIUME_PATTERN_MARGIN

        # Set size
        self.size = {
            'length_of_shirt': length_of_shirt,
            'armpit_height': armpit_height,
            'stomach_scope': stomach_scope,
            'neck_key': neck_key,
            'distance_neck_to_shoulder': distance_neck_to_shoulder,
            'neck_depth': neck_depth,
            'lower_shoulder_line': lower_shoulder_line,
            'sleeve_length': sleeve_length,
            'distance_shoulder_to_armpit': distance_shoulder_to_armpit,
            'arm_scope': arm_scope,
            'wrist_scope': wrist_scope,
            'expand_at_shoulder': expand_at_shoulder
        }

    def draw_pattern(self):
        """
        Draw t-shirt pattern and saves it as a .png file.
        """

        def get_mid_x(x0, x1):
            """
            Gets two x's and returns the x in the middle of both.
            :param x0: float, x mark
            :param x1: float, x mark
            :return: float, x mark
            """
            return (x1 - x0) / 2

        def get_mid_line(dot0, dot1):
            """
            Gets two dots and returns the dot in the middle of both.
            :param dot0: tuple, dot - (x,y)
            :param dot1: tuple, dot - (x,y)
            :return: tuple, dot - (x,y)
            """
            return (dot1[0] - dot0[0]) / 2, (dot1[1] - dot0[1]) / 2

        # convert measurements to cm
        self.size.update((x, y * IMAGE_CM) for x, y in self.size.items())

        sleeve_curve = {
            'sleeve_start': self.size['distance_shoulder_to_armpit'] + self.size['length_of_shirt'] + IMAGE_CM
        }

        self.size['sleeve_length'] += self.size['length_of_shirt'] + self.size['distance_shoulder_to_armpit'] + IMAGE_CM
        self.size['distance_shoulder_to_armpit'] += self.size['length_of_shirt'] + self.size[
            'distance_shoulder_to_armpit'] + IMAGE_CM

        sleeve_curve['x_sleeve_curve_1/2'] = get_mid_x(sleeve_curve['sleeve_start'],
                                                       self.size['distance_shoulder_to_armpit']) + sleeve_curve[
                                                 'sleeve_start']
        sleeve_curve['x_sleeve_curve_1/4'] = get_mid_x(sleeve_curve['sleeve_start'],
                                                       sleeve_curve['x_sleeve_curve_1/2']) + sleeve_curve[
                                                 'sleeve_start']
        sleeve_curve['y_sleeve_curve_1/2'] = 1 / 2 * self.size['arm_scope']
        sleeve_curve['y_sleeve_curve_1/4'] = 1 / 4 * self.size['arm_scope']

        # size of image
        w = math.ceil(self.size['sleeve_length'] + IMAGE_MARGIN * 2)
        h = math.ceil(self.size['stomach_scope'] + IMAGE_MARGIN)

        # init canvas
        im = Image.new("RGB", (w, h), color="white")
        draw = ImageDraw.Draw(im)

        # Draw cm Square
        cm_square = [(w - IMAGE_CM + IMAGE_MARGIN, h - IMAGE_CM + IMAGE_MARGIN), (w - IMAGE_MARGIN, h - IMAGE_MARGIN)]
        draw.rectangle(cm_square, fill="blue", outline="blue")
        draw.text((w - CM_SQUARE_POS, h - CM_SQUARE_POS), "cm\nSquare")

        # Draw T-Shirt
        # draw the length of the shirt line
        draw.line(
            xy=(
                (0, 0),
                (self.size['length_of_shirt'], 0)
            ),
            fill="blue",
            width=5
        )
        # drae the stomach scope lines
        draw.line(
            xy=(
                (self.size['length_of_shirt'], 0),
                (self.size['length_of_shirt'], self.size['stomach_scope'])
            ),
            fill="blue",
            width=5
        )
        draw.line(
            xy=(
                (self.size['armpit_height'], 0),
                (self.size['armpit_height'], self.size['stomach_scope'])
            ),
            fill="blue",
            width=5
        )
        draw.line(
            xy=(
                (self.size['length_of_shirt'], self.size['stomach_scope']),
                (self.size['armpit_height'], self.size['stomach_scope'])
            ),
            fill="blue",
            width=5
        )
        # drae the neck key lines
        draw.line(
            xy=(
                (self.size['neck_depth'], 0),
                (self.size['neck_depth'], self.size['neck_key'])
            ),
            fill="blue",
            width=5
        )
        draw.line(
            xy=(
                (0, self.size['neck_key']),
                (self.size['neck_depth'], self.size['neck_key'])
            ),
            fill="blue",
            width=5
        )
        # draw the neck key curve
        draw.line(
            xy=(
                (0, self.size['neck_key']),
                (self.size['neck_depth'], self.size['neck_key'] - self.size['neck_depth'])
            ),
            fill="blue",
            width=1
        )
        draw.arc(
            xy=(
                [(0, self.size['neck_key'] - self.size['neck_depth']),
                 (self.size['neck_depth'], self.size['neck_key'])]
            ),
            start=0,
            end=90,
            fill="blue",
            width=5
        )
        # draw the line between the neck and shoulder
        draw.line(
            xy=(
                (0, self.size['neck_key']),
                (self.size['lower_shoulder_line'], self.size['distance_neck_to_shoulder'])
            ),
            fill="blue",
            width=5
        )
        # draw the line between shoulder and armpit
        draw.line(
            xy=(
                (self.size['lower_shoulder_line'], self.size['distance_neck_to_shoulder']),
                (self.size['armpit_height'], self.size['distance_neck_to_shoulder'])
            ),
            fill="blue",
            width=5
        )
        # draw the curve at the armpit
        draw.arc(
            xy=(
                (self.size['armpit_height'] - (self.size['stomach_scope'] - self.size['distance_neck_to_shoulder']),
                 self.size['distance_neck_to_shoulder']),
                (self.size['armpit_height'], self.size['stomach_scope'])),
            start=270,
            end=0,
            fill="blue",
            width=5
        )

        # Draw sleeve
        # draw the sleeve length line
        draw.line(
            xy=(
                (0, 0),
                (self.size['sleeve_length'], 0)
            ),
            fill="blue",
            width=5
        )
        # draw the arm scope line
        draw.line(
            xy=(
                (self.size['distance_shoulder_to_armpit'], 0),
                (self.size['distance_shoulder_to_armpit'], self.size['arm_scope'])
            ),
            fill="blue",
            width=5)
        # draw the wrist scope line
        draw.line(
            xy=(
                (self.size['sleeve_length'], 0),
                (self.size['sleeve_length'], self.size['wrist_scope'])
            ),
            fill="blue",
            width=5
        )
        # draw the line between shoulder to wrist
        draw.line(
            xy=(
                (self.size['distance_shoulder_to_armpit'], self.size['arm_scope']),
                (self.size['sleeve_length'], self.size['wrist_scope'])
            ),
            fill="blue",
            width=5
        )

        # draw curve between shoulder to sleeve
        draw.line(
            xy=[
                (sleeve_curve['sleeve_start'], 0),
                (sleeve_curve['x_sleeve_curve_1/4'], sleeve_curve['y_sleeve_curve_1/4'])
            ],
            fill="blue",
            width=1
        )
        draw.line(
            xy=[
                (sleeve_curve['x_sleeve_curve_1/4'], sleeve_curve['y_sleeve_curve_1/4']),
                (sleeve_curve['x_sleeve_curve_1/2'], sleeve_curve['y_sleeve_curve_1/2'])
            ],
            fill="blue",
            width=1
        )
        draw.line(
            xy=[
                (sleeve_curve['x_sleeve_curve_1/2'], sleeve_curve['y_sleeve_curve_1/2']),
                (self.size['distance_shoulder_to_armpit'], self.size['arm_scope'])
            ],
            fill="blue",
            width=1
        )

        draw.arc(
            xy=(
                (sleeve_curve['sleeve_start'], 0 - IMAGE_CM * LARGE_PATTERN_MARGIN),
                (sleeve_curve['x_sleeve_curve_1/4'] + IMAGE_CM , sleeve_curve['y_sleeve_curve_1/4']+ IMAGE_CM * MEDIUME_PATTERN_MARGIN)
            ),
            start=100,
            end=200,
            fill="blue",
            width=5
        )

        draw.arc(
            xy=(
                (sleeve_curve['x_sleeve_curve_1/4'] -IMAGE_CM * MEDIUME_PATTERN_MARGIN , sleeve_curve['y_sleeve_curve_1/4'] - IMAGE_CM * LARGE_PATTERN_MARGIN),
                (sleeve_curve['x_sleeve_curve_1/2'] + IMAGE_CM * (LARGE_PATTERN_MARGIN + SMALL_PATTERN_MARGIN),
                 sleeve_curve['y_sleeve_curve_1/2'])
            ),
            start=100,
            end=150,
            fill="blue",
            width=5
        )
        draw.arc(
            xy=(
                (sleeve_curve['x_sleeve_curve_1/2'] - IMAGE_CM * (LARGE_PATTERN_MARGIN + MEDIUME_PATTERN_MARGIN),
                 sleeve_curve['y_sleeve_curve_1/2']),
                (self.size['distance_shoulder_to_armpit'], self.size['arm_scope'] + IMAGE_CM * LARGE_PATTERN_MARGIN)
            ),
            start=270,
            end=0,
            fill="blue",
            width=5
        )

        # Show pattern
        im.show()

        # Save pattern
        file_name = self.pattern_name + '.png'
        im.save(file_name)

    def __str__(self):
        return f'T-Shirt Pattern: {self.pattern_name}'

    def __repr__(self):
        return self.__str__()
