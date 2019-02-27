# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 13:15:33 2019

@author: vrinda
"""

from Bio import Entrez
from bokeh.plotting import figure
from bokeh.io import output_file, show
def generate_chart(startyear,endyear,disease):
    mydict ={}
    years = (range(endyear, startyear, -1))  # Creates a list from given range
    Entrez.email = "Example@mail.org"
    for year in years:
        
        # Go through the list 'years' and assign the value to the variable 'year'
        handle = Entrez.esearch(db ="pubmed", term= disease,
                         mindate=year, maxdate=year)
        record = Entrez.read(handle)
        
        mydict.update( {year :record["Count"] } )
#print (mydict)  


    lists = sorted(mydict.items()) # sorted by key, return a list of tuples

    x, y = zip(*lists) # unpack a list of pairs into two tuples
    for_xaxis = [i for i in x]
    for_yaxis = [j for j in y]
    #prepare the output file
   # output_file("Line.html")

    p = figure(plot_width=400, plot_height=400)

# add a line renderer
    p.line(for_xaxis, for_yaxis, line_width=2)

    show(p)



