# ioetChallange

## Goal:

calculate the total that the company has to pay an employee, based on the hours they worked and the times during which they worked.

## Solution overview

Basically the first thing I do is separate the input into manageable pieces of information, for this I use the split method, unpacking the values to as many variables as I expect if the format was correct, in case the split returns more or less values than the expected it will throw a value error that I catch and raise a custom error (dataError) telling the user that the data is in the wrong format. When I have the information I need, then it converts the hours to minutes from 00:00 (for example "09:00" would be 540 minutes) so I can easily calculate and compare them. Following this, I look at what time slot the schedule would be located and thus calculate the payment.

the architecture is quite functional: the main.py file contains the calculate method, which is the important one, and two more methods that are auxiliary, also in that file is the wages class that defines the prices and schedules. it is structured so that it can be run as a script or call the functions from another file if needed.
then there are two more files: exceptions.py that saves the custom exceptions and tests.py that has the unit tests (a github action was created to run test in any push on master branch).

## Aproach and methodology

the main aproach was to wirte the tests first (simple ones and limit-cases) and trying to think the solution, then start coding. once the tests passed, I continued with commenting and tidying up the code.

## Run instructions
```
python main.py data.txt
```
the parameter should be a path to a data file
(you should have python installed)
