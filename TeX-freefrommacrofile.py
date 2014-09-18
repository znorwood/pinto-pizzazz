#!/usr/bin/env python

# TeX-freefrommacrofile
# usage: TeX-freefrommacrofile macros.tex file.tex

# TODO: before writing macros above \begin{document} to new file, 
# remove all lines beginning with % and empty lines 
# (your macros file is full of them)

# TODO: expand to handle more than one macro file & more than one tex file
# usage: independentize [--save-aux-files] macro-file-1 ... macro-file-n --scan tex-file-1 ... tex-file-n
# writes tex-file-1-independent ... tex-file-n-indepedent

from sys import argv
import re
import shutil

macro_file = argv[1]
tex_file = argv[2]
output_file = tex_file[:-4] + "-ind" + tex_file[-4:]
macros_for_file = []
prefixes = ["\\newcommand", "\\def", "\\renewcommand", "\\newcommand*", "\\DeclareMathOperator"]
macro_pat = re.compile(r'\\[a-zA-Z]+')
tmp = output_file[:-4] + "-tmp" + output_file[-4:]
header = '''
% % % % % % % % % % % % % % % % % % % % % % %
% below are macros from your input file(s)  %
% % % % % % % % % % % % % % % % % % % % % % %

'''

def startsAMacro(string):
	for pref in prefixes:
		if re.search('\A\\%s' % pref, string):	
#			print "%s begins with %s" % (string, pref) # debug
			return pref

#finds the \begin{document} line of the file
def beginDocLine(file):
	with open(file) as f:
		for numb, line in enumerate(f,1):
			if re.search(r'^\\begin{document}',line):
				return numb

# takes things, a list, inserts (new lines separating items) before line number n
def insertMacros(things,file,n):
	with open(file,'r') as inputf:
		with open(tmp,'w') as outf:
			for i, line in enumerate(inputf,1):
				if i<n:
					outf.write(line)
					continue
				if i==n:
					outf.write(header)
					for item in things:
						outf.write('%s\n' % item)
#						outf.write(item)
					outf.write('\n%s' % line)
				if i>n:
					outf.write(line)
	shutil.move(tmp,output_file)	
		
with open(tex_file,'r') as inputf:
	with open(macro_file,'r') as macrof:
		input_text = inputf.read()
		macro_list = re.split(r'\n(?=(?:\\newcommand|\\def|\\renewcommand|\\DeclareMathOperator|\\newcommand*))',macrof.read())
		for macro in macro_list:
#			 have to check whether this isn't a dud macro (boundary case)
			if startsAMacro(macro):
				the_prefix = startsAMacro(macro)
				regex = re.compile('\\%s{?(\\\\[a-zA-Z]+)}?' % the_prefix)
				match = regex.search(macro)
				the_command = match.group(1)
#				 here want to search conservatively: the_command should not be
#				 an initial segment of another command, for instance
				if re.search('\\%s[^a-zA-Z]' % the_command,input_text):
#				if re.search('\\%s' % the_command,input_text):	# debug
					macros_for_file.append(macro)
		with open(output_file,'w') as outf: 
				outf.write(input_text)			#copy tex-file to tex-file-clean
		insertMacros(macros_for_file,output_file,beginDocLine(output_file))
