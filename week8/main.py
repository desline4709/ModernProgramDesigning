import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import mpsettings


class NotNumError(ValueError):
    def __init__(self, year, province, industry, type):
        self.year = year
        self.province = province
        self.industry = industry
        self.type = type
        self.message = 'Data in ({},{},{},{}) is NaN'.format(self.year, self.province, self.industry, self.type)


class DataAnalysis:
    def __init__(self, filepath, flag, sheet=''):
        self.__path = filepath
        self.load_excel(filepath, flag, sheet)

    def _check_nan(self, data: dict, year, province, industry, type):
        for key in data.keys():
            if np.isnan(data[key]):
                if year == '':
                    year = str(key)
                if province == '':
                    province = key
                raise NotNumError(year, province, industry, type)

    def _check_zero(self, data: dict, year, province, industry, type):
        for key in data.keys():
            if data[key] == 0:
                if year == '':
                    year = str(key)
                if province == '':
                    province = key
                raise ZeroDivisionError()

    def time_analysis(self, area, kind, industry='All Industries'):
        """
        某区域某类型的排放随时间的变化，返回对应地区对应类型的排放值的列表
        :param area: 地区
        :param kind: 排放种类
        :param industry: 工业类型
        :return:
        """
        assert self.__flag == 1
        data_list = []
        year_list = [1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008,
        2009, 2010, 2011, 2012, 2013, 2014, 2015]
        if industry == 'All Industries':
            area_list = list(self.df_list[0].iloc[:, 0])
            row_index = area_list.index(area)  # 此时行索引是地区（省市）
        else:
            self.load_excel('.', flag=1, sheet=area)
            industry_list = list(self.df_list[0].iloc[:, 0])
            row_index = industry_list.index(industry)  # 此时行索引是地区（省市）
        kind_list = list(self.df_list[0].columns)
        kind_index = kind_list.index(kind)

        for df in self.df_list:
            data_list.append(df.iloc[row_index, kind_index])
        data_dict = dict(zip(year_list, data_list))
        try:
            self._check_nan(data_dict, '', province=area, industry=industry, type=kind)
        except NotNumError as nerr:
            print(nerr.message)
            for key in data_dict.keys():
                if np.isnan(data_dict[key]):
                    data_dict[key] = -1
        if kind == 'Total':
            try:
                self._check_zero(data_dict, '', province=area, industry=industry, type=kind)
            except ZeroDivisionError:
                print('Data in ({},{},{},{}) is 0'.format(self.year, self.province, self.industry, self.type))
        return data_dict

    def area_analysis(self, year, kind):
        """
        指定年份下，全国某类型的排放随地区的变化，返回对应地区对应类型的排放值的字典
        :param year:
        :param kind:
        :return:
        """
        if self.is_series():
            for i in self.__file_list:
                if year in i:
                    index = self.__file_list.index(i)
                    df = self.df_list[index]
                    break
        else:
            if year not in self.__path:
                # 不是年份对应的文件
                path_list = self.__path.split('/')
                workpath = '/'.join(path_list[:-1])
                os.chdir(workpath)
                filelist = os.listdir()
                for i in filelist:
                    if year in i:
                        self.load_excel(i, flag=0)
                        break
            df = self.df
        column_list = list(df.columns)
        area_list = list(df.iloc[:, 0])
        data_list = []
        column_index = column_list.index(kind)
        for i in range(len(area_list)):
            data_list.append(df.iloc[i, column_index])
        data_dict = dict(zip(area_list, data_list))
        try:
            self._check_nan(data_dict, year, '', 'All Industries', kind)
        except NotNumError as nerr:
            print(nerr.message)
            data_df = pd.DataFrame(data_dict.values(),data_dict.keys())
            data_df = data_df.dropna()
            data_dict = data_df[0].to_dict()
        return data_dict

    def load_excel(self, filepath, flag, sheet=''):
        """
        数据加载方法
        :param filepath: 文件或者文件夹路径
        :param flag: 标志为 0 时读取单个文件，为 1 时读取系列文件
        :param sheet: 要读取的文件的工作表名称
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

    def is_series(self):
        if self.__flag == 1:
            return True
        else:
            return False


class Visualization:
    def __init__(self, da: DataAnalysis):
        self.da = da

    def time_analysis(self, area, kind, industry='All Industries'):
        data_dict = self.da.time_analysis(area, kind, industry)
        self.draw_pie(data_dict, year='', province=area, industry=industry, type=kind)
        self.draw_bar(data_dict, year='', province=area, industry=industry, type=kind)

    def area_analysis(self, year, kind):
        data_dict = self.da.area_analysis(year, kind)
        data_dict_nosum = data_dict.copy()
        data_dict_nosum.pop('Sum-CO2')
        self.draw_pie(data_dict_nosum, year, province='', industry='All Industries', type=kind)
        self.draw_bar(data_dict_nosum, year, province='', industry='All Industries', type=kind)

    def draw_pie(self, data_dict: dict, year, province, industry, type):
        plt.figure()
        pie = plt.pie(data_dict.values(), labels=data_dict.keys(),
                      autopct='%1.1f%%', startangle=-90)
        os.chdir('..')
        if year == '':
            plt.title('{}省{}企业{}种类排放的占比随时间变化图'.format(province, industry, type))
            plt.savefig('Pie-Time Analysis of province {}_industry {}_type {}.png'.format(province, industry, type))
        if province == '':
            plt.title('{}年全国各地区{}企业{}种类排放的占比分布图'.format(year, industry, type))
            plt.savefig('Pie-Area Analysis of year {}_industry {}_type {}.png'.format(year, industry, type))

    def draw_bar(self, data_dict: dict, year, province, industry, type):
        plt.figure()
        x = np.arange(len(data_dict))
        y = data_dict.values()
        plt.bar(x, y, width=0.8)
        labels = []
        for i in data_dict.keys():
            lb = str(i)
            labels.append('\n'.join(list(lb)))
        plt.tick_params(labelsize=6)
        plt.xticks(x, labels)
        if year == '':
            plt.title('{}省{}企业{}种类排放量随时间的变化'.format(province, industry, type))
            plt.savefig('Bar-Time Analysis of province {}_industry {}_type {}.png'.format(province, industry, type))
        if province == '':
            plt.title('{}年全国各地{}企业{}种类排放量随时间的变化'.format(year, industry, type))
            plt.savefig('Bar-Area Analysis of year {}_industry {}_type {}.png'.format(year, industry, type))
        # plt.show()



if __name__ == "__main__":
    da = DataAnalysis('co2_demo', flag=1)
    # da1 = DataAnalysis('co2_demo/Province sectoral CO2 emissions 1997.xlsx', flag=0)
    # data = da1.area_analysis('1998', 'Total')
    # data = da.time_analysis("Beijing", 'Total')
    # data = da.time_analysis("Beijing", 'Total', 'Urban')
    # data = da.area_analysis('1999', 'Total')
    # print(data)
    vs = Visualization(da)
    # vs.time_analysis('Beijing', "Total")
    vs.area_analysis('1999', 'Total')

