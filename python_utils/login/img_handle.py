#coding=utf-8

# Author: lim
# Email: 940711277@qq.com
# Date:  2018-06-10 14:23:37

import os
from PIL import Image, ImageFile
PATH = os.path.dirname(os.path.realpath(__file__))


def bin_handle(filename,new_name):

	"""bin code"""
	img = Image.open(filename)
	img = img.convert('L')
	pix_ = img.load()
	for y in range(img.size[1]):
		for x in range(img.size[0]):
			if  pix_[x,y]<=120:
				pix_[x,y] = 0
			if pix_[x,y]>120:
				pix_[x,y] =255

	img.save(new_name)



def recognize(filename):

	# handle captcha
	new_name = filename.replace('.jpg','')+ '_bin.jpg'
	bin_handle(filename,new_name)

	# for path
	result_path = os.sep.join([PATH,'result.txt'])
	tesseract_path = os.path.join(os.path.dirname(os.path.dirname(PATH)),'tools/Tesseract_OCR/tesseract.exe')

	#recognize
	os.system("{} {} {} -psm 7 2>NUL 1>NUL".format(tesseract_path,new_name,result_path))

	#return
	with open(result_path+'.txt') as f:
		result = f.read().strip().replace('\n','').replace('\r\n','')
	return result



if __name__ == '__main__':
	print(recognize('captcha.jpg'))

