from user import *
from Ai import *

def all_merchant_information(merchant_id, token):
    base_url = "https://team-connect.treasuredeal.com/api/v1"
    def user_order():
        inf = ''
        endpoint = "merchants/merchant-orders/1"
        # Call the function
        all_orders = get_request(base_url, endpoint, token)['data']['orders']
        orders_summary=list(map(extract_basic_order_info, all_orders))
        orders_summary=filter_orders(orders_summary)
        for x in orders_summary:
            inf+=dict_to_string(x)
        return inf
    # Example usage:
    api_url = "https://api.openai.com/v1/chat/completions"  # Use your correct API URL
    api_key = "vn-o-tAisFca21norxYX4tcXBUwa1ScTdxgUkdbGt6Gq2W3EoenIMZwYoDVnwAHh4ptsNjf_wPYO-Qfu8WqDka6t_G3sNvD"  # Replace with your actual API key
    api_key=caesar_decrypt(api_key, 3)
    model_name = "gpt-4o-mini"  # Or whichever model you're using
    agent = APIClientWithDynamicSystem(api_url, api_key, model_name)
    all_info=''
    prompt = """
        You are an AI assistant tasked with summarizing merchant information from a JSON data structure. 
        Focus on extracting and presenting the most essential and important details in a clear and concise manner.
        dont use id details or imgs or urls except website.(summarize within 300 words as less as possible)
        ----------------------- start of data -------------------------------------------------
        {merchant_details}
        ----------------------- End of data ---------------------------------------------------
"""
    endpoints = ["merchants/merchant-details?merchant_id="+str(merchant_id),
                 "merchants/merchant-products?merchant_id="+str(merchant_id),
                 "merchants/merchant-services?merchant_id="+str(merchant_id)
                ]
    header_info=['--------MERCHANT--------', '--------PRODUCTS--------', '--------SERVICES--------']
    for enpoint,header in zip(endpoints, header_info):
        if 'details' in enpoint.lower():
            header_info=''
        messages=[]
        data = get_request(base_url, enpoint)
        # Change the system message
        agent.change_system_message(prompt.format(merchant_details = data))
        messages.append({"role": "user", "content": 'Summary is:'})
        # Get the content again after changing the system message
        response_content = agent.get_content(messages)
        all_info +=header+'\n'+ response_content +'\n'
        information = all_info+'------USER ORDERS------'+'\n'+user_order()
    return information
    

token = "1822|8CgIAMh5B7EoWv6gZ284LNuPxdmGMvjnklR5MQfQ1aeb7f0a"
info=all_merchant_information(1, token)

