#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // Get variable
    string name = get_string("What is your name\n");
    // Execute variable
    printf("hello, %s\n", name);
}
