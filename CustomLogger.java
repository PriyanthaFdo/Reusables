import android.content.Context;
import android.util.Log;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

/*
	Created By Priyantha Fernando on 21/04/2023

	This Logger makes a normal android Log.d()/ Log.e()
	additionally it logs the calling Classname and the lineNumber

  ---Variations---
	static logD(String message);
	static logE(String message);
	
    -Following versions will also write to customLogs.txt file-
	static logD(Context context, String message);
	static logE(Context context, String message);
*/

public class CustomLogger {
  public static final String LOGGER_TAG = "TMS";

  public static void logD(String message) {
    StackTraceElement[] stackTrace = Thread.currentThread().getStackTrace();
    StackTraceElement caller = stackTrace[3]; // 3rd element is the caller of this method
    String className = caller.getClassName();
    int lineNumber = caller.getLineNumber();
    Log.d(LOGGER_TAG, className + ":" + lineNumber + " | " + message);
  }


  public static void logE(String message) {
    StackTraceElement[] stackTrace = Thread.currentThread().getStackTrace();
    StackTraceElement caller = stackTrace[3]; // 3rd element is the caller of this method
    String className = caller.getClassName();
    int lineNumber = caller.getLineNumber();
    Log.e(LOGGER_TAG, className + ":" + lineNumber + " | " + message);
  }


  // This logger versions will also write to a file
  public static void logD(Context context, String message) {
    StackTraceElement[] stackTrace = Thread.currentThread().getStackTrace();
    StackTraceElement caller = stackTrace[3]; // 3rd element is the caller of this method
    String className = caller.getClassName();
    int lineNumber = caller.getLineNumber();

    String logMessage = className + ":" + lineNumber + " | " + message;
    Log.d(LOGGER_TAG, logMessage);
    writeToFile(context, logMessage);
  }


  public static void logE(Context context, String message) {
    StackTraceElement[] stackTrace = Thread.currentThread().getStackTrace();
    StackTraceElement caller = stackTrace[3]; // 3rd element is the caller of this method
    String className = caller.getClassName();
    int lineNumber = caller.getLineNumber();

    String logMessage = className + ":" + lineNumber + " | " + message;
    Log.e(LOGGER_TAG, logMessage);
    writeToFile(context, "ERROR | " + logMessage);
  }


  private static void writeToFile(Context context, String logMessage) {
    try {
      File internalStorageDir = context.getFilesDir();
      File file = new File(internalStorageDir, "customLogs.txt");
      FileWriter writer = new FileWriter(file, true);

      SimpleDateFormat dateFormat = new SimpleDateFormat("dd-MMM-yyyy HH:mm:ss.SSS", Locale.getDefault());
      String dateTime = dateFormat.format(new Date());

      writer.write(dateTime + "  -  " + logMessage + "\n");
      writer.close();
    } catch (IOException e) {
      Log.e(LOGGER_TAG, "Write to customLog File failed");
    }
  }

}