#include <iostream>
#include <cmath>
#include <vector>
#include <queue>
#include <stack>
#include <string>
#include <pybind11/pybind11.h>
#include <map>

namespace py = pybind11;
using namespace std;
class Evaluate{
     private:
        float revenue;
        float gross_profit;
        float business_profit;

    public:
        float gross_margin_result(float revenue, float gross_profit, int billion_sample){
            revenue = float(revenue/billion_sample);
            gross_profit = float(gross_profit/billion_sample);
            float margin = round(revenue)/round(gross_profit);
            return round(float(margin * 100));
        }
        float operating_profit_result(float business_profit, float revenue,  int billion_sample){
            revenue = float(revenue/billion_sample);
            business_profit = float(business_profit/billion_sample);
            float margin = revenue/round(business_profit);
            return round(float(margin * 100));
        }


        vector<float> input_data(float result){
            vector<float> data;
            data.push_back(
                result
            );
            return data;
        }

        vector<float> result_data(vector<float> result){
            for (float data : result){
                cout<<data;
            }
        }
        map <int, float> dict_result(vector<float> data){
            float gmr = 0;
            float opr = 0;
            float bp = 0;
            for (float obj: data){
                gmr = data[0];
                opr = data[1];
                bp = data[2];
            }
            
        }
        
        
    Evaluate(): revenue(0), gross_profit(0), business_profit(0) {};
};





   
PYBIND11_MODULE(evaluate_module, m){
    py::class_<Evaluate>(m, "Evaluate").def(py::init<>())
    .def("gross_margin_result", &Evaluate::gross_margin_result,"caculate gross margin result")
    .def("operating_profit_result", &Evaluate::operating_profit_result,"caculate operating profit result");
}


int main(){
    return 0;
}