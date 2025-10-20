// #ifndef LIQUIDITY_H
// #define LIQUIDITY_H
#include <iostream>
#include <cmath>
#include <pybind11/pybind11.h>
#include <exception>


// parameter
namespace py = pybind11;
using namespace std;


// đơn vị chuẩn : 1,000,000,000
typedef long long SAMPLE;

// khởi tạo giá trị 
struct datasheet
{
    long long current_assets;
    long long liabilities;
    long long inventory;
    long long marketable_sc;
};



class Liquidity{
    public:
        const SAMPLE sample = 1000000000LL;
        Liquidity() = default;
        /*Template : sử dụng để làm biển mẫu nhằm xác định đa dạng kiểu dữ liệu vào*/
        template <typename T>
        // tỷ số thành khoản hiện tại
        double current_ratio(T current_assets, T liabilities){
            try
            {
                if(liabilities == 0){
                    if(current_assets > 0){
                        throw std::invalid_argument("liabilities is zero, undifined current assets");
                    }
                    return 0.0f;
                }

                //Ép kiểu dữ liệu double, chuyển đổi giá trị cho từng mục
                current_assets = static_cast<double>(current_assets);
                liabilities = static_cast<double>(liabilities);

                /*Ratio*/
                double ratio = current_assets / liabilities;
                return ratio;
                

            }
            catch(const std::exception& e)
            {
               std::cerr << e.what() << '\n';
               return 1.0f;
            }
            catch(const std::invalid_argument& e){
               std::cerr << e.what() << '\n';
               return 1.0f;
            }
            
        }
        
        //Tỷ số Thanh toán Nhanh
        template<typename T>
        double quick_ratio(T current_assets, T inventory, T liabilities ){
            try
            {
                if (liabilities == 0){
                    if(current_assets > 0 || inventory > 0){
                        throw std::invalid_argument("liabilities is zero, undefined current assets and inventory");
                    }
                    return 0.0f;
                }

                current_assets = static_cast<double>(current_assets);
                inventory = static_cast<double>(inventory);
                liabilities = static_cast<double>(liabilities);

                /*Ratio*/
                double ratio = (current_assets - inventory) / liabilities;

                return ratio;


            }
            catch(const std::exception& e)
            {
                std::cerr << e.what() << '\n';
                return 1.0f;
            }
            catch(const std::invalid_argument& e){
                std::cerr << e.what() << '\n';
                return 1.0f;
            }
            
        }

        // tỷ số thanh khoản bằng tiền
        template<typename T>
        double cash_ratio(T cash,T marketable_sc, T liabilities){
            try
            {
                if (liabilities == 0){
                    if(cash > 0 || marketable_sc > 0){
                        throw std::invalid_argument("liabilities is zero, undefined cash and marketable security");
                    }
                    return 0.0f;
                }

                cash = static_cast<double>(cash);
                marketable_sc = static_cast<double>(marketable_sc);
                liabilities = static_cast<double>(liabilities);

                /*Ratio*/
                double ratio = (cash + marketable_sc) / liabilities;
                return ratio;
            }
            catch(const std::exception& e)
            {
                std::cerr << e.what() << '\n';
                return 1.0f;
            }
            catch(const std::invalid_argument& e){
                std::cerr << e.what() << '\n';
                return 1.0f;
            }
            
        }

};
