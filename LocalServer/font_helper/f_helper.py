__author__ = 'Beast'
import os
import csv
import json
import win32api
import win32con
from _winreg import *
from fuzzywuzzy import process
import ctypes
import platform



def csv2list(file2read):
	with open(file2read, 'rb') as f:
		reader = csv.DictReader(f)
		your_list = list(reader)
	return your_list


def read_csv():
	try:
		if  platform.system() == 'Windows':
			vanilla_windows = csv2list('windows-vanilla_fonts.csv')
		else:
			vanilla_fonts = csv2list('windows-vanilla_fonts.csv')
	except IOError as e:
		print "I/O error({0}): {1}".format(e.errno, e.strerror)
	except ValueError:
		print "Could not convert data to an integer."

	vanilla_fonts_windows = []
	for x in range(len(vanilla_windows)):
		vanilla_fonts_windows.append(vanilla_windows[x]['Typeface'])
	return vanilla_fonts_windows


def find_fonts():
	font_list = []
	if platform.system() == 'Windows':
		aReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
		aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts")

		for i in range(10240):
			try:
				asubkey_name=EnumValue(aKey, i)
				font_list.append(asubkey_name)
				if "" == asubkey_name:
					raise WindowsError
			except WindowsError:
				break
		CloseKey(aKey)
	return font_list


def delete_font(font):

	if platform.system() == 'Windows':
		path = 'C:\Windows\Fonts\\' + font
		result = ctypes.windll.gdi32.RemoveFontResourceA(path)
		if not result:
			result = ctypes.windll.gdi32.RemoveFontResourceW(path)
		win32api.SendMessage(win32con.HWND_BROADCAST, win32con.WM_FONTCHANGE)
	return result

