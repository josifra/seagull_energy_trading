# Seagull Energy Trading tasks

Dear Jędrek, dear Marek,

**For the 1st task:**
I chose to compare the selected reference day with the current day, since this makes the evolution of the forecast immediately visible.
A refresh loop was added so the graph and CSV table update automatically every 30 minutes, which matches the update frequency of the dataset.
A small timestamp panel displays the last update time and the next scheduled refresh to make the process clearer.

_You will find everything of the TASK 1:_
https://github.com/josifra/seagull_energy_trading/tree/f5b02db403af2b785c1339481ac6e4635e21eac5/Task_1

**For the 2nd task:**
To the last question mentioned in the exercise: _what impact do you think the forecast error might have had on the system?_

When actual generation is lower than forecast (negative difference):
- The system must quickly find extra generation to fill the gap
- It may trigger reserve activation
- This increases balancing costs

_All the TASK 2 is here:_
https://github.com/josifra/seagull_energy_trading/tree/78e4405291d137167ebe772d55b3f8747e1ff0aa/Task_2

Kind regards,
Joris
