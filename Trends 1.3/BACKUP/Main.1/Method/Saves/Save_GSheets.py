import os, pandas as pd, time
import gspread, json
from oauth2client.service_account import ServiceAccountCredentials as OSS
from Validation.Method.Connection_Network import Valida_Connection

def SetValuesGSheets(NameTable, ListValue):
    PATH = 'C://PROJECTS/TRENDS/Main/Method/'
    #PATH = os.getcwd()
    try:
        VAR_GOOGLE =  ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        CREDENCIAIS = OSS.from_json_keyfile_name('{0}/FILES/JS/bot_whp.json'.format(PATH), VAR_GOOGLE)
        AUTORIZA = gspread.authorize(CREDENCIAIS) 
        Sheet = AUTORIZA.open(NameTable).sheet1
        Valida_Connection()
        Sheet.append_row(ListValue)
    except Exception as Erro:
        print(Erro)
        pass
    

def PrepareList(NameTable, ListValue, ColumnOne, KeyWord, self):
    df_Values = PrepareValue(ListValue, ColumnOne, KeyWord, self)
    df_InsertSheets = pd.DataFrame(df_Values)
    for index,Reads in df_InsertSheets.iterrows():
        SetValuesGSheets(NameTable, list(Reads))
def PrepareListOverTime(self, ListValue):
    df_InsertSheets = pd.DataFrame(ListValue)
    for index,Reads in df_InsertSheets.iterrows():
        SetValuesGSheets(self, list(Reads))

def PrepareValue(List, ColumnOne, KeyWord, self):
    Time = time.strftime("%d/%m/%Y %H:%M")
    ListData = {
        '{0}'.format(ColumnOne):[],
        'values':[],
        'Termo Buscado':[],
        'Data e Hora':[],
        'Palavra Pivo':[],
        'Num da Comp':[],
        'Periodo':[]
    }
    i = 1
    ListValue = pd.DataFrame(List)
    for KWords in KeyWord:
        for index,Reads in ListValue.iterrows():
            ListData['{0}'.format(ColumnOne)].append(Reads[ColumnOne])
            ListData['values'].append(Reads[KWords])
            ListData['Termo Buscado'].append(KWords)
            ListData['Data e Hora'].append(Time)
            ListData['Palavra Pivo'].append(KeyWord[0])
            ListData['Num da Comp'].append("{0}º".format(i))
            ListData['Periodo'].append(self)
    i = i+1
    return ListData