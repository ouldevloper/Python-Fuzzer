from subprocess import check_output
import sys
import time
import os
class Fuzz:
	def __init__(self):
		self.args = {}
		self.parse()
		if(self.checkArgs() == False): 
			self.usage()
		self.run()


	def usage(self):
		print(f"  Usage: python {sys.argv[0]}  target=<binary> type=<argv/stdin> num:<number of stdin> vuln:<N of vuln parameter>")
		print("     [+] target:  Target Binary Path")
		print("     [+] type:    Type of input from command line of get the value form stdin")
		print("     [+] num:     Number of parameters to fuzz")
		print("     [+] vuln:    Index of vuln parameter ")
		print("  Example:")
		print(f"     $ python {sys.argv[0]} target=./foo type=stdin num=2 vuln=2")
		
	def run(self):
		pass

	def checkArgs(self):
		if 'vuln' not in self.args:
			self.args['vuln'] = -1
		if len(sys.argv) < 3: return False
		return 'type' in self.args \
				and 'num' in self.args and \
			    type(self.args['num']) == int and \
				os.path.exists(self.args['target']) #and \
				#self.args['type'] in ['argv','stdin']
	
	def parse(self):
		for arg in sys.argv[1:]:
			try:
				tmp =  arg.split("=")
				if tmp[0] in  ['type','target']:
					self.args[tmp[0]] = tmp[1]
				else:
					self.args[tmp[0]] = int(tmp[1])
			except:
				pass
	def generatePayload(self,index:int=0,num:int=1,vuln:int=-1):
		if vuln == -1 or num < vuln:
			return "\n".join(["A"*index]*num)
		else:
			res = ["A"*8 for _ in range(num)]
			res[vuln-1] = "A"*index
			return "\n".join(res)
			
	def run(self):
		i=1
		target = self.args['target']
		NotFound = True	
		if self.args['type']=='argv':
			command = f"{target}  $(echo pad)"
		else:
			command = f"{target}  < pad"
		while NotFound:
			open("pad","w").write(self.generatePayload(i,self.args['num'],self.args['vuln']))
			try:
				res = check_output(["/bin/bash","-c",command])
				sys.stdout.write(f"\r\r[+] Trying {i} Bytes.")
				sys.stdout.flush()
			except:
				print(f"\n[*] Offset Found : {i} - {i-1}")
				NotFound = False
				break
			if(b"Segmentation fault" in res):
				print(f"\n[+] Offset Found : {i} - {i-1}")
				NotFound = False
				break
			time.sleep(0.01)
			i+=1

Fuzz()