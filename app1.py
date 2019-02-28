# import the necessary packages
from flask import Flask, render_template, request
from generate_chart import generate_chart
from bokeh.embed import components
from bokeh.resources import CDN 
from Bio import Entrez
from bokeh.plotting import figure
from bokeh.io import output_file, show
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
    if startyear == endyear :
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
    #prepare the output file
    output_file("Line.html")

    p = figure(plot_width=400, plot_height=400,title="PubMed citations")

# add a line renderer
    p.vbar(x=x, top=y,width=0.5)
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    show(p)
    return render_template("Line.html")
if __name__ == '__main__':
    app.debug = True
    app.run()
