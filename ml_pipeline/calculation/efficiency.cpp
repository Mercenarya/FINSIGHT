#include <iostream>
#include <cmath>
#include <pybind11/pybind11.h>
#include <exception>



class Efficiency {
    private :
        float revenue;
        float costGS;
        float ttassets;
        float avginventory;
        float avgaccountsrcv;
        
    public:
        
        const int sample = 1000000000;
        float inventory_turnover(float costGS, float avginventory){
            try
            {
                costGS = float(costGS/sample);
                avginventory = float(avginventory/sample);

                float turnover = costGS / avginventory;
                if(turnover == 0 ){
                    std::cout<<"Turnover cannot be none value"<<std::endl;
                }

                return turnover;
            }
            catch(const std::exception& e)
            {
                std::cerr << e.what() << '\n';
                return 0.0f;
            }
            
        }

        float recv_turnover(float revenue, float avgaccountsrcv){
            try
            {
                revenue = float(revenue / sample);
                avgaccountsrcv = float(avgaccountsrcv / sample);

                float turnover = revenue / avgaccountsrcv;
                if (turnover == 0){
                    std::cout<<"Turnover cannot be none value"<<std::endl;
                }
                return turnover;
            }
            catch(const std::exception& e)
            {
                std::cerr << e.what() << '\n';
                return 0.0f;
            }
            
        }

        float asset_turnover(float revenue, float ttassets){
            try
            {
                revenue = float(revenue / sample);
                ttassets = float(ttassets / sample);

                float turnover = revenue / ttassets;
                if (turnover == 0){
                    std::cout<<"Turnover cannot be none value"<<std::endl;
                }
                return turnover;
            }
            catch(const std::exception& e)
            {
                std::cerr << e.what() << '\n';
                return 0.0f;
            }
            
        }
        Efficiency(): revenue(0), costGS(0), ttassets(0), avgaccountsrcv(0), avginventory(0){};
};


