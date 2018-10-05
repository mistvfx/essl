import pymysql
import pandas as pd
from pandas import *
import datetime
import threading
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from db.calcWrkHrs import calActualWorkingHours
import openpyxl

def excelManip(filePath):
    db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
    cur = db.cursor()
    print(filePath[0])

    df = pd.read_excel(filePath[0], sheet_name='data')

    for i in df.index:
        id = df['Postcode'][i]
        artist = df['First Name'][i]
        dept = df['City'][i]
        reader_name = df['Reader Name'][i]
        date_time = df['Time'][i]
        door = df['Event Point'][i]
        try:
            reader = reader_name.split(" ")
            io = reader[1]
        except AttributeError:
            continue
        date = date_time.date()
        time = date_time.time()
        #print(type(time))

        if str(id) != 'nan':
            try:
                cur.execute("INSERT INTO essl.%d (IO, MTIME, MDATE, DOOR) VALUES('%s', '%s', '%s', '%s')" %(id, io, time, date, door))
            except:
                cur.execute("INSERT INTO essl.user_master(ID, Name, Department, Password) VALUES('%d','%s','%s','%d');" %(id, artist, dept, id))
                cur.execute("CREATE TABLE essl.%d (SNum int(11) NOT NULL AUTO_INCREMENT, IO char(4) NOT NULL, MTIME time NOT NULL, MDATE date NOT NULL, DOOR varchar(45) NOT NULL, PRIMARY KEY (`SNum`))" %(id))
                cur.execute("INSERT INTO essl.%d (IO, MTIME, MDATE, DOOR) VALUES('%s', '%s', '%s', '%s')" %(id, io, time, date, door))

    cur.close()
    db.close()
    return 0

def excelUpPB():
    infoLabel = Label(text='File Will be synced to the database in the background, please do not close the application')
    popup = Popup(content=infoLabel, size_hint=(0.5, 0.5))
    popup.open()

    return 0

def threads(filePath):
    t1 = threading.Thread(target=excelManip, args=(filePath,))
    t2 = threading.Thread(target=excelUpPB)

    t2.start()
    t1.start()

    t2.join()
    t1.join()

    print("EXCEL UPLOAD COMPLETE")

def formatDate(date):
    Date = date.split(".")
    dt = (str(Date[2])+"-"+str(Date[1])+"-"+str(Date[0]))
    return dt

