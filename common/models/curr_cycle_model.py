class CurrCycleModel():
    def __init__(self, cycle_id):
        self.cycle_id = cycle_id

    def to_list(self):
        """ Converts the CurrCycleModel instance to a list for CSV writing. """
        return [self.cycle_id]

    @staticmethod
    def get_headers():
        return ["cycle_id"]
