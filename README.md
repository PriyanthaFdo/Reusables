# Reusables
Some reusable modules created by me for various Quality of life and to ease my work

<hr />

## Android
#### CustomLogger.java
<p>A class that provides a set of static functions that can be used to make console logs. These functions, in additional to normal 'log' also displays the code location where this function is being called from. Also there are variations of this log functions that will write the logs into a "customLogs.txt" file within the application's files.</p>
<table>
  <tr>
    <td>static void logD(String message)</td>
    <td>Normal 'log.d' with calling location</td>
  </tr>
  <tr>
    <td>static void logE(String message)</td>
    <td>Normal 'log.e' with calling location</td>
  </tr>
  <tr>
    <td>static void logD(Context context, String message)</td>
    <td>Creates a logD and writes to file</td>
  </tr>
  <tr>
    <td>static void logE(Context context, String message)</td>
    <td>Creates a logE and writes to file with a preceding 'ERROR' tag</td>
  </tr>
</table>


## Node
#### logger.js
<p>This file provides 2 methods that can be imported and used in other js files. These methods will create console logs with calling filename and line. Provides ability to write log into a txt file</P>
<table>
  <tr>
    <td>logD(message, logToFile)</td>
    <td>Normal 'console.log()' with calling location. logToFile is optional. </td>
  </tr>
  <tr>
    <td>logE(message, logToFile)</td>
    <td>Normal 'console.error()' with calling location. logToFile is optional. </td>
  </tr>
</table>


## Python
#### extract_stops.py
<p>This script processes raw GPS data from a CSV file to detect vehicle stops, 
merge nearby consecutive stops, classify movement states, and enrich stops with 
human-readable location names using reverse geocoding.</p>

It is designed for analyzing GPS tracking datasets where:
- Each row contains a timestamp, latitude, and longitude.
- Gaps between points may indicate stops or GPS errors.