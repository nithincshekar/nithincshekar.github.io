import sys

f = open('anagram_out.txt', 'w')
def Anagram(Fstr, Rstr):
   if len(Rstr) == 0:
       f.write(Fstr+'\n')
   else:
       for i in range(len(Rstr)):
           cur = Rstr[i]
           remStr = Rstr[0:i] + Rstr[i+1:]
           Anagram(Fstr+cur, remStr)
stri = str(sys.argv[1]).replace("'","")
Anagram("", sorted(stri))