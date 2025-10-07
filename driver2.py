import requests
import json
import time
import concurrent.futures
import itertools

# Kubernetes service names (for local development in Kubernetes)
USER_SERVICE_URL = "http://10.103.72.32:31879/"  # Kubernetes service name
PRODUCT_SERVICE_URL = "http://10.103.72.32:31342"  # Kubernetes service name
ORDER_SERVICE_URL = "http://10.103.72.32:31520"  # Kubernetes service name

# Function to create a user (this will call the User Service)
def create_user(username, email):
    url = f"{USER_SERVICE_URL}/user"
    data = {
        "username": username,
        "email": email
    }
    start_time = time.time()
    response = requests.post(url, json=data)
    response_time = time.time() - start_time
    if response.status_code == 201:
        return response.json(), response_time
    else:
        print(f"Failed to create user: {response.text}")
        return None, response_time

# Function to add a product (this will call the Product Service)
def create_product(name, price):
    url = f"{PRODUCT_SERVICE_URL}/product"
    data = {
        "name": name,
        "price": price
    }
    start_time = time.time()
    response = requests.post(url, json=data)
    response_time = time.time() - start_time
    if response.status_code == 201:
        return response.json(), response_time
    else:
        print(f"Failed to create product: {response.text}")
        return None, response_time

# Function to create an order (this will call the Order Service, which internally calls User and Product Services)
def create_order(user_id, product_id):
    url = f"{ORDER_SERVICE_URL}/order"
    data = {
        "user_id": user_id,
        "product_id": product_id
    }
    start_time = time.time()
    response = requests.post(url, json=data)
    response_time = time.time() - start_time
    if response.status_code == 201:
        return response.json(), response_time
    else:
        print(f"Failed to create order: {response.text}")
        return None, response_time

# Function to run all steps for creating a user, product, and order
def run_process(username, email, product_name, product_price):
    # Step 1: Create a user
    user, user_time = create_user(username, email)
    if not user:
        return None, user_time, "Failed"

    # Step 2: Create a product
    product, product_time = create_product(product_name, product_price)
    if not product:
        return None, product_time, "Failed"

    # Step 3: Create an order
    order, order_time = create_order(user["user_id"], product["product_id"])
    if not order:
        return None, order_time, "Failed"

    # Return the response and the total time taken along with the status
    return order, user_time + product_time + order_time, "Success"

# Driver function that integrates everything
def main():
    # Ask user how many processes they want to execute concurrently
    num_processes = int(input("Enter the number of processes to execute concurrently: "))
    ramp_up_time = int(input("Enter the ramp-up time in seconds between each request: "))

    # Ensure product names and prices repeat properly if num_processes is smaller than 3
    product_names = ["Laptop", "Phone", "Tablet"]
    product_prices = [1000, 500, 700]

    # Use itertools.cycle to repeat product names and prices
    product_names = list(itertools.islice(itertools.cycle(product_names), num_processes))
    product_prices = list(itertools.islice(itertools.cycle(product_prices), num_processes))

    # Prepare the list of concurrent tasks
    usernames = [f"user_{i}" for i in range(num_processes)]
    emails = [f"user{i}@example.com" for i in range(num_processes)]

    # Track overall statistics
    total_requests = 0
    total_response_time = 0
    successful_requests = 0
    failed_requests = 0
    start_time = time.time()

    # Use a ThreadPoolExecutor to handle concurrency
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_processes) as executor:
        future_to_process = {
            executor.submit(run_process, usernames[i], emails[i], product_names[i], product_prices[i]): i
            for i in range(num_processes)
        }

        for future in concurrent.futures.as_completed(future_to_process):
            process_id = future_to_process[future]
            try:
                order, process_time, status = future.result()
                if status == "Success":
                    total_requests += 1
                    successful_requests += 1
                    total_response_time += process_time
                else:
                    failed_requests += 1
                    print(f"Process {process_id} failed")
            except Exception as exc:
                print(f"Process {process_id} generated an exception: {exc}")
                failed_requests += 1

            # Ramp up time: wait before next process
            if ramp_up_time > 0:
                time.sleep(ramp_up_time)

    end_time = time.time()
    total_time = end_time - start_time

    # Calculate average throughput and response time
    average_throughput = total_requests / total_time
    average_response_time = total_response_time / total_requests if total_requests > 0 else 0

    print(f"\nTotal processes executed: {total_requests}")
    print(f"Total processes failed: {failed_requests}")
    print(f"Total time taken: {total_time:.2f} seconds")
    print(f"Average throughput: {average_throughput:.2f} requests/second")
    print(f"Average response time: {average_response_time:.2f} seconds")

if __name__ == '__main__':
    main()
