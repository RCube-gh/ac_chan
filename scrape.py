import requests
from bs4 import BeautifulSoup
import os
import sys
import time
import logging
import re
import json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)

GREEN='\033[32m'
RED='\033[31m'
RESET='\033[0m'

PROBLEM_METADATA_FILE='metadata.json'
SLEEP_TIME=0.5


def get_problem_links(contest_str):
    print("getting problem links...")
    url=f"https://atcoder.jp/contests/{contest_str}/tasks"
    res=requests.get(url)
    res.raise_for_status()
    soup=BeautifulSoup(res.text,'html.parser')

    problem_links=[]
    for a in soup.select("a"):
        href=a.get("href","")
        if href.startswith(f"/contests/{contest_str}/tasks/"):
            problem_id=href.split("/")[-1]
            problem_links.append((problem_id,"https://atcoder.jp"+href))

    problem_links=list(dict(problem_links).items())
    print(f"{len(problem_links)} problem links found.")
    return problem_links

def scrape_contest(contest_str):
    current_dir=os.getcwd()
    contest_dir=os.path.join(current_dir,contest_str)
    os.makedirs(contest_dir,exist_ok=True)

    problem_links=get_problem_links(contest_str)

    for problem_id, url in problem_links:
        # create directory for problem
        problem_char=problem_id.split("_")[-1].upper()
        contest_problem_dir=os.path.join(contest_dir,problem_char.upper())
        os.makedirs(contest_problem_dir,exist_ok=True)
        
        print(f"fetching {problem_id}...")

        try:
            # get tastcases from atcoder
            res=requests.get(url)
            res.raise_for_status()
            soup=BeautifulSoup(res.text,'html.parser')

            # get time limit
            time_limit=-1
            for p in soup.find_all('p'):
                p_text=p.text.strip()
                if(p_text.startswith('Time Limit')):
                    match=re.search(r"(\d+(?:\.\d+)?)\s*sec",p_text)
                    time_limit=float(match.group(1))

            problem_metadata_path=os.path.join(contest_problem_dir,PROBLEM_METADATA_FILE)
            problem_metadata={}
            problem_metadata['time_limit']=time_limit


            try:
                with open(problem_metadata_path,"w",encoding="utf-8") as f:
                    json.dump(problem_metadata,f,indent=2,ensure_ascii=False)
                logging.info(f"Problem {problem_id}: Saved metadata to {problem_metadata_path}")
            except Exception as e:
                logging.warning(f"An error occurred: {e}")



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



            logging.info(f"Problem {problem_id}: {len(in_texts)} cases saved")
        except Exception as e:
            print(f"{problem_id} failed: {e}")


        time.sleep(SLEEP_TIME)

