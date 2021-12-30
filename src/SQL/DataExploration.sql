-- 



-- create a temp table with data from all years
CREATE TABLE #temp_all_years (
[DateTime] datetime,
station varchar(255),
cyclists float
);



Insert into #temp_all_years
Select * From data_2012$
Union 
Select * From data_2013$
Union 
Select * From data_2013$
Union 
Select * From data_2014$
Union 
Select * From data_2015$
Union 
Select * From data_2016$
Union 
Select * From data_2017$
Union 
Select * From data_2018$
Union 
Select * From data_2019$
Union 
Select * From data_2020$;

Select * from #temp_all_years;


-- seperating data between night and day
-- using Datepart is similar to 'extract'
Select *,
Case
	When DATEPART(HOUR,DateTime) Between 6 And 21 Then 'Day'
	Else 'Night'
End As Phase
Into #temp_phase
From #temp_all_years
order by DateTime;

-- calculate average over day and night in general
Select Phase, AVG(cyclists) as average 
From #temp_phase
Group By Phase;


-- compare the average of cyclists of every station with the average of all stations
With station_averages as(
Select station, AVG(cyclists) as average
From #temp_all_years
Group By station
),
total_average_table as(
Select AVG(cyclists) as total_average
From #temp_all_years
)
Select distinct a.station, a.average, ta.total_average, abs(ta.total_average - a.average) as diff, ((a.average*100)/ta.total_average) as percentage
From station_averages a right join total_average_table ta 
on 1=1
Order by percentage DESC;


-- Get the average number of cyclists within an hour
Select DATEPART(HOUR, d.DateTime) as Hour, AVG(cyclists) as Average_of_cyclists
From #temp_all_years d
Group By DATEPART(HOUR, d.DateTime)
Order By Average_of_cyclists DESC;


-- classify every station in ont of the four regions of Berlin 
-- then count where the stations are located
-- 52.501389, 13.402500 is the central point of Berlin
IF OBJECT_ID('tempdb..#temp_regions') Is Not Null Drop Table #temp_regions
Go
Select *
Into #temp_regions
From (
Select *, 
Case
	When Breitengrad > 52.501389 And Laengengrad > 13.402500 then 'North-East'
	When Breitengrad < 52.501389 And Laengengrad > 13.402500 then 'South-East'
	When Breitengrad > 52.501389 And Laengengrad < 13.402500 then 'North-West'
	When Breitengrad < 52.501389 And Laengengrad < 13.402500 then 'South-West'
	Else 'central'
End as relative_location
From data_location$) loc;

Select *
From #temp_regions;

Select count(Zaehlstelle) as number_stations, relative_location
From #temp_regions
Group by relative_location;



-- where are the most bicycles grouped by region
-- use only values since 2016 because from this year on all stations are installed
Select distinct r.relative_location, 
Sum(c.cyclists) over(Partition By r.relative_location) as num_cyclists
From #temp_regions r Join #temp_all_years c
on r.Zaehlstelle = c.station
where DATEPART(YEAR, c.Datetime) >= 2016
Order By num_cyclists DESC



-- check the development of biking in berlin over the years, and over months
Select DATEPART(YEAR, Datetime) as year, AVG(cyclists) as average_total
From #temp_all_years
Group By DATEPART(YEAR, Datetime)
order By year

Select DATEPART(MONTH, Datetime) as MONTH, AVG(cyclists) as average_total
From #temp_all_years
Group By DATEPART(MONTH, Datetime)
order By MONTH



-- compare the two directions of every point with two stations
-- First some data cleaning
Update data_location$ 
Set [Beschreibung - Fahrtrichtung]='Yorckstra�e West'
Where Zaehlstelle = 'yorw';

Select [Beschreibung - Fahrtrichtung], AVG(cyclists) as 'AVG #cyclists'
From #temp_all_years years Join (
Select Zaehlstelle, [Beschreibung - Fahrtrichtung]
From data_location$ 
Where [Beschreibung - Fahrtrichtung] Like '%S�d' 
	OR [Beschreibung - Fahrtrichtung] Like '%Nord'
	OR [Beschreibung - Fahrtrichtung] Like '%West'
	OR [Beschreibung - Fahrtrichtung] Like '%Ost'
	) pairs
on years.station = pairs.Zaehlstelle
Group by [Beschreibung - Fahrtrichtung];


-- which station has the most error values
Select station, Count(cyclists) as num_errors
From #temp_all_years
where cyclists = -1
Group By station
Order By num_errors DESC


-- select how many cyclists pass the stations until this time of day
-- this data only makes sense if you filter for one single station
Select DateTime, station, cyclists, Sum(cyclists) Over ( Partition by (CAST(DATEPART(Month, Datetime) as varchar)+Cast(DATEPART(Day, Datetime) as varchar))
	Order by DateTime
	ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as 'Count cycists'
From data_2020$
-- where station = 'obw'
Order by DateTime;


-- Categorize station based on their directions
IF OBJECT_ID('tempdb..#temp_directions') Is Not Null Drop Table #temp_directions
Go
Select *
Into #temp_directions
From (
Select *, 
Case
	When [Beschreibung - Fahrtrichtung] like '% Nord' then 'North'
	When [Beschreibung - Fahrtrichtung] like '% S�d' then 'South'
	When [Beschreibung - Fahrtrichtung] like '% West' then 'West'
	When [Beschreibung - Fahrtrichtung] like '% Ost' then 'East'
	Else 'no direction'
End as direction
From data_location$) direction;

-- In which direction do cyclists drive at which time?
Select AVG(y.cyclists) as number_cyclists, d.direction, DATEPART(HOUR, y.dateTime) as Time
From #temp_all_years y Join #temp_directions d
on y.station = d.Zaehlstelle
Where direction not like 'no direction'
Group By d.direction, DATEPART(HOUR, y.dateTime)
order by Time ;

-- In which direction do cyclists drive most?
Select sum(y.cyclists) as number_cyclists, d.direction
From #temp_all_years y Join #temp_directions d
on y.station = d.Zaehlstelle
Where direction not like 'no direction'
Group By d.direction
order by number_cyclists DESC;

-- Compare working days against weekend
Select AVG(cyclists) as #cyclists, weekday
From (
Select *, 
Case
	When DatePart(WEEKDAY, DateTime) = 6 or DatePart(WEEKDAY, DateTime) = 7 then 'weekend'
	Else 'working day'
End as weekday
From #temp_all_years) weekdays
Group By weekday;

-- When do the most errors occur?
Select DATEPART(MONTH, Datetime) as MONTH, count(cyclists) as error_num
From #temp_all_years
Where cyclists = -1
Group By DATEPART(MONTH, Datetime)
Order By error_num DESC;

-- At which Station do most errors occur?
-- I divide the total errors at each station by the number of months it is running to get a comparible result. As the stations started their service at different dates.
With #errors_station as (
	Select distinct l.[Beschreibung - Fahrtrichtung], l.Installationsdatum, count(cyclists) Over (Partition By l.[Beschreibung - Fahrtrichtung]) as error_num
	From #temp_all_years d Join data_location$ l
	On d.station = l.Zaehlstelle
	where d.cyclists = -1)
Select [Beschreibung - Fahrtrichtung], error_num as total_errors,  Round(Cast(error_num as float)/Cast(DATEDIFF(MONTH, installationsdatum, CAST('31/12/2020' as date)) as float), 3) as errors_per_month
From #errors_station
Order By errors_per_month DESC;