class BIN:
    def __init__(self, x_left, y_bottom, bin_size):
        self.latlng = (x_left, y_bottom)
        self.length = bin_size
        self.feature_dict = {}
        self.feature_size = {}
    def set_feature(self, feature, date):
        if self.feature_dict.get(date) == None:
            self.feature_dict[date] = feature
            self.feature_size[date] = 1
        else:
            self.feature_dict[date] = self.feature_dict.get(date) + feature
            self.feature_size[date] = self.feature_size.get(date) + 1
            
    def run_average_feature_setter(self):
        for date,value in self.feature_dict.items():
            self.feature_dict[date] = value/self.feature_size[date]
            
    def get_feature(self, date = 0):
        if date != 0:
            return self.feature_dict.get(date)
        return self.feature_dict
