#include <iostream>
#include <cmath>
#include <queue>
#include <vector>
#include <stdexcept>
#include <thread>


// standard namspace 
using namespace std;


// đơn vị chuẩn : 1,000,000,000
typedef long long SAMPLE;
// current ratio
typedef float CRT;
// const SAMPLE sample = 1'000'000'000;



// struct datasheet
// {
//     long long current_assets;
//     long long liabilities;
//     long long inventory;
//     long long marketable_sc;
// };



class Liquidity{
    public:
        Liquidity() = default;
        /*Template : sử dụng để làm biển mẫu nhằm xác định đa dạng kiểu dữ liệu vào*/
        template <typename T>
        // tỷ số thành khoản hiện tại
        float current_ratio(T current_assets, T liabilities){
            try
            {
                if(liabilities == 0.0){
                    if(current_assets > 0){
                        throw std::invalid_argument("liabilities is zero, undifined current assets");
                        return 1.0f;
                    }
                    return 0.0f;
                };

                //Ép kiểu dữ liệu double, chuyển đổi giá trị cho từng mục
                // current_assets = static_cast<double>(current_assets);
                // liabilities = static_cast<double>(liabilities);

                /*Ratio*/
                float ratio = static_cast<float> (current_assets) / liabilities;
                return ratio;
                

            }
            catch(const std::exception& e)
            {
               std::cerr << e.what() << '\n';
               return 1.0f;
            }

            
        }
        
        //Tỷ số Thanh toán Nhanh
        template<typename T>
        float quick_ratio(T current_assets, T inventory, T liabilities ){
            try
            {
                if (liabilities == 0.0){
                    if(current_assets > 0 || inventory > 0){
                        throw std::invalid_argument("liabilities is zero, undefined current assets and inventory");
                        return 1.0f;
                    }
                    return 0.0f;
                }

                // current_assets = static_cast<double>(current_assets);
                // inventory = static_cast<double>(inventory);
                // liabilities = static_cast<double>(liabilities);

                /*Ratio*/
                float ratio = static_cast<float>(current_assets - inventory) / liabilities;

                return ratio;


            }
            catch(const std::exception& e)
            {
                std::cerr << e.what() << '\n';
                return 1.0f;
            }
            
            
        }

        // tỷ số thanh khoản bằng tiền
        template<typename T>
        float cash_ratio(T cash, T liabilities){
            try
            {
                if (liabilities == 0.0){
                    if(cash > 0 ){
                        throw std::invalid_argument("liabilities is zero, undefined cash and marketable security");
                        return 1.0f;
                    }
                    return 0.0f;
                }

                // cash = static_cast<double>(cash);
                // marketable_sc = static_cast<double>(marketable_sc);
                // liabilities = static_cast<double>(liabilities);

                /*Ratio*/
                float ratio = static_cast<double>(cash) / liabilities;
                return ratio;
            }
            catch(const std::exception& e)
            {
                std::cerr << e.what() << '\n';
                return 1.0f;
            }
            
            
        }

};
