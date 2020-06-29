# Influx db

We use Influxdb as **persistent** data for openhab

# What is Influxdb ?

    - time series database
    - start = database(s) -> eg 'openhab'
        - measurements -> eg Emeter / Solar / AirQuality
            - field(s)  -> TotalKWhGrid_day, TotalKWhGrid_night, TotalKWhInj_day etc
            - tag(s)    = labels
    - Line Protocol:  





|Measurement|tag_set|field_set|timestamp|
|:---|:---|:---|:--|
|Gmeter|,type=FL99|m3=776.8|1465839830100400200 |
|Emeter|,version=1.0,type=1-fase|V=233 P=876|1465839830500800900 |

* tag_set => can bu multiple tags when separated by "comma"
* field_set => can be multiple when separated by "space'
* timestamp = RFC3339 time format = 1465839830100400200=2016-06-13T17:43:50.1004002Z



## Basic commands

Remember we have to attach a bash terminal onto a running container

So on pi execute:

'docker exec -it influxdb bash'

**Remark:** see under, we could simple start and open the  influxdb cli-console by typing 'influx' instead of 'influx -precission rfc3339' but then we would get the timestamp as an integer, eg: **'1465839830100400200'**, this is EPOC time format = elapsed time in nanosecods since 1 jan 1970. 

As humans we prefere something more readable like **2016-06-13T17:43:50.1004002Z**, this just what rfc3339 does.

```bash
# We are in the container 'base linux' but not yet into the influx DB so: 
influx -precision rfc3339           -> influx to start influx and rest is to get time in human readable format

CREATE DATABASE openhab
CREATE USER openhab WITH PASSWORD 'openhab' WITH ALL PRIVILEGES

show databases                      -> will list existing db's
show measurements                   -> will show measurement names in database

use opehab
select * FROM ...


```

### Database statistics

```bash
# In the linux container - use linux 'du = disk usage with -s=summary(all sub dirs) -h = human readable'
du -sh /var/lib/influxdb/data/              -> will return ...x MB for all databbases 
du -sh /var/lib/influxdb/data/openhab       -> will return ...x MB for db=openhabb

# -a gives all info per subdir
du -ah /var/lib/influxdb/data/

```

### Downsampling and Dataretention policies

When storing historical data:
* it can become a lot of data !
* the older the data, generally the less detail you need
* data must be 'actionable'

what does it mean:
* a lot of data = evident
* older data: eg. you might want 1sec interval E-power readings for the last 24h but after that might want 1min intercal or 15min interval. This is where **Continuuos Queries** help you to do this automatically. This is called **down-sampling**
* actionable: when deteriming what data you should keep is pretty simple. Ask yourself, what will I do whit it. Keeping GB's of data without 'action' on on is useless, slows down systems and application and cost money. Deleting unusefull data after some period is what **Retention policies** solve.

**CQ = Continuous Queries :** are queries that run automaticall & periodically and store the result in a new measurement
    - eg: downsample 1 sec data to 1 min average

**RP = Retention Policies :** defines how long you keep the data in the db.
    - eg: remove all 1sec interval data after 24h

**Examples:**

```bash
SHOW CONTINUOUS QUERIES
show retention policies
```

```bash
# example Continious Query
CREATE CONTINUOUS QUERY "downsampling_Solar_AC_Power" ON "openhab" BEGIN SELECT mean("Solar_AC_Power") AS "Solar_AC_Power" INTO "three_years"."ten_minute_Solar_AC_Power" FROM "two_weeks"."SolarInvertor" GROUP BY time(10m) END 

# example for workshop
CREATE CONTINUOUS QUERY "cq_downsampling_ActualPowerUsed" on "openhab" BEGIN SELECT mean("value") AS "ActualPower_1min_avg" INTO "one_month_PowerUsed" FROM "ActualPowerUsed" GROUP BY time(1m) END

# deleting  a continuous query
# DROP CONTINUOUS QUERY <queryName> on <database>
DROP CONTINUOUS QUERY cq_downsampling_ActualPowerUsed on openhab

# example Retention policy
CREATE RETENTION POLICY three_year ON openhab DURATION 156w REPLICATION 1;
CREATE RETENTION POLICY two_weeks ON openhab DURATION 2w REPLICATION 1 DEFAULT;
```

```bash
# enter influxdb application
influx -precision rfc3339  
show retention policies openhab
```


```bash
# getting the data
select * from ActualPowerUsed order by desc LIMIT 10
```

# deleting measurement data 
```bash
# this will delete all entries before that date
# remark time must in the format according to how you openned influx
# in case 'influx -precision rfc3339 -> time also in same format
use openhab
DELETE FROM Gasmeter WHERE time < '2020-06-15T06:42:04.853Z'

# in case you opened 'influx'-> NO rfc3339 !
DELETE FROM Gasmeter WHERE time < 1592334664000
```