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
