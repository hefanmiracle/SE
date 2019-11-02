import json
from prettyprinter import cpprint

from json_transfer import structure_create


class Json_Maintain():
	def __init__(self,questions_contents_name="questions_contents.json",questions_structure_name="questions_structure.json",answer_history_name="answer_history.json"):

		self.questions_contents_name = questions_contents_name
		self.questions_structure_name = questions_structure_name
		self.answer_history_name =answer_history_name
		#读入json
		self.questions_contents = None
		self.questions_structure = None
		self.answer_history = None
		#解析的数据结构，存着题号：解答的内容
		self.answers = None
		self.load()
		#构建题库数据结构
		self.questions_repo = self.repo_build()

	#退出程序时候的操作
	def exit(self):
		#调用refresh方法
		refresh()

	#修改answer_history的数据结构，目前只能回答，也就是没有把回答记录删去的功能，只能覆盖回答记录
	def answer_history_alter(self,num,answer,rightOrwrong="Wrong"):
		#修改类内部的数据结构
		self.answer_history[rightOrwrong][num] = answer
		#利用refresh将新内容冲回文件,同时也刷新了repo和structure，一举两得
		self.refresh()



	#修改question_contents的内容
	def questions_contents_alter(self):
		pass


	#保存题库文件和answer_history文件
	def save(self):
		#保存question_contents
		self.json_save(self.questions_contents,self.questions_contents_name)
		#保存structure
		self.json_save(self.questions_structure,self.questions_structure_name)
		#保存answer_history?
		self.json_save(self.answer_history,self.answer_history_name)

	#读入所有题库文件和answer_history文件
	def load(self):
		self.questions_contents = self.json_load(self.questions_contents_name)
		self.questions_structure = self.json_load(self.questions_structure_name)
		self.answer_history = self.json_load(self.answer_history_name)


	#刷新repo，由于answer_history在使用的过程中可能会变，日后可能会添加自己增加题目的功能,本质是刷新所有文件和类内数据结构
	def refresh(self):
		#第一步，利用save保存contents
		self.save()
		#第二步，利用从json_transfer引入的构建structure的方法创建新的structure然后引入新的structure
		structure_create(self.questions_contents_name,self.questions_structure_name)
		
		#第三步,利用load读入新的文件
		self.load()

		#第三步，结合answer_history，用repo_build，构建新的repo
		self.questions_repo = self.repo_build()


	#给定json文件名称，读入json
	def json_load(self,src):
		file = open(src,"r+",encoding="utf8")
		contents = json.load(file)
		file.close()
		return contents

	#给定json文件名称，写入json
	def json_save(self,dic,dest):
		dest_json = json.dumps(dic)
		file = open(dest,"w",encoding="utf8")
		file.write(dest_json)
		file.close()

	#结合回答历史，做一个新的repo,repo的一级结构是这道题目是否回答过，二级结构之后就和questions_structure一样了
	def repo_build(self):
		dic = {'done':{},'undone':{}}
		for typ_k,typ_v in self.questions_structure.items():
			#判断题型是否加入字典
			if typ_k not in dic['done'].keys():
				dic['done'][typ_k] ={}
			if typ_k not in dic['undone'].keys():
				dic['undone'][typ_k] ={}
			for diff_k,diff_v in typ_v.items():
				#判断难度
				if diff_k not in dic['done'][typ_k].keys():
					dic['done'][typ_k][diff_k] = []
				if diff_k not in dic['undone'][typ_k].keys():
					dic['undone'][typ_k][diff_k] = []
				
				#接下来判断每个题号是否在answer_history中
				for num in diff_v:
					if num in self.answer_history['Right'].keys() or num in self.answer_history['Wrong'].keys():
						dic['done'][typ_k][diff_k].append(num)
					else:
						dic['undone'][typ_k][diff_k].append(num)

		return dic


if __name__ == '__main__':
	json_maintainer = Json_Maintain()


	cpprint(json_maintainer.questions_repo)
	# cpprint(json_maintainer.questions_structure)
	cpprint(json_maintainer.answer_history)
	json_maintainer.answer_history_alter('2','b','Wrong')
	cpprint(json_maintainer.answer_history)


