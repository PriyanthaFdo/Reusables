/*
 * Created by Priyantha Fernando 18/07/2023 <br />
 * Last updated on 18/07/2023
 */

public class Alerts{
    /**
     * Create a Alert message with a title and a message. <br />
     * @Buttons ok
     */
    public static void createTextAlert(Context context, String title, String message) {
        AlertDialog.Builder builder = new AlertDialog.Builder(context);
        builder.setTitle(title);
        builder.setMessage(message);
        builder.setPositiveButton("OK", (dialog, which) -> dialog.cancel());
        builder.show();
    }

    /**
     * Create a Alert dialog that will auto dismiss after [seconds]
     * @Buttons none
     */
    public static void createAutoDismissAlert(Context context, String message, double seconds) {
        AlertDialog.Builder builder = new AlertDialog.Builder(context);
        builder.setMessage(message);

        final AlertDialog alertDialog = builder.create();
        alertDialog.show();

        // Create a Handler and post a delayed Runnable to dismiss the dialog after given seconds
        new Handler().postDelayed(() -> {
            if (alertDialog.isShowing())
                alertDialog.dismiss();

        }, (long) (seconds * 1000L));
    }

    /**
     * Callback interface to be used in inputAlert
     */
    public interface Callback {
        void onInputReceived(String value);
    }

    /**
     * AlertDialog with a password type input field<br />
     * Activates callback if input value is not Empty <br />
     * Change the [setInputType()] if want to change the input type
     * @Buttons ok, cancel
     */
    public static void createInputAlert(Context context, String title, Callback callback){
        final EditText input = new EditText(context);
        input.setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_VARIATION_PASSWORD);

        AlertDialog.Builder builder = new AlertDialog.Builder(context);
        builder.setTitle(title);
        builder.setView(input);
        builder.setPositiveButton("OK", (dialog, which) -> {
            ((AlertDialog) dialog).getButton(AlertDialog.BUTTON_POSITIVE).setEnabled(false);
            String value = input.getText().toString();
            if(value.isEmpty())
                dialog.cancel();
            else{
                callback.onInputReceived(value);
            }
        });
        builder.setNegativeButton("Cancel", (dialog, which) -> dialog.cancel());
        builder.show();
    }

    /**
     * Static class to handle a Alert dialog with Loading message.
     */
    public static class LoadingAlert {
        private static AlertDialog dialog;

        /**
         * Create the Loading Alert dialog
         */
        public static void createLoadAlert(Context context, String title) {
            AlertDialog.Builder builder = new AlertDialog.Builder(context);
            builder.setView(R.layout.loading_alert);
            builder.setTitle(title);
            builder.setCancelable(false);
            dialog = builder.create();
            dialog.show();
        }

        /**
         * Remove the Loading alert dialog
         */
        public static void removeLoadAlert() {
            if (dialog != null) {
                dialog.dismiss();
                dialog = null; // Reset dialog reference
            } else {
                throw new IllegalStateException("createLoadAlert() must be called before removeLoadAlert()");
            }
        }
    }
}