def excelExport(date):
    StdWrkHrs = datetime.timedelta(hours=8, minutes=29, seconds=59)
    absent = datetime.timedelta()
    db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
    cur = db.cursor()
    cur.execute("SELECT ID, Name, Department FROM essl.user_master WHERE ID != '1000'")
    cur1 = db.cursor()

    Artist_Code = []
    Artist_Name = []
    Department = []

    ios = []
    timings = []
    doors = []

    In_Time = []
    Out_Time = []
    Work_Duration = []
    Total_Duration = []
    Non_Completed_Hours = []
    Additional_Hours = []
    Remarks = []

    for id in cur.fetchall():
        cur1.execute("SELECT IO, MTIME, DOOR FROM essl.`%d` WHERE MDATE = '%s' ORDER BY MTIME ASC" %(id[0], formatDate(date)))
        #ios = []
        #timings = []
        #print('id:', id[0])
        #doors = []
        for data in cur1.fetchall():
            ios.append(data[0])
            timings.append(data[1])
            doors.append(data[2])
        Artist_Code.append(id[0])
        Artist_Name.append(id[1])
        Department.append(id[2])
        try:
            In_Time.append((datetime.datetime.min + min(timings)).time())
        except:
            In_Time.append('ABSENT')
        try:
            Out_Time.append((datetime.datetime.min + max(timings)).time())
        except:
            Out_Time.append('ABSENT')
        try:
            actWrkHrs = calActualWorkingHours(ios, timings, doors)
            if actWrkHrs == datetime.timedelta():
                Work_Duration.append('ABSENT')
            else:
                Work_Duration.append((datetime.datetime.min + actWrkHrs).time())
        except Exception as e:
            actWrkHrs = datetime.timedelta()
            Work_Duration.append('ABSENT')
        try:
            Total_Duration.append((datetime.datetime.min + max(timings)-min(timings)).time())
        except:
            Total_Duration.append('ABSENT')
        try:
            if actWrkHrs == absent:
                Non_Completed_Hours.append('ABSENT')
            elif actWrkHrs < StdWrkHrs :
                Non_Completed_Hours.append((datetime.datetime.min + StdWrkHrs-actWrkHrs).time())
            elif actWrkHrs >= StdWrkHrs :
                Non_Completed_Hours.append(datetime.time())
        except:
            if actWrkHrs == absent:
                Non_Completed_Hours.append('ABSENT')
            elif actWrkHrs >= StdWrkHrs :
                Non_Completed_Hours.append(datetime.time())
        if actWrkHrs >= StdWrkHrs :
            Remarks.append('COMPLETED')
            Additional_Hours.append((datetime.datetime.min + actWrkHrs-StdWrkHrs).time())
        elif actWrkHrs == absent:
            Remarks.append('ABSENT')
            Additional_Hours.append('ABSENT')
        elif actWrkHrs < StdWrkHrs :
            Remarks.append('NOT COMPLETED')
            Additional_Hours.append(datetime.time())
        del ios[:]; del timings[:]; del doors[:]

    #print(len(Artist_Code))
    #print(len(Artist_Name))
    #print(len(Department))
    #print(len(In_Time))
    #print(len(Out_Time))
    #print(len(Work_Duration))
    #print(len(Total_Duration))

    df = pd.DataFrame({'Artist Code':Artist_Code, 'Artist Name':Artist_Name, 'Department':Department, 'In Time':In_Time, 'Out Time':Out_Time, 'Work Duration':Work_Duration, 'Total Duration':Total_Duration, 'Non Completed Hours':Non_Completed_Hours, 'Additional Hours':Additional_Hours, 'Remarks':Remarks})

    ##writer = pd.ExcelWriter('export_test.xlsx', engine='xlsxwriter')
    #df.to_csv('export_testing.csv')
    ##df.to_excel(writer, sheet_name=formatDate(date))
    ##workbook = writer.book
    ##worksheet = writer.sheets[formatDate(date)]
    #timeFormat = workbook.add_format({'num_format': 'hh:mm:ss'})
    #worksheet.set_column('E:H', None, timeFormat)

    from openpyxl import Workbook
    from openpyxl.utils.dataframe import dataframe_to_rows
    from openpyxl.formatting import Rule
    from openpyxl.styles import Font, PatternFill
    from openpyxl.styles.differential import DifferentialStyle
    from openpyxl.styles import Alignment
    from openpyxl.styles.borders import Border, Side

    thin_border = Border(left=Side(style='thin'),
                     right=Side(style='thin'),
                     top=Side(style='thin'),
                     bottom=Side(style='thin'))

    red_text = Font(color="9C0006")
    red_fill = PatternFill(bgColor='FFC7CE')
    dxf = DifferentialStyle(font=red_text, fill=red_fill)
    rule = Rule(type="containsText", operator='containsText', text='ABSENT', dxf=dxf)
    rule.formula = ['NOT(ISERROR(SEARCH("ABSENT",E1)))']

    try:
        wb = openpyxl.load_workbook('export_test.xlsx')
        ws = wb.create_sheet(formatDate(date))

        for r in dataframe_to_rows(df, index=True, header=True):
            ws.append(r)

        for cell in ws['A'] + ws[1]:
            cell.style = 'Pandas'

        for row in ws['A1:K100']:
            for cell in row:
                cell.alignment = Alignment(wrap_text=True, horizontal='center', vertical='center')
                cell.border = thin_border

        for col in ws.columns:
            max_length = 0
            column = col[0].column # Get the column name
            for cell in col:
                try: # Necessary to avoid error on empty cells
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2) * 1.2
            ws.column_dimensions[column].width = adjusted_width

        ws['A1'].fill = PatternFill(bgColor="5fff00", fill_type = "solid")

        ws.conditional_formatting.add('E1:K500', rule)

        wb.save('export_test.xlsx')
    except Exception as e:
        print('ERROR :', e)
        wb = Workbook()
        ws = wb.create_sheet(formatDate(date))

        for r in dataframe_to_rows(df, index=True, header=True):
            ws.append(r)

        for cell in ws['A'] + ws[1]:
            cell.style = 'Pandas'

        for row in ws['A1:K100']:
            for cell in row:
                cell.alignment = Alignment(wrap_text=True, horizontal='center', vertical='center')
                cell.border = thin_border

        for col in ws.columns:
            max_length = 0
            column = col[0].column # Get the column name
            for cell in col:
                try: # Necessary to avoid error on empty cells
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2) * 1.2
            ws.column_dimensions[column].width = adjusted_width

        ws.conditional_formatting.add('E1:K500', rule)
        ws.sheet_properties.tabColor = "1072BA"

        wb.save('export_test.xlsx')
