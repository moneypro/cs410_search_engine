dic = {}
with open('parsed_author_school.txt') as f:
    for line in f.readlines():
        s = line.strip().split("||")

        school = s[1].lower()\
        .replace("univ. of","university")\
        .replace("university of","university")\
        .replace("university","university of")\
        .replace("u. c.","university of california at")\
        .replace(" - ","-")\
        .replace("-"," ")\
        .replace(";"," ")
        
        name = s[0]
        if dic.get(school):
            if dic[school].get(name):
                dic[school][name]+=1
            else:
                dic[school].update({name:1})
        else:
            dic[school] = {name:1}

query = "university of illinois at urbana champaign, united states of america"
print (dic[query])
# print (dic.keys())