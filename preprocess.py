#coding=utf-8

import sys
import re

#reload(sys)
#sys.setdefaultencoding('utf-8')

with open(sys.argv[1],"r") as f:
	for l in f.readlines():
		s_new = re.sub('"|,|\||/|\(|\)|-|:|：|<|>|~|。|、|;|《|》|——|“|”',' ',l).strip().split(" ")
		for s in s_new:
			if len(s) > 0:
				print s
