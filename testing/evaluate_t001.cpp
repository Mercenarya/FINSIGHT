#include <iostream>
#include <vector>
#include <string>

using namespace std;

const int sample = 1000000000;
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
float net_profit(float revenue, float net_income, float billion_sample){
    revenue = float(revenue/billion_sample);
    net_income = float(net_income/billion_sample);
    float net_pft = net_income/revenue;
    return float(net_pft*100);
    
}

// lơi nhuận ROA
float ROA_profit(float revenue, float share, float billion_sample){
    revenue = float(revenue/billion_sample);
    share = float(share/billion_sample);
    float roa_pft = share/revenue;
    return float(roa_pft*100);
}

// chỉ số tăng trưởng doanh thu
float increase_revenue(float pre_rv, float current_rv, float billion_sample){
    pre_rv = float(pre_rv/billion_sample);
    current_rv = float(current_rv/billion_sample);
    float inc_rev = (current_rv-pre_rv)/pre_rv;
    return float(inc_rev*100);
}

// chi phí tài chính doanh thu
float finance_cost(float revenue, float cost , float billion_sample){
    revenue = float(revenue/billion_sample);
    cost = float(cost/billion_sample);
    float fn_cost = cost/revenue;
    return float(fn_cost*100);
}
float current_ratio(float currentassets, float liabilities){

    try
    {
        currentassets = float(currentassets/sample);
        liabilities = float(liabilities/sample);
        float ratio_result = currentassets / liabilities;
        return float(ratio_result*100);
    }
    catch(const std::exception& e)
    {
        std::cerr <<"current ratio : " <<e.what() << '\n';
    }
    
}
float quick_ratio(float currentassets, float inventory, float liabilities){
    try
    {
        currentassets = float(currentassets/sample);
        liabilities = float(liabilities/sample);
        inventory = float(inventory/sample);
        float quick_ratio_result = (currentassets-inventory)/liabilities;
        return float(quick_ratio_result*100);

    }
    catch(const std::exception& e)
    {
        std::cerr <<"quick ratio : "<< e.what() << '\n';
    }
    
}

float cash_ratio(float cash, float liabilities){
    try
    {
        cash = float(cash/sample);
        liabilities = float(liabilities/sample);
        float cash_ratỉo_result = cash / liabilities;
        return float(cash_ratỉo_result*100);
    }
    catch(const std::exception& e)
    {
        std::cerr << e.what() << '\n';
    }
    
}


int main(){
    
    float ev = 0;
    float gr = 0;
    float revenue = 27245717878312;
    float gross_profit = -2818409788534;
    int sample = 1000000000;

    ev = gross_margin_result(revenue,gross_profit,sample);
    cout<<ev;
    
    
}
