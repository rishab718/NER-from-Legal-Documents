
import os
import fitz
import spacy
import time
from spacy import displacy
from flask import Flask, render_template,request,request,redirect,flash
from werkzeug.utils import secure_filename
from flaskext.markdown import Markdown
import pickle


#nlp_model10 = spacy.load('C:/users/RISHAB/nlp_model10')
nlp_model10=pickle.load(open('ner_model.pkl','rb'))
app1 = Flask(__name__)
Markdown(app1)

UPLOAD_FOLDER = 'E:/uploads/'
app1.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app1.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
@app1.route("/")
def h():
    return render_template('index.html')

global oname
@app1.route('/upload',methods=["GET", "POST"])
def upload():
    
    if request.method=="POST":
        file=request.files["file"]
        file_name=file.filename
        print(file_name)
        filename=secure_filename(file_name)
        file.save(os.path.join(app1.config['UPLOAD_FOLDER'], file_name))
        x=time.strftime("%Y%m_%M%S")
        global oname
        oname="output"+x+".pdf"
        os.rename(r'E:\\uploads\\'+file_name,r'E:\\uploads\\'+oname)
        
        return render_template('id.html') 
 
    return render_template('id.html')





 
@app1.route("/showentities",methods=["GET", "POST"])
def showentities():
    fname = 'E:/uploads/'+oname
    doc= fitz.open(fname)
    letter=""
    for page in doc:
        letter = letter + str(page.getText())
    m=" ".join(letter.split())
    doc1 = nlp_model10(m)
    x=[]
    for ent in doc1.ents:
        y=f'{ent.label_.upper()} - {ent.text.upper()} '
        if y in x:
            continue
        else:
            x.append(y)
    
    colors={'execution_date':"linear-gradient(90deg, #aa9cfc, #fc9ce7)",'company_name':"radial-gradient(white,red)","emp_name":'#FFC0CB','job_role':"radial-gradient( white, orange )",'effective_date':"radial-gradient(blue, white)","salary":"radial-gradient(#ADFF2F,white)",'term_period':"linear-gradient(to bottom, #33ccff 0%, #ff99cc 100%)",'bonus':"linear-gradient(  yellow, green)","hours_of_work":"#00FFFF"}

    options={"ents":["execution_date","company_name","emp_name","job_role","salary","bonus","term_period","hours_of_work","effective_date"],"colors":colors}
    html=displacy.render(doc1,style='ent',options=options)
    result=html
    return render_template('res.html',x=x,result=result)    

 


if __name__ =="__main__":
    app1.run(debug=True)    

