class Santorini:
    def __init__(self):
        self._turn_count = 0
        # ? keeping track of each level of each square

    def get_turn_count(self):
        return self._turn_count

    def increment_turn_count(self):
        self._turn_count += 1
    