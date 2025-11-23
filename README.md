# Seagull Energy Trading tasks

Dear Jędrek, dear Marek,

**For the 1st task:**
I chose to compare the selected reference day with the current day, since this makes the evolution of the forecast immediately visible.
A refresh loop was added so the graph and CSV table update automatically every 30 minutes, which matches the update frequency of the dataset.
A small timestamp panel displays the last update time and the next scheduled refresh to make the process clearer.

You will find everything of the TASK 1

**For the 2nd task:**
To the last question mentioned in the exercise: _what impact do you think the forecast error might have had on the system?_

When actual generation is lower than forecast (negative difference):
- The system must quickly find extra generation to fill the gap
- It may trigger reserve activation
- This increases balancing costs

All the TASK 2 is here
