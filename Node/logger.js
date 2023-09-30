import fs from 'fs';
import path from 'path';

function extractClassNameAndLineNumber(caller) {
  const regex = /\((.*?):(\d+):\d+\)/;
  const matches = regex.exec(caller);
  if (matches) {
    return [matches[1], matches[2]];
  }
  return ['', ''];
}

function writeToFile(logMessage) {
  const filename = 'logs';

  try {
    const filePath = path.join(__dirname, filename);
    const dateTime = new Date().toISOString();
    fs.appendFileSync(filePath, `${dateTime} - ${logMessage}\n`);
  } catch (error) {
    console.error('Write to customLog File failed');
  }
}

function logD(message, logToFile = false) {
  const caller = new Error().stack.split('\n')[2];
  const [className, lineNumber] = extractClassNameAndLineNumber(caller);
  const logMessage = `${className}:${lineNumber} | ${message}`;
  console.log(logMessage);
  if (logToFile) {
    writeToFile(logMessage);
  }
}

function logE(message, logToFile = false) {
  const caller = new Error().stack.split('\n')[2];
  const [className, lineNumber] = extractClassNameAndLineNumber(caller);
  const logMessage = `Error - ${className}:${lineNumber} | ${message}`;
  console.error(logMessage);
  if (logToFile) {
    writeToFile(logMessage);
  }
}

export { logD, logE };
