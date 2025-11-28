#include <iostream>
#include <cmath>
#include <vector>
#include <queue>
#include <exception>
#include <algorithm>
using namespace std;

// gom dữ liệu 2D hoặc hơn về 1 vector
template<typename T>
vector<T> pool (vector<vector<T>> data){
    try
    {
        if (data.empty()){
            std::cout<<"Data is empty";
        }

        vector<T> temp;
        int count = 0;
        // kiểm tra các độ rộng y
        for (size_t obj1 = 0; obj1 < data.size(); obj1 ++ ){
            // lọc array theo y 
            for(size_t obj2 = 0; obj2 < data[obj1].size(); obj2 ++){
                if(data[obj1].empty()){ // nếu như dữ liệu là 1 vector và nó rỗng giá trị
                    count+=1;
                    cout<<"internal data "<<count<<" is none";
                    continue;
                }
                temp.push_back(data[obj1][obj2]);
            }
        }
        return temp;
    }
    catch(const std::exception& e)
    {
        std::cerr << e.what() << '\n';
        
    }
    
};

// kiểm tra dữ liệu được gộp hay không
template<typename T>
void reveal (vector<T> &data){
    if (data.empty()){
        std::cout<<"Data is empty";
    }
    for(T value : data){
        std::cout<<value<<" ";
    }
}

/*
Công thức ( Formula )
- Mean : trung bình
- deviation : độ lệch
- standard score : loại chuẩn hóa
*/
// giá trị trung bình dữ liệu
template<typename T>
float means(vector<T> &data){
    try
    {
        if(data.empty()){
            cout<<"Data is empty";
        }
        T sum = 0;
        int noo = data.size();
        for( T value : data ){
            sum += value;
        }
        return sum/noo;
    }
    catch(const std::exception& e)
    {
        std::cerr << e.what() << '\n';
        return 0.0f;
    }
    
}


// độ lệch chuẩn
template<typename T>
float deviation(vector<T> &data, T &mean){
    /*
    chuẩn hóa công thức
    σ2 = ∑in (xi - x̄)2/n
    */
    T calc = 0;
    T sum = 0;
    T size = data.size();
    try
    {
        for(T value : data){
            T calc = pow((value - mean),2);
            sum += calc;
        }
        return sqrt(sum / size);
    }
    catch(const std::exception& e)
    {
        std::cerr << e.what() << '\n';
        return 0.0f;
    }
    
}


// công thức chuẩn hóa
template<typename T>
vector<T> normalization(vector<T> &data, T &mean, T &devi){
    vector<T> result;
    T formula = 0;
    for(T value : data){
        formula = (value - mean) / devi;
        result.push_back(formula);
    }
    return result;
};


int main(){
    
    vector<vector<float>> DATAVT_2D = {
        {10.0, 15.0, 22.0, 45.0 , 30.0},
        {11.0, 14.0, 23.0, 70.0 , 30.0},
    };

    vector<float> pooldata = pool(DATAVT_2D);
    reveal(pooldata);
    cout<<endl;

    float mean = 0;
    float devi = 0;
    vector<float> nml;
    
    mean = means(pooldata);
    devi = deviation(pooldata,mean);
    nml = normalization(pooldata,mean,devi);
    
    cout<<"Mean's value : "<<mean<<endl;
    cout<<"Standard deviation : "<<devi<<endl;
    cout<<"Normalized's data :";
    reveal(nml);

    
}