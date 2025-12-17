#include <iostream>
#include <cmath>
#include <exception>
#include <stdexcept>
#include <vector>
#include <limits>
#include <algorithm>

using namespace std;

// định nghĩa kiểu dữ liệu
typedef float EF; // hiêỵ quả
typedef float RATIOS;// tỷ syất
typedef float DIO; //số ngày tồn kho bình quân
typedef float TOV; // turnover
typedef float DSO; // days sale outstanding
typedef float TAT; //vòng quay tổng tài sản
typedef float DPO; // kỳ trả bình quân 

typedef long long SAMPLE; // đơn vị khử 
// const SAMPLE sample = 1'000'000'000;


// constructor dữ liệu nạp vào
// struct efficiency
// {
//     double revenue;
//     double costGS;
//     double avgttassets;
//     double avginventory;
//     double avgaccountsrcv;
//     double inventoryturnover;
//     double netcreditsales;
//     double netsales;
//     double avgaccpay;
//     double accpayturnover;
// };

/* Trưng dụng hàm */
// void extract_data(){};
// void merge_vct(){};
// vector<EF> crt_ratio_vt(){};
// void progress();


// lớp tính mức độ hiệu quả BCTC
class Efficiency {
    public:
        /// khởi tạo lại class khi dùng
        Efficiency() = default;

        // vòng quay tồn kho
        template<typename T>
        RATIOS inventory_turnover_ratio(T costGS , T avginventory){
            try
            {
                if(avginventory == 0.0){
                    throw std::invalid_argument("Undefined average inventory");
                    
                }
                
                // xử lí kiểu dữ liệu
                costGS = static_cast<float> (costGS);
                avginventory = static_cast<float> (avginventory);

                RATIOS ratio = static_cast<float>(costGS) / avginventory;
                return ratio;
            }
            catch(const std::exception& e)
            {
                std::cerr << e.what() << '\n';
                return numeric_limits<RATIOS>::quiet_NaN();
            }
            
        }

        //days sale outstanding ( số ngày tồn kho )
        
        DIO dio_stand(long long inventoryturnover, const int days = 365){
            try{
                if(inventoryturnover == 0.0){
                    throw std::invalid_argument("Undefined inventory turnover");
                    
                }

                // xử lí kiểu dữ liêu
                inventoryturnover = static_cast<long long> (inventoryturnover);
                DIO dio = static_cast<long long> (days) / inventoryturnover;
                return dio;

            }
            catch(const std::exception& e)
            {
                std::cerr << e.what() << '\n';
                return numeric_limits<DIO>::quiet_NaN();
            }
            
        }

        //vòng quay khoản phải thu (Account recieveable turnover)
        template<typename T>
        TOV art_turnover(T netcreditsale, T avgaccountsrcv){
            try
            {
                if(avgaccountsrcv == 0.0){
                    throw std::invalid_argument("undefined average account recieve");
                    // return 0.0f;
                }
                TOV result = (TOV)netcreditsale / (TOV)avgaccountsrcv;
                return result;
                
            }
            catch(const std::exception& e)
            {
                std::cerr << e.what() << '\n';
                return numeric_limits<TOV>::quiet_NaN();
            }
            
        }
        
        // vòng quay tổng tài sản
        template<typename T>
        TOV tta_turnover(T netsales, T avgttassets){
            try
            {
                if(avgttassets == 0.0){
                    throw std::invalid_argument("undefined average total assets");
                    
                }

                // xử lí kiểu dữ liệu
                netsales = static_cast<float> (netsales);
                avgttassets = static_cast<float> (avgttassets);

                TOV turnover = static_cast<float> (netsales) / avgttassets;
                return turnover;
            }
            catch(const std::exception& e)
            {
                std::cerr << e.what() << '\n';
                return numeric_limits<TOV>::quiet_NaN();
            }
            
        }

        //vòng quay khoản phải trả
        template<typename T>
        TOV apt_turnover(T costGS, T avgaccpay){
            try
            {
                if(avgaccpay == 0.0){
                    throw std::invalid_argument("Undefined average account payable");
                    
                }

                // xử lí kiểu dữ liệu
                costGS = static_cast<float> (costGS);
                avgaccpay = static_cast<float> (avgaccpay);

                // giá trị vòng quay
                TOV turnover = static_cast<float> (costGS) / avgaccpay;
                return turnover;
            }
            catch(const std::exception& e)
            {
                std::cerr << e.what() << '\n';
                return numeric_limits<TOV>::quiet_NaN();
            }
            
        }

        // kỳ trả tiền bình quân
        
        DPO dpo_outstanding(long long accpayturnover , const int days=365 ){
            try
            {
                if(accpayturnover == 0.0){
                    throw std::invalid_argument("Undefined account payable turnover");
                    
                }

                //xử lí kiểu dữ liệu
                accpayturnover = static_cast<long long> (accpayturnover);

                DPO result = days / accpayturnover;
                return result;

            }
            catch(const std::exception& e)
            {
                std::cerr << e.what() << '\n';
                return numeric_limits<DPO>::quiet_NaN();
            }
            
        }
        DIO dio_stand_py(int days, long long inventoryturnover) {
            return dio_stand(inventoryturnover, days);
        }
        DPO dpo_outstanding_py(int days, long long accpayturnover) {
            return dpo_outstanding(accpayturnover, days);
        }

};


