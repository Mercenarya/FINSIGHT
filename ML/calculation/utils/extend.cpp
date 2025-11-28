#include <iostream>
#include <queue>
#include <vector>
#include <algorithm>
#include <limits>
#include <stdexcept>
#include <typeinfo>
#include "../efficiency.cpp"


using namespace std;

typedef double AVG;
typedef double UTIL;

template<typename T>
T average_value(){};
bool invalid_value(){};



bool datatype_check(){};

vector<double> merge_data(){};

struct datasheet {
    // ----------------------------------------------------
    // 1. DỮ LIỆU TỪ BÁO CÁO KẾT QUẢ KINH DOANH (Income Statement)
    // ----------------------------------------------------
    double net_sales;           // Doanh thu thuần (Mẫu số cho nhiều Tỷ suất và TAT)
    double cogs;                // Giá vốn hàng bán (Tử số cho Inventory Turnover, AP Turnover)
    double operating_expense;   // Chi phí hoạt động/bán hàng/quản lý (Tính EBIT)
    double interest_expense;    // Chi phí lãi vay (Tính EBT/EBITDA)
    double tax_expense;         // Chi phí thuế
    double net_income;          // Lợi nhuận ròng (Tử số cho ROA, ROE, Profit Margins)

    // ----------------------------------------------------
    // 2. DỮ LIỆU TỪ BẢNG CÂN ĐỐI KẾ TOÁN (Balance Sheet)
    //    *Lưu ý: Thường cần cả giá trị CUỐI KỲ và giá trị BÌNH QUÂN (Average)
    // ----------------------------------------------------
    double total_assets_end;    // Tổng tài sản cuối kỳ
    double total_assets_avg;    // Tổng tài sản bình quân (Mẫu số cho TAT, ROA)
    double total_equity_avg;    // Tổng vốn chủ sở hữu bình quân (Mẫu số cho ROE)
    double total_liabilities_end;// Tổng nợ phải trả cuối kỳ
    
    // 2.1. Thanh khoản & Vốn lưu động
    double cash;                // Tiền mặt
    double accounts_receivable_avg;// Khoản phải thu bình quân (Mẫu số cho AR Turnover)
    double inventory_avg;       // Hàng tồn kho bình quân (Mẫu số cho Inventory Turnover)
    double accounts_payable_avg; // Khoản phải trả bình quân (Mẫu số cho AP Turnover)
    
    // ----------------------------------------------------
    // 3. DỮ LIỆU LỊCH SỬ & KHÁC
    // ----------------------------------------------------
    double previous_period_value;// Giá trị của kỳ trước (Cho các phép tính Growth rate, ví dụ: Revenue kỳ trước)
    int num_years;              // Số năm giữa kỳ hiện tại và kỳ trước (Cho CAGR)
};


class DataQueue{
    private: 
        queue<datasheet> storage;
    public:
        DataQueue() = default;

        void add_queue( const datasheet& data){
            storage.push(data);
            cout<<"Datasheet added to queue";
        }

        // out data
        void pop_data(){
            if (storage.empty()){
                throw std::out_of_range("Exception : Queue is empty ");
            }
            datasheet data = storage.front();
            storage.pop();
            cout<<"Data popped"<<endl;
            
        }
        // extract data in queue
        void extract_queue(){
            Efficiency ef;
            cout<<endl;
            cout<<"---------------"<<endl;
            while (!storage.empty())
            {
                datasheet data = storage.front();
                // cout<<"Quarter 1: "<<data.q1<<endl;
                // cout<<"Quarter 2: "<<data.q2<<endl;
                // cout<<"turnover ratio: "<<ef.inventory_turnover_ratio(data.q1, data.q2)<<endl;
                storage.pop();
            }
            cout<<"---------------"<<endl;
        } 


};

template<typename T>
AVG average_value(T prev, T end){
    try
    {
        if(prev == 0){
            throw std::invalid_argument("undefined previous value");
        }
        prev = static_cast<AVG>(prev);
        end = static_cast<AVG>(end);

        return (prev-end)/2;
    }
    catch(const std::exception& e)
    {
        std::cerr << e.what() << '\n';
        return numeric_limits<AVG>::quiet_NaN();
    }
    
}

// kiểm tra kiểu dữ liệu
template<typename T>
string datatype_check(T data){
    try
    {
        if(data == 0){
            return 0.0f;
        }
        string datatype = typeid(data).name();
        return datatype;
    }
    catch(const std::exception& e)
    {
        std::cerr << e.what() << '\n';
    }
    
}

// merging data
template<typename T>
vector<UTIL> merge_data(vector<T> &x, vector<T> &y){
    vector<UTIL> result;
    if(x.size() != y.size()){
        throw std::runtime_error("Assets and liabilities must be same length");
    }

    //cấp phát bộ nhớ để tăng hiệu suất
    result.reserve(x.size() + y.size());

    for(int value = 0; value < x.size(); value ++){
        
        result.push_back(x[value]);
        result.push_back(y[value]);
    
    }
    return result;
};

// extract result
template<typename T>
void extract_data( vector<T> &data){
    for(auto value : data){
        cout<<value<<",";
    }

};




// mẫu chạy thử
void progress(){
    DataQueue mng;

    mng.add_queue({ 423'990'500, 400'374'790,});
    mng.extract_queue();
    mng.add_queue({372'183'892, 528'475'505});
    mng.extract_queue();
    mng.pop_data();
    mng.extract_queue();

    vector<datasheet> data = {
        { 
            2'500'000.0, 1'800'000.0, 200'000.0,
            10'000'000.0, 300'000.0, 5'000'000.0,
            2'200'000.0, 1
        },
        {
            2'400'000.0, 1'750'000.0, 210'000.0,
            10'100'000.0, 310'000.0, 5'100'000.0,
            2'500'000.0, 0
        },

    };


}

// int main(){
//     progress();
// }

