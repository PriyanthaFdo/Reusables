// Created By Priyantha @27/Aug/2024

import 'package:flutter/material.dart';
import 'package:loading_indicator/loading_indicator.dart';

/// Uses `loading_indicator: ^3.1.1`
class LoadingIndicatorHandler {
  static final LoadingIndicatorHandler _instance = LoadingIndicatorHandler._internal();

  factory LoadingIndicatorHandler() {
    return _instance;
  }

  LoadingIndicatorHandler._internal();

  BuildContext? _context;

  void show(
    BuildContext context, {
    Color? color1,
    Color? color2,
    Color? color3,
    Color? color4,
    Color? color5,
  }) {
    if (_context != null) return; // Prevent showing another loading indicator if one is already displayed

    _context = context;
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) {
        return Center(
          child: SizedBox.square(
            dimension: 100,
            child: LoadingIndicator(
              indicatorType: Indicator.ballRotateChase,
              colors: [
                color5 ?? Colors.white,
                color4 ?? Colors.white,
                color3 ?? Colors.white,
                color2 ?? Colors.white,
                color1 ?? Colors.white,
              ],
            ),
          ),
        );
      },
    );
  }

  void dismiss() {
    if (_context != null) {
      Navigator.of(_context!).pop();
      _context = null;
    }
  }
}
