# MLB Showdown
Project for re-creating MLB Showdown cards programmatically. I will scrape the data, save it as a csv, and then use league averages for that season to assign Control/Out for pitchers and On-base/Out for hitters. The final step is giving out values for each outcome on the player's chart, with the constraint that the outcomes add up to 20.

This may turn into a catch-all repo for baseball related programming, or at least until the other projects become too big for this repo. Currently the 'other projects' are limited to scraping and saving data on my Ottoneu league.

### TO DO:
<ul type='square'>
	<li> Rewrite Fangraphs scraper to get columns of interest in addition to the standard columns </li>
	<li> Assign Control/Out and On-base/Out </li>
	<li> Assign player chart outcomes: look into integer programming/optimization for this</li>
	<li> Assign IP for pitchers, and fielding and baserunning for hitters </li>
	<li> Look into any over 20 outcomes for players </li>
