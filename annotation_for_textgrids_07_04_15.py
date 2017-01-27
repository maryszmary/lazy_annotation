# -*- coding: utf-8 -*-
# TODO: refactor
import codecs
import re
import sys


the_name = raw_input('Please type the filename ').decode(sys.stdin.encoding)
sourcetier = input('Type the number of the source tier ')

def file_array(name):
    '''возвращает массив строк'''
    with codecs.open(name + u'.TextGrid','r', 'utf-8') as f: # 'utf-16-be'
        text = []
        for line in f.readlines():
            text.append(line.strip())
    return text

def write_from_array(name, array):
    f1 = codecs.open(name,'w','utf-16-be')
    for el in array:
        f1.write(el + '\r\n')
    f1.close()
    return f1

lines = file_array(the_name)

#названия слоёв

tier_words = u'! ' + re.sub('\"IntervalTier\" \"(.+)\".+', '\\1',
                            lines[3], flags = re.U) + u':'
tier_sounds = u'! ' + re.sub('\"IntervalTier\" \"(.+)\".+', '\\1',
                            lines[4], flags = re.U) + u':'
tier_stops = u'! ' + re.sub('\"IntervalTier\" \"(.+)\".+', '\\1',
                            lines[5], flags = re.U) + u':'
tier_diffwords = u'! ' + re.sub('\"IntervalTier\" \"(.+)\".+', '\\1',
                            lines[sourcetier + 2], flags = re.U) + u':'

intr = []
for el in lines:
    # if el != tier_diffwords: commented out: 27.01.17
    if el not in [tier_diffwords, tier_words, tier_stops, tier_sounds]:
        intr.append(el)
    else:
        print('ended intr. length of intr: ' + str(len(intr)))
        break

#все сеты лексем

n = 0
all_sets = []
while n < len(lines):
    if tier_diffwords in lines[n]:
        diff_words = []
        m = n
        while m < len(lines):
            if m == n or tier_diffwords not in lines[m]:
                diff_words.append(lines[m])
                m += 1
            else:
                break
        all_sets.append(diff_words)
    n += 1
    
#аннотация слов

for arr in all_sets:
    if arr[2] != '\"\"':
        i = 0
        ii = 1
        while i < len(arr):
            if arr[i] == tier_words:
                ii += 1
                if ii%2 == 0:
                    arr[i + 2] = arr[2]
            i += 1

#new_lines - это весь файл

new_lines = []
new_lines += intr
for el in all_sets:
    new_lines += el

#новое вступление

intr = []
for el in lines:
    if el != tier_words:
        intr.append(el)
    else:
        break

#все сеты отдельных слов

n = 0
all_words = []
while n < len(new_lines):
    if tier_words == new_lines[n]:
        words = []
        m = n
        while m < len(lines):
            if m == n or tier_words != new_lines[m]:
                words.append(new_lines[m])
                m += 1
            else:
                break
        all_words.append(words)
    n += 1

#здесь аннотируется второй слой

modificators = u'\'ˤʃʷˀ:͡'

for arr in all_words:
    if arr[2] != '\"\"' and tier_sounds in arr:
        word = arr[2][1:(len(arr[2]) - 1)]
        sounds = []
        sound = 0
        for l in range(len(word)):
##            if sound != 0 and word[l] == u's' and word[l - 1] == u't':
##                sounds[sound - 1] += word[l]
##            elif sound != 0 and word[l] == u'ɬ' and word[l - 1] == u't':
##                sounds[sound - 1] += word[l]
##            elif word[l] not in modificators:
##                sounds.append(word[l])
##                sound += 1            
##            else:
##                if sound != 0:
##                    sounds[sound - 1] += word[l]
            if (sound != 0 and ((word[l] == u's' and word[l - 1] == u't') or
                                (word[l] == u'ɬ' and word[l - 1] == u't') or
                                (word[l] == u'χ' and word[l - 1] == u'͡')) or
                word[l] in modificators):
                sounds[sound - 1] += word[l]
            else:
                sounds.append(word[l])
                sound += 1            
        #в этой части кода получившиеся звуки приписываются интервалам в файле
        #здесь всё нормально
        #не надо ничего трогать
        boundary = 0
        for w in range(len(arr)):
            if tier_sounds == arr[w]:
                if boundary < len(sounds):
                    arr[w + 2] = u'\"' + sounds[boundary] + u'\"'
                    boundary += 1
                    
#здесь аннотируется третий слой

stops = u'p\'k\'q\'dt\''

for arr in all_words:
    for w in range(len(arr)):
        if arr[w] == tier_sounds:
            thesound = arr[w + 2].strip('"')
            if thesound != u'' and thesound in stops:
                if tier_stops not in arr[w + 7:]:
                    print "SOMETHING GONE WRONG at", w
                    print u'\n'.join(arr[w:])
                    print "UTTERLY"
                if tier_stops in arr[w + 7:]:
                    if arr[w + 4] == tier_stops and arr[w + 8] == tier_stops:
                        arr[w + 6] = u'\"C_' + thesound + u'\"'
                        arr[w + 10] = u'\"V_' + thesound + u'\"'
                    if w == 4 and arr[w + 4] == tier_stops:
                        arr[w + 6] = u'\"C_(' + thesound + u'\"'
                    if w == len(arr) - 12 and arr[w + 8] == tier_stops:
                        arr[w + 10] = u'\"V_(' + thesound + u'\"'

#здесь создаётся окончательная версия массива для записи в новый файл

for el in all_words:
    intr += el            

write_from_array(u'annotated_' + the_name + u'.TextGrid', intr)
