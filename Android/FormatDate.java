package com.kingslake.tms2.utils;

import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;

/**
 * Created Priyantha Fernando on 18/07/2023
 * Last updated by Priyantha Fernando on 18/07/2023
 */
public class FormatDate {
  /**
   * Converts input unixTimeStamp [String] into required format
   * @param pattern <br />
   * MM - month <br />
   * HH - 24 hrs format <br />
   * hh - 12 hrs format <br />
   * mm - minute <br />
   * ss - second <br />
   * @param unixTimeString unixTimeStamp in milliseconds
   * @return formatted dateTime [String]
   */
  public static String formatDate(String pattern, String unixTimeString) {
    long unixTime = Long.parseLong(unixTimeString);

    // Convert Unix time to LocalDate
    Instant instant = Instant.ofEpochMilli(unixTime);
    LocalDateTime date = instant.atZone(ZoneId.systemDefault()).toLocalDateTime();

    // Format the date with the given pattern
    DateTimeFormatter formatter = DateTimeFormatter.ofPattern(pattern);

    return date.format(formatter);
  }
}
