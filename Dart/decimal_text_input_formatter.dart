// Generated using ChatGPT(v3.5) by Priyantha Fernando on 7/Feb/2024

// Update by Priyantha @03/Mar/2024

import 'package:flutter/services.dart';

class DecimalTextInputFormatter extends TextInputFormatter {
  final int decimalDigits;

  DecimalTextInputFormatter({required this.decimalDigits});

  @override
  TextEditingValue formatEditUpdate(
    TextEditingValue oldValue,
    TextEditingValue newValue,
  ) {
    // Handle backspace
    if (newValue.text.isEmpty) {
      return newValue;
    }

    // Remove non-digit characters
    String newText = newValue.text.replaceAll(RegExp(r'[^0-9.]'), '');

    // Split the text into integer and decimal parts
    List<String> parts = newText.split('.');

    // Ensure that only one dot is present
    if (parts.length > 2) {
      newText = parts[0] + '.' + parts[1];
      parts = newText.split('.');
    }

    // Keep only the specified number of decimal digits
    if (parts.length > 1 && parts[1].length > decimalDigits) {
      parts[1] = parts[1].substring(0, decimalDigits);
    }

    // Combine the integer and decimal parts
    newText = parts.join('.');

    // Return new TextEditingValue Object to trigger modifications
    return TextEditingValue(
      text: newText,
      selection: TextSelection.collapsed(offset: newText.length),
    );
  }
}
