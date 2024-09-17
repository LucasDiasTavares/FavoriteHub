import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from favoritehub.models import Product


def print_history_summary(obj, limit=None):
    """
    Prints a summary of actions taken on the given object's history records.

    This function outputs a summary of the actions performed on the object over time. Each record in the history can represent different types of actions, including:
    - `+`: Creation
    - `~`: Update
    - `-`: Deletion

    Parameters:
    obj (model instance): The Django model instance for which the history summary is to be printed. The instance must have historical records available through a history tracking mechanism (e.g., `django-simple-history`).
    limit (int, optional): The maximum number of historical records to include in the summary. If specified, only the most recent `limit` records are considered. If `None`, all available historical records are included.

    Example:
    To use this function, pass a model instance and optionally specify the number of history records to limit:
        product = Product.objects.first()
        print_history_summary(product, limit=10)

    Note:
    - The `history_type` field indicates the type of action, where:
        - `+` denotes a creation of the record.
        - `~` denotes an update to the record.
        - `-` denotes a deletion of the record.
    - Ensure that the object passed to this function is an instance of a model with history tracking enabled.
    """
    history = obj.history.all()
    if limit:
        history = history[:limit]
    for record in history:
        print(f"Date: {record.history_date}, Action: {record.history_type}, User: {record.history_user}")


def print_field_changes(obj, limit=None):
    """
    Prints the changes to fields between versions of the given object's history records.

    This function compares field values between consecutive versions of the object's history records and prints any differences.
    It helps in tracking how the values of fields have changed over time.

    Parameters:
    obj (model instance): The Django model instance for which field changes are to be printed. The instance must have historical records available through a history tracking mechanism (e.g., `django-simple-history`).
    limit (int, optional): The maximum number of historical records to process. If specified, only the most recent `limit` records are considered. If `None`, all available historical records are processed.

    Example:
    To use this function, pass a model instance and optionally specify the number of history records to limit:
        product = Product.objects.first()
        print_field_changes(product, limit=5)

    Note:
    - The comparison skips any fields that are not directly accessible or should not be compared (like primary keys or history-specific fields).
    - Ensure that the object passed to this function is an instance of a model that has history tracking enabled.
    """
    history = obj.history.all()
    if limit:
        history = history[:limit]
    previous_record = None
    for record in history:
        if previous_record:
            for field in obj._meta.fields:
                field_name = field.name
                old_value = getattr(previous_record, field_name, None)
                new_value = getattr(record, field_name, None)
                if old_value != new_value:
                    print(f"Field {field_name} changed from {old_value} to {new_value}")
        previous_record = record


def print_all_history(obj):
    """
    Prints the complete history of changes for the given object.

    This function provides a detailed overview of changes made to the specified object, including:
    1. **History Summary**: Displays a summary of actions performed on the object, such as creation, updates, and deletions. This is achieved using the `print_history_summary` function.
    2. **Field Changes**: Shows changes to individual fields between versions of the object. This is done by comparing the current record with the previous one, using the `print_field_changes` function.

    Parameters:
    obj (model instance): The Django model instance for which the history is to be printed. This instance should have historical records available through `django-simple-history` or a similar history tracking mechanism.

    Example:
    To use this function, pass a model instance like so:
        product = Product.objects.first()
        print_all_history(product)

    Note:
    Ensure that the `obj` passed to this function is an instance of a model that has history tracking enabled.
    """
    print("History Summary:")
    print_history_summary(obj)
    print("\nChanges to Fields:")
    print_field_changes(obj)


if __name__ == "__main__":
    """
    Executes the main script to display the history of a product.

    This block of code is executed when the script is run directly. It performs the following steps:
    1. Retrieves the first `Product` object from the database.
    2. If a `Product` object is found, it prints the product's history using the `print_all_history` function.
    3. If no product is found, it displays a message indicating that no products were found.

    You can modify the query to retrieve different data as needed. For example:
    - Change `Product.objects.first()` to a query that returns a specific product or a list of products.
    - Adjust the parameters passed to `print_all_history` to customize the amount of history displayed.

    Example modification to get a specific product by ID:
    obj = Product.objects.get(pk=<PRODUCT_ID>)

    Example modification to get a product based on some criteria:
    obj = Product.objects.filter(<FILTER_CONDITION>).first()
    """
    obj = Product.objects.first()
    if obj:
        print_all_history(obj)
    else:
        print("No Products found.")
