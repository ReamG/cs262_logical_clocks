# Testing

To run the unit tests, ensure that you have virtual environment set up and running. Then simply navigate to the tests folder and run `pytest`. There are 24 tests.

## What We Tested

We wrote comprehensive tests for every function in our `ConnectionManager` class as well as our `Machine` class. These two classes alone have complete coverage of the code required to run our experiments.

## Mocking

To mock complex system calls and socket events we put code in the `conftest.py` folder. Part of the `pytest` system imports this file before running the scripts, so by overriding the relevant modules we could replace actual sockets with our mocked socket class and precisely seed the random number generator.

Our mocked socket class contains flags for closing, binding, and listening, connecting, as well as information about the address used in these calls. We also maintain a list of things that were sent using the fake socket, as well as a queue that tests can fill with things they want to be returned from the next receive. This allows us to test both proper functionality, as well as expected and unexpected socket errors.

For the machine tests, we also made a mock `ConnectionManager` class stored in `test_utils.py`. The logic here is that since we've already written unit tests for the `ConnectionManager`, when we're testing the machine we should be able to abstract to a higher level and assume the underlying connections function as intended. Then, our mocked `ConnectionManager` simply helps us ensure that initialization functions are called at the proper times, the write information is sent/received, and shutting down connections is possible.
