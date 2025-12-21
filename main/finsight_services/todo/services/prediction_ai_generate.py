from google import genai
import os
import sys
import asyncio


API_KEY = "AIzaSyA49kjTnNRiWrRD5Wu4YWAp2eNL44sWRK0"

# Lớp thông tin gốm các đối số đặc thù được truuyền vào để hận giá trị
# linh hoạt cho việc tạo nhiều đối tượng phân tích đặc thù và có tính kế thừa cho các phần sau
class AgentGenerative:
    def __init__(self,cash_ratio,current_ratio,quick_ratio):
        self.cash_ratio = cash_ratio
        self.current_ratio = current_ratio
        self.quick_ratio = quick_ratio

    def _result(self):
        template = {
            "quick ratio":self.quick_ratio,
            "cash ratio":self.cash_ratio,
            "current ratio":self.current_ratio
        }
        return template

# tạo prompt -> sheet result
async def genereative(template:dict,prev_data:list):
    try:
        # các giá trị cần đánh giá và phân tích
        prediction_data = f'''
        - Quick Ratio : {template['quick ratio']}%\n
        - Cash Ratio : {template['cash ratio']}%\n
        - Current Ratio : {template['current ratio']}%
        '''
        client = genai.Client(api_key=API_KEY)

        res = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=f'''Đánh giá và đề xuất hướng đầu tư cho tôi dựa trên báo cáo thanh khoản quý 5 
            (tức quý tiếp theo và quý đầu cho nắm tiếp) tóm gọn trong 100 từ và bằng tiếng anh\n
            với dữ liệu dưới đây:\n{prediction_data}\nList dữ liệu đầy đủ trước đó để dựa vào \n{prev_data}'''
        )
        return res.text

    except Exception as error:
        print("An error occured during generating : ",error)
        return error
    

