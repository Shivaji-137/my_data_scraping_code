# created by Shivaji Chaulagain

try:
    import requests
    from bs4 import BeautifulSoup as bs
    import webbrowser
    import sys
    import pandas as pd
    import time
    import numpy as np
    import os
  
except ImportError as e:
    print(f"Required module {e.name} not found. You can install it using 'pip install {e.name}'.")
     

class arxiv:
    def __init__(self, content, abs_state, sort_results, page=0):
        self.content = content
        self.abs_state = abs_state
        self.sort_results = sort_results
        self.page = page
        start = self.page*25
        self.file = requests.get(f"https://arxiv.org/search/?query={self.content}&searchtype=title&abstracts={self.abs_state}&order={self.sort_results}&size=25&start={start}")
        self.soup = bs(self.file.content, "lxml")
    def scrape(self):
            title = []
            links = []
            date = []
            category = []
            for j in self.soup.find_all("li", class_ = "arxiv-result"):
                title.append(j.find("p", class_= "title is-5 mathjax").get_text().strip('\n '))
                date.append(j.find("p", class_ = "is-size-7").contents[1].strip())
                category.append(j.find("div", class_ = "tags is-inline-block").find("span")["data-tooltip"])
                pdf_element = j.find(string=lambda text: text and text.startswith('pdf'))
                if pdf_element is not None:
                    parent_element = pdf_element.find_parent()
                    if parent_element is not None:
                        pdf_link = parent_element.get("href")
                        links.append(pdf_link)
                    else:
                        links.append("Link not found")
                else:
                    links.append("PDF not found")
                
            result = list(zip(title,category, date))
            df = pd.DataFrame(result, columns = ["Title", "Category", "Date"], index = np.arange(1, len(title)+1) )
            print(df)
            return links, title
    def abstract(self, num):
        n = num -1
        abst = []
        #abst.append(soup.find_all("span", id = "quant-ph/9807064v1-abstract-full").getText())
        #for j in soup.find_all("p", class_="abstract mathjax"):
            #for k in j.find_all(id = "quant-ph/9807064v1-abstract-full"):
                #abst.append(k.get_text())
            #abst.append(j.get_text())#j.find("span",id = "quant-ph/9807064v1-abstract-full").get_text())
        for j in self.soup.find_all(class_="abstract-full has-text-grey-dark mathjax"):
            abst.append(j.get_text().strip())#.find("span",id = "quant-ph/9807064v1-abstract-full"))
        links, titl = self.scrape()
        print("\n")
        print(f"Title({num}):",list(titl)[n])
        print("--------------------------------------------------------")
        print("Abstract:\n ", abst[n].replace('Less',''))
        print("---------------------------------------------------------")
            
if __name__ == "__main__":
    if len(sys.argv) == 4:
        content = sys.argv[1]
        abs_state = sys.argv[2]     # abstract state- either show or hide
        sort_results = sys.argv[3]
        if sort_results == "new":
           sort_results = "-submitted_date"
        elif sort_results == "old":
            sort_results = "submitted_date"
        page = 0
        page_history = []
        print("-------------------------------------------------------------------->>")
        print("                             WELCOME TO ARXIV SCRAPING PYTHON for personal purposes only, by Shivaji Chaulagain")
        print("-------------------------------------------------------------------->>")
    
 
        while True:
            print(f"                                     Page_number = {page+1}")
            links, title = arxiv(content,abs_state,sort_results,page).scrape()
            print("\n")
            link_choice = input("Enter the number of the link you want to visit or 'a' for 'Abstract', or 'n' for the next page, 'b' for the previous page  or 'e' for exit: ")
            if link_choice.isdigit() and int(link_choice) <= len(links):
                  webbrowser.open_new_tab(links[int(link_choice)-1])                 
            elif link_choice.lower() == 'a':
                  choice = int(input("Enter the number of the title which you want to see abstract of: "))
                  arxiv(content, abs_state, sort_results, page).abstract(choice) 
                  ask = input("Do you wanna open the pdf in browser or download it or continue further? 'y' for yes or 'd' for download or 'c' for continue:")
                  if ask == "d":  
                      file_name = title[choice-1][:20]            
                      file_na = open(f"{file_name}.pdf","wb")
                      print("Downloading............................")
                      file_na.write(requests.get(links[choice-1]).content)
                  
                      file_na.close()
                  elif ask == "y":
                      webbrowser.open_new_tab(links[choice-1])
                  elif ask == "c":
                      continue
            elif link_choice.lower() == 's':
                 pass
               
            elif link_choice.lower() == 'n':
                  page_history.append(page)
                  page += 1
            elif link_choice.lower() == 'b':
                if page_history:
                        page = page_history.pop()
                else:
                   print("You are already on the first page.")
            elif link_choice.lower() == 'e':
                  sys.exit(1)
            else:
                print("Invalid input. Please enter a valid number, 'n' for the next page, or 'b' for the previous page.")
            if os.name == "nt":
                os.system('cls')
            else:
                os.system('clear')
            
    else:
        print("Please provide a search query.")
        

      
    
        
