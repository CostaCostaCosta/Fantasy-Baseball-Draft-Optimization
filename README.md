# Fantasy-Baseball-Draft-Optimization
The goal of this project is to turn existing projection systems into actionable data for different types of fantasy baseball leagues.

Data sources: fangraphs.com is used extensively for base data. Projection systems such as steamer, atc, as well as their auctiontool are used to create the base data.

You'll need jupyter to run the notebooks, and anaconda packages.

What is done:
Salary Points League - Leagues without a draft, and all players are available at a fixed cost.
Auction Roto League - Auction draft style league with different hitting/pitching categories. Live draft optimization is available.

What needs to be done:
New Auction value calculator - fangraphs auction calculator provides a good starting point for projection -> auction value, but it should be improved upon
Auction Points League
Snake Draft Simulator
Improved roto function*

*The objective function for roto leagues is simple addition of categories. The optimal objective function should change on the interval length of the league, and can be modeled on historic league data.
