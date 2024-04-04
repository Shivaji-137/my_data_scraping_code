try:
    import requests
    import os
    from bs4 import BeautifulSoup as bs
    import webbrowser
    import sys
    import pandas as pd
except ImportError as e:
    print(f"Required module {e.name} not found. You can install it using 'pip install {e.name}'.")

def contents(content, time, pages=0):
    """you can rename this file as url.py for simplicity
    use this command: python3 url.py* your_query. 
    for example:
    python3 url.py fast fourier transform
    *assuming you have renamed this file as url.py"""
    links = []
    title = []
    cite = []
    free_con = []
    lin = []
    date = []
    start = pages * 10
    #url = "https://scholar.google.com/scholar?q=%22precipitable+water+vapor%22&hl=en&as_sdt=0%2C5&as_ylo=2020&as_yhi=2020"
    #https://scholar.google.com/scholar?q=gravitational+waves&hl=en&as_sdt=0%2C5&as_ylo=2019&as_yhi=2019
    if time != "all":
        url = f"https://scholar.google.com/scholar?start={start}&q={content}&hl=en&as_sdt=0,5&as_ylo={int(time)}&as_yhi={int(time)}"
        r = requests.get(url)
    elif time == "all":
        r = requests.get(f"https://scholar.google.com/scholar?hl=en&start={start}&as_sdt=0,5&q={content}")
    soup = bs(r.content, "lxml")
    for div in soup.find_all("h3", class_="gs_rt"):
        for j in div.find_all("a"):
            title.append(j.getText())
            links.append(j.get("href"))
    for link in soup.find_all('a'):
        if link.find(string=lambda text: text and text.startswith('Cited by')):
            cite.append(link.get_text().replace("Cited by", ""))
    for div in soup.find_all("div", class_="gs_r gs_or gs_scl"):
        free_co = div.find('span').getText()
        if 'Save' in free_co:
            free_con.append(free_co.replace('Save', 'Non free'))
        elif '[' and ']' in free_co:
            free_con.append(free_co.strip('[]'))
        lin.append(div.find('a').get('href'))
    
    for div in soup.find_all("div", class_="gs_a"):
        free_co = div.getText()
        date.append(free_co.rsplit('-')[1].rsplit(',')[-1])
    result = list(zip(title, cite, date, free_con))
    col = ["Title", "Number_of_citation", "Published Date", "Available(Free or not)"]
    res = pd.DataFrame(result, columns=col)
    print(res)#.sort_values(by="Published Date", ascending=False))
    return links, title, cite, free_con, lin, date
 
if __name__ == "__main__":
    if len(sys.argv) == 3:
        query = sys.argv[1]
        queries = query.replace(' ','+')
        time = sys.argv[2]
        page = 0
        page_history = []
        print("WELCOME TO GOOGLE SCHOLARS SCRAPING PYTHON for personal purposes only, by Shivaji Chaulagain")
        print("-------------------------------------------------------------------->>")
        while True:
            links, titles, cite, free_con, lin, date = contents(queries,time, page)
            print("\n")
            # title_choice = input("Enter the number of the link you want to see full title: ")
            # if title_choice.isdigit() and int(title_choice) <= len(title_choice):
            #     print(titles[int(title_choice)])
            #     print("---------------------------------------------------------------")
            # print("Do you want to continue looking articles of any time? or Enter specific year of the article:y/s")
            # specific_year = input("Do you want to continue looking articles of any time? or Enter specific year of the article(y/s): ")
            # if specific_year == 's':
            #     year = input("Then enter which year?: ")
            #     links, titles, cite, free_con, lin, date = contents(query, lower=int(year), page)
            link_choice = input("Enter the number of the link you want to see full title, 'n' for the next page, or 'b' for the previous page: or 'e' for the exit:  ")
            if link_choice.isdigit() and int(link_choice) <= len(links):
                  print("-------------------------------------------------------------------------")
                  print(f"Title of number {link_choice}: | ", end=" ")
                  print(f"'{titles[int(link_choice)]}'")
                  print("------------------------------------------------------------------------")
                  print(f"Number of citation: {cite[int(link_choice)]}, Published Date: {date[int(link_choice)]}, Available: {free_con[int(link_choice)]}")
                  print("---------------------------------------------------------------------")
                  continue_ = input("Enter 'y' for visiting that title link in website or 'd' for downloading that title for only the pdf format, not html in your pc or 'c' for continue searching in terminal: ")
                  if continue_ == 'y':
                    print("Opening in browser .......")
                    webbrowser.open_new_tab(links[int(link_choice)])
                  elif continue_ == 'd':
                      with open(f"{titles[int(link_choice)]}.pdf", 'wb') as f:
                          content = requests.get(f'{lin[int(link_choice)]}').content
                          f.write(content)
                      print("Downloading completed!")
                      if os.name == "nt":
                          os.system('cls')
                      else:
                          os.system('clear')
                  elif continue_ == 'c':
                      if os.name == "nt":
                          os.system('cls')
                      else:
                          os.system('clear')
                      continue
                  
            elif link_choice.lower() == 'n':
                  if os.name == "nt":
                     os.system('cls')
                  else:
                     os.system('clear')
                  page_history.append(page)
                  page += 1
                  print(f"                                                 Page:{page+1}")
                  print("\n")
            elif link_choice.lower() == 'b':
                if os.name == "nt":
                   os.system('cls')
                else:
                   os.system('clear')
                if page_history:
                        page = page_history.pop()
                else:
                   print("You are already on the first page.")
                print(f"                                                   page: {page+1}")
            elif link_choice.lower() == 'e':
                 sys.exit(1)
    
            else:
                print("Invalid input. Please enter a valid number, 'n' for the next page, or 'b' for the previous page.")
                if os.name == "nt":
                   os.system('cls')
                else:
                   os.system('clear')
    elif sys.argv[1] == "help":
        docstring = """ A journal scraping code from google scholar only by Shivaji Chaulagain.
         ---------------------------------------------------------------------------------------------------------------
It can search a paper, show it in terminal with title, published date and citation and even you can browser it or can even directly download the paper (if only pdf is available) into your computer without going to the browser, alll from terminal.

It only runs from linux terminal and command prompt in windows. For better visualization, please maximize your terminal.
-------------------------------------------------------------------------------------------------------------------------------
To run scholar_scrape.py,
-------------------------------------------------------------------
Use:
-------------------------------------------------------------------
python scholar_scrape.py arg1 arg2 
------------------------------------------------------------------------------------------------------
Here arg1 takes title content you want to search for. For single world, pass title_name as arg1 but for multiple words(inside double quotes) use "title_name". Here arg2 takes time. In arg2, pass 'all' for any time or pass year_number for specific year

Note: scholar_scrape.py should be in current working directory. If not, specifies full path

for example:
---------------------------------------------------------
python scholar_scrape.py "Gravitational wave" 2024      # for 2024 year
python scholar_scrape.py "Gravitational wave" all       # for any time
----------------------------------------------------------
===> It searches latest new paper on Gravitational wave in arxiv with abstract state show """
        print(docstring)
    else:
        print("Please provide a search query.")
        print("For help, Enter a command: python scholar_scrape.py help")

