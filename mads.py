#Library
from subprocess import Popen, PIPE
import tempfile
import os
import sys
import time
import subprocess

#	argument handler

def arg_handle(arg_in, arg_name_in):
	arg_out = []
	for i in arg_name_in:
		arg_out.append([])
	for i,command in enumerate(arg_in):
		for ii, arg in enumerate(arg_name_in):
			if arg == command:
				try:
					arg_out[ii] = str(arg_in[i+1])
				except:
					arg_out[ii] = True
	return arg_out

#downloading---------------------------------------------------------------------

def get_url(url="http://www2.nve.no/h/hd/plotreal/Q/0122.00017.000/knekkpunkt.html"):
	import codecs,sys
	import urllib
	sys.stdout = codecs.getwriter('utf8')(sys.stdout)
	opener = urllib.URLopener()
	f = opener.open(url)
	content = f.read().decode('iso-8859-1')
	out=[]
	for line in content.split("\n"):
		out.append(line)
	return out



#piping and bash--------------------------------------------#
def create_pipe(term="my_pipe"):
	PIPE_PATH = "/tmp/"+term
	if not os.path.exists(PIPE_PATH):
		os.mkfifo(PIE_PATH)
	print "test"
	Popen(['gnome-terminal', '-e', 'tail -f %s' % PIPE_PATH])
	return term

def get_term_result(cmdline):
	outlist=[]
	cmdline = cmdline.rstrip()
	cmdline = cmdline.split(" ")
	cmd=[]
	for item in cmdline:
		cmd.append(item)
	print str(cmd)
	with tempfile.TemporaryFile() as tempf:
		proc = subprocess.Popen(cmd, stdout=tempf)
		proc.wait()
		tempf.seek(0)
		corr_line=False
		for line in tempf.readlines():
			#remove newline character
			line=line[:len(line)-1]
			outlist.append(line)
	return outlist

def term_exist(term):
	cwd = os.getcwd()
	os.chdir("/bin/")
	check = get_term_result("bash pi_ex.bash "+term)
	os.chdir(cwd)
	print str(check)
	if check:
		check=check[0]
	if check == 'True':
		return True
	elif check == 'False':
		return False
	else:
		return False
		print "ERROR in term_exist()"

class pipewrite(object):
	def __init__(self, term):
		self.PIPE_PATH="/tmp/"+term

	def write(self, stra):
		with open(self.PIPE_PATH, "w") as p:
			p.write(stra)

#sorting----------------------------------------------------#

#Returns sorted version of unsorted_list, sorted by list index 'idx'
#Can return both in ascending and descending order.
def bubblesort(unsorted_list,idx=999,descending=True):
	unsorted_item=unsorted_list[0]
	#case index not specified.
	if idx == 999:
		#Find and integer in case of tuples or lists in lists
		if not isinstance(unsorted_item,(int,long)):
			idx=[]
			for i,item in enumerate(unsorted_item):
				if isinstance(item,(int,long)):
					#found int in list item
					idx=i
					break
			if not isinstance(idx,(int,long)):
				#int not found
				return "Error, no integer in list item"
		else:
			idx = 0
	# one pass through the bubblesort
	def bubblepass(unsorted_list,idx):
		def listswap(inlist,idx1,idx2):
				tmp1=inlist[idx1]
				tmp2=inlist[idx2]
				outlist=inlist
				outlist[idx1]=tmp2
				outlist[idx2]=tmp1
				return outlist
		for i, item in enumerate(unsorted_list):
			if i == 0:
				pass
			else:
				try:
					if item[idx] > last_item[idx]:
						unsorted_list=listswap(unsorted_list,i,i-1)
				except:
					if item > last_item:
						unsorted_list=listswap(unsorted_list,i,i-1)
			last_item=item
		return unsorted_list

	#repeat passes until list doesn't change
	last_list=[]
	while unsorted_list != last_list:
		last_list = [x for x in unsorted_list] #same as last_list=unsorted_list except python >.<
		unsorted_list = bubblepass(unsorted_list, idx)
	if descending:
		return unsorted_list
	else:
		return list(reversed(unsorted_list))

#-------------------- 5.9 Review ---------------------------#

def setbytebit(byte,bit,val):
	out=""
	bitstr="{0:08b}".format(int(byte,16))
	for i, bin in enumerate(bitstr):
		if 7-i == bit:
			out += str(val)
		else:
			out += str(bin)
	return hex(int(out,2))

