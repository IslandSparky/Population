# Population
Plot of the population fractal equation.

The population fractal equation produces interesting fractal plots as it is interated through ranges of the scaling variable.

The basic simple non-linear equation is:
    new_x = lambda * old_x * (1 - old_x) or alternatively:

    new_x = lamba * (old_x - old_x ** 2)

for each value of lambda in the range of 0 to 4 the program interates the equation thousands of times and
plots a color weighted plot of the results.

The plot shows typical chaotic results with bifircation and self similiar fractals. 

The physical implication can be thought of as a simple model of a close population where lambda represents a population gain multiplier and x is the population at each point in time for a given lambda.
The results show how populations can lock on to a series of semi-stable values.

More importantly, it shows how very chaotic behavior can result from even simple non-linear systems.  Something to think about when preturbing large non-linear systems such as the earth's climate.

# Usage 

left mouse button zooms in to the area where the mouse is pointing

right mouse button zooms out from the area where the mouse is pointing

center mouse button toggles to an alternate view showing the locus of plots on the basic parabolic equation. 

# Notes
Requires that the user download the pygame library into their library path. 