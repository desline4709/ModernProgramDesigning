import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


class DataAnalysis:
    def __init__(self, filepath, flag, sheet=''):
        self.load_excel(filepath, flag, sheet)
    
    def time_analysis(self, area, kind):
        """
        某区域某类型的排放随时间的变化，返回对应地区对应类型的排放值的列表
        :param area: 地区
        :param kind: 排放种类
        :return:
        """
        assert self.__flag == 1
        column_list = list(self.df_list[0].columns)
        area_list = list(self.df_list[0].iloc[:, 0])
        data_list = []
        try:
            column_index = column_list.index(kind)
            area_index = area_list.index(area)
        except ValueError:
            if kind not in column_list:
                print("There's no kind of {}".format(kind))
            if area not in area_list:
                print("There's no area of {}".format(area))
        else:
            for df in self.df_list:
                data_list.append(df.iloc[area_index, column_index])
            return data_list

    def area_analysis(self, path, year, kind):
        """
        指定年份下，全国某类型的排放随地区的变化，返回对应地区对应类型的排放值的字典
        :param year:
        :param filepath:
        :param kind:
        :return:
        """
        if self.__flag == 1:
            for i in self.__file_list:
                if year in i:
                    index = self.__file_list.index(i)
                    df = self.df_list[i]
                    break
            column_list = list(df.columns)

            try:
                column_index = column_list.index(kind)
                area_index = area_list.index(area)
            except ValueError:
                if kind not in column_list:
                    print("There's no kind of {}".format(kind))
                if area not in area_list:
                    print("There's no area of {}".format(area))
            else:
                for df in self.df_list:
                    data_list.append(df.iloc[area_index, column_index])
                return data_list

    def load_excel(self, filepath, flag, sheet=''):
        """
        数据加载
        :param filepath:
        :param flag:
        :param sheet:
        :return:
        """
        self.__flag = flag
        if flag == 0:
            if sheet == '':
                df = pd.read_excel(filepath)
            else:
                df = pd.read_excel(filepath, sheet)
            self.df = df
        else:
            os.chdir(filepath)  # 切换工作路径
            self.__file_list = os.listdir()
            self.df_list = []
            if sheet == '':
                for i in self.__file_list:
                    df = pd.read_excel(i)
                    self.df_list.append(df)
            else:
                for i in self.__file_list:
                    df = pd.read_excel(i, sheet)
                    self.df_list.append(df)


if __name__ == "__main__":
    # da1 = DataAnalysis("co2_demo/Province sectoral CO2 emissions 1997.xlsx", flag=0)
    # print(da1.df.head())
    # da_list = DataAnalysis('co2_demo', flag=1)
    # da = da_list.df_list[1]
    # print(list(da.columns))
    # os.chdir('co2_demo')
    # print(os.listdir())
    da = DataAnalysis('co2_demo', flag=1)
    data = da.time_analysis("Beijing", 'Total')