def getbytebit(byte,bit):
	bitstr="{0:08b}".format(int(byte,16))
	for i, bin in enumerate(bitstr):
		if 7-i == bit:
			out = bin
	return bool(int(out))

def is_list_greater_than(lst,val):
	for item in lst:
		if item > val:
			return True
	return False

def check_alarm_group(alarm_list):
	#If alarm belongs to one group, all other alarms after alarm shall be true. else print error.
	general_delay_group=[0,3,4,5,6,7,8,9,17,19,20,22,24,29]
	nf_delay_group=[10,11,12]
	ident_delay_group=[1,2,14,15,28,30]
	ffm_delay_group=[13,16,18,21,23,25]
	al=[[],[],[],[]]
	gen,nf,ident,ffm = False,False,False,False
	missing_ids_gen,missing_ids_nf,missing_ids_ident,missing_ids_ffm=[],[],[],[]
	out = "\n\t"
	for i in alarm_list:
			if i in general_delay_group:
				if not gen: al[0] = i
				gen=True
				missing_ids_gen=[]
				for ii in general_delay_group:
					if ii not in alarm_list:
						missing_ids_gen.append(ii)
			if i in nf_delay_group:
				if not nf: al[1] = i
				nf=True
				missing_ids_nf=[]
				for ii in nf_delay_group:
					if ii not in alarm_list:
						missing_ids_nf.append(ii)
			if i in ident_delay_group:
				if not ident: al[2] = i
				ident=True
				missing_ids_ident=[]
				for ii in ident_delay_group:
					if ii not in alarm_list:
						missing_ids_ident.append(ii)
			if i in ffm_delay_group:
				if not ffm: al[3] = i
				ffm=True
				missing_ids_ffm=[]
				for ii in ffm_delay_group:
					if ii not in alarm_list:
						missing_ids_ffm.append(ii)
	if is_list_greater_than(missing_ids_gen, al[0]):
		out += clrstr("Missing alarm id: "+str(missing_ids_gen)+" from ")
	if gen:
		out+= "("+str(al[0])+") MS_AL General Delay Group, \n\t"
	if is_list_greater_than(missing_ids_nf, al[1]):
		out += "Missing alarm id: "+str(missing_ids_nf)+" from "
	if nf:
		out+= "("+str(al[1])+") MS_AL NF Delay Group, \n\t"
	if is_list_greater_than(missing_ids_ident,al[2]):
		out += "Missing alarm id: "+str(missing_ids_ident)+" from "
	if ident:
		out+= "("+str(al[2])+") MS_AL Ident Delay Group, \n\t"
	if is_list_greater_than(missing_ids_ffm,al[3]):
		out += "Missing alarm id: "+str(missing_ids_ffm)+" from "
	if ffm:
		out+= "("+str(al[3])+") MS_AL FFM Delay Group, \n\t"
	if out != "":
		out = out[:len(out)-4]+". "
	return out
	for item in lst:
		if item > val:
			return True
	return False

def translate_bits(number,cmd):
	error=""
	#Alarm interface packet
	if cmd == 0:
		statuses = ["MS_AL","AL_RAW","MS_AL_N"]
	#MO_FPGA_Status_Reg
	elif cmd == 1:
		statuses=["HRA","TX Feedback Retrigger Alarm","Test Channel Check Error","Parameter CRC",
		"MF Data Interface Error","Test Channel Check Warning","Test Parameter Toggle Error","Parameter ID error"]
	#REG_MO_CPLD_STATUS
	elif cmd == 2:
		statuses=["HRA","TX Feedback Retrigger Alarm","Test Channel Check Error","EEPROM limit/delay CRC error",
		"Parameter CRC","Test Channel Check Warning","Test Parameter Toggle Error","Parameter ID error"]
	#REG_MOMF_STAT
	elif cmd == 3:
		statuses=["N/A","Frame synchronization error","Sequence number error","Packet CRC error","Packet early",
		"Packet timeout","N/A","N/A"]
	#RMS status
	elif cmd == 4:
		statuses=["EEPROM busy","EEPROM CRC error","EEPROM read error","MF control error","\033[94mFIFO complete dataset\033[0m",
		"FIFO synchronization","FIFO full","\033[94mFFIFO not empty\033[0m"]
	#RMS Primary Fifo status byte
	elif cmd == 5:
		statuses=["HRA","N/A","EE_RD_ERROR","EE_CRC_ERROR","MS_AL_N",
		"MS_AL","MS_AL_RAW","MF_ERROR"]
	#RMS maintenance status
	elif cmd == 6:
		statuses=["FFM error","MF maintenance error","N/A","N/A","\033[94mFIFO complete dataset\033[0m",
		"FIFO synchronization","FIFO full","\033[94mFFIFO not empty\033[0m"]
	#RMS Maintenance Fifo status byte
	elif cmd == 7:
		statuses=["CRC_ERR","SEQ_ERR","PKT_ERR","ID_ERR","N/A","N/A","N/A","N/A"]

	#if cmd in [1,2,3,4,5,6,7]:
	for i in range(8):
		bits = "{0:08b}".format(number)
		if int(bits[len(bits)-1]):
			error += statuses[i]+", "
		number = number >> 1
	if len(error) > 2:
		error = error[:len(error)-2]+"."
		return error
	else:
		return "0"

