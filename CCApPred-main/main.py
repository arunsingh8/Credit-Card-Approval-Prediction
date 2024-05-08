from flask import Flask, request, render_template
import joblib
import numpy as np

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("CCAP form.html")

@app.route('/predict', methods=['POST'])
def predict():
    model = joblib.load('models/CCApPred.pkl')
    global f
    global l
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    gender = int(request.form["gender"])
    age = float(request.form["age"])
    maritalstatus = int(request.form["maritalstatus"])
    education = int(request.form["education"])
    incometype = int(request.form["incometype"])
    occupation = int(request.form["occupation"])
    employment = int(request.form["employement"])
    income = float(request.form["income"])
    property = int(request.form["property"])
    housingtype = int(request.form["housingtype"])
    car = int(request.form["car"])
    creditscore = int(request.form["creditscore"])
    f = firstname.upper()
    l = lastname.upper()
    features = [
        [gender, car, property, income, incometype, education, maritalstatus, housingtype, occupation, age, employment]]
    x = np.array(features)
    prediction = model.predict(x)
    def pred(predic):
        global stat
        status3 = ""
        status1 = ""
        status2 = ""
        if income==0 or incometype==3:
            status4="Sorry!\nWe regret to inform you that, after consideration of your credit history and final circumstances\n, our system has determined that you are not eligible for credit card this time.This may be because your income is zero or you are a student.\n Please understand that this decision does not reflect your character or worth as an individual.\n We encourage you to continue to work  on improving  your credit score and financial situation,\n as this may increase your chance of being eligible in future."
        elif predic == 1 and creditscore >= 750:
            if 18 <= age < 21:
                status2 = "but your age is between 18 to 21 years therefore, you are eligible for the credit card for the banks with minimum age criteria 18"
            status1 = "Congratulations!\n \tWe are pleased to inform you that you are eligible for the credit card.\n" + status2 + " \nBased on the details of your credit score and financial circumstances provided by you,\nour system has determined that you are eligible for credit card,we believe that \n credit card is a valuable financial tool and you will use it responsibly.\n As a responsible lender banks expect their card holder to use their card in a responsible manner.\nThis means making timely payments on your credit balance limit.Failure to do so\n could result in additional fees,interest charges,and damage to your credit score."
        elif predic == 1 and (680 < creditscore < 750):
            if 18 <= age < 21:
                status2 = "and your age is between 18 to 21 years you are eligible for the credit card for the banks with minimum age criteria 18 "
            status1 = "Congratulations!<br> \t We are pleased to inform you that you are eligible for credit card\n but your credit score lies in good category, therefore banks may reject your application.\n" + status2 + "\n Our system has determined that you are eligible for the credit card based on the other financial\n circumstances provided by you.We believe that \n credit card is a valuable financial tool and you will use it responsibly.\n As a responsible lender banks expect their card holder to use their card in a responsible manner.\nThis means making timely payments on your credit balance limit.Failure to do so\n could result in additional fees,interest charges,and damage to your credit score."
        else:
            status3 = "Sorry!\nWe regret to inform you that, after consideration of your credit history and final circumstances\n, our system has determined that you are not eligible for credit card this time.\n Please understand that this decision does not reflect your character or worth as an individual.\n We encourage you to continue to work  on improving  your credit score and financial situation,\n as this may increase your chance of being eligible in future"
        stat=status1+status2+status3+status4
    pred(prediction[0])

    return render_template("predict.html", prediction_result=stat)


if __name__ == "__main__":
    app.run(debug=True)