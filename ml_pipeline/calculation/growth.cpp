#include <iostream>
#include <cmath>
#include <vector>
#include <queue>
#include <stack>
#include <string>
#include <pybind11/pybind11.h>
#include <exception>

class Growth{
    private:

        float revenue_last;
        float revenue_past;
        float eps_last;
        float eps_past;
        float opicm_last;
        float opicm_past;

    public:
        float sample = 1000000000;
        Growth(): revenue_past(0), revenue_last(0), eps_past(0),
        eps_last(0), opicm_last(0), opicm_past(0) {};

        float growth_rate(float current, float previous){
            try
            {
                if (previous == 0){
                    return 0.0f;
                }
                current = float(current/sample);
                previous = float(previous/sample);
                float growth = (current - previous) / previous;
                if (growth == 0){
                    std::cout<<"Growth rate cannot be none";

                }
                return float(growth * 100);
            }
            catch(const std::exception& e)
            {
                std::cerr << e.what() << '\n';
                return 0.0f;
            }
            
        }
        
};