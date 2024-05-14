## What are Fixtures?

Fixture is a function that provides a fixed state or a set-up resources needed by python tests. 
The resources could be anything from simple data structures to complex objects, database, webserver or any other dependencies required by test functions. 
Fixed state refers to a consistent and predefined condition or setup that remains constant throughout the execution of one or more tests. It ensures that each test
starts with the same initial conditions, making the test results predictable and reliable.


## How to declare Fixture in python?

Fixtures are functions that are marked with the `@pytest.fixture` decorator. 
When a test function includes a fixture as an argument, pytest automatically calls the fixture function and passes its return value to the test function.


```python
import pytest

@pytest.fixture
def setup_database():
    # Setup database connection
    db = connect_to_database()
    yield db  # Provide the fixture value to the test function
    # Teardown logic
    db.close()

def test_query_data(setup_database):
    # Test logic using the setup_database fixture
    data = setup_database.query("SELECT * FROM table")
    assert len(data) > 0
```

### What is yield
`yield` is a keyword that is used in the context of generators and generator functions. When a function contains a `yield`
statement, it becomes a generator function. In the above example, `setup_database` serves as a generator function, responsible for generating the test database.

Instead of returning a single value and exiting, a generator function can yield 
multiple values over time, pausing execution between each yield.

```python
def generate_numbers():
    yield 1
    yield 2
    yield 3

# Using the generator function to produce values
numbers = generate_numbers()

print(next(numbers))  # Output: 1
print(next(numbers))  # Output: 2
print(next(numbers))  # Output: 3
```

## What are some common scenarios or use cases where fixtures are beneficial in pytest?
Fixtures in pytest can be used in various scenarios across test suite to set up and tear down resources, manage dependencies, and streamline testing workflows.
Here are some common scenarios where fixtures can be used:
- Setup and Teardown:  Fixtures can be used to set up and tear down resources required for testing, such as database connections, temporary files, web servers, etc.
- Configuration and Initialization:  Fixtures can be used to configure and initialize test environments, including setting up configuration settings, loading test data, and preparing the system for testing.
- Mocking and Stubbing: Fixtures can be used to mock or stub external dependencies, such as APIs, databases, or external services, allowing tests to isolate the code under test and control its behavior.
- Test Data Generation: Fixtures can generate test data dynamically, allowing tests to operate on realistic data sets and cover a wide range of scenarios without the need for manual data setup.
- Parameterization: Fixtures can be parameterized to create multiple instances of a fixture with different configurations, allowing tests to run with different inputs or setups and cover various test cases.

### Examples of Fixtures

* Setup and Teardown
  ```python
    # Fixture to set up a temporary SQLite in-memory database
    @pytest.fixture(scope="module")
    def db_engine():
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        yield engine
        Base.metadata.drop_all(engine)
        engine.dispose()
    ```
* Configuration and Initialization  
  `config.py`
    ```python
      # config.py   
    def load_config():
      # Load configuration settings from a file or any other source
      return {
          'database_url': 'sqlite:///:memory:',
          'api_key': '1234567890'
      }
    ```
  `test_config.py`
    ```python
      #test_config.py
      import pytest
      from config import load_config
      @pytest.fixture(scope='session')
      def config():
          # Load configuration settings
          return load_config()
        
      def test_database_url(config):
          assert 'database_url' in config
          assert config['database_url'] == 'sqlite:///:memory:'
        
      def test_api_key(config):
          assert 'api_key' in config
          assert len(config['api_key']) == 10
     ```
* Mocking and Stubbing
  `email_sender.py`
  ```python
    # email_sender.py

  import smtplib
  
  def send_email(to_address, subject, body):
      with smtplib.SMTP('smtp.example.com', 587) as server:
          server.starttls()
          server.login('username', 'password')
          server.sendmail('sender@example.com', to_address, f"Subject: {subject}\n\n{body}")
  ```
  `test_email_sender.py`
  ```python
  import pytest
  from unittest.mock import patch
  from email_sender import send_email
  
  @pytest.fixture
  def mock_smtp_connection():
      with patch('smtplib.SMTP') as mock_smtp:
          yield mock_smtp.return_value
  
  def test_send_email(mock_smtp_connection):
      # Configure the mock SMTP server
      mock_smtp_connection.starttls.return_value = None
      mock_smtp_connection.login.return_value = None
      mock_smtp_connection.sendmail.return_value = {}
  
      # Call the function under test
      send_email('recipient@example.com', 'Test Subject', 'Test Body')
  
      # Assert that the SMTP methods were called with the correct arguments
      mock_smtp_connection.assert_called_once_with('smtp.example.com', 587)
      mock_smtp_connection.starttls.assert_called_once()
      mock_smtp_connection.login.assert_called_once_with('username', 'password')
      mock_smtp_connection.sendmail.assert_called_once_with('sender@example.com', 'recipient@example.com', "Subject: Test Subject\n\nTest Body")
  ```
* Test Data Generation
  `data_generator.py`
  ```python
  #data_generator.py
  import random  
  def generate_random_numbers(n):
      return [random.randint(1, 100) for _ in range(n)]  
  ```
  `test_data_generation.py`
  ```python
  import pytest
  from data_generator import generate_random_numbers
  
  @pytest.fixture
  def random_numbers():
      # Generate 5 random numbers
      return generate_random_numbers(5)
  
  def test_sum_of_random_numbers(random_numbers):
      total = sum(random_numbers)
      assert total > 0
  
  def test_average_of_random_numbers(random_numbers):
      average = sum(random_numbers) / len(random_numbers)
      assert 1 <= average <= 100
  
  def test_max_of_random_numbers(random_numbers):
      maximum = max(random_numbers)
      assert maximum <= 100
  
  def test_min_of_random_numbers(random_numbers):
      minimum = min(random_numbers)
      assert minimum >= 1
  ```
* Parameterization
  ```python
  import pytest
  
  # Fixture with parameterization
  @pytest.fixture(params=[(1, 2), (3, 4), (5, 6)])
  def input_data(request):
      return request.param
  
  def test_addition(input_data):
      a, b = input_data
      assert a + b == a + b
  ```