def translate_bytes(byte_list, cmd, param_value = False):
	out = ""
	if cmd == 0:
		MS_AL_RAW=False
		changed = False
		status = []
		last_status = []
		MS_AL_ARRAY= [] #Shall be in 1 of 4 delay groups
		for i,byte in enumerate(byte_list):

			status = translate_bits(int(byte,16)>>6, 0)

			if "AL_RAW" in status and "AL_RAW" not in last_status and i > 0:
				#status changed during packet.
				out += "MS_AL_RAW asserted at " +str(i)+", "
				changed = True
			elif "AL_RAW" not in status and "AL_RAW" in last_status:
				out += "MS_AL_RAW deasserted at " +str(i)+", "
				changed = True
			elif "AL_RAW" in status:
				MS_AL_RAW = True
			if "MS_AL" in status:# and i in general_delay_group + nf_delay_group +ident_delay_group + ffm_delay_group:
				MS_AL_ARRAY.append(i)
			last_status=status
		if out != "":
			out = out[:len(out)-2]+". "
		if MS_AL_RAW and not changed:
			out += "MS_AL_RAW. "
		if MS_AL_ARRAY:
			out += check_alarm_group(MS_AL_ARRAY)
	if cmd in [5,7]:
		ls_error=[]
		error=[]
		id_list=[]
		status_list=[]
		param_list=[]
		twobyte_param=[]
		for ii,four_bytes in enumerate(byte_list):
			i=0
			for half_byte in four_bytes:
				if(i % 2):
					byte += half_byte
					#First byte, Alarmid.
					if i == 1:
						id_list.append(byte)
					#Second byte, alarm parameter LS
					if i == 3 and param_value:
						twobyte_param = byte
					#Third byte, alarm parameter MS
					if i == 5 and param_value:
						twobyte_param = byte + twobyte_param
						param_list.append(twobyte_param)
					#Last byte, containing status reg
					if i == 7:
						#error = translate_bits(int(byte,16),cmd)
						status_list.append(byte)
						#print byte
				else:
					byte = half_byte
				i+=1
		inc_fault, where = inccheck(id_list,cmd)
		if inc_fault:
			out += " Alarm_id incrementation fault at parameter: " +str(where)
		#if cmd == 5:
		#	out = translate_bytes(id_list, 0)
		elif cmd == 7:
			MF_STAT, FFM_STAT = param_bit_check(status_list, cmd)
			out += "MNT_STAT_MF: "+MF_STAT +"\t MNT_STAT_FFM: " +FFM_STAT
		else:
			out += param_bit_check(status_list, cmd)
		if param_value:
			out += "\n"
			for i,param in enumerate(param_list):
				out += "ID "+id_list[i]+":\t\t"
				out += str(int(param,16))+"\t\t"+translate_bits(int(status_list[i],16),cmd)+"\n"

	return out

def inccheck(byte_list,cmd):
	if cmd == 5:
		mode = "PRIM"
	else:
		mode = "MNT"
	last_byte='AA'
	error = False
	out = []
	inc=1
	for i, byte in enumerate(byte_list):
		if (int(byte,16) != int(last_byte,16)+inc) and (i > 0):
			if mode == "MNT" and (i > 28 or i == 20): #avoid maintenance byte irregularities
				inc+=1
			else:
				error=True
				out.append(i)
				#to avoid double fault  13 00 14 15
				inc=2
		else:
			inc=1
			last_byte=byte
	return error, out

