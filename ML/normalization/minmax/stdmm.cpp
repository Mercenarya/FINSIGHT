#include <iostream>
#include <cmath>
#include <queue>
#include <vector>
#include <exception>

using namespace std;


float get_max(vector<float> data){
    if(data.empty()){
        cout<<"Data is empty";
    }
    float max = data[0];
    for(size_t obj = 0; obj < data.size(); obj ++){
        if (data[obj] > max){
            max = data[obj]; 
        }
    }
    return max;
}
float get_min(vector<float> data){
    if(data.empty()){
        cout<<"Data is empty";
    }
    float min = data[0];
    for(size_t obj = 0; obj < data.size(); obj++){
        if (data[obj] < min){
            min = data[obj];
        }
    }
    return min;
}

float scale_min_max(float min, float max, float value){
    float formula = (value - min) / (max - min);
    return formula;
}



void check_queue(queue<float> data){
    cout << "Scaled Data (Queue):" << endl;
    while (!data.empty()){
        cout << data.front() << endl;
        data.pop();
    }
}

void get_scaled(vector<float> data, float min, float max){
    queue<float> scaled_data;
    if(data.empty()){
        cout<<"Data is empty";
    }
    for(size_t obj =0; obj < data.size(); obj++){
        float scaled = scale_min_max(min,max,data[obj]);
        scaled_data.push(scaled);
    }
    check_queue(scaled_data);
}


// multi vector //

template<typename T>
vector<T> multi_approve(vector<vector<T>>& data){
    /*
 (cols) x  x1  x2  x3 (rows)
    y   0  1   2   3 (arrays)
    y1  10 30  40  50
    y2  1f 3x  3f  4x
    y3  7x 8f  9x  10x
    */
   //2D vector
    vector<T> approved_vt;
    if (data.empty()){
        cout<<"data is empty";
    }
    for(auto dt : data){
        for(auto obj : dt){
            approved_vt.push_back(obj);
        }
    }
    
    return approved_vt;
}


template<typename T>
float get_max_2d(vector<vector<T>> data){
    T max2 = data[0][0];
    for(size_t obj1 = 0; obj1 < data.size(); obj1++){
        for (size_t obj2 = 0; obj2 < data[obj1].size(); obj2++ ){
            
            if (data[obj1][obj2] > max2){
                max2 = data[obj1][obj2];
            }
        }
    }
    return max2;

}

template<typename T>
float get_min_2d(vector<vector<T>> data){
    T min2 = data[0][0];
    for(size_t obj1 = 0; obj1 < data.size(); obj1++){
        for(size_t obj2 = 0; obj2 < data[obj1].size(); obj2 ++){
            if (data[obj1][obj2] < min2){
                min2 = data[obj1][obj2];
            }
        }
    }
    return min2;
}

// calculation
template<typename T>
float scaled_min_max_2d(T data, T min, T max){
    float formula = (data - min) / (max - min);
    return formula;
}

// get scalling data review
template<typename T>
float get_scaled(vector<vector<T>> data, T min, T max){
    
}

int main(){
    vector <float> DATA_VT = {10.0, 15.0, 22.0, 45.0 , 30.0};
    vector<vector<float>> DATAVT_2D = {
        {10.0, 15.0, 22.0, 45.0 , 30.0},
        {11.0, 14.0, 23.0, 70.0 , 30.0},
    };
    
    float min = get_min(DATA_VT);
    float max = get_max(DATA_VT);

    cout<<min<<" - "<<max<<endl;
    float min2 = get_min_2d(DATAVT_2D);
    float max2 = get_max_2d(DATAVT_2D);
    cout<<min2<<" - "<<max2<<endl;
    // get_scaled(DATA_VT, min, max);
    
    // cout<<sizeof(get_scaled(DATA_VT, min, max))<<" kb";
}