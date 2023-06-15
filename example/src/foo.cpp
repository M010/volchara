#include "foo.hpp"
#include <iostream>

void foo() {
        for (int num = 1; num <= 100; num += 1)
    {
        if ((num % 3 == 0) && (num % 5 == 0))
        {
            std::cout << "FizzBuzz" << std::endl;
        }
        else if (num % 3 == 0)
        {
            std::cout << "Fizz" << std::endl;
        }
        else if (num % 5 == 0)
        {
            std::cout << "Buzz" << std::endl;
        }
        else if (num % 75 == 0)
        {
            std::cout << "Fizz" << std::endl;
        }
        else
        {
            std::cout << num << std::endl;
        }
    }
}