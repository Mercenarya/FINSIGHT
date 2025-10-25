#include <iostream>
#include <cmath>
#include <exception>
#include <stdexcept>
#include <vector>
#include <limits>
#include <algorithm>

using namespace std;

// định nghĩa kiểu dữ liệu
typedef double EF; // hiêỵ quả
typedef double RATIOS;// tỷ syất
typedef double DIO; //số ngày tồn kho bình quân
typedef double TOV; // turnover
typedef double DSO; // days sale outstanding
typedef double TAT; //vòng quay tổng tài sản
typedef double DPO; // kỳ trả bình quân 

typedef long long SAMPLE; // đơn vị khử 
const SAMPLE sample = 1'000'000'000;


// constructor dữ liệu nạp vào
struct efficiency
{
    double revenue;
    double costGS;
    double avgttassets;
    double avginventory;
    double avgaccountsrcv;
    double inventoryturnover;
    double netcreditsales;
    double netsales;
    double avgaccpay;
    double accpayturnover;
};

/* Trưng dụng hàm */
void extract_data(){};
void merge_vct(){};
vector<EF> crt_ratio_vt(){};
void progress();


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
                if(avginventory == 0){
                    throw std::invalid_argument("Undefined average inventory");
                    
                }
                
                // xử lí kiểu dữ liệu
                costGS = static_cast<double> (costGS);
                avginventory = static_cast<double> (avginventory);

                RATIOS ratio = static_cast<double>(costGS) / avginventory;
                return ratio;
            }
            catch(const std::exception& e)
            {
                std::cerr << e.what() << '\n';
                return numeric_limits<RATIOS>::quiet_NaN();
            }
            
        }

        //days sale outstanding ( số ngày tồn kho )
        template<typename T>
        DIO dio_stand(const int days = 365, T inventoryturnover){
            try{
                if(inventoryturnover == 0){
                    throw std::invalid_argument("Undefined inventory turnover");
                    
                }

                // xử lí kiểu dữ liêu
                inventoryturnover = static_cast<double> (inventoryturnover);
                DIO dio = static_cast<double> (days) / inventoryturnover;
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
                if(avgaccountsrcv == 0){
                    throw std::invalid_argument("undefined average account recieve");
                    
                }
                
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
                if(avgttassets == 0){
                    throw std::invalid_argument("undefined average total assets");
                    
                }

                // xử lí kiểu dữ liệu
                netsales = static_cast<double> (netsales);
                avgttassets = static_cast<double> (avgttassets);

                TOV turnover = static_cast<double> (netsales) / avgttassets;
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
                if(avgaccpay == 0){
                    throw std::invalid_argument("Undefined average account payable");
                    
                }

                // xử lí kiểu dữ liệu
                costGS = static_cast<double> (costGS);
                avgaccpay = static_cast<double> (avgaccpay);

                // giá trị vòng quay
                TOV turnover = static_cast<double> (costGS) / avgaccpay;
                return turnover;
            }
            catch(const std::exception& e)
            {
                std::cerr << e.what() << '\n';
                return numeric_limits<TOV>::quiet_NaN();
            }
            
        }

        // kỳ trả tiền bình quân
        template<typename T>
        DPO dpo_outstanding(const int days=365, T accpayturnover ){
            try
            {
                if(accpayturnover == 0){
                    throw std::invalid_argument("Undefined account payable turnover");
                    
                }

                //xử lí kiểu dữ liệu
                accpayturnover = static_cast<double> (accpayturnover);

                DPO result = days / accpayturnover;
                return result;

            }
            catch(const std::exception& e)
            {
                std::cerr << e.what() << '\n';
                return numeric_limits<DPO>::quiet_NaN();
            }
            
        }


};


