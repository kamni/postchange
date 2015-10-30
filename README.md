# Post Change

## The Challenge

German stamp machines are a really good way to get rid of loose change. Just
take your loose change to the machine, and voila! You have something useful,
while getting rid of a bunch of those low-denomination coins.

So how do you maximize the number of coins that you get rid of when buying a
stamp?

The constraints of the problem are this:

1. German stamp machines only allow up to 15 coins (so you can't just use
all 1-cent coins).
2. You don't want change, because the stamp machine give change in stamps
with weird denominations (like 1- and 2- cent stamps, which you then have to
somehow figure out how to use).
3. You probably have a limit to the number of coins of any given denomination
you have. For example, you may only have 8 1-cent coins, but you may have 20
2-cent coins.

There are other real-world constraints:

1. You can't have a negative number of coins.
2. Solutions to this problem have to be integers (because you can't have half
a coin).

## The Project

This is just an exploration of different ways to solve this problem. Why?
Because buying stamps has never been so much fun...

There are plenty of great libraries out there for doing integer programming,
but this is an exploriation into the algorithms themselves. All but the first
solution (a POC spreadsheet to show that the problem is solvable) try to rely
as little as possible on external libraries.

## Trying Out Existing Solutions

Most solutions require an installation of Python 2.7. The solutions may work
on other versions of Python, but they have not explicitly been tested against
them.

### Solution 1: spreadsheet

This is a simple Apache OpenOffice spreadsheet (version 4.1.1) that uses the
built-in solver. Open the spreadsheet and configure it as follows:

* In Row 3, cells D-I, enter how many of each coin you have. For example, if
you have 4 .50-cent coins, enter 4 in cell D3. If the number does not matter,
then use some number (e.g., 100) larger than the max number of coins the
machine will take.
* In cell D5, enter the cost of a stamp.
* In cell D6, enter the max number of coins that the machine will take.

Next, you need to configure the solver. Go to the menu for Tools -> Solver...
and enter the following:

* Target cell: $I$11
* Optimize result to: Maximum
* By changing cells: $C$11:$H$11
* Limiting conditions:
  * $I$13  <=  $K$13
  * $I$14  =  $K$14  <-- Take special note that this is '='
  * $I$16  <=  $K$16
  * $I$17  <=  $K$17
  * $I$18  <=  $K$18
  * $I$19  <=  $K$19
  * $I$20  <=  $K$20
  * $I$21  <=  $I$21

Hit the 'Solve' button, and then choose 'Keep Result'. The number of each coin
that you should use is in Row 11, cells C-H.