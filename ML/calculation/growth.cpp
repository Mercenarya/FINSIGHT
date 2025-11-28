#include <iostream>
#include <cmath>
#include <vector>
#include <stdexcept>
#include <algorithm>
#include <limits>

using namespace std;

typedef double GROWTH; // định nghĩa kiểu dữ liệu
typedef double CAGR; // tăng trưởng kép

// // khởi tạo datasheet
// struct datasheet {
//     double current; // kì hiện tại
//     double previous; // kì trước
//     double year; // số năm
// };


// lóp tăng trưởng
class Growth{
    public:
        // constructor cho lớp tăng trưởng cho mỗi đối tượng
        Growth() = default;

        template<typename T>
        GROWTH single_growth_rate(T current, T previous){
            try
            {
                if(previous == 0){
                    
                    throw std::invalid_argument("Previous cannot be none");
          
                }

                current = static_cast<double>(current);
                previous = static_cast<double>(previous);
                
                GROWTH growth = static_cast<double>(current - previous) / previous;
                return growth * 100;
            }
            catch(const std::exception& e)
            {
                std::cerr << e.what() << '\n';
                return numeric_limits<GROWTH>::quiet_NaN();
            }
            
        }
        
        // tẳng trưởng kép theo năm
        template<typename T>
        CAGR cagr_growth_rate(T current, T previous, T year){
            try
            {
                if(previous == 0){
                    
                    throw std::invalid_argument("Previous cannot be none");
                    
                }

                current = static_cast<double> (current);
                previous = static_cast<double> (previous);
                year = static_cast<double> (year);
        
                GROWTH growth = static_cast<double> (pow(current/previous, 1.0 /year))-1;
                return growth * 100;
            }
            catch(const std::exception& e)
            {
                std::cerr << e.what() << '\n';
                return numeric_limits<GROWTH>::quiet_NaN();
            }
            
        }
};
