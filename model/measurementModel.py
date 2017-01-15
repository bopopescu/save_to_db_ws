class MeasurementModel:
    def __init__(self, status=False, model=None, errors=None):
        self.status = status
        self.model = model
        self.errors = errors
        pass

    status = False
    model = None
    errors = None
