class BankModel():
    def __init__(self, cycle_id, balance):
        """ Initializes the BankModel instance. 
        Negative balance means extra hours worked.
        Positive balance means hours owed."""
        self.cycle_id = cycle_id
        self.balance = balance

    def to_list(self):
        """ Converts the BankModel instance to a list for CSV writing. """
        return [self.cycle_id, self.balance]

    @staticmethod
    def get_headers():
        """ Returns the headers for the CSV representation of the BankModel. """
        return ["cycle_id", "balance"]
