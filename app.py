from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import gzip

app = Flask(__name__)
model = pickle.load(gzip.open("Model.pkl", "rb"))


@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")


@app.route("/predict", methods=["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":

        
        # Age -------------------------------------------------------------------------------

        age = request.form['Age']

        if (age == '0-20'):
            age = 20

        elif (age == '21-30'):
            age = 30

        elif (age == '31-40'):
            age = 40

        elif (age == '41-50'):
            age = 50

        elif (age == '51-60'):
            age = 60

        elif (age == '61-70'):
            age = 70

        elif (age == '71-80'):
            age = 80

        elif (age == '81-100'):
            age = 100
            
   
        # Department ---------------------------------------------------------------------------------------

        d = request.form['Department']
        
        d_anesthesia = d_gynecology = d_radiotherapy = d_surgery = 0

        if(d == 'anesthesia'):
            d_anesthesia = 1
           
        elif(d == 'gynecology'):
            d_gynecology = 1

        elif(d == 'radiotherapy'):
            d_radiotherapy = 1

        elif(d == 'surgery'):
            d_surgery = 1


        # Type of Admission ----------------------------------------------------------------------------------

        ta = request.form['Type_of_Admission']
        
        if (ta == 'Trauma'):
            ta = 1

        elif (ta == 'Urgent'):
            ta = 2

        elif (ta == 'Emergency'):
            ta = 3


        # Severity of Illness -------------------------------------------------------------------------------

        si = request.form['Severity_of_Illness']

        if (si == 'Minor'):
            si = 1

        elif (si == 'Moderate'):
            si = 2

        elif (si == 'Extreme'):
            si = 3


        # Ward type ------------------------------------------------------------------------------------------

        wt = request.form['Ward_Type']
        
        wt_Q = wt_R = wt_S = wt_T = wt_U = 0

        if(wt == 'Q'):
            wt_Q = 1

        elif(wt == 'R'):
            wt_R = 1

        elif(wt == 'S'):
            wt_S = 1         

        elif(wt == 'T'):
            wt_T = 1

        elif(wt == 'U'):
            wt_U = 1



        # Bed Grade --------------------------------------------------------------------------------
        
        bg = request.form['Bed_Grade']

        bg_2 =  bg_3 = bg_4 = 0
        
        if(bg == '2'):
            bg_2 = 1

        elif(bg == '3'):
            bg_3 = 1

        elif(bg == '4'):
            bg_4 = 1



        # Numerical Columns ------------------------------------------------------------------------------

        Available_Extra_Rooms  =  int(request.form["Available_Extra_Rooms"])
        Visitors_with_Patient  =  int(request.form["Visitors_with_Patient"])
        Admission_Deposit      =  int(request.form["Admission_Deposit"])


        # Prediction -------------------------------------------------------------------------------------

        prediction = model.predict([[
                                        Available_Extra_Rooms,
                                        ta,
                                        si,
                                        Visitors_with_Patient,
                                        Admission_Deposit,
                                        age,                           
                                        d_anesthesia  ,  d_gynecology  ,  d_radiotherapy  ,  d_surgery,
                                        wt_Q , wt_R , wt_S , wt_T , wt_U,
                                        bg_2 , bg_3 , bg_4
                                    ]])
    
    
        if (prediction==1):
            output = '0-10'
        elif (prediction==2):
            output = '11-20'
        elif (prediction==3):
            output = '21-30'
        elif (prediction==4):
            output = '31-40'
        elif (prediction==5):
            output = '41-50'
        elif (prediction==6):
            output = '51-60'
        elif (prediction==7):
            output = '60+'
            
        return render_template('result.html', prediction_text="LOS = {} days".format(output))

    return render_template("result.html")


if __name__ == "__main__":
    app.run(debug=True)
