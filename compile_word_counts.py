import pandas as pd
import re
import argparse
import os.path as osp
import json

canonical_ponys=['twilight','applejack','rarity','pinkie','rainbow','fluttershy']
ponys_fullname=['Twilight Sparkle', 'Applejack','Rarity', 'Pinkie Pie', 'Rainbow Dash','Fluttershy']
full_to_can={'Twilight Sparkle':'twilight','Applejack':'applejack','Rarity':'rarity','Pinkie Pie':'pinkie','Rainbow Dash':'rainbow','Fluttershy':'fluttershy'}


def get_dialogs(df):
    #this function return a dictionary with value of lists of words
    result={}
    for pony in ponys_fullname:
        temp=df[df['pony']==pony]['dialog']
        out = ' '.join(temp.astype(str))
        out=re.sub("\<U\+[0-9]{4}\>"," ",out)
        words=re.sub("[^\w]", " ",out).split()
        words=[word.lower() for word in words if (word.isalpha())]
        result[full_to_can[pony]]=words
    return result

def counts(dialogs):
    result=dict.fromkeys(dialogs)
    for pony in list(dialogs.keys()):
        list_of_words=dialogs[pony]
        wordsUnique=set(list_of_words)

        count={key:0 for key in wordsUnique}
        for word in list_of_words:
            count[word]+=1
        for word in list(count.keys()):
            if count[word]<5:
                del count[word]
        result[pony]=count
    return result

def main():
    parser=argparse.ArgumentParser() 
    parser.add_argument('-o',help='the output file')
    parser.add_argument('src',help='the csv file which contains the dialog')
    args=parser.parse_args()
    try:
        dialog=pd.read_csv(args.src)
    except:
        print("Error. Cannot read the input file.")
        return
    dialog=get_dialogs(dialog)
    result=counts(dialog)
    json_out=json.dumps(out,indent=4)
    if filename != None:
        with open(args.o,'w')as out:
            out.write(json_out)
    return
if __name__=='__main__':
    main()
