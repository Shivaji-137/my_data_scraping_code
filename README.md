# my_data_scraping_code

I have written a code to search a paper in terminal from journal in Arxiv and google scholars using Beautifulsoup in python.
It can search a paper, show it in terminal with title, catalog, date, show abstract of the title and even you can browser it or can even directly download the paper into your computer without going to the browser, alll from terminal.

It only runs from linux terminal and command prompt.

To run arxiv_scrape.py,

Use: 

python arxiv_scrape.py arg1 arg2 arg3

Here arg1 takes title content you want to search for. For single world, pass title_name as arg1 but for multiple words use pass "title_name".
Here arg2 takes abstract state. Abstract state is either show or hide. 

Here arg3 takes either old or new paper. so pass either old or new

Note: arxiv_scrape.py should be in current working directory. If not, specifies full path

for example:

python arxiv_scrape.py "Gravitational wave" show new

===> It searches latest new paper on Gravitational wave in arxiv with abstract state show
