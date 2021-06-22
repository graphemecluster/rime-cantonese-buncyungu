# -*- coding: utf-8 -*-
import Qieyun

skipped = []

def transform(字, 粵拼):
	global skipped
	音韻地位 = Qieyun.query字頭(字)
	if not len(音韻地位) and 字 not in skipped:
		skipped += [字]
		return 粵拼
	def _is(表達式):
		return any([_音韻地位.屬於(表達式) for _音韻地位, 解釋 in 音韻地位])
	if 粵拼[0] == 'j':
		if _is('疑母'):
			粵拼 = 'ng' + 粵拼[1:]
		elif _is('日母'):
			粵拼 = 'nj' + 粵拼[1:]
	if 粵拼[0] in 'bpmf' and _is('深咸攝'):
		粵拼 = 粵拼.replace('n', 'm').replace('t', 'p')
	if _is('覃談韻') and 'aa' not in 粵拼:
		粵拼 = 粵拼.replace('a', 'o')
	if 粵拼[0] in 'zcs' and _is('莊章組'):
		粵拼 = 粵拼[0] + 'h' + 粵拼[1:]
	return 粵拼

def process():
	with open('jyut6ping3.dict.yaml') as f:
		for line in f:
			print(line.rstrip())
			if line == '...\n':
				break
		next(f)
		print()
		for line in f:
			if line and line != '\n' and line[0] != '#':
				parts = line.rstrip().split('\t')
				if len(parts) == 2:
					字, 粵拼 = parts
					詞頻 = ''
				else:
					字, 粵拼, 詞頻 = parts
					詞頻 = '\t' + 詞頻
				粵拼 = 粵拼.split(' ')
				transformed粵拼 = []
				if len(字) == len(粵拼):
					for _字, _粵拼 in zip(字, 粵拼):
						transformed粵拼 += [transform(_字, _粵拼)]
					print(字 + '\t' + ' '.join(transformed粵拼) + 詞頻)
					continue
			print(line.rstrip())

process()

with open('skipped.txt', 'w') as f:
	for 字 in skipped:
		print(字, file=f)
