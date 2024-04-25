// Created by Priyantha Fernando @25/Apr/2024

/// Use this class to encapsulate an item of type [T] and track its selection state.
/// The selection state can be toggled using the [isSelected] property.
///
/// Example:
/// ```dart
/// SelectableItem<String> item = SelectableItem(item: "Example");
/// print(item.isSelected); // Outputs: false (default)
///
/// item.isSelected = true;
/// print(item.isSelected); // Outputs: true
/// ```
class SelectableItem<T> {
  /// Item of type [T] held by [SelectableItem] object
  T item;

  /// Indicates current selection state.
  ///
  /// Defaults to `false`.
  bool? isSelected;

  /// Constructs a [SelectableItem] object that encapsulates an item of type [T] and manages its selection state.
  ///
  /// The [item] parameter is required and represents the item of type [T] that this [SelectableItem] holds.
  ///
  /// The [isSelected] parameter is optional and defaults to `false`. It indicates the initial selection state
  /// of the item. Set it to `true` if you want the item to be initially selected.
  ///
  /// Example:
  /// ```dart
  /// // Create a SelectableItem with a string item that is initially selected
  /// SelectableItem<String> selectedItem = SelectableItem(item: "Example", isSelected: true);
  /// print(selectedItem.isSelected); // Outputs: true
  /// print(selectedItem.item); // Outputs: Example
  /// ```
  ///
  /// The [isSelected] state can be changed later by directly accessing or modifying the [isSelected] property.
  ///
  /// Note: The [T] type must be specified when creating a new instance of [SelectableItem].
  ///
  /// Throws an [ArgumentError] if [item] is not provided.
  SelectableItem({
    required this.item,
    bool? isSelected = false,
  });
}
