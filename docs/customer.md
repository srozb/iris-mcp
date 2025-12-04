# [Customers ](#module-dfir_iris_client.customer)

*class* dfir\_iris\_client.customer. Customer ( *session* ) [](#dfir_iris_client.customer.Customer)

Handles the customer methods

get\_customer\_by\_id (

*customer\_id : int* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.customer.Customer.get_customer_by_id)

Returns a customer from its ID

Parameters :

**customer\_id** - Customer ID to look up

Returns :

ApiResponse object

list\_customers ( ) →

[ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.customer.Customer.list_customers)

Returns a list of the available customers

Returns :

ApiResponse object

Args:

Returns :

ApiResponse object

lookup\_customer (

*customer\_name* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.customer.Customer.lookup_customer)

Returns a customer ID if customer name is found. Customer names are unique in the database.

Customer ID is in the data section of the API response aka id = parse\_api\_data(resp.get\_data(), 'customer\_id')

Parameters :

**customer\_name** - Name of the customer to lookup

Returns :

ApiResponse object