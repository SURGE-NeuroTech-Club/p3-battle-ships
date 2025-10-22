
class Ship:
    """
    A simple class to represent a placed ship piece.
    For now, it just stores the coordinates of a single 1x1 ship.
    """

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.coordinates = (row, col)

    def __repr__(self):
        """A helper for printing and debugging."""
        return f"[Ship at ({self.row}, {self.col})]"