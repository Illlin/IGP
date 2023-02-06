# IGP

## GitHub Workflow

To ensure a smooth and organized process, please follow these guidelines:

1. Clone the repository to your local machine.
2. Create a new branch for the changes you are making, using the format `<your-name>/<feature-name>` as the branch name. ie `Sol/ReadMe-Setup`
3. Make your changes and commit them to your branch.
4. Push your branch to the remote repository.
5. Open a pull request to merge your changes into the `main` branch.

**IMPORTANT**: Please do not make direct changes to the `main` branch. All changes should be made in separate branches and reviewed through pull requests to maintain a clean and organized codebase.

## Code practice
We won't be super strict about all the minutia, but please adhear to the general style of these. They are hear to help with readability and consistancy between developers.

### Python
We will be using Pep-8 for the python style guide.

[PEP 8 -- Style Guide for Python Code](https://peps.python.org/pep-0008/)

Example code
```python
# Add extra indentation for for extra arguments
# To help readability
def long_function_name(
        var_one, var_two, var_three,
        var_four):
    print(var_one)


# Variable names should use snake_case
long_variable_name = 10

# Class names should use PascalCase
class LongClassName:
    def __init__(self):
        print("Hello World")
```

### JavaScript
We will be using the Airbnb JavaScript Style Guide for our coding standards and style.

[Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)

Example code
```javascript
// Add extra indentation for for extra arguments
// To help readability
function longFunctionName(
  varOne, varTwo, varThree,
  varFour
) {
  console.log(varOne);
}

// Variable names should use camelCase
const longVariableName = 10;

// Class names should use PascalCase
class LongClassName {
  constructor() {
    console.log("Hello World");
  }
}
```
