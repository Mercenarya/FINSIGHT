#include <iostream>
#include <cmath>
#include <vector>
#include <queue>
#include <stack>
#include <string>
#include <pybind11/pybind11.h>
#include <map>

// parameter
namespace py = pybind11;
using namespace std;

class Profitability{
    private:
        float revenue; 
        int billion_sample;

    public:
        // tỉ suất lợi nhuận gộp
        float gross_margin_result(float revenue, float gross_profit, int billion_sample){
            revenue = float(revenue/billion_sample);
            gross_profit = float(gross_profit/billion_sample);
            float margin = gross_profit / revenue;
            return float(margin * 100);
        }
        // tỉ suất lợi nhuận hoạt động kinh doanh
        float operating_profit_result(float business_profit, float revenue,  int billion_sample){
            revenue = float(revenue/billion_sample);
            business_profit = float(business_profit/billion_sample);
            float margin = business_profit/revenue;
            return float(margin * 100);
        }
        // ROS ( Tỉ suất lợi nhuận ròng )
        float ros_result(float revenue, float profit_atm, int billion_sample ){
            revenue = float(revenue/billion_sample);
            profit_atm = float(profit_atm/billion_sample);
            float margin = profit_atm / revenue;
            return float(margin*100);
        }

        // biên lợi nhuận ròng
        float net_profit(float revenue, float net_income, int billion_sample){
            revenue = float(revenue/billion_sample);
            net_income = float(net_income/billion_sample);
            float net_pft = net_income/revenue;
            return float(net_pft*100);
            
        }

        // lơi nhuận ROA
        float roa_profit(float revenue, float share, int billion_sample){
            revenue = float(revenue/billion_sample);
            share = float(share/billion_sample);
            float roa_pft = share/revenue;
            return float(roa_pft*100);
        }

        // chỉ số tăng trưởng doanh thu
        float increase_revenue(float pre_rv, float current_rv, int billion_sample){
            pre_rv = float(pre_rv/billion_sample);
            current_rv = float(current_rv/billion_sample);
            float inc_rev = (current_rv-pre_rv)/pre_rv;
            return float(inc_rev*100);
        }

        // chi phí tài chính doanh thu
        float finance_cost(float revenue, float cost , int billion_sample){
            revenue = float(revenue/billion_sample);
            cost = float(cost/billion_sample);
            float fn_cost = cost/revenue;
            return float(fn_cost*100);
        }
        
        
    Profitability(): revenue(0), billion_sample(0) {};
};

// chuyển đổi sang thư viện assets python
PYBIND11_MODULE(evaluate_module, m){
    py::class_<Profitability>(m, "Profitability").def(py::init<>())
    .def("gross_margin_result", &Profitability::gross_margin_result,"caculate gross margin result")
    .def("operating_profit_result", &Profitability::operating_profit_result,"caculate operating profit result")
    .def("ros_result", &Profitability::ros_result,"Calculating ROS profit")
    .def("net_profit", &Profitability::net_profit,"Recieve Net Profit")
    .def("roa_profit", &Profitability::roa_profit,"Recieve ROA")
    .def("increase_revenue", &Profitability::increase_revenue,"increased revenue")
    .def("finance_cost", &Profitability::finance_cost, "get finance & revenue cost");

    // .def("input_data", &Evaluate::input_data,"input all elements");
}


int main(){
    return 0;
}