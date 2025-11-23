# seagull_energy_trading

Dear Jędrek, dear Marek,

For the 1st exercice, I chose to compare the selected reference day with the current day, since this makes the evolution of the forecast immediately visible.
The script reconstructs each full day according to the API structure (periods 47–48 from the previous UTC day + periods 1–46).

A second plot shows the forecast change (visual indicator), which is simply the difference between today’s imbalance and the reference day.

A refresh loop was added so the graph and CSV table update automatically every 30 minutes, which matches the update frequency of the dataset.
A small timestamp panel displays the last update time and the next scheduled refresh to make the process clearer.

Here you have the full code:
The table: 
And the graph:

For the second exercise:
