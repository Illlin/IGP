# IGP

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
