import os
import time
import json
import xlrd
from openpyxl import Workbook

from config import SUFFIX,WORKER,WORK_PATH
from config import IR_SITENAME,CHANNAL_PATH,DOCCHANNEL,URL,STATE,STATE_INFO
from config import HEAD_1,HEAD_2,CHANNAL_PATH_F,DOCCHANNEL_F

PATH = WORK_PATH


def get_abs_path(filename):
    """return a abs path of file"""
    return os.path.join(PATH,filename)


def get_date_name():
    """return a date-name string"""
    _time = time.strftime("%Y-%m-%d_%H-%M-%S")
    data_name = _time+'_'+WORKER
    return data_name


def get_filename(): 
    """ return the first xlsx filename in the dir"""
    file_list = os.listdir(PATH)
    for i in file_list:
        if (not  i.startswith('~')) and i.endswith(SUFFIX):
            return i

    
def get_new_filename(filename):
    """return a filename-data-workname.xlsx string"""
    new_filename = '^'.join([filename.replace(SUFFIX,'').split('^')[0],get_date_name()])+SUFFIX
    return new_filename


def file_is_open(filename):

    """ckeck file is open or not.
        file is open return False,
        not open return filename"""

    n_filename = get_new_filename(filename)
    try:
        os.rename(get_abs_path(filename),get_abs_path(n_filename))
        return get_abs_path(n_filename)
    except Exception as e:
        return False


def write_info_to_file(ir_sitename,channel_path,state,state_info):

    """func to enter fields to excel"""

    filename = get_filename()
    new_filename =  file_is_open(filename)

    # file is open ?
    if not new_filename:
        return b'0'

    # for read excel to get a tabel sheet
    r_file = xlrd.open_workbook(new_filename)
    try:
        table = r_file.sheet_by_name(u'{}'.format(WORKER))
    except xlrd.biffh.XLRDError as e:
        table = r_file.sheet_by_index(0)
    except Exception as e:
        print(e)

    # for excel head check
    if table.ncols < STATE_INFO+1:
        return b'-1'

    # fixed the unique row`s state and state info field
    total_con = []
    for i in range(table.nrows):
        row  = table.row_values(i)
        if row[CHANNAL_PATH] == CHANNAL_PATH_F and row[DOCCHANNEL] == DOCCHANNEL_F:
            row[STATE] = '不检查'
        if row[IR_SITENAME].strip() == ir_sitename.strip() and row[DOCCHANNEL].strip() == channel_path.strip():
            row[STATE] = state
            row[STATE_INFO] = state_info
        total_con.append(row)

    # for rewrite total data to file
    wb = Workbook()
    ws = wb.active  
    ws.title = WORKER
    for i,con_1 in enumerate(total_con):
        for j,con_2 in enumerate(con_1):
            ws.cell(row=i+1, column=j+1, value=con_2)
    wb.save(new_filename)

    return b'1'


def read_info_by_file():

    """get need check site from excel
        return [string,string,string]"""

    filename = get_filename()

    if not filename:
        return b'[]'

    new_filename =  file_is_open(filename)

    # file is open ?
    if not new_filename:
        return b'0'

    # for read excel to get a tabel sheet
    r_file = xlrd.open_workbook(new_filename)
    try:
        table = r_file.sheet_by_name(u'{}'.format(WORKER))
    except xlrd.biffh.XLRDError as e:
        table = r_file.sheet_by_index(0)
    except Exception as e:
        print(e)

    # for excel head check
    if table.ncols < STATE_INFO+1:
        return b'-1'

    # filter some need check row append to line_con[]
    index = 1
    line_con = []
    for i in range(table.nrows):
        row  = table.row_values(i)
        if HEAD_1 in row or HEAD_2 in row:
            continue
        if row[CHANNAL_PATH] in CHANNAL_PATH_F and row[DOCCHANNEL] == DOCCHANNEL_F:
            continue
        if row[STATE]:
            continue
        line = '^'.join([str(index),row[IR_SITENAME],row[DOCCHANNEL],row[URL]])
        index +=1
        line_con.append(line)

    json_f = json.dumps(line_con)
    data = json_f.encode('utf-8')
    return data




if __name__ == '__main__':

    print(read_info_by_file())
    print(write_info_to_file('瑞安广电','瑞安广电_首页','正常','4geewfawefawef'))