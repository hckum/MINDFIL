Deployed
  http://ppirl2.herokuapp.com/

ppirl-userstudy/config.py

mode 1= not clickable all info<br>
mode 2= clickable, no meter<br>
mode 3= clickable, with meter, no limit<br>
mode 4= clickable, with meter, and limit (budget can be set)<br><br>

[host]/index?mode=1&id=1<br>
[host]/index?mode=4&budget=35<br>
[host]/index?mode=4&budget=minimum<br><br>

mode can take 1, 2, 3, 4, 5. <br>
budget [optional] can take any number from 0 to 100, and 'moderate', 'minimum'.<br>

Data collection:<br>
1. use [host]/pull_data_all to get the data.<br>
2. put it in the /data_analysis folder<br>
3. run:<br>
>> python raw2csv.py raw_data raw_data<br>

where the first parameter is the data file name, and second parameter is the output file name (it can be the same because the program will append .csv to the output file name, suppose the data filename is not 'raw_data.csv')

Instructions:
MINDFIRL/ppirl-userstudy/static/images/tutorial/clickable/slides/
