import numpy as np
from .criteria import Criteria


class Splitter:

    def __init__(self,
                 criteria:Criteria,
                 min_impurity_decrease=0.0,
                 min_impurity_split=0.0,
                 min_samples_split=2,
                 min_samples_leaf=1):

        self.criteria = criteria
        self.min_impurity_decrease = min_impurity_decrease
        self.min_impurity_split = min_impurity_split
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf

    def split(self, x, y, feature_indexes: [int], row_indexes: [int], whole_impurity: float) -> (int, float, [([int], float)]):
        """
        Parameters
        ----------
        x:
        y:
        feature_indexes:
        row_indexes:
        whole_impurity:

        Returns
        -------
            第一个返回值：被选择用来分裂的特征的索引；
            第二个返回值：分裂点；
            第三个返回值：分裂之后左叶片/右叶片的行号索引，及叶片的不纯度
        """

        lst_feature = []
        for fidx in feature_indexes:
            sorted_row_indexes = sorted(row_indexes, key=lambda r: x[r][fidx])
            lst = []

            whole_count = len(sorted_row_indexes)

            for row in range(len(sorted_row_indexes)-1):

                fcol = x[:,fidx]
                if abs(fcol[sorted_row_indexes[row]] - fcol[sorted_row_indexes[row+1]]) < 1e-7:
                    continue
                cut_point = (fcol[sorted_row_indexes[row]] + fcol[sorted_row_indexes[row+1]]) / 2

                left_value = self.criteria.calculate(y[sorted_row_indexes[:row+1]])
                right_value = self.criteria.calculate(y[sorted_row_indexes[row+1:]])

                left_proportion = (row+1) / whole_count
                lst.append((row, cut_point, left_value, right_value, left_proportion*left_value + (1-left_proportion)*right_value))

            if not lst:
                continue

            cut = min(lst, key=lambda x: x[4])
            left_row_indexes = sorted_row_indexes[:cut[0] + 1]
            right_row_indexes = sorted_row_indexes[cut[0] + 1:]
            lst_feature.append((fidx, cut[1], [(left_row_indexes, cut[2]), (right_row_indexes, cut[3])], cut[4]))

        feature_cut = min(lst_feature, key=lambda x: x[3])

        return feature_cut[:3] + (whole_impurity - feature_cut[3],)

