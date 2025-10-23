#include <iostream>
#include <cmath>
#include <vector>
#include <queue>
#include <stack>
#include <string>
#include <pybind11/pybind11.h>
// #include "liquidity.h"

// parameter
namespace py = pybind11;
using namespace std;

typedef long long SAMPLE;// đơn vị chuẩn : 1,000,000,000
typedef double RATIOS;// tỷ suất
typedef double MARGIN;// biên 
typedef vector<double> DATA;// quy chuẩn kiểu dữ liệu cho luồng dữ liệu 

// đơn vị mẫu
const SAMPLE sample = 1'000'000'000;

/*
    float revenue; 
    float gross_profit;
    float business_profit;
    float profit_atm;
    float net_income;
    float share;
*/


// khởi tạo datasheet 
struct datasheet{
    long long GP; // gross profit (lợi nhuận gộp)
    long long RV; // revenue (doanh thu thuần)
    long long NI; // Net income (lợi nhuận ròng)
    long long SEQ; // Shareholder enquity 
    long long TTA; // total assets (tài sản)
    long long BSNP; // business profit (lơi nhuận hoạt động EBIT)
    long long BATMP; // lợi nhuận sau thuế
};

/* Trưng dụng hàm */
void extract_data(){};
void merge_vct(){};
vector<double> ratio_vt(){};
vector<double> margin_vt(){};

class Profitability {
    public:
        /* Constructor cho Class*/
        Profitability() = default;
        
        /*Xây dựng hàm tính toán tỉ suất*/
        template <typename T>
        MARGIN gross_profit_margin(T GP, T RV){
            try{
                if(RV == 0){
                    if (GP > 0){
                        throw std::invalid_argument("Revenue (RV) is none, undefined Gross margin");
                        return 1.0f;
                    }
                    return 0.0f;
                }
                // xử lí ép kiểu dữ liệu từ long long --> double
                GP = static_cast<double>(GP);
                RV = static_cast<double>(RV);

                // xử lí kết quả biên lợi nhuận
                double margin = static_cast<double>(GP)/RV ;
                return margin* 100;
            }catch(const std::exception& e){
                std::cerr << e.what() << '\n';
            }
            

        }


        template<typename T>
        MARGIN opm_margin(T BSNP, T RV){
            try{
                if(RV == 0){if (BSNP > 0){
                    throw std::invalid_argument("Revenue (RV) is none, undefined Business net profit ");
                        return 1.0f;
                    }
                    return 0.0f;
                }
                // xử lí ép kiểu dữ liệu long long --> double
                BSNP = static_cast<double>(BSNP);
                RV = static_cast<double>(RV);

                //xử lí kết quả biên lợi nhuận
                double margin = static_cast<double>(BSNP) / RV;
                return margin*100;
            }catch(const std::exception& e){
                std::cerr << e.what() << '\n';
            }
        
            
        }
        

        template <typename T>
        MARGIN npm_margin(T BATMP, T RV ){
            try{
                if( RV == 0){
                    if(BATMP > 0){
                        throw std::invalid_argument("Revenue (RV) is none, undefined Net income");
                        return 1.0f;
                 
                    }
                    return 0.0f;
                }
                
                //xử lí ép kiểu dữ liệu long long --> double
                BATMP = static_cast<double>(BATMP);
                RV = static_cast<double>(RV);

                // xử lí kết quả biên lợi nhuận
                double margin = static_cast<double>(BATMP) / RV;
                return margin*100;
            }catch(const std::exception& e){
                std::cerr << e.what() << '\n';
            }
            
        }
         /*
        Module thiết kế tính tỷ suất (ratios)
        - tỉ suất sinh lời trên tài sản ()
        - tỉ suất sinh lời trên vốn sở hữu
        */

        // tỉ suất ROA 
        template<typename T>
        RATIOS roa_ratios(T TTA, T NI){
            try
            {
                if(TTA == 0){
                    if(NI > 0){
                        throw std::invalid_argument("Total assest is none, Net income is undefined");
                        return 1.0f;
                    }
                    return 0.0f;
                }
                TTA = static_cast<double>(TTA);
                NI = static_cast<double>(NI);

                double ratios = static_cast<double>(NI) / TTA;
                return ratios * 100;
                
            }
            catch(const std::exception& e)
            {
            

                std::cerr << e.what() << '\n';
            }
            
        }


        // tỉ suất ROE
        template<typename T>
        RATIOS roe_ratios(T ATE ,T NI){
            try
            {
                if(ATE==0){
                    if(NI > 0){
                        throw std::invalid_argument("After-tax Equity is none, net income is undefined");
                        return 1.0f;
                    }
                    return 0.0f;
                }

                ATE = static_cast<double>(ATE);
                NI = static_cast<double>(NI);

                double ratios = static_cast<double>(NI) / ATE;
                return ratios * 100;


            }
            catch(const std::exception& e)
            {
                std::cerr << e.what() << '\n';
            }
            
        }

        // Thu nhập trên mỗi cổ phần
        template<typename T>
        RATIOS eps_ratios(T NI, T PD, T ASO){
            try{
                
                NI = static_cast<double>(NI);// net income
                PD = static_cast<double>(PD);// Preffered Dividend
                ASO = static_cast<double>(ASO);// Average shares outstanding

                double ratios = static_cast<double>((NI)-PD) / ASO;
                return ratios

            }
            catch(const std::exception& e)
            {
                std::cerr << e.what() << '\n';
            }
            
        }

};




// extract result of current ratio to absolute vector
template<typename T>
vector<double> margin_vt(vector<T> &x, vector<T> &y){
    vector<double> result;
    MARGIN margin = 0;
    if(x.size() != y.size()){
        throw std::invalid_argument("Assets and liabilities must be same length");
    }
    /*
    Vì 2 luồng vector dữ liệu là 2 luồng vector
    vốn dĩ là cùng kích thướng nên ta chỉ cần
    sử dụng 1 vector làm mẫu 
    */
   // x[value].y[value] là vị trí giá trị để lấy giá trị đó vào result
    for(int value = 0; value < x.size(); value ++){
        // đẩy các giá trị vào result
        margin = Profitability().gross_profit_margin(x[value],y[value]);
        result.push_back(margin);
    }
    return result;
};

// extract result
template<typename T>
void extract_data( vector<T> &data){
    for(auto value : data){
        cout<<value<<",";
    }

};


// chuyển đổi sang thư viện assets python
// PYBIND11_MODULE(evaluate_module, m){
//     py::class_<Profitability>(m, "Profitability").def(py::init<>())
//     .def("gross_margin_result", &Profitability::gross_margin_result,"caculate gross margin result")
//     .def("operating_profit_result", &Profitability::operating_profit_result,"caculate operating profit result")
//     .def("ros_result", &Profitability::ros_result,"Calculating ROS profit")
//     .def("net_profit", &Profitability::net_profit,"Recieve Net Profit")
//     .def("roa_profit", &Profitability::roa_profit,"Recieve ROA")
//     .def("increase_revenue", &Profitability::increase_revenue,"increased revenue")
//     .def("finance_cost", &Profitability::finance_cost, "get finance & revenue cost");

//     // .def("input_data", &Evaluate::input_data,"input all elements");
// }


