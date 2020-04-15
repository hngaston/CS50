#include <stdio.h>
#include <cs50.h>
#include <math.h>


int main(void)
{
    float change;
    int coins = 0;
    int cents;

    do
    {
        change = get_float("Change owed: ");
    }
    // condition
    while (change < 0);

    cents = round(change * 100);

    // quarters
    while (cents >= 25)
    {
        coins = coins + 1;
        cents = (cents - 25);
    }

    // dimes
    while (cents >= 10)
    {
        coins = (coins + 1);
        cents = (cents - 10);
    }

    // nickels
    while (cents >= 5)
    {
        coins = (coins + 1);
        cents = (cents - 5);
    }

    // pennies
    while (cents >= 1)
    {
        coins = (coins + 1);
        cents = (cents - 1);
    }

    // output
    if (cents == 0)
    {
        printf("%i\n", coins);
    }
}
