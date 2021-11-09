import pandas as pd
import os

class DataAnalyse:
    def __init__(self, filepath, flag, sheet=''):
        if flag == 0:
            if sheet == '':
                df = pd.read_excel(filepath)
            else:
                df = pd.read_excel(filepath, sheet)
            self.df = df
        else:
            self.file_list = os.listdir()
            self.df_list = []
            if sheet == '':
                for i in file_list:
                    df = pd.read_excel(i)
                    self.df_list.append(df)
            else:
                for i in file_list:
                    df = pd.read_excel(i,sheet)
                    self.df_list.append(df)
    
    def time_analyse(self):
        pass





if __name__ == "__main__":
    da = DataAnalyse("co2_demo",flag=1)
    print(da.dataframe)