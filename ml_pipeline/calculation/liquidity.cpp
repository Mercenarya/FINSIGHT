// #ifndef LIQUIDITY_H
// #define LIQUIDITY_H
#include <iostream>
#include <cmath>
#include <pybind11/pybind11.h>
#include <exception>


// parameter
namespace py = pybind11;
using namespace std;


class Liquidity{
    private:
        float currentassets;
        float liabilities;
        float cash;
        float inventory;
    public:
        
        const int sample = 1000000000;
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
        Liquidity(): currentassets(0), cash(0), inventory(0), liabilities(0) {};

};

// PYBIND11_MODULE(evaluate_module, m){
//     py::class_<Liquidity>(m, "Liquidity").def(py::init<>())
//     .def("cash_ratio", &Liquidity::cash_ratio,"Cash ratio assume")
//     .def("quick_ratio", &Liquidity::quick_ratio,"Quick ratio assume")
//     .def("current_ratio", &Liquidity::current_ratio,"Current Ratio assume");

// }

// #endif