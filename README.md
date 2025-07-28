# Robot Coding Challenge

## Challenge Overview 
This challenge forms part of a developer coding challenge, described [here](/instructions.md)

## My experience / observations 
Are detailed [here](/observations.md)

## Running the game 
Execute `python src/main.py` from the root folder. The debug logs can be found (once generated), in the `/logs` folder. The logging level should be set to `DEBUG` (if it has been changed) to ensure a detailed level of logs.

## Running the tests 
Execute `pytest` from anywhere within the project. Executing it from the root folder will result in errors (due to the relative referencing of the input file)

## Known issues 
- Test coverage is extremely limited, only to validate the output data (as expected in the given worksheet). I hope to retrospectively instrument the testing for the models, processor and game over the next few days (time permitting). I'm mindful that retrospective unit test creation is not an appropriate developer workflow, but this was the manner in which this work was completed. 

- The git commit log has not been rebased on a per feature basis, or a meaningful commit history

- The abstractions may have bled across the various models. There could be work to ensure that the Single Responsibility Principle is more closely adhered to 

- There are no doubt, many other issues, but I'm hopeful that this challenge is not viewed in the light of me coming from a professional Software Engineering background