/// Created By Priyantha Fernando
/// on 30-Oct-2023
/// 
/// This widget can be used to easily deactivate any widget.
/// This will remove all pointer interactions 
/// and add an opacity when deactivated
import 'package:flutter/material.dart';

class Deactivate extends StatelessWidget {
  final Widget child;
  final bool deactivate;
  final double deactivatedOpacity;
  const Deactivate({
    Key? key,
    required this.child,
    required this.deactivate,
    this.deactivatedOpacity = 0.3,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return IgnorePointer(
      ignoring: deactivate,
      child: Opacity(
        opacity: deactivate ? deactivatedOpacity : 1,
        child: child,
      ),
    );
  }
}
