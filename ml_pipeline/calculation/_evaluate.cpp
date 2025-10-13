#include <pybind11/pybind11.h>
#include "liquidity.cpp"
#include "profitability.cpp"
#include "efficiency.cpp"
#include "growth.cpp"

using namespace std;
namespace py = pybind11;


PYBIND11_MODULE(evaluate_module, m){
    py::class_<Liquidity>(m, "Liquidity").def(py::init<>())
    .def("cash_ratio", &Liquidity::cash_ratio,"Cash ratio assume")
    .def("quick_ratio", &Liquidity::quick_ratio,"Quick ratio assume")
    .def("current_ratio", &Liquidity::current_ratio,"Current Ratio assume");


    py::class_<Profitability>(m, "Profitability").def(py::init<>())
    .def("gross_margin_result", &Profitability::gross_margin_result,"caculate gross margin result")
    .def("operating_profit_result", &Profitability::operating_profit_result,"caculate operating profit result")
    .def("ros_result", &Profitability::ros_result,"Calculating ROS profit")
    .def("net_profit", &Profitability::net_profit,"Recieve Net Profit")
    .def("roa_profit", &Profitability::roa_profit,"Recieve ROA")
    .def("increase_revenue", &Profitability::increase_revenue,"increased revenue")
    .def("finance_cost", &Profitability::finance_cost, "get finance & revenue cost")
    .def("roe_profit", &Profitability::roe_profit, "ROE profit");

    py::class_<Efficiency>(m, "Efficiency").def(py::init<>())
    .def("inventory_turnover", &Efficiency::inventory_turnover,"Inventory tuernover ratios")
    .def("recv_turnover", &Efficiency::recv_turnover,"Receivable turnover ratios")
    .def("asset_turnover", &Efficiency::asset_turnover, "Asset turnover ratios");

    py::class_<Growth>(m, "Growth").def(py::init<>())
    .def("growth_rate", &Growth::growth_rate, "Growth rate percentage");

}

