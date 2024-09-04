from django.apps import AppConfig


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

    def ready(self):
        from .views import run_table_7_data_check, run_table_8_data_check, run_table_9_data_check, run_table_12_data_check

        # Run the view
        run_table_7_data_check()
        run_table_8_data_check()
        run_table_9_data_check()
        run_table_12_data_check()


