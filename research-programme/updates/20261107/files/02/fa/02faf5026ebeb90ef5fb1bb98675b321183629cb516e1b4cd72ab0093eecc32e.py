import numpy as np


class ProfilePreservingFeatures:
    def __init__(self,compact,retained_features):
        if not np.array_equal(compact.frequency,retained_features.frequency):
            raise ValueError("Retained and full-tail master grids must agree exactly")
        if len(retained_features.splines)!=2 or any(spline.c.shape[-1]<compact.profile_count for spline in retained_features.splines):
            raise ValueError("Both retained profile spline banks are required")
        self.compact=compact
        self.retained_features=retained_features

    def __getattr__(self,name):
        return getattr(self.compact,name)

    def evaluate(self,frequency,join,derivative=False):
        values=self.compact.evaluate(frequency,join,derivative)
        values[...,:self.profile_count]=self.retained_features.evaluate(frequency,join,derivative)[...,:self.profile_count]
        return values
