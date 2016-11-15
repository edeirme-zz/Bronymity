import json
import ast
import csv

def simple_intersect(res1, res2):

	cnt = 0

	new_res1 = []
	new_res2 = []
	for x in range(len(res1)):
		new_res1.append(res1[x]['fontId'])
	for x in range(len(res2)):
		new_res2.append(res2[x]['fontId'])

	r = list(set(new_res1).intersection(new_res2))

	cnt += len(r)
	return r, cnt



