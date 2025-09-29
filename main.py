import requests
from bs4 import BeautifulSoup
import os
import sys
import time


def go_soup():
    current_dir=os.getcwd()
    contest_type='abc'
    contest_num=423
    contest_str=contest_type+str(contest_num)
    problem_chars=['a','b','c','d','e','f','g','ex']


    contest_dir=os.path.join(current_dir,contest_str)
    os.makedirs(contest_dir,exist_ok=True)



    for problem_char in problem_chars:
        # create directory for problem
        contest_problem_dir=os.path.join(current_dir,problem_char.upper())
        os.makedirs(contest_problem_dir,exist_ok=True)

        # get tastcases from atcoder
        url=f'https://atcoder.jp/contests/abc{contest_num}/tasks/abc{contest_num}_{problem_char}'
        res=requests.get(url)
        res.raise_for_status()
        soup=BeautifulSoup(res.text,'html.parser')

        in_texts=[]
        out_texts=[]
        for section in soup.select("section"):
            h3=section.find('h3')
            pre=section.find('pre')
            if h3.text.startswith('入力例'):
                in_texts.append(pre.text)
            elif h3.text.startswith('出力例'):
                out_texts.append(pre.text)
        for idx,i in enumerate(in_texts):
            with open(os.path.join(contest_problem_dir,f"in_{idx+1}.txt"),"w",encoding="utf-8") as f:
                f.write(i)
        for idx,o in enumerate(out_texts):
            with open(os.path.join(contest_problem_dir,f"out_{idx+1}.txt"),"w",encoding="utf-8") as f:
                f.write(o)

def main():
    go_soup()



if __name__ =="__main__":
    main()

