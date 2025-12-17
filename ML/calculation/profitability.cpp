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
typedef float RATIOS;// tỷ suất
typedef float MARGIN;// biên 
typedef vector<float> DATA;// quy chuẩn kiểu dữ liệu cho luồng dữ liệu 

// đơn vị mẫu
// const SAMPLE sample = 1'000'000'000;

/*
    float revenue; 
    float gross_profit;
    float business_profit;
    float profit_atm;
    float net_income;
    float share;
*/


// khởi tạo datasheet 
// struct datasheet{
//     long long GP; // gross profit (lợi nhuận gộp)
//     long long RV; // revenue (doanh thu thuần)
//     long long NI; // Net income (lợi nhuận ròng)
//     long long SEQ; // Shareholder enquity 
//     long long TTA; // total assets (tài sản)
//     long long BSNP; // business profit (lơi nhuận hoạt động EBIT)
//     long long BATMP; // lợi nhuận sau thuế
// };

// /* Trưng dụng hàm */
// void extract_data(){};
// void merge_vct(){};
// vector<double> ratio_vt(){};
// vector<double> margin_vt(){};

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
                GP = static_cast<float>(GP);
                RV = static_cast<float>(RV);

                // xử lí kết quả biên lợi nhuận
                double margin = static_cast<float>(GP)/RV ;
                return margin* 100;
            }catch(const std::exception& e){
                std::cerr << e.what() << '\n';
                return 0.0;
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
                BSNP = static_cast<float>(BSNP);
                RV = static_cast<float>(RV);

                //xử lí kết quả biên lợi nhuận
                double margin = static_cast<float>(BSNP) / RV;
                return margin*100;
            }catch(const std::exception& e){
                std::cerr << e.what() << '\n';
                return 0.0;
            }
        
            
        }
        

        template <typename T>
        MARGIN npm_margin(T BATMP, T RV ){
            try{
                if( RV == 0.0){
                    if(BATMP > 0){
                        throw std::invalid_argument("Revenue (RV) is none, undefined Net income");
                        return 1.0f;
                 
                    }
                    return 0.0f;
                }
                
                //xử lí ép kiểu dữ liệu long long --> double
                BATMP = static_cast<float>(BATMP);
                RV = static_cast<float>(RV);

                // xử lí kết quả biên lợi nhuận
                double margin = static_cast<float>(BATMP) / RV;
                return margin*100;
            }catch(const std::exception& e){
                std::cerr << e.what() << '\n';
                return 0.0;
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
                if(TTA == 0.0){
                    if(NI > 0.0){
                        throw std::invalid_argument("Total assest is none, Net income is undefined");
                        return 1.0f;
                    }
                    return 0.0f;
                }
                TTA = static_cast<float>(TTA);
                NI = static_cast<float>(NI);

                double ratios = static_cast<float>(NI) / TTA;
                return ratios * 100;
                
            }
            catch(const std::exception& e)
            {
            

                std::cerr << e.what() << '\n';
                return 0.0;
            }
            
        }


        // tỉ suất ROE
        template<typename T>
        RATIOS roe_ratios(T ATE ,T NI){
            try
            {
                if(ATE==0.0){
                    if(NI > 0.0){
                        throw std::invalid_argument("After-tax Equity is none, net income is undefined");
                        return 1.0f;
                    }
                    return 0.0f;
                }

                ATE = static_cast<float>(ATE);
                NI = static_cast<float>(NI);

                double ratios = static_cast<float>(NI) / ATE;
                return ratios * 100;


            }
            catch(const std::exception& e)
            {
                std::cerr << e.what() << '\n';
                return 0.0;
            }
            
        }

        // Thu nhập trên mỗi cổ phần
        template<typename T>
        RATIOS eps_ratios(T NI, T PD, T ASO){
            try{
                
                NI = static_cast<float>(NI);// net income
                PD = static_cast<float>(PD);// Preffered Dividend
                ASO = static_cast<float>(ASO);// Average shares outstanding

                double ratios = static_cast<float>((NI)-PD) / ASO;
                return ratios;

            }
            catch(const std::exception& e)
            {
                std::cerr << e.what() << '\n';
                return 0.0;
            }
            
        }

};


