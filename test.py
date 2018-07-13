from python_utils.data_spider import get_data
from python_utils.for_excel import read_info_by_file,write_info_to_file



# for spider
# print(get_data('余姚新闻网','公证_公证案例','1'))
print(get_data( '龙游新闻网','休闲生活'  ,'1'))

# for excel
print(read_info_by_file())
# print(write_info_to_file('丽水在线','理财_本地资讯','正常','wefwefw'))