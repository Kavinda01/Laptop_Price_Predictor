from flask import Flask, render_template, request
import pickle
import numpy as np

# setup application
app = Flask(__name__)

def prediction(lst):
    filename = 'model/laptop_prices_model.pickle'
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    pred_value = model.predict([lst])
    return pred_value

@app.route('/', methods=['POST', 'GET'])
def index():
    # return "Hello World"
    pred_value = 0
    if request.method == 'POST':
        ram = request.form['ram']
        hdd = request.form['hdd']
        ssd = request.form['ssd']
        weight = request.form['weight']
        company = request.form['company']
        typename = request.form['typename']
        opsys = request.form['opsys']
        cpu = request.form['cpuname']
        gpu = request.form['gpuname']
        ppi = request.form['ppi']
        touchscreen = request.form.getlist('touchscreen')
        ips = request.form.getlist('ips')
        
        feature_list = []

        feature_list.append(int(ram))
        feature_list.append(int(hdd))
        feature_list.append(int(ssd))
        feature_list.append(float(weight))
        feature_list.append(float(ppi))
        feature_list.append(len(touchscreen))
        feature_list.append(len(ips))

        company_list = ['acer','apple','asus','dell','hp','lenovo','msi','other']
        typename_list = ['2in1convertible','gaming','netbook','notebook','ultrabook']
        opsys_list = ['mac','windows']
        cpu_list = ['amd','intelcorei3','intelcorei5','intelcorei7']
        gpu_list = ['amd','intel']

        # for item in company_list:
        #     if item == company:
        #         feature_list.append(1)
        #     else:
        #         feature_list.append(0)

        def traverse_list(lst, value):
            for item in lst:
                if item == value:
                    feature_list.append(1)
                else:
                    feature_list.append(0)
        
        traverse_list(company_list, company)
        traverse_list(typename_list, typename)
        traverse_list(opsys_list, opsys)
        traverse_list(cpu_list, cpu)
        traverse_list(gpu_list, gpu)

        pred_value = prediction(feature_list)*38800
        pred_value = np.round(pred_value[0],2)

    return render_template('index.html', pred_value=pred_value)


if __name__ == '__main__':
    app.run(debug=True)