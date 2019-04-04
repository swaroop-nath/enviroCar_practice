class BIN:
    def __init__(self, x_left, y_bottom, bin_size):
        self.latlng = (x_left, y_bottom)
        self.length = bin_size
        self.feature_dict = {}
    def set_feature(self, feature, date):
        self.feature_dict[date] = feature
    def get_feature(self, date = 0):
        if date != 0:
            return self.feature_dict[date]
        return self.feature_dict