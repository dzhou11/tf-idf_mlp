import pandas as pd
import argparse
import json
import math


canonical_ponys=['twilight','applejack','rarity','pinkie','rainbow','fluttershy']
ponys_fullname=['Twilight Sparkle', 'Applejack','Rarity', 'Pinkie Pie', 'Rainbow Dash','Fluttershy']
full_to_can={'Twilight Sparkle':'twilight','Applejack':'applejack','Rarity':'rarity','Pinkie Pie':'pinkie','Rainbow Dash':'rainbow','Fluttershy':'fluttershy'}

def load_json(fname):
    with open(fname, 'r') as content_file:
        Dict = json.load(content_file)
    return Dict

def cal_idf(b):
    N=0
    wordsUnique=[]
    for dic in list(b.values()):
        N+=sum(dic.values())
        wordsUnique.extend(dic.keys())
    wordsUnique=set(wordsUnique)
    idf={key:0 for key in wordsUnique}
    #total_words=[x for y in list(b.values()) for x in y ]
    for pony in b:
        for word in b[pony].keys():
            idf[word]+=b[pony][word]
    for word in idf:
        idf[word]=math.log(N/idf[word])

    return idf
def cal_idf_p(b):
    N=6 
    wordsUnique=[]
    ponys_wordset={ key: set(b[key].keys()) for key in b }
    for dic in list(b.values()):
        wordsUnique.extend(dic.keys())
    wordsUnique=set(wordsUnique)
    idf={key:0 for key in wordsUnique}
    
    
    for pony in b:
        for word in b[pony].keys():
            idf[word]+=1
    for word in idf:
        idf[word]=math.log(N/idf[word])

    return idf 

def tfidf(b,idf):
    tfidfs=dict.fromkeys(b)
    for pony in tfidfs:
        tfidf={}
        for word in b[pony].keys():
            tfidf[word]=b[pony][word] * idf[word]
        tfidfs[pony]=tfidf
    return tfidfs
def take_top_n(tfidf,num):
    top={}
    for pony in tfidf:
        x=tfidf[pony]
        top[pony]=list(dict(sorted(x.items(), key=lambda item: item[1],reverse=True)[:num]).keys())
    return top
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('-p',help='if you choose to calculate idf in a meaningful way.',action='store_true')
    parser.add_argument('word_count',help='the words count file(.json)')
    parser.add_argument('out_num',help='number of output you want.')

    args=parser.parse_args()

    count=load_json(args.word_count)
    if args.p == False:
        idf=cal_idf(count)
    else:
        idf=cal_idf_p(count)
    tf_idf=tfidf(count,idf)
    result=take_top_n(tf_idf, int(args.out_num))
    
    json_out=json.dumps(result,indent=4)
    print(json_out)
    return json_out
if __name__=='__main__':
    main()
