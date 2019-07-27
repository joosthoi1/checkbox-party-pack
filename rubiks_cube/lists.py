class list:
    def __init__(self):
        self.yellow = [
        [[4, 9], 'Yellow2'], [[5, 9], 'Yellow2'], [[6, 9], 'Yellow2'],
        [[4, 8], 'Yellow2'], [[5, 8], 'Yellow2'], [[6, 8], 'Yellow2'],
        [[4, 7], 'Yellow2'], [[5, 7], 'Yellow2'], [[6, 7], 'Yellow2']
        ]
        self.white = [
        [[4, 3], 'White'], [[5, 3], 'White'], [[6, 3], 'White'],
        [[4, 2], 'White'], [[5, 2], 'White'], [[6, 2], 'White'],
        [[4, 1], 'White'], [[5, 1], 'White'], [[6, 1], 'White']
        ]
        self.green = [
        [[1, 6], 'dark green'], [[2, 6], 'dark green'], [[3, 6], 'dark green'],
        [[1, 5], 'dark green'], [[2, 5], 'dark green'], [[3, 5], 'dark green'],
        [[1, 4], 'dark green'], [[2, 4], 'dark green'], [[3, 4], 'dark green']
        ]
        self.orange = [
        [[4, 6], 'dark orange'], [[5, 6], 'dark orange'], [[6, 6], 'dark orange'],
        [[4, 5], 'dark orange'], [[5, 5], 'dark orange'], [[6, 5], 'dark orange'],
        [[4, 4], 'dark orange'], [[5, 4], 'dark orange'], [[6, 4], 'dark orange']
        ]
        self.blue = [
        [[7, 6], 'DodgerBlue4'], [[8, 6], 'DodgerBlue4'], [[9, 6], 'DodgerBlue4'],
        [[7, 5], 'DodgerBlue4'], [[8, 5], 'DodgerBlue4'], [[9, 5], 'DodgerBlue4'],
        [[7, 4], 'DodgerBlue4'], [[8, 4], 'DodgerBlue4'], [[9, 4], 'DodgerBlue4']
        ]
        self.red = [
        [[10, 6], 'OrangeRed3'], [[11, 6], 'OrangeRed3'], [[12, 6], 'OrangeRed3'],
        [[10, 5], 'OrangeRed3'], [[11, 5], 'OrangeRed3'], [[12, 5], 'OrangeRed3'],
        [[10, 4], 'OrangeRed3'], [[11, 4], 'OrangeRed3'], [[12, 4], 'OrangeRed3']
        ]

        self.all = [
                    self.yellow,
        self.green, self.orange, self.blue, self.red,
                    self.white
        ]

        self.side_names = ['F', 'R', 'U', 'B', 'L', 'D']

        self.sides = {
            "F":[
                "blue", "blue", "orange",
                "orange", "orange", "red",
                "green", "red", "white",
            ],
            "R":[
                "yellow", "blue", "orange",
                "green", "blue", "red",
                "red", "yellow", "red",
            ],
            "U":[
                "blue", "orange", "blue",
                "white", "yellow", "orange",
                "red", "yellow", "green",
            ],
            "B":[
                "yellow", "yellow", "white",
                "white", "red", "white",
                "red", "yellow", "yellow",
            ],
            "L":[
                "orange", "green", "yellow",
                "blue", "green", "green",
                "white", "orange", "white",
            ],
            "D":[
                "orange", "blue", "green",
                "white", "white", "green",
                "blue", "red", "green",
            ]
        }

        self.sides = {
            "F":[
                "orange", "orange", "orange",
                "orange", "orange", "orange",
                "orange", "orange", "orange",
            ],
            "R":[
                "blue", "blue", "blue",
                "blue", "blue", "blue",
                "blue", "blue", "blue",
            ],
            "U":[
                "yellow", "yellow", "yellow",
                "yellow", "yellow", "yellow",
                "yellow", "yellow", "yellow",
            ],
            "B":[
                "red", "red", "red",
                "red", "red", "red",
                "red", "red", "red",
            ],
            "L":[
                "green", "green", "green",
                "green", "green", "green",
                "green", "green", "green",
            ],
            "D":[
                "white", "white", "white",
                "white", "white", "white",
                "white", "white", "white",
            ]
        }
