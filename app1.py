# import the necessary packages
from flask import Flask, render_template, request
from bokeh.embed import components
from bokeh.resources import CDN 
from Bio import Entrez
from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.embed import file_html
# mapping URLs to code
app=Flask(__name__)

@app.route('/')

def home(): #function to return home screen
    return render_template("home.html")

@app.route('/about/') #function to return home screen
def about():
    return render_template("about.html")
@app.route("/")
def index(): 
    return render_template("index.html")
@app.route("/chartgeneration", methods=['POST'])
def generate_chart(): #function to generate a bar plot
    startyear = int(request.form["startyear"])
    endyear = int(request.form["endyear"])   
    disease = request.form["disease"]
    charttype = request.form.get("charttype")
    if startyear >= endyear :
      return render_template("error.html") 
    else:
        mydict ={}
        years = (range(endyear, startyear, -1))  # Creates a list from given range
        Entrez.email = "Example@mail.org"
        for year in years:
            # Go through the list 'years' and assign the value to the variable 'year'
            handle = Entrez.esearch(db ="pubmed", term= disease,
                         mindate=year, maxdate=year)
            record = Entrez.read(handle)
            mydict.update( {year :int(record["Count"]) } )

        lists = sorted(mydict.items()) # sorted by key, return a list of tuples

        x, y = zip(*lists) # unpack a list of pairs into two tuples
        if all([ v == 0 for v in y ]) :# checking if the term doesnt exist.
            return render_template("nil.html") 
    #prepare the output file
    output_file("Line.html")

    p = figure(plot_width=400, plot_height=400,title="PubMed citations")
    p.xaxis.axis_label = 'Years'
    p.yaxis.axis_label = 'Disease/disease prone area'
# BAR PLOT
    if charttype == "barplot":
        p.vbar(x=x, top=y,width=0.5)
        p.xgrid.grid_line_color = None
        p.y_range.start = 0
        p.xaxis.axis_label = 'Years'
        p.yaxis.axis_label = 'Disease'
        #show(p)
        html = file_html(p, CDN, "my plot")
        return html
# lINE PLOT
      
    elif charttype == "line":
        for_xaxis = [i for i in x]
        for_yaxis = [j for j in y]
        p.line(for_xaxis, for_yaxis, line_width=2)
        html = file_html(p, CDN, "my plot")
        return html
#SCATTER PLOT
    else:
        for_xaxis = [i for i in x]
        for_yaxis = [j for j in y]
        p.circle(for_xaxis,for_yaxis, size=20, color="navy", alpha=0.5)
        html = file_html(p, CDN, "my plot")
        return html

    
if __name__ == '__main__':
    app.debug = True
    app.run()
