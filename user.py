import requests
import json

def get_request(base_url, endpoint, token=None):
    # Combine base URL and endpoint to form the full URL
    url = f"{base_url}/{endpoint}"
    
    # Prepare headers if token is provided
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    try:
        # Make the GET request
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Return the JSON response
            return response.json()
        else:
            # Print the error code and message if not successful
            print(f"Error: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def fetch_all_orders(base_url, initial_endpoint, token=None):
    orders = []
    page = 1
    while True:
        endpoint = f"{initial_endpoint}&page={page}"
        
        try:
            response_data = get_request(base_url, endpoint, token)
            
            # Check if the response contains valid data
            if response_data and isinstance(response_data, dict) and 'data' in response_data:
                if not response_data['data']['orders']: 
                    return orders
                print(f"Fetching page {page}...")
                orders.extend(response_data['data']['orders'])
                page += 1
            else:
                # If the page has no valid data, log and move to the next page
                print(f"Page {page} has missing or invalid data. Skipping to the next page.")
                page += 1
        except Exception as e:
            # Handle any errors that occur while fetching or processing the page
            print(f"Error on page {page}: {e}. Skipping to the next page.")
            page += 1
        
    # Optionally, you can set a condition to stop after a certain number of pages or after consecutive errors
    return orders
    
def dict_to_string(d):
    # Convert each key-value pair in the dictionary to a formatted string
    formatted_str = ""
    for key, value in d.items():
        formatted_str += f"{key}: {value}\n"
    return formatted_str
def extract_basic_order_info(order_data):
    # Extract basic order information
    if order_data.get('voucher', {}):
        merchant_name=order_data.get('voucher', {}).get('merchant')
    elif order_data.get('event', {}):
        merchant_name=order_data.get('event', {}).get('merchant_name')
    else:
        merchant_name='N/A'
    if order_data.get('voucher', {}):
        category=order_data.get('voucher', {}).get('category')
    elif order_data.get('event', {}):
        category=order_data.get('event', {}).get('category_name')
    else:
        category='N/A'
    basic_info = {
        'order_number': order_data.get('order_num'),
        'order_date': order_data.get('created_at'),
        'merchant_name':merchant_name,
        'category': category,
        'type': order_data.get('type', {}),
        'status': order_data.get('status', {}),
        'final total':  order_data.get('final_total', {})
    }
    
    return basic_info
# Function to filter orders based on provided filters
def filter_orders(orders, **filters):
    def match(order, filters):
        return all(order.get(k) == v for k, v in filters.items() if v)
    return [order for order in orders if match(order, filters)]

