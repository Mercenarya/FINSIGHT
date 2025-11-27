#include <pybind11/pybind11.h>
#include "liquidity.cpp"
#include "profitability.cpp"
#include "efficiency.cpp"
#include "growth.cpp"

using namespace std;
namespace py = pybind11;


using T = long long;
// nhóm liquidity
using cash_ratio_sig = double (Liquidity::*)(T, T);
using quick_ratio_sig = double (Liquidity::*)(T, T, T);
using current_ratio_sig = double (Liquidity::*)(T, T);

// nhóm Profitability
using gross_profit_margin_sig = double (Profitability::*)(T ,T);
using opm_margin_sig = double (Profitability::*)(T,T);
using npm_margin_sig = double (Profitability::*)(T,T);
using roa_ratios_sig = double (Profitability::*)(T,T);
using roe_ratios_sig = double (Profitability::*)(T,T);
using eps_ratios_sig = double (Profitability::*)(T,T,T);

// nhóm Efficiency
using inventory_TOR_sig = double (Efficiency::*)(T,T);
using dio_stand_sig = double (Efficiency::*)(const int,T);
using art_turnover_sig = double (Efficiency::*)(T,T);
using tta_turnover_sig = double (Efficiency::*)(T,T);
using apt_turnover_sig = double (Efficiency::*)(T,T);
using dpo_outstanding_sig = double (Efficiency::*)(const int,T);

// Nhóm growth
using single_growth_rate_sig = double (Growth::*)(T,T);
using cagr_growth_rate_sig = double (Growth::*)(T,T,T);


PYBIND11_MODULE(evaluate_module_update, m){
    py::class_<Liquidity>(m, "Liquidity")
    .def(py::init<>())
    .def("cash_ratio", static_cast<cash_ratio_sig>(&Liquidity::cash_ratio), "Cash ratio assume")
    .def("quick_ratio", static_cast<quick_ratio_sig>(&Liquidity::quick_ratio),"Quick ratio assume")
    .def("current_ratio", static_cast<current_ratio_sig>(&Liquidity::current_ratio),"Current Ratio assume");
    


    py::class_<Profitability>(m, "Profitability").def(py::init<>())
    .def("gross_margin", static_cast<gross_profit_margin_sig>(&Profitability::gross_profit_margin),"caculate gross margin result")
    .def("opm_margin", static_cast<opm_margin_sig>(&Profitability::opm_margin),"opm margin")
    .def("npm_margin", static_cast<npm_margin_sig>(&Profitability::npm_margin),"npm margin")
    .def("roa_ratio", static_cast<roa_ratios_sig>(&Profitability::roa_ratios),"roa ratio")
    .def("roe_profit", static_cast<roe_ratios_sig>(&Profitability::roe_ratios),"ROE profit")
    .def("eps_ratios", static_cast<eps_ratios_sig>(&Profitability::eps_ratios),"EPS ratio");
    


    py::class_<Efficiency>(m, "Efficiency").def(py::init<>())
    .def("inventory_turnover_ratio", static_cast<inventory_TOR_sig>(&Efficiency::inventory_turnover_ratio),"Inventory turnover ratio")
    // .def("dio_stand", static_cast<dio_stand_sig>(&Efficiency::dio_stand),"DIO Stand")
    .def("art_turnover", static_cast<art_turnover_sig>(&Efficiency::art_turnover),"ART Turnover")
    .def("tta_turnover", static_cast<tta_turnover_sig>(&Efficiency::tta_turnover),"TTA Turnover")
    .def("apt_turnover", static_cast<apt_turnover_sig>(&Efficiency::apt_turnover),"APT Turnover")
    .def("dio_stand",&Efficiency::dio_stand_py, "DIO Stand")
    .def("dpo_outstanding",&Efficiency::dpo_outstanding_py, "DPO Outstanding");
  
    py::class_<Growth>(m, "Growth").def(py::init<>())
    .def("single_growth_rate",static_cast<single_growth_rate_sig>(&Growth::single_growth_rate),"Single growth rate")
    .def("cagr_growth_rate",static_cast<cagr_growth_rate_sig>(&Growth::cagr_growth_rate),"CAGR growth rate");
}

