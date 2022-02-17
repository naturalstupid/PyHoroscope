PyHoroscope 0.9.5
=================

Observational Indian lunisolar calendar, horoscope and matching using the Swiss ephemeris (Hindu
Drig-ganita Panchanga).

Features
--------

Core Files:`panchanga.py`, `horoscope.py`, `compatibility.py` and `horo_chart.py`
 
Computation of the five essentials of the panchangam:
* Tithi
* Nakshatra
* Yoga
* Karana
* Vaara

Not just the values, but also the end times of tithis and nakshatras
are computed. The only factor limiting the accuracy of the program
output is the uncertainity in your input values (latitude, longitude).

Also includes computation of sunrise, sunset, moonrise and moonset.

Also Included :
* Instantaneous planetary positions, including Lagna (Ascendant)
* Navamsa positions
* Choghadiya/Gauri panchanga
* Vimsottari Dasha-Bhukti
* Rahu Kala, Yamaganda Kala, Gulika Kala
* Abhijit muhurta and Durmuhurtams

Available in English, Tamil and Telugu
-----------------------------------------

You can add your own language by creating `list_values_xx.txt` and `msg_strings_xx.txt`	by copying the _en files and replacing with appropriate native language strings.

Do not forget to add the new language into the `available_languages` in `horo_chart.py`

NOTE:
All timings are end timings. Timings displayed higher than 24:00 denote
hours past midnight because the Hindu day (tithi) starts and ends with
sunrise. If applicable, daylight savings (DST) are accounted for
automatically based on the date and place entered in the textboxes.


Requirements
------------

Python interface to Swiss ephemeris.

```
	pip install pyswisseph	# OR apt-get install pyswisseph
```
The core of the library (`panchanga.py` and `horoscope.py`) can be imported into other code
or used from the command line.

There are three UI files namely: `horo_chart.py`, `horo_chart_tabs.py` and `match_ui.py`.
`horo_chart.py` - provides a one page panchanga, rasi and navamsa charts
`horo_chart_tabs.py`- provides multi-tab/page panchanga, divisional charts and marriage compatibility
`match_ui.py` - provides just marriage compatibility between boy and girl based on their birh stars.

In order to just _run_ the GUI, you also need pyqt6:

```
    pip install pyqt6

```

Using the GUI
-------------

Enter Name, and Place with country name (e.g. Chennai, IN)
If you get an error, enter latitude, longitude and time zone manually.
If you want to be precise, enter the lat/long of the exact place (e.g. hospital)
You can use google to find the latitude, longitude, time zone of the place

Type the Date in YYY,MM,DD format in the 'Date' field. Negative value for YYYY are
interpolated as proleptic Gregorian calendar (Before Christ BC).

Enter Time of birth, choose chart style, ayanamsa mode, language of display

Click Show Chart to display the birth (Raasi and Navamsam) charts

Click Show PDF to save the screen as a PDF file

Using the Code / command line
------------------------------
```
	import horo_chart, panchanga, horoscope
    App = QApplication(sys.argv)
    chart_type = 'North'
    chart = horo_chart.ChartWindow(chart_type=chart_type)
    chart.language('Tamil')
    """
    chart.name('Krishna')
    chart.place('Mathura,IN')
    chart.date_of_birth('-3229,6,17')
    chart.time_of_birth('23:59:00')
    chart.time_zone('5.5')
    chart.chart_type(chart_type)
    chart.compute_horoscope()
    """
    chart.show()
```
Accuracy
--------

The program is as accurate as the Swiss Ephemeris installed on your system. So generally it is
accurate for years 13000 BCE to 16800 CE. The
computational speed stays the same no matter which date you enter. Required swiss ephimeres files are also /ephe/ folder of this repository.
Overall size of these files is more than 100 MB. To reduce your application size, you can restrict the dates within a range and could remove those ephimeres files from the folder.

Personal Opinion:
------------------
When using BC dates (such as mahabharatha dates) it is advised to use `SURYA_SIDHANTHA` or `SUNDAR_SS` as ayanamsa styles, as ayanamsa values of every other ayanamsa types such as `LAHIRI, KP` etc are inaccurate. 
`SUNDAR_SS` is a sine curve forcing zero ayanamsa every 3200 years from -3101 BCE and 27 degrees as peak ayanamsa.

License
-------

MIT License.

