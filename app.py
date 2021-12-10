import streamlit as st
from transformers import pipeline
import requests
from bs4 import BeautifulSoup



def model_save():
    summarizer = pipeline("summarization")
    return summarizer

def main():
    
    st.title("Article Summarization")
    st.subheader("""
                As these days, we keep getting bussy and bussy,
                and if we have to read any article, its better to get a gist of what is in the article before actually reading it.
                So i creating a solution for the same.
                You can paste any blog link and a summary will be prvided.
                """)
    URL = st.text_input(label="Enter the URl : ")
    r = requests.get(URL)
    st.write(r)

    soup = BeautifulSoup(r.text,"html.parser")
    results = soup.find_all(["h1","p"])

    text = [result.text for result in results]
    article = " ".join(text)
    
    article = article.replace(".",".<eos>")
    article = article.replace("!","!<eos>")
    article = article.replace("?","?<eos>")
    #article= article.replace("\n","<eos>")
    sentences = article.split("<eos>")

    max_chunk=450
    current_chunk=0
    chunks=[]

    for sentence in sentences:
        if len(chunks) == current_chunk + 1:
            if len(chunks[current_chunk]) + len(sentence.split(" ")) <= max_chunk:
                chunks[current_chunk].extend(sentence.split(" "))
            else:
                current_chunk +=1
                chunks.append(sentence.split(" "))
        else:
            print(current_chunk)
            chunks.append(sentence.split(" "))
            pass

    for i in range(len(chunks)):
        chunks[i] = " ".join(chunks[i])

    #st.write(chunks[0])
    #pass
    summarizer = model_save()
    res = summarizer(chunks,max_length=150,min_lenght=30,do_sample=False)
    
    for i in res:
        st.write(i["summary_text"])
        #print("\n")
    #st.write(res)

if __name__=="__main__":
    main()