def param_bit_check(byte_list, cmd):
	status=""
	last_status=[]
	Mf_out = ""
	#mnt_register
	if cmd == 7:
		ffm_status=""
		ffm_last_status=[]
		FFM_out= ""
		for i, byte in enumerate(byte_list):
			#FFM status
			if i in [18,19]:
				ffm_status = translate_bits(int(byte,16), cmd)
				if i == 19 and ffm_status != ffm_last_status:
					FFM_out += clrstr("ERROR, FFM parameters not equal")
					break
				ffm_last_status=ffm_status
			#20,29,30 and 31 are unused.
			elif i == 20 or i > 28:
				pass
			else:
				status = translate_bits(int(byte,16), cmd)
			if status != last_status and i > 0:
				#status changed during packet.
				Mf_out += last_status+ " until param " +str(i)+ ", then "
			last_status=status
		Mf_out += status
		FFM_out += ffm_status
		return Mf_out , FFM_out
	#prim_register
	else:
		MS_AL_ARRAY=[]
		for i, byte in enumerate(byte_list):
			#not interested in ms_al_n or ms_al here
			tbyte = setbytebit(byte, 4, 0)
			tbyte = setbytebit(tbyte, 5, 0)
			status = translate_bits(int(tbyte,16), cmd)
			if status != last_status and i > 0:
				Mf_out += last_status+ " until param " +str(i)+ ", then "
			last_status=status
		Mf_out += status
		#check ms_al
		for i, byte in enumerate(byte_list):
			if getbytebit(byte, 5):
				MS_AL_ARRAY.append(i)
		ms_al_out = check_alarm_group(MS_AL_ARRAY)

		return Mf_out + ms_al_out


#-------------------- COLORS --------------------------------#
class bcolors:
		HEADER = '\033[95m'
		OKBLUE = '\033[94m'
		OKGREEN = '\033[92m'
		WARNING = '\033[93m'
		FAIL = '\033[91m'
		ENDC = '\033[0m'
		BOLD = '\033[1m'
		UNDERLINE = '\033[4m'
		CURSIVE = '\033[3m'
		BLACK = '\033[8m'
		TEAL = '\033[96m'

def clrstr(str,color=["RED"]):
	out = ""
	for param in color:
		if param=="RED":
			out += bcolors.FAIL
		elif param =="BLUE":
			out += bcolors.OKBLUE
		elif param =="GREEN":
			out += bcolors.OKGREEN
		elif param =="YELLOW":
			out += bcolors.WARNING
		elif param =="BOLD":
			out += bcolors.BOLD
		elif param =="LINE":
			out += bcolors.UNDERLINE
		elif param =="PURPLE":
			out += bcolors.HEADER
		elif param =="CURSIVE":
			out += bcolors.CURSIVE
		elif param =="BLACK":
			out += bcolors.BLACK
		elif param =="TEAL":
			out += bcolors.TEAL
		else:
			pass
	return out + str + bcolors.ENDC

#------------- ENCRYPTION-------------------------------------#

#Takes a list of text in 'textlist', returns it encoded using password 'phrase'.
#Mode='Encode'/'Decode' which basically does the reverse thing.
def encode(textlist, phrase, mode, legal_chars="abcdefghijklmnopqrstuvwxyz\011\012\015\040\057\134\042\043.,1234567890ABC5DEFGHIJKLMNOPQ:;[]RSTUVWXYZ!?'()%&@$-_="):
	def get_char_nr(char,legal_chars):
		for i,m_char in enumerate(legal_chars):
			if m_char == char:
				return i
		print "ERROR, char: "+char+"("+str(ord(char))+") not in legal chars"
		raise SystemExit()

	def switch_char(char,shift,legal_chars):
		mx_nr = len(legal_chars)
		o_nr=get_char_nr(char, legal_chars)
		if o_nr+shift >= mx_nr:
			n_char_nr = o_nr + shift - mx_nr
		elif o_nr + shift < 0:
			n_char_nr = mx_nr + o_nr + shift
		else:
			n_char_nr = o_nr + shift
		try:
			return legal_chars[n_char_nr]
		except:
			print "Fault in encode(switch_char)"
			print o_nr, "\t", shift, "\t", n_char_nr, "\t", mx_nr
			raise SystemExit()
	output=[]
	cnt = 0
	for i,line in enumerate(textlist):
		output.append("")
		for char in line:
			shift = get_char_nr(phrase[cnt], legal_chars)+1
			if (cnt % 2):
				shift = -shift
			cnt += 1
			if cnt > len(phrase)-1:
				cnt = 0
			if mode == "Decode":
				shift = -shift
			n_char=switch_char(char,shift,legal_chars)
			output[i] += n_char
	return output