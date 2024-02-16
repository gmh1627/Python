# -*- coding:utf-8 -*-
from MyQR.myqr import run
from urllib import parse

import tkinter.messagebox as msgbox
import tkinter as tk
import webbrowser
import re
import json
import os

"""
类说明:爱奇艺、优酷等实现在线观看以及视频下载的类

Parameters:
	width - tkinter主界面宽
	height - tkinter主界面高

"""

class APP:
	def __init__(self, width = 500, height = 250):
		self.w = width
		self.h = height
		self.title = ' 李承VIP视频破解系统'
		self.root = tk.Tk(className=self.title)
		self.url = tk.StringVar()
		self.v = tk.IntVar()
		self.v.set(1)

		#Frame空间
		frame_1 = tk.Frame(self.root)
		frame_2 = tk.Frame(self.root)
		frame_3 = tk.Frame(self.root)

		#Menu菜单
		menu = tk.Menu(self.root)
		self.root.config(menu = menu)
		filemenu = tk.Menu(menu,tearoff=0)
		moviemenu = tk.Menu(menu,tearoff = 0)

		#控件内容设置
		group = tk.Label(frame_1,text = '播放通道选择:', padx = 10, pady = 10)
		tb1 = tk.Radiobutton(frame_1,text = '网通', variable = self.v, value = 1, width = 10, height = 3)
		tb2 = tk.Radiobutton(frame_1,text = '电信', variable = self.v, value = 2, width = 10, height = 3)
		label1 = tk.Label(frame_2, text = "需要查看的电影链接:")
		entry = tk.Entry(frame_2, textvariable = self.url, highlightcolor = 'Fuchsia', highlightthickness = 1,width = 35)
		label2 = tk.Label(frame_2, text = " ")
		play = tk.Button(frame_2, text = "电脑端播放", font = ('黑体',12), fg = 'Purple', width = 8, height = 1, command = self.video_play)
		label3 = tk.Label(frame_2, text = " ")
		# download = tk.Button(frame_2, text = "下载", font = ('楷体',12), fg = 'Purple', width = 2, height = 1, command = self.download_wmxz)
		QR_Code = tk.Button(frame_3, text = "手机端播放", font = ('黑体',12), fg = 'Purple', width = 10, height = 2, command = self.QR_Code)
		label_explain = tk.Label(frame_3, fg = 'GREEN', font = ('黑体',12), text = '\n注意：支持大部分主流视频网站的视频播放！\n此软件仅用于交流学习，请勿用于任何商业用途！')



		#控件布局
		frame_1.pack()
		frame_2.pack()
		frame_3.pack()
		group.grid(row = 0, column = 0)
		tb1.grid(row = 0, column = 1)
		tb2.grid(row = 0, column = 2)
		label1.grid(row = 0, column = 0)
		entry.grid(row = 0, column = 1)
		label2.grid(row = 0, column = 2)
		play.grid(row = 0, column = 3,ipadx = 10, ipady = 10)
		label3.grid(row = 0, column = 4)
		# download.grid(row = 0, column = 5,ipadx = 10, ipady = 10)
		QR_Code.grid(row = 0, column = 0)
		label_explain.grid(row = 1, column = 0)

	def loads_jsonp(self, _jsonp):
		try:
			_json = json.loads(re.match(".*?({.*}).*",_jsonp,re.S).group(1))
			return _json
		except:
			raise ValueError('Invalid Input')

	"""
	函数说明:视频播放

	Parameters:
		self

	Returns:
		无

	Modify:
		2017-05-09 
	"""
	def video_play(self):
		#视频解析网站地址
		port_1 = 'https://jx.aidouer.net/?url='
		port_2 = 'http://www.vipjiexi.com/tong.php?url='

		#正则表达是判定是否为合法链接
		if re.match(r'^https?:/{2}\w.+$', self.url.get()):
			if self.v.get() == 1:
				#视频链接获取
				ip = self.url.get()
				#视频链接加密
				ip = parse.quote_plus(ip)
				#浏览器打开
				webbrowser.open(port_1 + self.url.get())
			elif self.v.get() == 2:
				#链接获取
				ip = self.url.get()
				#链接加密
				ip = parse.quote_plus(ip)

				#获取time、key、url
				get_url = 'http://www.vipjiexi.com/x2/tong.php?url=%s' % ip
				# get_url_head = {
				# 	'User-Agent':'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19',
				# 	'Referer':'http://www.vipjiexi.com/',
				# }
				# get_url_req = request.Request(url = get_url, headers = get_url_head)
				# get_url_response = request.urlopen(get_url_req)
				# get_url_html = get_url_response.read().decode('utf-8')
				# bf = BeautifulSoup(get_url_html, 'lxml')
				# a = str(bf.find_all('script'))
				# pattern = re.compile('"api.php", {"time":"(\d+)", "key": "(.+)", "url": "(.+)","type"', re.IGNORECASE)
				# string = pattern.findall(a)
				# now_time = string[0][0]
				# now_key = string[0][1]
				# now_url = string[0][2]

				# #请求播放,获取Success = 1
				# get_movie_url = 'http://www.vipjiexi.com/x2/api.php'
				# get_movie_data = {
				# 	'key':'%s' % now_key,
				# 	'time':'%s' % now_time,
				# 	'type':'',
				# 	'url':'%s' % now_url
				# }
				# get_movie_head = {
				# 	'User-Agent':'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19',
				# 	'Referer':'http://www.vipjiexi.com/x2/tong.php?',
				# 	'url':'%s' % ip,
				# }
				# get_movie_req = request.Request(url = get_movie_url, headers = get_movie_head)
				# get_movie_data = parse.urlencode(get_movie_data).encode('utf-8')
				# get_movie_response = request.urlopen(get_movie_req, get_movie_data)
				#请求之后立刻打开
				webbrowser.open(get_url)

		else:
			msgbox.showerror(title='错误',message='视频链接地址无效，请重新输入！')



	"""
	函数说明:生成二维码,手机观看

	Parameters:
		self

	Returns:
		无

	Modify:
		2017-05-12
	"""
	def QR_Code(self):
		if re.match(r'^https?:/{2}\w.+$', self.url.get()):
			#视频链接获取
			ip = self.url.get()
			#视频链接加密
			ip = parse.quote_plus(ip)

			url = 'http://www.wmxz.wang/video.php?url=%s' % ip
			words = url
			images_pwd = os.getcwd() + '\Images\\'
			png_path = images_pwd + 'bg.png'
			qr_name = 'qrcode.png'
			qr_path = images_pwd + 'qrcode.png'

			run(words = words, picture = png_path, save_name = qr_name, save_dir = images_pwd)

			top = tk.Toplevel(self.root)
			img = tk.PhotoImage(file = qr_path)
			text_label = tk.Label(top, fg = 'red', font = ('楷体',15), text = "手机浏览器扫描二维码，在线观看视频！")
			img_label = tk.Label(top, image = img)
			text_label.pack()
			img_label.pack()
			top.mainloop()

		else:
			msgbox.showerror(title='错误',message='视频链接地址无效，请重新输入！')
	"""
	函数说明:tkinter窗口居中

	Parameters:
		self

	Returns:
		无

	Modify:
		2017-05-09
	"""
	def center(self):
		ws = self.root.winfo_screenwidth()
		hs = self.root.winfo_screenheight()
		x = int( (ws/2) - (self.w/2) )
		y = int( (hs/2) - (self.h/2) )
		self.root.geometry('{}x{}+{}+{}'.format(self.w, self.h, x, y))

	"""
	函数说明:loop等待用户事件

	Parameters:
		self

	Returns:
		无

	Modify:
		2017-05-09
	"""
	def loop(self):
		self.root.resizable(False, False)	#禁止修改窗口大小
		self.center()						#窗口居中
		self.root.mainloop()

if __name__ == '__main__':
	app = APP()			#实例化APP对象
	app.loop()			#loop等待用户事件









