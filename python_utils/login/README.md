TRS 自动登陆模块,调用login模块中的login直接返回cookies

基于python 3.6
	依赖包 最新版即可，无太严格版本要求
	json
	PyExecJS  
	random
	requests
	lxml
tesseract-ocr:工具在文件夹内。
安装好后，设置好环境变量，设置识别的白名单，通过pyhton的system模块调用系统，进行验证码的自动识别。

原理：访问登陆页面进行登陆，记录登陆成功的cookies用于下次调用。
其中使用了python的execjs来执行js的加密代码，实现参数的构造。使用tesseract来识别验证码。