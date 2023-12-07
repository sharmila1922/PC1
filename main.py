from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.app import App
import boto3
from datetime import datetime
from kivy.clock import Clock
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner
from kivymd.uix.pickers import MDDatePicker
from kivy.uix.stacklayout import StackLayout
import pymysql
from kivy.metrics import dp,sp
from kivy.uix.image import AsyncImage
import os
from kivymd.toast import toast
import re
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivymd.uix.button import MDIconButton, MDRectangleFlatButton, MDFloatingActionButton , MDRoundFlatButton, MDRaisedButton
from kivymd.uix.label import MDLabel
from screen_nav import screen_helper
from kivy.utils import get_color_from_hex
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty
from kivymd.uix.textfield import MDTextField
from kivymd.uix.filemanager import MDFileManager
from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.graphics import Line
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.image import Image
Bucket_Name = "insurence-management-s3-project"
s3_client = boto3.client('s3', aws_access_key_id="AKIA6E6I24PMFYM3NRPD", aws_secret_access_key="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")
conn = pymysql.connect(host="insurencemanagementrds.cwhayzj5qrw4.us-east-1.rds.amazonaws.com", user="admin", password="admin123", db="SnowRemovalApp")
cursor = conn.cursor()

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        home_icon = MDFloatingActionButton(
            icon="static/myfiles/1.png",
            size=(100, 100),  # Set the size as needed
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            on_release=self.go_to_dashboard  # Set the on_release event
        )

        label = MDLabel(
            text="Snow Removal App",
            halign="center",
            font_style="H5",
            pos_hint={'center_x': 0.5, 'center_y': 0.45},
            theme_text_color="Primary",
        )

        self.add_widget(home_icon)
        self.add_widget(label)

    def go_to_dashboard(self, instance):
        self.manager.current = 'selection_screen'

class SelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        service_provider_label = MDLabel(
            text="Service Provider",
            halign="center",
            font_style="H5",
            pos_hint={'center_x': 0.5, 'center_y': 0.8},
            theme_text_color="Custom",  # Set theme text color to custom
            text_color=(1, 1, 0.6, 1)  # Pale yellow color in RGBA format
        )

        button_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=60,
            spacing=20,
            padding=[10, 0, 10, 0],
            pos_hint={'center_x': 0.7, 'center_y': 0.7}
        )

        login_button = MDRaisedButton(
            text="  Login   ",
            size_hint=(None, None),
            size=(200, 50),  # Adjust width and height as needed
            md_bg_color=(0, 128 / 255, 128 / 255, 1),  # Teal color in RGBA format
            text_color=(1, 1, 1, 1),
            on_release=self.service_provider_login
        )
        button_layout.add_widget(login_button)

        register_button = MDRaisedButton(
            text="Register",
            size_hint=(None, None),
            size=(200, 50),  # Adjust width and height as needed
            md_bg_color=(0, 128 / 255, 128 / 255, 1),  # Teal color in RGBA format
            text_color=(1, 1, 1, 1),
            on_release=self.open_service_provider_register_screen
        )
        button_layout.add_widget(register_button)

        line = Widget(
            size=(300, 2),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        with line.canvas:
            Line(points=[0, 0, line.width, 0], width=1, cap='round', joint='round', close=True)

        self.add_widget(line)

        customer_label = MDLabel(
            text="Customer",
            halign="center",
            font_style="H5",
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            theme_text_color="Custom",  # Set theme text color to custom
            text_color=(1, 1, 0.6, 1)  # Pale yellow color in RGBA format
        )

        customer_button_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=60,
            spacing=20,
            padding=[10, 0, 10, 0],
            pos_hint={'center_x': 0.7, 'center_y': 0.4}
        )

        login_button = MDRaisedButton(
            text="  Login   ",
            size_hint_x=None,
            width=200,
            md_bg_color=(0, 128 / 255, 128 / 255, 1),  # Teal color in RGBA format
            text_color=(1, 1, 1, 1),  # White text color in RGBA format
            on_release=self.customer_login
        )
        customer_button_layout.add_widget(login_button)

        register_button = MDRaisedButton(
            text="Register",
            size_hint_x=None,
            md_bg_color=(0, 128 / 255, 128 / 255, 1),  # Teal color in RGBA format
            text_color=(1, 1, 1, 1),  # White text color in RGBA format
            width=200,
            on_release=self.open_customer_register_screen
        )
        customer_button_layout.add_widget(register_button)

        self.add_widget(service_provider_label)
        self.add_widget(button_layout)
        self.add_widget(customer_label)
        self.add_widget(customer_button_layout)

    def service_provider_login(self, instance):
        self.manager.current = 'provider_login_screen'

    def customer_login(self, instance):
        self.manager.current = 'customer_login_screen'

    def open_service_provider_register_screen(self, instance ):
        self.manager.current = 'service_provider_register_screen'

    def open_customer_register_screen(self, instance):
        self.manager.current = 'customer_register_screen'

    def logout(self):
        App.get_running_app().logout()

class ProviderRegistrationScreen(Screen):

    sname = ObjectProperty(None)
    email = ObjectProperty(None)
    phone = ObjectProperty(None)
    password = ObjectProperty(None)
    address = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        back_button = MDIconButton(
            icon="arrow-left",
            pos_hint={'center_x': 0.05, 'center_y': 0.95},
            on_release=self.go_back
        )
        self.add_widget(back_button)

    def go_back(self, instance):
        self.manager.current = 'selection_screen'

    def validate_provider_name(self, instance):
        name = instance.text.strip()  # Remove leading and trailing whitespaces
        pattern = r'^[a-zA-Z]+$'
        # Check if the name contains only alphabets
        if re.match(pattern, name):
            return True  # Valid name
        else:
            print("Invalid name. Please use only alphabets.")
            return False  # Invalid name

    def toggle_password_visibility(self):
        self.ids.password.password = not self.ids.password.password
        self.ids.password.focus = True  # To ensure the cursor position is updated

    def validate_email(self, instance):
        email = instance.text.strip()
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if re.match(pattern, email):
            return True  # Valid email address
        else:
            print("Invalid email address")
            return False  # Invalid email address

    def validate_phone(self, instance):
        phone = instance.text
        if len(phone) == 10 and phone.isdigit():
            return True
        else:
            print("Invalid phone number")
            return False  # Invalid email address

    def register_data(self):
        sname = self.sname.text
        if not self.validate_provider_name(self.ids.sname):
            toast("Invalid name. Please use only alphabets.")
            return
        email = self.email.text.strip()
        if not self.validate_email(self.ids.email):
            toast("Invalid email address")
            return
        phone = self.phone.text
        if not self.validate_phone(self.ids.phone):
            toast("Invalid Phone Number")
            return
        password = self.password.text
        address = self.address.text
        profile = self.ids.profile_img.source
        license = self.ids.licence_img.source
        idproof = self.ids.id_proof_img.source

        if not sname or not email or not phone or not password or not address or not profile or not license or not idproof:
            toast("Please fill out all required fields")
            return

        profile_file_name = os.path.basename(profile)
        license_file_name = os.path.basename(license)
        idproof_file_name = os.path.basename(idproof)
        s3_client.upload_file(profile, Bucket_Name, profile_file_name)
        s3_client.upload_file(license, Bucket_Name, license_file_name)
        s3_client.upload_file(idproof, Bucket_Name, idproof_file_name)
        bucket_name = 'insurence-management-s3-project'
        s3_file_name = profile_file_name
        s3_file_name_license = license_file_name
        s3_file_name_idproof = idproof_file_name

        profile_image_url = f'https://{bucket_name}.s3.amazonaws.com/{s3_file_name}'
        license_image_url = f'https://{bucket_name}.s3.amazonaws.com/{s3_file_name_license}'
        idproof_image_url = f'https://{bucket_name}.s3.amazonaws.com/{s3_file_name_idproof}'
        count = cursor.execute("select * from service_provider where email = '" + str(email) + "' or phone = '" + str(phone) + "'")
        if count == 0:
            query = ("insert into service_provider(service_provider_name,email,phone,password,address,profile_picture,license,id_proof,status) values('" + str(sname) + "' , '" + str(email) + "' , '" + str(phone) + "' , '" + str(password) + "' , '" + str(address) + "' , '" + str(profile_image_url) + "' , '" + str(license_image_url) + "' , '" + str(idproof_image_url) + "' , 'Deactivate')")
            cursor.execute(query)
            conn.commit()
            Clock.schedule_once(lambda dt: toast("Registration Successfull"), 0.1)
        else:
            toast("Duplicate Details")
        self.sname.text = ''
        self.email.text = ''
        self.phone.text = ''
        self.password.text = ''
        self.address.text = ''
        self.ids.profile_img.source = ''
        self.ids.licence_img.source = ''
        self.ids.id_proof_img.source = ''

        self.manager.current = 'provider_login_screen'

        # Log in the user automatically
        provider_login_screen = self.manager.get_screen('provider_login_screen')
        provider_login_screen.service_provider_login()

    def profile_button(self):
        from plyer import filechooser
        filechooser.open_file(on_selection=self.selected)

    def selected(self, selection):
        self.ids.profile_img.source = selection[0]
        toast("Profile Selected")

    def licence_button(self):
        from plyer import filechooser
        filechooser.open_file(on_selection=self.licence_selected)

    def licence_selected(self, selection):
        self.ids.licence_img.source = selection[0]
        toast("Licence Uploaded")
    def id_proof_button(self):
        from plyer import filechooser
        filechooser.open_file(on_selection=self.id_proof_selected)

    def id_proof_selected(self, selection):
        self.ids.id_proof_img.source = selection[0]
        toast("ID Proof Selected")


class CustomerRegistrationScreen(Screen):

    fname = ObjectProperty(None)
    email = ObjectProperty(None)
    phone = ObjectProperty(None)
    password = ObjectProperty(None)
    address = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        customer_back_button = MDIconButton(
            icon="arrow-left",
            pos_hint={'center_x': 0.05, 'center_y': 0.95},
            on_release=self.go_customer_back
        )
        self.add_widget(customer_back_button)

    def go_customer_back(self, instance):
        self.manager.current = 'selection_screen'

    def validate_customer_name(self, instance):
        name = instance.text.strip()  # Remove leading and trailing whitespaces
        pattern = r'^[a-zA-Z]+$'
        # Check if the name contains only alphabets
        if re.match(pattern, name):
            return True  # Valid name
        else:
            print("Invalid name. Please use only alphabets.")
            return False  # Invalid name

    def toggle_password_visibility(self):
        self.ids.password.password = not self.ids.password.password
        self.ids.password.focus = True  # To ensure the cursor position is updated

    def validate_customer_email(self, instance):
        email = instance.text.strip()  # Remove leading and trailing whitespaces
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if re.match(pattern, email):
            return True  # Valid email address
        else:
            print("Invalid email address")
            return False  # Invalid email address

    def validate_customer_phone(self, instance):
        phone = instance.text
        if len(phone) == 10 and phone.isdigit():
            return True
        else:
            print("Invalid phone number")
            return False  # Invalid email address

    def customer_register(self):
        fname = self.fname.text
        if not self.validate_customer_name(self.ids.fname):
            toast("Invalid name. Please use only alphabets.")
            return
        email =  self.email.text.strip()

        if not self.validate_customer_email(self.ids.email):
            toast("Invalid email address")
            return
        phone =  self.phone.text
        if not self.validate_customer_phone(self.ids.phone):
            toast("Invalid Phone Number")
            return
        password =  self.password.text
        address =  self.address.text
        customer_profile = self.ids.customer_profile_img.source

        if not fname or not email or not phone or not password or not address or not customer_profile:
            toast("Please fill out all required fields")
            return

        customer_profile_file_name = os.path.basename(customer_profile)
        s3_client.upload_file(customer_profile, Bucket_Name, customer_profile_file_name)
        bucket_name = 'insurence-management-s3-project'
        s3_file_name = customer_profile_file_name

        customer_profile_image_url = f'https://{bucket_name}.s3.amazonaws.com/{s3_file_name}'

        count = cursor.execute("select * from customer where email = '"+str(email)+"' or phone = '"+str(phone)+"'")
        conn.commit()
        if count == 0:
            query = ("insert into customer(customer_name,email,phone,password,address,customer_profile_picture) values('" + str(fname) + "' , '" + str(email) + "' , '" + str(phone) + "' , '" + str(password) + "' , '" + str(address) + "', '"+str(customer_profile_image_url)+"')")
            cursor.execute(query)
            conn.commit()
            # Display the toast message after a delay
            Clock.schedule_once(lambda dt: toast("Registration Successfull"), 0.1)
        else:
            toast("Duplicate Details")

        self.fname.text = ''
        self.email.text = ''
        self.phone.text = ''
        self.password.text = ''
        self.address.text = ''
        self.ids.customer_profile_img.source = ''

        # Log in the user automatically
        customer_login_screen = self.manager.get_screen('customer_login_screen')
        customer_login_screen.customer_login()

        self.manager.current = 'customer_login_screen'

    def customer_profile_button(self):
        from plyer import filechooser
        filechooser.open_file(on_selection=self.selected)

    def selected(self, selection):
        self.ids.customer_profile_img.source = selection[0]
        self.ids.customer_profile_img.opacity = 1
        toast("Profile Selected")

class ProviderLoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        provider_back = MDIconButton(
            icon="arrow-left",
            pos_hint={'center_x': 0.05, 'center_y': 0.95},
            on_release=self.go_back_to_provider
        )
        self.add_widget(provider_back)

    def go_back_to_provider(self, instance):
        self.manager.current = 'selection_screen'

    def toggle_password_visibility(self):
        self.ids.service_password.password = not self.ids.service_password.password
        self.ids.service_password.focus = True  # To ensure the cursor position is updated

    def validate_provider_email(self, instance):
        service_email = instance.text
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if re.match(pattern, service_email):
            return True  # Valid email address
        else:
            print("Invalid email address")
            return False  # Valid email address

    def service_provider_login(self):
        service_email = self.ids.service_email.text
        if not self.validate_provider_email(self.ids.service_email):
            toast("Invalid email address")
            return
        service_password = self.ids.service_password.text

        if not service_email or not service_password:
            toast("Please fill out all required fields")
            return

        try:
            count = cursor.execute("select * from service_provider where email = '" + str(service_email) + "' and password = '" + str(service_password) + "'")
            service_provider = cursor.fetchone()
            if count > 0 and service_provider[9] == 'Activate':
                App.get_running_app().is_logged_in = True
                App.get_running_app().user_type = 'service_provider'
                App.get_running_app().service_provider_id = service_provider[0]

                self.fetch_provider_details()
                self.fetch_service_provider_view_services()
                self.fetch_service_provider_view_requests()
                self.fetch_service_provider_history()

                self.manager.current = 'dashboard_provider'
                toast("Login Successfull")
            elif count > 0 and service_provider[9] == 'Deactivate':
                toast("Account is Deactivated")
            else:
                toast("Invalid Login Details")
        except Exception as e:
            print(f"Error during service provider login: {e}")

        self.ids.service_email.text = ''
        self.ids.service_password.text = ''

    def fetch_provider_details(self):
        try:
            service_provider_id = App.get_running_app().service_provider_id
            cursor.execute("select * from service_provider where service_provider_id = '"+str(service_provider_id)+"'")
            conn.commit()
            service_provider_details = cursor.fetchone()
            App.get_running_app().service_provider_details = service_provider_details
            return service_provider_details
        except Exception as e:
            print(f"Error fetching Provider Details: {e}")

    def fetch_service_provider_view_services(self):
        try:
            service_provider_id = App.get_running_app().service_provider_id
            cursor.execute("SELECT * FROM service WHERE service_provider_id = '" + str(service_provider_id) + "'")
            conn.commit()
            service_provider_view_services = cursor.fetchall()
            App.get_running_app().service_provider_view_services = service_provider_view_services
            return service_provider_view_services
        except Exception as e:
            print(f"Error fetching service provider requests: {e}")

    def fetch_service_provider_view_requests(self):
        try:
            service_provider_id = App.get_running_app().service_provider_id
            cursor.execute("SELECT * FROM service where service_provider_id = '" + str(service_provider_id) + "'")
            services = cursor.fetchall()
            service_ids = [service[0] for service in services]
            if service_ids:  # Check if service_ids list is not empty
                cursor.execute("SELECT * FROM service_booking WHERE service_id IN %s AND (status = 'Request Sended' OR status = 'Accepted Request' OR status = 'Paid Advance Amount' OR status = 'Service Completed')",(tuple(service_ids),))
                conn.commit()
                service_provider_view_requests = cursor.fetchall()
                App.get_running_app().service_provider_view_requests = service_provider_view_requests
                return service_provider_view_requests
            else:
                print("No services found for this provider.")
                return []  # Return an empty list in this case

        except Exception as e:
            print(f"Error fetching service provider requests: {e}")


    def fetch_service_provider_history(self):
        try:
            service_provider_id = App.get_running_app().service_provider_id
            cursor.execute("SELECT * FROM service where service_provider_id = '" + str(service_provider_id) + "'")
            services = cursor.fetchall()
            service_ids = [service[0] for service in services]
            if service_ids:  # Check if service_ids list is not empty
                cursor.execute("SELECT * FROM service_booking WHERE service_id IN %s AND (status = 'Request Cancelled by Customer' or status = 'Rejected Request' or status = 'Full Payment Successfull')",(tuple(service_ids),))
                service_provider_view_history = cursor.fetchall()
                App.get_running_app().service_provider_view_history = service_provider_view_history
                return service_provider_view_history
            else:
                print("No services found for this provider.")
                return []  # Return an empty list in this case

        except Exception as e:
            print(f"Error fetching service provider history requests: {e}")


class CustomerLoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        customer_back = MDIconButton(
            icon="arrow-left",
            pos_hint={'center_x': 0.05, 'center_y': 0.95},
            on_release=self.go_back_to_customer
        )
        self.add_widget(customer_back)

    def go_back_to_customer(self, instance):
        self.manager.current = 'selection_screen'

    def toggle_password_visibility(self):
        self.ids.customer_password.password = not self.ids.customer_password.password
        self.ids.customer_password.focus = True  # To ensure the cursor position is updated

    def validate_customer_login_email(self, instance):
        customer_email = instance.text
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if re.match(pattern, customer_email):
            return True  # Valid email address
        else:
            print("Invalid email address")
            return False  # Valid email address


    def customer_login(self):
        customer_email = self.ids.customer_email.text
        if not self.validate_customer_login_email(self.ids.customer_email):
            toast("Invalid email address")
            return
        customer_password = self.ids.customer_password.text

        if not customer_email or not customer_password:
            toast("Please fill out all required fields")
            return

        try:
            count = cursor.execute("select * from customer where email = '" + str(customer_email) + "' and password = '" + str(customer_password) + "'")
            customer = cursor.fetchone()
            conn.commit()
            if count > 0:
                App.get_running_app().is_logged_in = True
                App.get_running_app().user_type = 'customer'
                App.get_running_app().customer_id = customer[0]

                self.fetch_customer_details()
                self.fetch_customer_view_services()
                self.fetch_customer_requests()
                self.fetch_customer_history()

                self.manager.current = 'dashboard_customer'
                toast("Login Successful")
            else:
                toast("Invalid Login Details")
        except Exception as e:
            print(f"Error during login: {e}")

        self.ids.customer_email.text = ''
        self.ids.customer_password.text = ''

    def fetch_customer_details(self):
        try:
            customer_id = App.get_running_app().customer_id
            cursor.execute("select * from customer where customer_id = '" + str(customer_id) + "'")
            conn.commit()
            customer_profile__details = cursor.fetchone()
            App.get_running_app().customer_profile__details = customer_profile__details
            return customer_profile__details
        except Exception as e:
            print(f"Error fetching Customer Details: {e}")

    def fetch_customer_view_services(self):
        try:
            cursor.execute("SELECT * FROM service")
            conn.commit()
            customer_view_services = cursor.fetchall()
            App.get_running_app().customer_view_services = customer_view_services
            return customer_view_services
        except Exception as e:
            print(f"Error fetching customer requests: {e}")

    def fetch_customer_requests(self):
        try:
            customer_id = App.get_running_app().customer_id
            cursor.execute("SELECT * FROM service_booking WHERE customer_id = '" + str(customer_id) + "' and (status = 'Request Sended' or status = 'Accepted Request' or status = 'Paid Advance Amount' or status = 'Service Completed')")
            customer_requests = cursor.fetchall()
            App.get_running_app().customer_requests = customer_requests
            return customer_requests
        except Exception as e:
            print(f"Error fetching customer requests: {e}")

    def fetch_customer_history(self):
        try:
            customer_id = App.get_running_app().customer_id
            cursor.execute("SELECT * FROM service_booking WHERE customer_id = '" + str(customer_id) + "' and (status = 'Request Cancelled by Customer' or status = 'Rejected Request' or status = 'Full Payment Successfull')")
            customer_history = cursor.fetchall()
            App.get_running_app().customer_history = customer_history
            return customer_history
        except Exception as e:
            print(f"Error fetching customer requests: {e}")

class DashboardProvider(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def toggle_nav_drawer(self):
        self.ids.provider_nav_drawer.set_state()

    def on_enter(self, *args):
        service_provider_view_services = App.get_running_app().service_provider_view_services
        try:
            # Assuming you have customer_id available in MDApp
            service_provider_id = App.get_running_app().service_provider_id
            cursor.execute("SELECT service_provider_name, email, profile_picture FROM service_provider WHERE service_provider_id = '" + str(service_provider_id) + "'")
            conn.commit()
            provider_data = cursor.fetchone()
            if provider_data:
                service_provider_name, service_provider_email, service_provider_profile = provider_data
                self.update_provider_info(service_provider_name, service_provider_email, service_provider_profile)
        except Exception as e:
            print(f"Error fetching Provider info: {e}")

        top_services_provider = self.ids['top_services_provider']
        top_services_provider.clear_widgets()

        for provider_service in service_provider_view_services:
            top_service_image_provider = provider_service[4]
            top_service_name_provider = provider_service[1]
            top_service_price_provider = provider_service[3]

            # Create a StackLayout for overlaying blurred image, service name, and price
            stack_layout = StackLayout(size_hint=(None, None), size=("80dp", "120dp"))

            async_image_provider = AsyncImage(
                source=top_service_image_provider,
                size_hint=(None, None),
                size=("100dp", "60dp"),
                allow_stretch=True,  # Allow stretching to fit the specified size
                keep_ratio=True,  # Maintain the aspect ratio
                pos_hint={"center_x": 0.4, "center_y": 0.3}  # Center the image
            )

            spacer = Widget(size_hint_y=None, height="10dp")
            # Create labels for service name and price
            service_name_label_provider = MDLabel(
                text=top_service_name_provider,
                font_size=sp(10),
                font_name="Comic",
                halign="center",
                size_hint_y=None,
                height="20dp",
                theme_text_color="Custom",  # Set theme_text_color to "Custom"
                text_color=(0, 0, 0, 1)  # Set text_color to black (RGBA)
            )
            service_name_label_provider.font_size= 10

            service_price_label_provider = MDLabel(
                text=f"${top_service_price_provider}",
                font_size=sp(12),
                font_name="Comic",
                halign="center",
                size_hint_y=None,
                height="20dp",
                theme_text_color="Custom",  # Set theme_text_color to "Custom"
                text_color=(0, 0, 0, 1)  # Set text_color to black (RGBA)
            )

            # Add widgets to the StackLayout
            stack_layout.add_widget(async_image_provider)
            stack_layout.add_widget(spacer)
            stack_layout.add_widget(service_name_label_provider)
            stack_layout.add_widget(service_price_label_provider)

            # Create an MDCard and add the StackLayout
            card = MDCard(
                orientation='vertical',
                size_hint=(None, None),
                size=(dp(250), dp(250)),  # Adjusted size to fit content
                md_bg_color=(0.8, 0.8, 0.8, 1),
                padding=15
            )
            card.add_widget(stack_layout)

            # Add the card to the GridLayout with id 'top_services'
            top_services_provider.add_widget(card)

    def update_provider_info(self, service_provider_name, service_provider_email, service_provider_profile):
        if service_provider_name and service_provider_email and service_provider_profile:
            # Update labels with customer info
            self.ids.welcome_provider_name_label.text = f"Welcome {service_provider_name}"
            self.ids.provider_welcome_profile.source = f"{service_provider_profile}"

    def on_pre_enter(self, *args):
        service_provider_id = App.get_running_app().service_provider_id

        cursor.execute("SELECT * FROM service WHERE service_provider_id = '"+str(service_provider_id)+"'")
        conn.commit()
        services = cursor.fetchall()

        if services:
            service_count = len(services)
            self.ids.service_count_label.text = f"({service_count})"
        else:
            self.ids.service_count_label.text = "0"

        request_count = 0
        for service in services:
            service_id = service[0]
            cursor.execute("SELECT COUNT(*) FROM service_booking WHERE service_id = %s AND status = 'Request Sended'",(service_id,))
            request_count += cursor.fetchone()[0]

        if request_count > 0:
            self.ids.request_count_label.text = f"({request_count})"
        else:
            self.ids.request_count_label.text = "0"

        processing_count = 0
        for service in services:
            service_id = service[0]
            cursor.execute("SELECT COUNT(*) FROM service_booking WHERE service_id = %s AND (status = 'Request Sended' OR status = 'Accepted Request' OR status = 'Paid Advance Amount' OR status = 'Service Completed')",(service_id,))
            processing_count += cursor.fetchone()[0]

        if processing_count > 0:
            self.ids.processing_count_label.text = f"({processing_count})"
        else:
            self.ids.processing_count_label.text = "0"

        complete_count = 0
        for service in services:
            service_id = service[0]
            cursor.execute("SELECT COUNT(*) FROM service_booking WHERE service_id = %s AND status = 'Full Payment Successfull'",(service_id,))
            complete_count += cursor.fetchone()[0]

        if complete_count > 0:
            self.ids.complete_count_label.text = f"({complete_count})"
        else:
            self.ids.complete_count_label.text = "0"


    def search_services_provider(self):
        search_ter_provider = self.ids['top_service_search_field_provider'].text.lower()  # Get the search term
        top_services_grid_provider = self.ids['top_services_provider']  # Get the GridLayout

        # Clear existing widgets in the GridLayout
        top_services_grid_provider.clear_widgets()

        for provider_service in App.get_running_app().service_provider_view_services:
            if search_ter_provider.lower() in provider_service[1].lower():  # Check if search term is in service name
                top_service_image_provider = provider_service[4]
                top_service_name_provider = provider_service[1]
                top_service_price_provider = provider_service[3]

                # Create a StackLayout for overlaying blurred image, service name, and price
                stack_layout = StackLayout(size_hint=(None, None), size=("80dp", "120dp"))

                async_image_provider = AsyncImage(
                    source=top_service_image_provider,
                    size_hint=(None, None),
                    size=("100dp", "60dp"),
                    allow_stretch=True,  # Allow stretching to fit the specified size
                    keep_ratio=True,  # Maintain the aspect ratio
                    pos_hint={"center_x": 0.4, "center_y": 0.3}  # Center the image
                )

                spacer = Widget(size_hint_y=None, height="10dp")
                # Create labels for service name and price
                service_name_label_provider = MDLabel(
                    text=top_service_name_provider,
                    font_size=sp(12),
                    font_name="Comic",
                    halign="center",
                    size_hint_y=None,
                    height="20dp",
                    theme_text_color="Custom",  # Set theme_text_color to "Custom"
                    text_color=(0, 0, 0, 1)  # Set text_color to black (RGBA)
                )
                service_name_label_provider.font_size = 10

                service_price_label_provider = MDLabel(
                    text=f"${top_service_price_provider}",
                    font_size=sp(12),
                    font_name="Comic",
                    halign="center",
                    size_hint_y=None,
                    height="20dp",
                    theme_text_color="Custom",  # Set theme_text_color to "Custom"
                    text_color=(0, 0, 0, 1)  # Set text_color to black (RGBA)
                )

                # Add widgets to the StackLayout
                stack_layout.add_widget(async_image_provider)
                stack_layout.add_widget(spacer)
                stack_layout.add_widget(service_name_label_provider)
                stack_layout.add_widget(service_price_label_provider)

                # Create an MDCard and add the StackLayout
                card = MDCard(
                    orientation='vertical',
                    size_hint=(None, None),
                    size=("120dp", "130dp"),  # Adjusted size to fit content
                    md_bg_color=(0.8, 0.8, 0.8, 1),
                    padding=15
                )
                card.add_widget(stack_layout)

                # Add the card to the GridLayout with id 'top_services'
                top_services_grid_provider.add_widget(card)

    def go_to_service_form(self):
        self.manager.current = 'add_service'

    def logout(self):
        App.get_running_app().service_provider_id = None
        App.get_running_app().service_provider_details = []
        App.get_running_app().service_provider_view_services = []
        App.get_running_app().service_provider_view_requests = []
        App.get_running_app().service_provider_view_history = []
        self.manager.current = 'selection_screen'


class DashboardCustomer(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def toggle_customer_nav_drawer(self):
        self.ids.customer_nav_drawer.set_state()

    def on_pre_enter(self, *args):
        customer_view_services = App.get_running_app().customer_view_services
        try:
            # Assuming you have customer_id available in MDApp
            customer_id = App.get_running_app().customer_id
            cursor.execute("SELECT customer_name, email, customer_profile_picture, address FROM customer WHERE customer_id = '"+str(customer_id)+"'")
            conn.commit()
            customer_data = cursor.fetchone()
            if customer_data:
                customer_name, customer_email, customer_profile_picture, customer_address = customer_data
                self.update_customer_info(customer_name, customer_email, customer_profile_picture, customer_address)
        except Exception as e:
            print(f"Error fetching customer info: {e}")

        # Fetch services from the database
        top_services = self.ids['top_services']
        top_services.clear_widgets()

        for customer_service in customer_view_services:
            top_service_image = customer_service[4]
            top_service_name = customer_service[1]
            top_service_price = customer_service[3]

            # Create a StackLayout for overlaying blurred image, service name, and price
            stack_layout = StackLayout(size_hint=(None, None), size=("80dp", "120dp"))

            async_image = AsyncImage(
                source=top_service_image,
                size_hint=(None, None),
                size=("100dp", "60dp"),
                allow_stretch=True,  # Allow stretching to fit the specified size
                keep_ratio=True,  # Maintain the aspect ratio
                pos_hint={"center_x": 0.4, "center_y": 0.3}  # Center the image
            )

            spacer = Widget(size_hint_y=None, height="10dp")
            # Create labels for service name and price
            service_name_label = MDLabel(
                text=top_service_name,
                font_size=sp(12),
                font_name="Comic",
                halign="center",
                size_hint_y=None,
                height="20dp",
                theme_text_color="Custom",  # Set theme_text_color to "Custom"
                text_color=(0, 0, 0, 1)  # Set text_color to black (RGBA)
            )
            service_name_label.font_size = 10

            service_price_label = MDLabel(
                text=f"${top_service_price}",
                font_size=sp(12),
                font_name="Comic",
                halign="center",
                size_hint_y=None,
                height="20dp",
                theme_text_color="Custom",  # Set theme_text_color to "Custom"
                text_color = (0, 0, 0, 1)  # Set text_color to black (RGBA)
            )

            # Add widgets to the StackLayout
            stack_layout.add_widget(async_image)
            stack_layout.add_widget(spacer)
            stack_layout.add_widget(service_name_label)
            stack_layout.add_widget(service_price_label)

            # Create an MDCard and add the StackLayout
            card = MDCard(
                orientation='vertical',
                size_hint=(None, None),
                size=("120dp", "130dp"),  # Adjusted size to fit content
                md_bg_color=(0.8, 0.8, 0.8, 1),
                padding= 15
            )
            card.add_widget(stack_layout)

            # Add the card to the GridLayout with id 'top_services'
            top_services.add_widget(card)

    def update_customer_info(self, customer_name, customer_email, customer_profile_picture, customer_address):
        if customer_name and customer_email and customer_profile_picture and customer_address:
            # Update labels with customer info
            self.ids.welcome_customer_name_label.text = f"Welcome {customer_name}"
            self.ids.welcome_profile.source = f"{customer_profile_picture}"
            self.ids.customer_location_home.text = f"{customer_address}"

    def on_enter(self, *args):
        cursor.execute("SELECT * FROM service")
        conn.commit()
        services = cursor.fetchall()
        service_count = len(services)

        if service_count > 0:
            self.ids.service_count.text = f"({service_count})"
        else:
            self.ids.service_count.text = "0"

        request_count = 0
        for service in services:
            service_id = service[0]
            cursor.execute("SELECT COUNT(*) FROM service_booking WHERE service_id = %s AND status = 'Request Sended'",(service_id,))
            request_count += cursor.fetchone()[0]

        if request_count > 0:
            self.ids.request_count.text = f"({request_count})"
        else:
            self.ids.request_count.text = "0"

        processing_count = 0
        for service in services:
            service_id = service[0]
            cursor.execute( "SELECT COUNT(*) FROM service_booking WHERE service_id = %s AND (status = 'Request Sended' OR status = 'Accepted Request' OR status = 'Paid Advance Amount' OR status = 'Service Completed')",(service_id,))
            processing_count += cursor.fetchone()[0]

        if processing_count > 0:
            self.ids.processing_count.text = f"({processing_count})"
        else:
            self.ids.processing_count.text = "0"

        complete_count = 0
        for service in services:
            service_id = service[0]
            cursor.execute("SELECT COUNT(*) FROM service_booking WHERE service_id = %s AND status = 'Full Payment Successfull'",(service_id,))
            complete_count += cursor.fetchone()[0]

        if complete_count > 0:
            self.ids.complete_count.text = f"({complete_count})"
        else:
            self.ids.complete_count.text = "0"

    def search_services(self):
        search_term = self.ids['top_service_search_field'] .text.lower()  # Get the search term
        top_services_grid = self.ids['top_services'] # Get the GridLayout

        # Clear existing widgets in the GridLayout
        top_services_grid.clear_widgets()

        for customer_service in App.get_running_app().customer_view_services:
            if search_term.lower() in customer_service[1].lower():  # Check if search term is in service name
                top_service_image = customer_service[4]
                top_service_name = customer_service[1]
                top_service_price = customer_service[3]

                # Create a StackLayout for overlaying blurred image, service name, and price
                stack_layout = StackLayout(size_hint=(None, None), size=("80dp", "120dp"))

                async_image = AsyncImage(
                    source=top_service_image,
                    size_hint=(None, None),
                    size=("100dp", "60dp"),
                    allow_stretch=True,  # Allow stretching to fit the specified size
                    keep_ratio=True,  # Maintain the aspect ratio
                    pos_hint={"center_x": 0.4, "center_y": 0.3}  # Center the image
                )

                spacer = Widget(size_hint_y=None, height="10dp")
                # Create labels for service name and price
                service_name_label = MDLabel(
                    text=top_service_name,
                    font_size=sp(12),
                    font_name="Comic",
                    halign="center",
                    size_hint_y=None,
                    height="30dp",
                    theme_text_color="Custom",  # Set theme_text_color to "Custom"
                    text_color=(0, 0, 0, 1)  # Set text_color to black (RGBA)
                )
                service_name_label.font_size = 10

                spacer = Widget(size_hint_y=None, height="10dp")

                service_price_label = MDLabel(
                    text=f"${top_service_price}",
                    font_size=sp(12),
                    font_name="Comic",
                    halign="center",
                    size_hint_y=None,
                    height="20dp",
                    theme_text_color="Custom",  # Set theme_text_color to "Custom"
                    text_color=(0, 0, 0, 1)  # Set text_color to black (RGBA)
                )

                # Add widgets to the StackLayout
                stack_layout.add_widget(async_image)
                stack_layout.add_widget(spacer)
                stack_layout.add_widget(service_name_label)
                stack_layout.add_widget(service_price_label)

                # Create an MDCard and add the StackLayout
                card = MDCard(
                    orientation='vertical',
                    size_hint=(None, None),
                    size=("120dp", "130dp"),  # Adjusted size to fit content
                    md_bg_color=(0.8, 0.8, 0.8, 1),
                    padding=15
                )
                card.add_widget(stack_layout)

                # Add the card to the GridLayout with id 'top_services'
                top_services_grid .add_widget(card)

    def logout(self):
        App.get_running_app().customer_id = None
        App.get_running_app().customer_profile__details = []
        App.get_running_app().customer_view_services = []
        App.get_running_app().customer_requests = []
        App.get_running_app().customer_history = []
        self.manager.current = 'selection_screen'

class AddServiceScreen(Screen):

    service_name = ObjectProperty(None)
    charge_per_sq_feet = ObjectProperty(None)
    service_description = ObjectProperty(None)
    selected_date = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def toggle_nav_drawer(self):
        self.ids.provider_nav_drawer.set_state()

    def on_pre_enter(self, *args):
        App.get_running_app().switch_to_add_service()

    def fetch_location_names_from_database(self):
        cursor.execute("SELECT location_name FROM location")
        conn.commit()
        locations = cursor.fetchall()
        location_names = [location[0] for location in locations]
        return location_names

    def fetch_category_names_from_database(self):
        cursor.execute("SELECT category_name FROM category")
        conn.commit()
        categories = cursor.fetchall()
        category_names = [category[0] for category in categories]
        return category_names

    def add_service_data(self):
        selected_location_name = self.ids.location_id.text
        selected_category_name = self.ids.category_id.text

        cursor.execute("SELECT location_id FROM location WHERE location_name = '"+str(selected_location_name)+"'")
        conn.commit()
        location = cursor.fetchone()
        location_id = location[0]

        cursor.execute("SELECT category_id FROM category WHERE category_name = '" + str(selected_category_name) + "'")
        conn.commit()
        category = cursor.fetchone()
        category_id = category[0]

        service_name = self.service_name.text
        charge_per_sq_feet = self.charge_per_sq_feet.text
        service_description = self.service_description.text
        service_picture = self.ids.service_picture.source
        service_file_name = os.path.basename(service_picture)
        s3_client.upload_file(service_picture, Bucket_Name, service_file_name)
        bucket_name = 'insurence-management-s3-project'
        s3_file_name = service_file_name

        service_image_url = f'https://{bucket_name}.s3.amazonaws.com/{s3_file_name}'
        service_provider_id = App.get_running_app().service_provider_id

        # Check if any required fields are empty
        if not (selected_location_name and selected_category_name and service_name and charge_per_sq_feet and service_description and service_picture):
            # Display an error message or handle it in your application logic
            toast("All fields are required")
            return

        query = ("insert into service(service_name,description,charge_per_sq_feet,service_picture,category_id,location_id,service_provider_id) values('" + str(service_name) + "' , '" + str(service_description) + "' , '" + str(charge_per_sq_feet) + "' ,  '" + str(service_image_url) + "' , '" + str(category_id) + "' , '" + str(location_id) + "' , '" + str(service_provider_id) + "')")
        cursor.execute(query)
        conn.commit()

        # Fetch the newly added service
        cursor.execute("SELECT * FROM service WHERE service_id = LAST_INSERT_ID()")
        new_service = cursor.fetchone()

        # Convert the tuple to a list
        new_service_list = list(new_service)

        App.get_running_app().service_provider_view_services = list(App.get_running_app().service_provider_view_services)
        App.get_running_app().service_provider_view_services.append(new_service_list)

        toast("Service Added Successfull")


        self.service_name.text = ''
        self.charge_per_sq_feet.text = ''
        self.service_description.text = ''
        self.ids.service_picture.source = ''
        self.ids.location_id.text = ''
        self.ids.category_id.text = ''

        self.ids.location_id.text = 'Select Locations'
        self.ids.category_id.text = 'Select Category'

    def service_button(self):
        from plyer import filechooser
        filechooser.open_file(on_selection=self.selected)

    def selected(self, selection):
        self.ids.service_picture.source = selection[0]
        self.ids.service_picture.opacity = 1
        toast("Service Picture Selected")

    def logout(self):
        App.get_running_app().service_provider_id = None
        App.get_running_app().service_provider_details = []
        App.get_running_app().service_provider_view_services = []
        App.get_running_app().service_provider_view_requests = []
        App.get_running_app().service_provider_view_history = []
        self.manager.current = 'selection_screen'

class ViewServiceScreen(Screen):

    def toggle_nav_drawer(self):
        self.ids.provider_nav_drawer.set_state()

    def on_view_pre_enter(self, *args):
        App.get_running_app().switch_to_view_service()

    def on_pre_enter(self, *args):
        if not App.get_running_app().is_logged_in:
            return
        try:
            service_cards_layout = self.ids['service_cards_layout']
            service_cards_layout.clear_widgets()  # Clear existing widgets
            service_cards_layout.padding = [40]  # Add padding around the GridLayout
            service_cards_layout.spacing = 20  # Add spacing between the cards
            service_provider_view_services = App.get_running_app().service_provider_view_services
            for service in service_provider_view_services:
                service_id = service[0]
                service_name = service[1]

                card = MDCard(
                    orientation='vertical',
                    size_hint = (None, None),
                    size=(dp(150), dp(150)),  # Adjust the size of the card
                    elevation = 5,
                    padding = 2,
                    on_press=lambda x, sid=service_id: self.show_service_details(sid),  # Pass service_id as an argument
                    md_bg_color=(0, 0.5, 0.5, 1),  # Teal color (RGBA)
                )
                card.add_widget(
                    MDLabel(
                        text=service_name,
                        font_size=sp(20),
                        halign="center"
                    )
                )
                service_cards_layout.add_widget(card)

        except Exception as e:
            print(f"An error occurred: {e}")

    def show_service_details(self, service_id):
        try:
            service_details_screen = self.manager.get_screen('service_detail_screen')

            if service_details_screen:
                self.manager.current = 'service_detail_screen'
                service_details_data = self.get_service_details_by_id(service_id)
                service_details_screen.update_with_service_details(service_details_data)
            else:
                print("Screen 'service_detail_screen' not found.")

        except Exception as e:
            print(f"An error occurred: {e}")

    def get_service_details_by_id(self, service_id):
        cursor.execute("select * from service where service_id = '"+str(service_id)+"' ")
        conn.commit()
        return cursor.fetchone()  # Return the service details

    def logout(self):
        App.get_running_app().service_provider_id = None
        App.get_running_app().service_provider_details = []
        App.get_running_app().service_provider_view_services = []
        App.get_running_app().service_provider_view_requests = []
        App.get_running_app().service_provider_view_history = []
        self.manager.current = 'selection_screen'

class ServiceDetailScreen(Screen):

    def update_with_service_details(self, service_details_data):
        try:
            service_details = self.ids['service_details']
            service_details.clear_widgets()
            service_details.padding = [40]

            if service_details_data:
                category_name = ServiceDetailScreen.get_name_from_service_category_id(service_details_data[5])
                location_name = ServiceDetailScreen.get_name_from_service_location_id(service_details_data[6])

                self.ids['service_image'].source = service_details_data[4]
                self.ids['category_name'].text = f"Category: {category_name}"
                self.ids['location_name'].text = f"Location: {location_name}"
                self.ids['service_name'].text = service_details_data[1]
                self.ids['charge_per_sq_feet'].text = f"Charge per sq. feet: ${service_details_data[3]}"
                self.ids['description'].text = f"Description: {service_details_data[2]}"

                service_details.add_widget(self.ids['service_image'])
                service_details.add_widget(self.ids['service_name'])
                service_details.add_widget(self.ids['category_name'])
                service_details.add_widget(self.ids['location_name'])
                service_details.add_widget(self.ids['charge_per_sq_feet'])
                service_details.add_widget(self.ids['description'])

                spacer = Widget(size_hint_y=None, height=20)
                service_details.add_widget(spacer)
        except Exception as e:
            print(f"An error occurred: {e}")

    def go_back_view_service(self, instance):
        self.manager.current = 'view_service'

    def get_name_from_service_category_id(category_id):
        try:
            cursor.execute("SELECT category_name FROM category WHERE category_id = '" + str(category_id) + "'")
            conn.commit()
            category = cursor.fetchone()
            if category:
                return category[0]
            else:
                return None
        except Exception as e:
            print(f"Error fetching category name: {e}")
            return None

    def get_name_from_service_location_id(location_id):
        try:
            cursor.execute("SELECT location_name FROM location WHERE location_id = '" + str(location_id) + "'")
            conn.commit()
            location = cursor.fetchone()
            if location:
                return location[0]
            else:
                return None
        except Exception as e:
            print(f"Error fetching location name: {e}")
            return None

class ProviderHomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class ProviderProfile(Screen):

    def toggle_nav_drawer(self):
        self.ids.provider_nav_drawer.set_state()

    def on_pre_enter(self, *args):
        App.get_running_app().switch_to_provider_profile()

    def on_enter(self, *args):
        provider_details = self.ids['provider_details']
        provider_details.clear_widgets()

        try:
            service_provider_details = App.get_running_app().service_provider_details

            self.ids['service_provider_image'].source = service_provider_details[6]
            self.ids['service_provider_name_label'].text = str(service_provider_details[1])
            self.ids['service_provider_email_label'].text = str(service_provider_details[2])
            self.ids['service_provider_phone_label'].text = str(service_provider_details[3])
            self.ids['service_provider_address_label'].text = str(service_provider_details[5])

            provider_details.add_widget(self.ids['service_provider_image'])
            provider_details.add_widget(self.ids['service_provider_name_label'])
            provider_details.add_widget(self.ids['service_provider_email_label'])
            provider_details.add_widget(self.ids['service_provider_phone_label'])
            provider_details.add_widget(self.ids['service_provider_address_label'])

        except Exception as e:
            print(f"Error in on_enter: {e}")

    def logout(self):
        App.get_running_app().service_provider_id = None
        App.get_running_app().service_provider_details = []
        App.get_running_app().service_provider_view_services = []
        App.get_running_app().service_provider_view_requests = []
        App.get_running_app().service_provider_view_history = []
        self.manager.current = 'selection_screen'

class CustomerHomeScreen(Screen):
    pass

class CustomerProfile(Screen):

    def toggle_customer_nav_drawer(self):
        self.ids.customer_nav_drawer.set_state()

    def on_pre_enter(self, *args):
        App.get_running_app().switch_to_customer_profile()

    def on_enter(self, *args):
        customer_details = self.ids['customer_details']
        customer_details.clear_widgets()

        try:
            customer_profile__details = App.get_running_app().customer_profile__details

            self.ids['customer_image'].source = customer_profile__details[6]
            self.ids['customer_name_label'].text = str(customer_profile__details[1])
            self.ids['customer_email_label'].text = str(customer_profile__details[2])
            self.ids['customer_phone_label'].text = str(customer_profile__details[3])
            self.ids['customer_address_label'].text = str(customer_profile__details[5])

            customer_details.add_widget(self.ids['customer_image'])
            customer_details.add_widget(self.ids['customer_name_label'])
            customer_details.add_widget(self.ids['customer_email_label'])
            customer_details.add_widget(self.ids['customer_phone_label'])
            customer_details.add_widget(self.ids['customer_address_label'])

        except Exception as e:
            print(f"Error in on_enter: {e}")

    def logout(self):
        App.get_running_app().customer_id = None
        App.get_running_app().customer_profile__details = []
        App.get_running_app().customer_view_services = []
        App.get_running_app().customer_requests = []
        App.get_running_app().customer_history = []
        self.manager.current = 'selection_screen'

class ViewCustomerServiceScreen(Screen):

    def toggle_customer_nav_drawer(self):
        self.ids.customer_nav_drawer.set_state()

    def on_customer_view_pre_enter(self, *args):
        App.get_running_app().switch_to_customer_view_service()

    def on_pre_enter(self, *args):
        if not App.get_running_app().is_logged_in:
            return
        try:
            customer_service_cards_layout = self.ids['customer_service_cards_layout']
            customer_service_cards_layout.clear_widgets()  # Clear existing widgets
            customer_service_cards_layout.padding = [40]  # Add padding around the GridLayout
            customer_service_cards_layout.spacing = 20  # Add spacing between the cards
            customer_view_services = App.get_running_app().customer_view_services

            service_dict = {}

            for service in customer_view_services:
                service_id = service[0]
                customer_service = service[1]

                # Add service to the dictionary using its name as the key
                if customer_service in service_dict:
                    service_dict[customer_service].append(service_id)
                else:
                    service_dict[customer_service] = [service_id]

            # Iterate through the dictionary and create cards for unique services
            for service_name, service_ids in service_dict.items():

                card = MDCard(
                    orientation='vertical',
                    size_hint=(None, None),
                    size=(dp(150), dp(150)),  # Adjust the size of the card
                    elevation=5,
                    padding=2,
                    on_press=lambda x, sid=service_ids: self.show_customer_service_details(sid),  # Pass service_id as an argument
                    md_bg_color=(0, 0.5, 0.5, 1),  # Teal color (RGBA)
                )
                card.add_widget(
                    MDLabel(
                        text=service_name,
                        font_size=sp(20),
                        halign="center"
                    )
                )
                customer_service_cards_layout.add_widget(card)

        except Exception as e:
            print(f"An error occurred: {e}")

    def show_customer_service_details(self, service_ids):
        try:
            customer_service_screen = self.manager.get_screen('customer_service_detail_screen')

            if customer_service_screen:
                self.manager.current = 'customer_service_detail_screen'
                customer_service_details_data = self.get_customer_service_details_by_id(service_ids)

                if customer_service_details_data:
                    customer_service_screen.update_with_customer_service_details(customer_service_details_data)
                else:
                    print("No service details found.")

            else:
                print("Screen 'customer_service_detail_screen' not found.")

        except Exception as e:
            print(f"An error occurred: {e}")

    def get_customer_service_details_by_id(self, service_ids):
        try:
            # Create a list to store the details of all services
            service_details = []

            # Iterate through the list of service IDs
            for service_id in service_ids:
                cursor.execute("select * from service where service_id = '" + str(service_id) + "' ")
                conn.commit()
                service_details.append(cursor.fetchone())  # Append the service details to the list

            return service_details  # Return the list of service details

        except Exception as e:
            print(f"An error occurred: {e}")

    def logout(self):
        App.get_running_app().customer_id = None
        App.get_running_app().customer_profile__details = []
        App.get_running_app().customer_view_services = []
        App.get_running_app().customer_requests = []
        App.get_running_app().customer_history = []
        self.manager.current = 'selection_screen'

class CustomerServiceDetailScreen(Screen):

    def update_with_customer_service_details(self, customer_service_details_data):
        try:
            customer_id = App.get_running_app().customer_id
            customer_service_details = self.ids['customer_service_details']
            customer_service_details.clear_widgets()
            customer_service_details.spacing = 10

            service_dict = {}

            for service_details in customer_service_details_data:
                if service_details:
                    service_name = service_details[1]
                    if service_name in service_dict:
                        service_dict[service_name].append(service_details)
                    else:
                        service_dict[service_name] = [service_details]

            for service_name, service_details_list in service_dict.items():
                for service_details in service_details_list:
                    card = MDCard(
                        orientation='vertical',
                        size_hint=(None, None),
                        size=(dp(250), dp(300)),
                        elevation=5,
                        padding=10,
                        md_bg_color=(0.9, 0.9, 0.9, 1)
                    )

                    location_name_label = CustomerServiceDetailScreen.get_location_id(service_details[6])
                    category_name_label = CustomerServiceDetailScreen.get_category_id(service_details[5])
                    service_provider_details = CustomerServiceDetailScreen.get_service_provider_id(service_details[7])

                    box1 = MDBoxLayout(orientation='vertical')
                    location_from_customer = MDLabel(
                        text="Location:",
                        theme_text_color="Custom",
                        font_style="Caption",
                        font_size=sp(18),
                        text_color=(0, 0, 0, 1),  # Set text color to black
                        bold=True  # Make the text bold
                    )
                    location_from_customer.font_size = 18
                    box1.add_widget(location_from_customer)

                    location_name_from_customer = MDLabel(
                        text=location_name_label,
                        theme_text_color="Custom",
                        font_style="Caption",
                        font_size=sp(20),
                        text_color=(0, 0, 0.5, 1),  # Dark blue color (RGBA)
                        bold=True  # Make the text bold
                    )
                    location_name_from_customer.font_size = 20
                    box1.add_widget(location_name_from_customer)

                    spacer = Widget(size_hint_y=None, height=20)
                    box1.add_widget(spacer)

                    category_from_customer = MDLabel(
                        text="Category:",
                        theme_text_color="Custom",
                        font_style="Caption",
                        font_size=sp(18),
                        text_color=(0, 0, 0, 1),  # Set text color to black
                        bold=True  # Make the text bold
                    )
                    category_from_customer.font_size = 18
                    box1.add_widget(category_from_customer)

                    category_name_from_customer = MDLabel(
                        text=category_name_label,
                        theme_text_color="Custom",
                        font_style="Caption",
                        font_size=sp(20),
                        text_color=(0, 0, 0.5, 1),  # Dark blue color (RGBA)
                        bold=True  # Make the text bold
                    )
                    category_name_from_customer.font_size = 20
                    box1.add_widget(category_name_from_customer)

                    spacer = Widget(size_hint_y=None, height=20)
                    box1.add_widget(spacer)

                    charge_from_customer = MDLabel(
                        text="Charge per sq. feet:",
                        theme_text_color="Custom",
                        font_style="Caption",
                        font_size=sp(18),
                        text_color=(0, 0, 0, 1),  # Set text color to black
                        bold=True  # Make the text bold
                    )
                    charge_from_customer.font_size = 18
                    box1.add_widget(charge_from_customer)

                    charge_name_from_customer = MDLabel(
                        text=f"${service_details[3]}",
                        theme_text_color="Custom",
                        font_style="Caption",
                        font_size=sp(20),
                        text_color=(0, 0, 0.5, 1),  # Dark blue color (RGBA)
                        bold=True  # Make the text bold
                    )
                    charge_name_from_customer.font_size = 20
                    box1.add_widget(charge_name_from_customer)

                    spacer = Widget(size_hint_y=None, height=20)
                    box1.add_widget(spacer)

                    description_from_customer = MDLabel(
                        text=f"Description: ",
                        theme_text_color="Custom",
                        font_style="Caption",
                        font_size=sp(18),
                        text_color=(0, 0, 0, 1),  # Set text color to black
                        bold=True  # Make the text bold
                    )
                    description_from_customer.font_size = 18
                    box1.add_widget(description_from_customer)

                    spacer = Widget(size_hint_y=None, height=10)
                    box1.add_widget(spacer)

                    description_name_from_customer = MDLabel(
                        text=f"{service_details[2]}",
                        theme_text_color="Custom",
                        font_style="Caption",
                        font_size=sp(20),
                        text_color=(0, 0, 0.5, 1),  # Dark blue color (RGBA)
                        bold=True  # Make the text bold
                    )
                    description_name_from_customer.font_size = 20
                    box1.add_widget(description_name_from_customer)

                    spacer = Widget(size_hint_y=None, height=20)
                    box1.add_widget(spacer)

                    service_provider_details_customer = MDLabel(
                        text=f"Service Provider Details: ",
                        theme_text_color="Custom",
                        font_style="Caption",
                        font_size=sp(18),
                        text_color=(0, 0, 0, 1),  # Set text color to black
                        bold=True  # Make the text bold
                    )
                    service_provider_details_customer.font_size = 18
                    box1.add_widget(service_provider_details_customer)

                    if service_provider_details is not None:
                        service_provider_name = service_provider_details[0]  # Access the customer name
                        service_provider_email = service_provider_details[1]  # Access the phone number
                        service_provider_phone = service_provider_details[2]  # Access the phone number

                        box1.add_widget(MDLabel(
                            text=service_provider_name,
                            theme_text_color="Custom",
                            font_style="Caption",
                            font_size=sp(10),
                            text_color=(0, 0, 0.5, 1),  # Dark blue color (RGBA)
                            bold =True  # Make the text bold
                        ))

                        box1.add_widget(MDLabel(
                            text=service_provider_email,
                            theme_text_color="Custom",
                            font_style="Caption",
                            font_size=sp(10),
                            text_color=(0, 0, 0.5, 1),  # Dark blue color (RGBA)
                            bold=True  # Make the text bold
                        ))

                        box1.add_widget(MDLabel(
                            text=service_provider_phone,
                            theme_text_color="Custom",
                            font_style="Caption",
                            font_size=sp(10),
                            text_color=(0, 0, 0.5, 1),  # Dark blue color (RGBA)
                            bold=True  # Make the text bold
                        ))

                    box2 = MDBoxLayout(orientation='vertical', padding=10, spacing=10)

                    customer_service_image = AsyncImage(
                        source=service_details[4],
                        keep_ratio=True,  # Maintain the aspect ratio of the image
                        allow_stretch=True,  # Allow the image to stretch to fit the widget
                        size=(500, 500)  # Set the size of the image (adjust as needed)
                    )
                    box2.add_widget(customer_service_image)

                    sq_feet_input_textfield = MDTextField(hint_text= "Enter Your sq.feet",hint_text_color=(0, 0, 0, 1),mode= "fill")
                    description_input_textfield = MDTextField(hint_text= "Enter Your Description",hint_text_color=(0, 0, 0, 1),mode= "fill")

                    self.ids[f'sq_feet_input_{service_details[0]}'] = sq_feet_input_textfield
                    self.ids[f'description_input_{service_details[0]}'] = description_input_textfield

                    request_button = MDRaisedButton(
                        text="REQUEST SERVICE",
                        size_hint=(None, None),
                        size=(50, 30),  # Adjust size as needed
                        pos_hint={'center_x': 0.5},
                        md_bg_color=(0, 0.588, 0.533, 1),  # Teal background color (RGBA)
                        text_color=(0, 0, 0, 1),  # Black text color (RGBA)
                        on_press=self.on_request_button_press  # Define a function to handle the button press
                    )
                    request_button.service_id = service_details[0]
                    service_id = service_details[0]

                    cursor.execute("SELECT COUNT(*) FROM service_booking ""WHERE customer_id = '" + str(customer_id) + "' AND service_id = '" + str(service_id) + "' AND status IN ('Request Sended', 'Accepted Request')")
                    count = cursor.fetchone()[0]

                    if count > 0:
                        box2.remove_widget(sq_feet_input_textfield)
                        box2.remove_widget(description_input_textfield)
                        box2.remove_widget(request_button)
                    else:
                        box2.add_widget(sq_feet_input_textfield)
                        box2.add_widget(description_input_textfield)
                        box2.add_widget(request_button)

                    box = MDBoxLayout(orientation='horizontal')
                    box.add_widget(box1)
                    box.add_widget(box2)

                    # Add the box layout to the card
                    card.add_widget(box)

                    customer_service_details.add_widget(card)

        except Exception as e:
            print(f"An error occurred: {e}")

    def on_request_button_press(self, instance):
        print("Button pressed")
        try:
            service_id = instance.service_id
            customer_id = App.get_running_app().customer_id

            sq_feet_input_textfield = self.ids[f'sq_feet_input_{service_id}']
            description_input_textfield = self.ids[f'description_input_{service_id}']

            # Get the current date and time for booking_date
            booking_date = datetime.now().strftime('%Y-%m-%d')

            # Get sq_feet_input and description_input from the TextInput fields
            sq_feet = sq_feet_input_textfield.text
            description = description_input_textfield.text

            sq_feet_input_textfield.text = ''
            description_input_textfield.text = ''

            # Insert data into the service_booking table
            try:
                cursor.execute("insert into service_booking(number_of_sq_feet,description,booking_date,status,service_id,customer_id) values ('" + str(sq_feet) + "' , '" + str(description) + "' , '" + str(booking_date) + "' , 'Request Sended' , '" + str(service_id) + "' , '" + str(customer_id) + "')")
                conn.commit()
                toast("Request submitted successfully!")

                # Fetch the newly added service
                cursor.execute("SELECT * FROM service_booking WHERE service_booking_id = LAST_INSERT_ID()")
                new_requests = cursor.fetchone()

                # Convert the tuple to a list
                new_request_list = list(new_requests)

                App.get_running_app().customer_requests = list(App.get_running_app().customer_requests)
                App.get_running_app().customer_requests.append(new_request_list)

            except Exception as e:
                print(f"An error occurred during insert: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_category_id(category_id):
        try:
            cursor.execute("SELECT category_name FROM category WHERE category_id = '" + str(category_id) + "'")
            conn.commit()
            category = cursor.fetchone()
            if category:
                return category[0]
            else:
                return None
        except Exception as e:
            print(f"Error fetching category name: {e}")
            return None

    def get_location_id(location_id):
        try:
            cursor.execute("SELECT location_name FROM location WHERE location_id = '" + str(location_id) + "'")
            conn.commit()
            location = cursor.fetchone()
            if location:
                return location[0]
            else:
                return None
        except Exception as e:
            print(f"Error fetching location name: {e}")
            return None

    def get_service_provider_id(service_provider_id):
        try:
            cursor.execute("SELECT service_provider_name, email, phone FROM service_provider WHERE service_provider_id = '" + str(service_provider_id) + "'")
            conn.commit()
            service_provider = cursor.fetchone()
            if service_provider:
                return service_provider[0], service_provider[1], service_provider[2]
            else:
                return None
        except Exception as e:
            print(f"Error fetching service_provider_name name: {e}")
            return None

    def request_service(self, instance):
        pass

class CustomerViewRequests(Screen):

    def toggle_customer_nav_drawer(self):
        self.ids.customer_nav_drawer.set_state()

    def on_pre_enter(self, *args):
        App.get_running_app().switch_to_customer_view_request()

    def on_enter(self, dt=None):
        if not App.get_running_app().is_logged_in:
            return
        try:
            customer_id = App.get_running_app().customer_id
            request_table_layout = self.ids['request_table_layout']
            request_table_layout.clear_widgets()  # Clear existing widgets
            request_table_layout.padding = [50]  # Add padding around the GridLayout
            request_table_layout.spacing = [20]  # Add padding around the GridLayout

            customer_requests = App.get_running_app().customer_requests

            if not customer_requests:
                no_requests_label_customer = MDLabel(
                    text="No Requests Found",
                    font_size=sp(30),
                    text_color=(1, 1, 1, 1),  # Purple color (RGBA values)
                    theme_text_color="Custom",
                    halign="center"
                )
                no_requests_label_customer.font_size = 30
                request_table_layout.add_widget(no_requests_label_customer)
                return

            for service_booking in customer_requests:
                service_booking_id = service_booking[0]
                number_of_sq_feet = float(service_booking[1])
                description = service_booking[2]
                booking_date = service_booking[3]
                status = service_booking[7]
                service_id = service_booking[8]
                service_date_time = service_booking[4]
                advance_amount = service_booking[5]
                remaining_amount = service_booking[6]

                if status in ["Rejected Request", "Request Cancelled by Customer"]:
                    continue  # Skip this card

                cursor.execute("select * from service where service_id = '" + str(service_id) + "'")
                service = cursor.fetchone()
                service_image = service[4]
                charger_per_sq_feet = float(service[3])

                total_charge = number_of_sq_feet * charger_per_sq_feet

                service_name_data_label = CustomerViewRequests.get_service_name_from_service(service_id)
                service_provider_details_customer = CustomerViewRequests.get_service_provider_details_from_service(service_id)
                service_provider_name, service_provider_email, service_provider_phone = service_provider_details_customer
                service_provider_name_customer = MDLabel(text=str(service_provider_name), font_size=sp(15),text_color=(0, 0, 0.5, 1), theme_text_color="Custom")
                service_provider_email_customer = MDLabel(text=str(service_provider_email), font_size=sp(15),text_color=(0, 0, 0.5, 1), theme_text_color="Custom")
                service_provider_phone_customer = MDLabel(text=str(service_provider_phone), font_size=sp(15),text_color=(0, 0, 0.5, 1), theme_text_color="Custom")

                service_provider_name_customer.font_size = 15
                service_provider_email_customer.font_size = 15
                service_provider_phone_customer.font_size = 15

                card = MDCard(
                    orientation='vertical',
                    size_hint=(None, None),
                    size=(dp(250), dp(300)),
                    elevation=5,
                    padding=10,
                    md_bg_color=(0.9, 0.9, 0.9, 1)
                )

                number_of_sq_feet_label = MDLabel(text=str(number_of_sq_feet),font_size=sp(20),text_color=(0, 0, 0.5, 1),theme_text_color="Custom")
                description_label = MDLabel(text=str(description),font_size=sp(20),text_color=(0, 0, 0.5, 1),theme_text_color="Custom")
                booking_date_label = MDLabel(text=str(booking_date),font_size=sp(20),text_color=(0, 0, 0.5, 1),theme_text_color="Custom")
                status_label = MDLabel(
                    text=str(status),
                    theme_text_color="Custom",
                    text_color=(0.5, 0, 0.5, 1),  # RGB values for purple
                    bold=True,
                    font_size=sp(20),
                )
                service_name_label = MDLabel(text=service_name_data_label,font_size=sp(20),text_color=(0, 0, 0.5, 1),theme_text_color="Custom")
                charger_per_sq_feet_label = MDLabel(text=f"${charger_per_sq_feet}",font_size=sp(20),text_color=(0, 0, 0.5, 1),theme_text_color="Custom")
                service_picture_label = AsyncImage(source=service_image, keep_ratio=True, allow_stretch=True)

                box1 = MDBoxLayout(orientation='vertical')  # Add spacing between labels

                service_name_data = MDLabel(
                    text="Service Name:",
                    theme_text_color="Custom",
                    font_style="Caption",
                    size_hint_y=None,
                    height=20
                )
                box1.add_widget(service_name_data)
                box1.add_widget(service_name_label)

                spacer = Widget(size_hint_y=None, height=20)
                box1.add_widget(spacer)

                charge_per_sq_feet = MDLabel(
                    text="Charger Per sq.feet:",
                    theme_text_color="Custom",
                    font_style="Caption",
                    size_hint_y=None,
                    height=20
                )
                box1.add_widget(charge_per_sq_feet)
                box1.add_widget(charger_per_sq_feet_label)

                spacer = Widget(size_hint_y=None, height=20)
                box1.add_widget(spacer)

                number_of_sq_feet = MDLabel(
                    text="No.of sq.feet:",
                    theme_text_color="Custom",
                    font_style="Caption",
                    size_hint_y=None,
                    height=20
                )
                box1.add_widget(number_of_sq_feet)
                box1.add_widget(number_of_sq_feet_label)

                spacer = Widget(size_hint_y=None, height=20)
                box1.add_widget(spacer)

                description = MDLabel(
                    text="Description:",
                    theme_text_color="Custom",
                    font_style="Caption",
                    size_hint_y=None,
                    height=20
                )
                box1.add_widget(description)
                box1.add_widget(description_label)

                spacer = Widget(size_hint_y=None, height=20)
                box1.add_widget(spacer)

                booking_date = MDLabel(
                    text="Booking Date:",
                    theme_text_color="Custom",
                    font_style="Caption",
                    size_hint_y=None,
                    height=20
                )
                box1.add_widget(booking_date)
                box1.add_widget(booking_date_label)

                spacer = Widget(size_hint_y=None, height=20)
                box1.add_widget(spacer)

                if service_booking[7] in ["Request Sended", "Paid Advance Amount", "Accepted Request", "Full Payment Successfull", "Service Completed"]:
                    status = MDLabel(
                        text="Status:",
                        theme_text_color="Custom",
                        font_style="Caption",
                        size_hint_y=None,
                        height=20
                    )
                    box1.add_widget(status)
                    box1.add_widget(status_label)

                spacer = Widget(size_hint_y=None, height=20)
                box1.add_widget(spacer)

                service_provider_name_customer_id = MDLabel(
                    text="Service Provider:",
                    theme_text_color="Custom",
                    font_style="Caption",
                    size_hint_y=None,
                    height=20
                )
                box1.add_widget(service_provider_name_customer_id)
                box1.add_widget(service_provider_name_customer)
                box1.add_widget(service_provider_email_customer)
                box1.add_widget(service_provider_phone_customer)

                if service_booking[7] == "Accepted Request":
                    Total_Amount = MDLabel(
                        text=f"Total Charge: ${total_charge}",
                        theme_text_color="Custom",
                        text_color=(0.5, 0, 0.5, 1),  # Violet color (RGBA values)
                        font_style="Caption",
                        size_hint_y=None,
                        height=dp(30),
                        bold=True
                    )
                    Advance_amount = MDLabel(
                        text=f"Advance Amount: ${advance_amount}",
                        theme_text_color="Custom",
                        text_color=(0.5, 0, 0.5, 1),  # Violet color (RGBA values)
                        font_style="Caption",
                        size_hint_y=None,
                        height=dp(30),
                        bold=True
                    )
                    Remaining_Amount = MDLabel(
                        text=f"Remaining Amount: ${remaining_amount}",
                        theme_text_color="Custom",
                        text_color=(0.5, 0, 0.5, 1),  # Violet color (RGBA values)
                        font_style="Caption",
                        size_hint_y=None,
                        height=dp(30),
                        bold=True
                    )
                    service_booking_date = MDLabel(
                        text=f"Service Booking Date: {service_date_time}",
                        theme_text_color="Custom",
                        text_color=(0, 0, 0, 1),  # Black color (RGBA values)
                        font_style="Caption",
                        font_size=dp(20),  # Set the font size to 20 density-independent pixels (dp)
                        size_hint_y=None,
                        height=dp(30),
                        bold=True
                    )
                    box1.add_widget(Total_Amount)
                    box1.add_widget(Advance_amount)
                    box1.add_widget(Remaining_Amount)
                    box1.add_widget(service_booking_date)

                elif service_booking[7] in ["Paid Advance Amount", "Service Completed"]:
                    Total_Amount = MDLabel(
                        text=f"Total Charge: ${total_charge}",
                        theme_text_color="Custom",
                        text_color=(0.5, 0, 0.5, 1),  # Violet color (RGBA values)
                        font_style="Caption",
                        size_hint_y=None,
                        height=dp(30),
                        bold=True
                    )
                    Remaining_Amount = MDLabel(
                        text=f"Remaining Amount: ${remaining_amount}",
                        theme_text_color="Custom",
                        text_color=(0.5, 0, 0.5, 1),  # Violet color (RGBA values)
                        font_style="Caption",
                        size_hint_y=None,
                        height=dp(30),
                        bold=True
                    )
                    service_booking_date = MDLabel(
                        text=f"Service Booking Date: {service_date_time}",
                        theme_text_color="Custom",
                        text_color=(0, 0, 0, 1),  # Black color (RGBA values)
                        font_style="Caption",
                        font_size=dp(20),  # Set the font size to 20 density-independent pixels (dp)
                        size_hint_y=None,
                        height=dp(30),
                        bold=True
                    )
                    box1.add_widget(Total_Amount)
                    box1.add_widget(Remaining_Amount)
                    box1.add_widget(service_booking_date)

                if service_booking[7] in ["Paid Advance Amount", "Service Completed"]:
                    paid_amount = MDLabel(
                        text=f"Paid Amount: ${advance_amount}",
                        theme_text_color="Custom",
                        text_color=(0, 0.5, 0, 1),  # Dark green color (RGBA values)
                        font_style="Caption",
                        size_hint_y=None,
                        height=dp(30),
                        bold=True
                    )
                    box1.add_widget(paid_amount)

                box2 = MDBoxLayout(orientation='vertical')
                box2.add_widget(service_picture_label)

                cursor.execute("select * from review where service_booking_id in (select service_booking_id from service_booking where service_id = '" + str(service_id) + "')")
                reviews = cursor.fetchall()
                reviews = list(reviews)
                if len(reviews) == 0:
                    no_rating = "No Rating"
                    average_rating_label = MDLabel(text=f"Rating: {no_rating}",theme_text_color="Custom", text_color=(0, 0, 0, 1))
                else:
                    total_ratings = 0
                    number_of_ratings = 0
                    for review in reviews:
                        total_ratings = total_ratings + int(review[2])
                        number_of_ratings = number_of_ratings + 1
                    rating = total_ratings / number_of_ratings
                    rating = round(rating, 2)
                    average_rating_label = MDLabel(text=f"Rating: {rating}", theme_text_color="Custom", text_color=(0, 0, 0, 1))
                box2.add_widget(average_rating_label)

                if service_booking[7] == "Request Sended":
                    cancel_button = MDRectangleFlatButton(
                        text="Cancel Request",
                        on_press=self.on_cancel_button_press,
                        md_bg_color=get_color_from_hex("#FF5733"),  # Hexadecimal color for red
                        text_color=(0, 0, 0, 1)  # Black color (RGBA values)
                    )
                    cancel_button.service_booking_id = service_booking_id
                    box2.add_widget(cancel_button)

                    spacer = Widget(size_hint_y=None, height=5)  # Adjust height as needed
                    box2.add_widget(spacer)
                elif service_booking[7] == "Accepted Request":
                    payment_button = MDRectangleFlatButton(
                        text="Make Payment",
                        on_press=self.on_pay_button_press,
                        md_bg_color=get_color_from_hex("#0000FF"),  # Hexadecimal color for blue
                        text_color=(1, 1, 1, 1)  # White color (RGBA values)
                    )
                    payment_button.service_booking_id = service_booking_id
                    payment_button.customer_id = customer_id
                    box2.add_widget(payment_button)
                elif service_booking[7] == "Service Completed":
                    payment_button = MDRectangleFlatButton(
                        text="Make Full Payment",
                        on_press=self.on_pay_full_button_press,
                        md_bg_color=get_color_from_hex("#0000FF"),  # Hexadecimal color for blue
                        text_color=(1, 1, 1, 1)  # White color (RGBA values)
                    )
                    payment_button.service_booking_id = service_booking_id
                    payment_button.customer_id = customer_id
                    box2.add_widget(payment_button)

                box = MDBoxLayout(orientation='horizontal')
                box.add_widget(box1)
                box.add_widget(box2)

                # Add the box layout to the card
                card.add_widget(box)

                request_table_layout.add_widget(card)
        except Exception as e:
            print(f"An error occurred: {e}")

    def on_pay_full_button_press(self, instance):
        service_booking_id = instance.service_booking_id
        customer_id = instance.customer_id
        card_details_screen = self.manager.get_screen('fullcarddetails')
        card_details_screen.service_booking_id = service_booking_id
        card_details_screen.customer_id = customer_id
        self.manager.current = 'fullcarddetails'

    def on_pay_button_press(self, instance):
        service_booking_id = instance.service_booking_id
        customer_id = instance.customer_id
        card_details_screen = self.manager.get_screen('carddetails')
        card_details_screen.service_booking_id = service_booking_id
        card_details_screen.customer_id = customer_id
        self.manager.current = 'carddetails'

    def on_cancel_button_press(self, instance):
        try:
            service_booking_id = instance.service_booking_id
            customer_id = App.get_running_app().customer_id

            # Set the status to "Request Cancelled by Customer"
            status = "Request Cancelled by Customer"

            # Update the status in the database
            cursor.execute("update service_booking set status = '"+str(status)+"' where service_booking_id = '" + str(service_booking_id) + "' and customer_id = '" + str(customer_id) + "'")
            conn.commit()
            toast("Request cancelled successfully!")
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_service_name_from_service(service_id):
        try:
            cursor.execute("SELECT service_name FROM service WHERE service_id = '" + str(service_id) + "'")
            service = cursor.fetchone()
            if service:
                return service[0]
            else:
                return None
        except Exception as e:
            print(f"Error fetching service name: {e}")
            return None

    def get_service_provider_details_from_service(service_id):
        try:
            cursor.execute("SELECT sp.service_provider_name, sp.email, sp.phone "
                           "FROM service s "
                           "JOIN service_provider sp ON s.service_provider_id = sp.service_provider_id "
                           "WHERE s.service_id = '" + str(service_id) + "'")
            service_provider = cursor.fetchone()
            if service_provider:
                return service_provider[0], service_provider[1], service_provider[2]
            else:
                return None
        except Exception as e:
            print(f"Error fetching service provider name: {e}")
            return None

    def logout(self):
        App.get_running_app().customer_id = None
        App.get_running_app().customer_profile__details = []
        App.get_running_app().customer_view_services = []
        App.get_running_app().customer_requests = []
        App.get_running_app().customer_history = []
        self.manager.current = 'selection_screen'

class CustomerViewHistory(Screen):

    def toggle_customer_nav_drawer(self):
        self.ids.customer_nav_drawer.set_state()

    def on_pre_enter(self, *args):
        App.get_running_app().switch_to_customer_view_history()

    def on_enter(self):
        if not App.get_running_app().is_logged_in:
            return
        try:
            customer_id = App.get_running_app().customer_id
            history_table_layout = self.ids['history_table_layout']
            history_table_layout.clear_widgets()  # Clear existing widgets
            history_table_layout.padding = [50]  # Add padding around the GridLayout
            history_table_layout.spacing = [20]  # Add padding around the GridLayout

            customer_history = App.get_running_app().customer_history

            if not customer_history:
                no_history_label_customer = MDLabel(
                    text="No History Found",
                    font_size=sp(30),
                    text_color=(1, 1, 1, 1),
                    theme_text_color="Custom",
                    halign="center"
                )
                no_history_label_customer.font_size = 30
                history_table_layout.add_widget(no_history_label_customer)
                return

            for service_booking in customer_history:
                number_of_sq_feet = service_booking[1]
                description = service_booking[2]
                booking_date = service_booking[3]
                status = service_booking[7]
                service_id = service_booking[8]
                service_booking_id = service_booking[0]

                cursor.execute("select * from service where service_id = '" + str(service_id) + "'")
                service = cursor.fetchone()
                service_image = service[4]
                charger_per_sq_feet = service[3]

                service_full_name = CustomerViewHistory.get_service_by_service_id(service_id)

                service_provider_details = CustomerViewHistory.get_service_provider_details_from_service(service_id)
                service_provider_full, service_provider_email_id, service_provider_phone_number = service_provider_details

                service_provider_full_customer = MDLabel(text=str(service_provider_full), font_size=sp(15),text_color=(0, 0, 0.5, 1), theme_text_color="Custom")
                service_provider_emailid_customer = MDLabel(text=str(service_provider_email_id), font_size=sp(15),text_color=(0, 0, 0.5, 1), theme_text_color="Custom")
                service_provider_phonenum_customer = MDLabel(text=str(service_provider_phone_number), font_size=sp(15),text_color=(0, 0, 0.5, 1), theme_text_color="Custom")

                service_provider_full_customer.font_size = 15
                service_provider_emailid_customer.font_size = 15
                service_provider_phonenum_customer.font_size = 15

                card = MDCard(
                    orientation='vertical',
                    size_hint=(None, None),
                    size=(dp(300), dp(300)),
                    elevation=5,
                    padding=10,
                    md_bg_color=(0.9, 0.9, 0.9, 1)
                )

                number_of_sqfeet = MDLabel(text=str(number_of_sq_feet),font_size=sp(17),text_color=(0, 0, 0.5, 1),theme_text_color="Custom")
                service_description_full = MDLabel(text=str(description),font_size=sp(17),text_color=(0, 0, 0.5, 1),theme_text_color="Custom")
                service_booking_date_full = MDLabel(text=str(booking_date),font_size=sp(17),text_color=(0, 0, 0.5, 1),theme_text_color="Custom")
                service_status_full = MDLabel(
                    text=str(status),
                    theme_text_color="Custom",
                    text_color=(0.5, 0, 0.5, 1),  # RGB values for purple
                    bold=True,
                    font_size=sp(17),
                )
                service = MDLabel(text=service_full_name,font_size=sp(17),text_color=(0, 0, 0.5, 1),theme_text_color="Custom")
                charger = MDLabel(text=f"${charger_per_sq_feet}",font_size=sp(17),text_color=(0, 0, 0.5, 1),theme_text_color="Custom")
                service_picture = AsyncImage(source=service_image, keep_ratio=True, allow_stretch=True)

                box1 = MDBoxLayout(orientation='vertical')  # Add spacing between labels

                service_name_data = MDLabel(
                    text="Service Name:",
                    theme_text_color="Custom",
                    font_style="Caption",
                    size_hint_y=None,
                    height=20
                )
                box1.add_widget(service_name_data)
                box1.add_widget(service)

                spacer = Widget(size_hint_y=None, height=20)
                box1.add_widget(spacer)

                charge_per_sq_feet = MDLabel(
                    text="Charger Per sq.feet:",
                    theme_text_color="Custom",
                    font_style="Caption",
                    size_hint_y=None,
                    height=20
                )
                box1.add_widget(charge_per_sq_feet)
                box1.add_widget(charger)

                spacer = Widget(size_hint_y=None, height=20)
                box1.add_widget(spacer)

                number_of_sq_feet = MDLabel(
                    text="No.of sq.feet:",
                    theme_text_color="Custom",
                    font_style="Caption",
                    size_hint_y=None,
                    height=20
                )
                box1.add_widget(number_of_sq_feet)
                box1.add_widget(number_of_sqfeet)

                spacer = Widget(size_hint_y=None, height=20)
                box1.add_widget(spacer)

                description = MDLabel(
                    text="Description:",
                    theme_text_color="Custom",
                    font_style="Caption",
                    size_hint_y=None,
                    height=20
                )
                box1.add_widget(description)
                box1.add_widget(service_description_full)

                spacer = Widget(size_hint_y=None, height=20)
                box1.add_widget(spacer)

                booking_date = MDLabel(
                    text="Booking Date:",
                    theme_text_color="Custom",
                    font_style="Caption",
                    size_hint_y=None,
                    height=20
                )
                box1.add_widget(booking_date)
                box1.add_widget(service_booking_date_full)

                spacer = Widget(size_hint_y=None, height=20)
                box1.add_widget(spacer)

                if service_booking[7] in ["Request Cancelled by Customer", "Rejected Request", "Full Payment Successfull"]:
                    customer_status = MDLabel(
                        text="Status:",
                        theme_text_color="Custom",
                        font_style="Caption",
                        size_hint_y=None,
                        height=20
                    )
                    box1.add_widget(customer_status)

                    spacer = Widget(size_hint_y=None, height=20)
                    box1.add_widget(spacer)

                    box1.add_widget(service_status_full)


                spacer = Widget(size_hint_y=None, height=30)
                box1.add_widget(spacer)

                service_provider_name_customer_id = MDLabel(
                    text="Service Provider:",
                    theme_text_color="Custom",
                    font_style="Caption",
                    size_hint_y=None,
                    height=20
                )
                box1.add_widget(service_provider_name_customer_id)
                box1.add_widget(service_provider_full_customer)
                box1.add_widget(service_provider_emailid_customer)
                box1.add_widget(service_provider_phonenum_customer)

                box2 = MDBoxLayout(orientation='vertical')
                box2.add_widget(service_picture)

                cursor.execute("select * from review where service_booking_id in (select service_booking_id from service_booking where service_id = '" + str(service_id) + "')")
                reviews = cursor.fetchall()
                reviews = list(reviews)
                if len(reviews) == 0:
                    no_rating = "No Rating"
                    average_rating_label = MDLabel(text=f"Rating: {no_rating}", theme_text_color="Custom", text_color=(0, 0, 0, 1))
                else:
                    total_ratings = 0
                    number_of_ratings = 0
                    for review in reviews:
                        total_ratings = total_ratings + int(review[2])
                        number_of_ratings = number_of_ratings + 1
                    rating = total_ratings / number_of_ratings
                    rating = round(rating, 2)
                    average_rating_label = MDLabel(text=f"Rating: {rating}", theme_text_color="Custom", text_color=(0, 0, 0, 1))
                box2.add_widget(average_rating_label)

                if service_booking[7] == "Full Payment Successfull":
                    button_box = MDBoxLayout(orientation='vertical')

                    view_payment_button = MDRectangleFlatButton(
                        text="View Payment",
                        on_press=self.on_view_payment_button_press,
                        md_bg_color=get_color_from_hex("#006400"),  # Hexadecimal color for dark green
                        text_color=(1, 1, 1, 1)  # White color (RGBA values)
                    )
                    view_payment_button.service_booking_id = service_booking_id
                    button_box.add_widget(view_payment_button)

                    spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
                    button_box.add_widget(spacer)

                    view_customer_compaints = MDRectangleFlatButton(
                        text="View Complaints",
                        on_press=self.on_view_complaint_press,
                        md_bg_color=get_color_from_hex("#008080"),   # Hexadecimal color for red
                        text_color=(1, 1, 1, 1)  # White color (RGBA values)
                    )
                    view_customer_compaints.service_booking_id = service_booking_id
                    view_customer_compaints.customer_id = customer_id

                    cursor.execute("SELECT COUNT(*) FROM complaints WHERE service_booking_id = %s AND customer_id = %s",(service_booking_id, customer_id))
                    count = cursor.fetchone()[0]
                    if count > 0:
                        button_box.add_widget(view_customer_compaints)
                    else:
                        button_box.remove_widget(view_customer_compaints)

                    spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
                    button_box.add_widget(spacer)

                    review_rating = MDRectangleFlatButton(
                        text="Rating",
                        on_press=self.on_review_rating_press,
                        md_bg_color=get_color_from_hex("#8A2BE2"),  # Hexadecimal color for violet
                        text_color=(1, 1, 1, 1)  # White color (RGBA values)
                    )
                    review_rating.service_booking_id = service_booking_id

                    cursor.execute("SELECT COUNT(*) FROM review ""WHERE service_booking_id = '" + str(service_booking_id) + "'")
                    count = cursor.fetchone()[0]
                    if count > 0:
                        box2.remove_widget(review_rating)
                    else:
                        box2.add_widget(review_rating)

                    spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
                    button_box.add_widget(spacer)

                    complaints = MDRectangleFlatButton(
                        text="Raise Complaints",
                        on_press=self.on_raise_complaints_press,
                        md_bg_color=get_color_from_hex("#008080"),   # Hexadecimal color for red
                        text_color=(1, 1, 1, 1)  # White color (RGBA values)
                    )
                    complaints.service_booking_id = service_booking_id
                    complaints.customer_id = customer_id

                    cursor.execute("SELECT COUNT(*) FROM complaints ""WHERE service_booking_id = '" + str(service_booking_id) + "' and customer_id = '"+str(customer_id)+"'")
                    count = cursor.fetchone()[0]
                    if count > 0:
                        button_box.remove_widget(complaints)
                    else:
                        button_box.add_widget(complaints)

                    box2.add_widget(button_box)

                box = MDBoxLayout(orientation='horizontal')
                box.add_widget(box1)
                box.add_widget(box2)

                # Add the box layout to the card
                card.add_widget(box)

                history_table_layout.add_widget(card)
        except Exception as e:
            print(f"An error occurred: {e}")

    def on_view_payment_button_press(self, instance):
        service_booking_id = instance.service_booking_id
        view_full_payment_screen = self.manager.get_screen('customer_view_full_payment')
        view_full_payment_screen.service_booking_id = service_booking_id
        self.manager.current = 'customer_view_full_payment'

    def on_raise_complaints_press(self, instance):
        service_booking_id = instance.service_booking_id
        customer_id = instance.customer_id

        complaints_screen = self.manager.get_screen('customer_raise_complaint')
        complaints_screen.service_booking_id = service_booking_id
        complaints_screen.customer_id = customer_id
        complaints_screen.service_provider_id = None  # Set to None for customer
        self.manager.current = 'customer_raise_complaint'

    def on_view_complaint_press(self, instance):
        service_booking_id = instance.service_booking_id
        customer_id = instance.customer_id
        view_complaint_screen = self.manager.get_screen('viewcomplaint')
        view_complaint_screen.service_booking_id = service_booking_id
        view_complaint_screen.customer_id = customer_id
        self.manager.current = 'viewcomplaint'

    def on_review_rating_press(self, instance):
        service_booking_id = instance.service_booking_id
        review_rating_screen = self.manager.get_screen('reviewrating')
        review_rating_screen.service_booking_id = service_booking_id
        self.manager.current = 'reviewrating'

    def get_service_by_service_id(service_id):
        try:
            cursor.execute("SELECT service_name FROM service WHERE service_id = '" + str(service_id) + "'")
            service = cursor.fetchone()
            if service:
                return service[0]
            else:
                return None
        except Exception as e:
            print(f"Error fetching service name: {e}")
            return None

    def get_service_provider_details_from_service(service_id):
        try:
            cursor.execute("SELECT sp.service_provider_name, sp.email, sp.phone "
                           "FROM service s "
                           "JOIN service_provider sp ON s.service_provider_id = sp.service_provider_id "
                           "WHERE s.service_id = '" + str(service_id) + "'")
            service_provider = cursor.fetchone()
            if service_provider:
                return service_provider[0], service_provider[1], service_provider[2]
            else:
                return None
        except Exception as e:
            print(f"Error fetching service provider name: {e}")
            return None

    def logout(self):
        App.get_running_app().customer_id = None
        App.get_running_app().customer_profile__details = []
        App.get_running_app().customer_view_services = []
        App.get_running_app().customer_requests = []
        App.get_running_app().customer_history = []
        self.manager.current = 'selection_screen'

class ProviderViewRequests(Screen):
    selected_date = None  # Initialize the selected_date attribute

    def __init__(self, **kwargs):
        super(ProviderViewRequests, self).__init__(**kwargs)
        self.calendar_labels = {}

    def toggle_nav_drawer(self):
        self.ids.provider_nav_drawer.set_state()

    def on_pre_enter(self, *args):
        App.get_running_app().switch_to_provider_view_request()


    def on_enter(self):
        if not App.get_running_app().is_logged_in:
            return
        try:
            provider_request_table_layout = self.ids['provider_request_table_layout']
            provider_request_table_layout.clear_widgets()  # Clear existing widgets
            provider_request_table_layout.padding = [40]  # Add padding around the GridLayout
            provider_request_table_layout.spacing = [20]  # Add padding around the GridLayout

            service_provider_view_requests = App.get_running_app().service_provider_view_requests

            # Fetch the newly added service
            cursor.execute("SELECT * FROM service_booking WHERE service_booking_id = LAST_INSERT_ID()")
            conn.commit()
            new_provider_request = cursor.fetchone()

            App.get_running_app().service_provider_view_requests = list(App.get_running_app().service_provider_view_requests)
            App.get_running_app().service_provider_view_requests.append(new_provider_request)

            if not service_provider_view_requests:
                no_requests_label = MDLabel(
                    text="No Requests Found",
                    font_size=sp(30),
                    text_color=(1, 1, 1, 1),
                    theme_text_color="Custom",
                    halign="center"
                )
                no_requests_label.font_size = 30
                provider_request_table_layout.add_widget(no_requests_label)
                return

            for service_booking in service_provider_view_requests:
                service_booking_id = service_booking[0]
                service_id = service_booking[8]
                number_of_sq_feet = float(service_booking[1])
                description = service_booking[2]
                status = service_booking[7]
                customer_id = service_booking[9]
                booking_date = service_booking[3]

                if status in ["Rejected Request", "Request Cancelled by Customer"]:
                    continue  # Skip this card

                cursor.execute("select * from service where service_id = '" + str(service_id) + "'")
                service = cursor.fetchone()
                service_image = service[4]
                charger_per_sq_feet = float(service[3])

                total_charge = number_of_sq_feet * charger_per_sq_feet
                advance_payment = total_charge * 0.2
                remaining_amount = total_charge - advance_payment

                service_name_provider = ProviderViewRequests.get_service_name_from_ProviderViewRequests(service_id)

                customer_data = ProviderViewRequests.get_customer_name_from_service(customer_id)

                card = MDCard(
                    orientation='vertical',
                    size_hint=(None, None),
                    size=(dp(250), dp(300)),
                    elevation=5,
                    padding=15,
                    md_bg_color=(0.9, 0.9, 0.9, 1)
                )

                number_of_sq_feet_provider = MDLabel(text=str(number_of_sq_feet),font_size=sp(15),text_color=(0, 0, 0.5, 1),theme_text_color="Custom")
                description_provider = MDLabel(text=str(description),font_size=sp(15),text_color=(0, 0, 0.5, 1),theme_text_color="Custom")
                booking_date_provider = MDLabel(text=str(booking_date),font_size=sp(15),text_color=(0, 0, 0.5, 1),theme_text_color="Custom")
                status_provider = MDLabel(
                    text=str(status),
                    id=f"status_label_{service_booking_id}",
                    theme_text_color="Custom",
                    text_color=(0.5, 0, 0.5, 1),  # RGB values for purple
                    bold=True,
                    font_size=sp(15),
                )
                service_name_provider_label = MDLabel(text=service_name_provider,font_size=sp(15),text_color=(0, 0, 0.5, 1),theme_text_color="Custom")
                charger_per_sq_feet_provider = MDLabel(text=f"${charger_per_sq_feet}",font_size=sp(15),text_color=(0, 0, 0.5, 1),theme_text_color="Custom")
                service_picture_provider = AsyncImage(source=service_image, keep_ratio=True, allow_stretch=True)

                box1 = MDBoxLayout(orientation='vertical')  # Add spacing between labels

                service_name_data_provider = MDLabel(
                    text="Service Name:",
                    theme_text_color="Custom",
                    font_style="Caption",
                    size_hint_y=None,
                    height=20
                )
                box1.add_widget(service_name_data_provider)
                box1.add_widget(Widget(size_hint_y=None, height=10))  # Adjust the height value as needed
                box1.add_widget(service_name_provider_label)

                spacer = Widget(size_hint_y=None, height=30)
                box1.add_widget(spacer)

                charge_per_sq_feet_data_provider = MDLabel(
                    text="Charger Per sq.feet:",
                    theme_text_color="Custom",
                    font_style="Caption",
                    size_hint_y=None,
                    height=20
                )
                box1.add_widget(charge_per_sq_feet_data_provider)
                box1.add_widget(Widget(size_hint_y=None, height=10))  # Adjust the height value as needed
                box1.add_widget(charger_per_sq_feet_provider)

                spacer = Widget(size_hint_y=None, height=30)
                box1.add_widget(spacer)

                number_of_sq_feet_data_provider = MDLabel(
                    text="No.of sq.feet:",
                    theme_text_color="Custom",
                    font_style="Caption",
                    size_hint_y=None,
                    height=20
                )
                box1.add_widget(number_of_sq_feet_data_provider)
                box1.add_widget(Widget(size_hint_y=None, height=10))  # Adjust the height value as needed
                box1.add_widget(number_of_sq_feet_provider)

                spacer = Widget(size_hint_y=None, height=30)
                box1.add_widget(spacer)

                description_data_provider = MDLabel(
                    text="Description:",
                    theme_text_color="Custom",
                    font_style="Caption",
                    size_hint_y=None,
                    height=20
                )
                box1.add_widget(description_data_provider)
                box1.add_widget(Widget(size_hint_y=None, height=10))  # Adjust the height value as needed
                box1.add_widget(description_provider)

                spacer = Widget(size_hint_y=None, height=30)
                box1.add_widget(spacer)

                booking_provider = MDLabel(
                    text="Booking Date:",
                    theme_text_color="Custom",
                    font_style="Caption",
                    size_hint_y=None,
                    height=20
                )
                box1.add_widget(booking_provider)
                box1.add_widget(Widget(size_hint_y=None, height=10))  # Adjust the height value as needed
                box1.add_widget(booking_date_provider)

                spacer = Widget(size_hint_y=None, height=30)
                box1.add_widget(spacer)

                if service_booking[7] in ["Request Sended", "Paid Advance Amount", "Rejected Request", "Cancelled by customer", "Accepted Request", "Service Completed", "Full Payment Successfull"]:
                    status_data_provider = MDLabel(
                        text="Status:",
                        theme_text_color="Custom",
                        font_style="Caption",
                        size_hint_y=None,
                        height=20
                    )
                    box1.add_widget(status_data_provider)
                    box1.add_widget(Widget(size_hint_y=None, height=10))  # Adjust the height value as needed
                    box1.add_widget(status_provider)

                spacer = Widget(size_hint_y=None, height=30)
                box1.add_widget(spacer)

                Customer_Details = MDLabel(
                    text="Customer Details",
                    theme_text_color="Custom",
                    font_style="Caption",
                    size_hint_y=None,
                    height=dp(30)
                )
                box1.add_widget(Customer_Details)
                box1.add_widget(Widget(size_hint_y=None, height=10))  # Adjust the height value as needed
                if customer_data is not None:
                    customer_name = customer_data[0]  # Access the customer name
                    phone_number = customer_data[1]  # Access the phone number
                    address = customer_data[2]
                    customer_name_data_label = MDLabel(
                        text=f"Name: {customer_name}",
                        font_size=sp(13),
                        text_color=(0, 0, 0.5, 1),
                        theme_text_color="Custom"
                    )
                    box1.add_widget(customer_name_data_label)

                    box1.add_widget(Widget(size_hint_y=None, height=25))  # Adjust the height value as needed

                    customer_phone_data_label = MDLabel(
                        text=f"Phone: {phone_number}",
                        font_size=sp(13),
                        text_color=(0, 0, 0.5, 1),
                        theme_text_color="Custom"
                    )
                    box1.add_widget(customer_phone_data_label)

                    box1.add_widget(Widget(size_hint_y=None, height=25))  # Adjust the height value as needed

                    customer_address_label = MDLabel(
                        text=f"Address: {address}",
                        font_size=sp(13),
                        text_color=(0, 0, 0.5, 1),
                        theme_text_color="Custom"
                    )
                    box1.add_widget(customer_address_label)
                else:
                    print("No matching customer found.")

                spacer = Widget(size_hint_y=None, height=35)
                box1.add_widget(spacer)

                if service_booking[7] in ["Request Sended", "Accepted Request"]:
                    total_charge = MDLabel(
                        text=f"Total Charge: ${total_charge}",
                        theme_text_color="Custom",
                        text_color=(0.5, 0, 0.5, 1),
                        font_style="Caption",
                        size_hint_y=None,
                        height=dp(30),
                        bold=True
                    )
                    box1.add_widget(total_charge)

                    advance_amount = MDLabel(
                        text=f"Advance Amount: ${advance_payment}",
                        theme_text_color="Custom",
                        text_color=(0.5, 0, 0.5, 1),
                        font_style="Caption",
                        size_hint_y=None,
                        height=dp(30),
                        bold=True
                    )
                    box1.add_widget(advance_amount)

                    remaining_amount = MDLabel(
                        text=f"Remaining Amount: ${remaining_amount}",
                        theme_text_color="Custom",
                        text_color=(0.5, 0, 0.5, 1),
                        font_style="Caption",
                        size_hint_y=None,
                        height=dp(30),
                        bold=True
                    )
                    box1.add_widget(remaining_amount)

                elif service_booking[7] in ["Paid Advance Amount", "Service Completed"]:
                    total_charge = MDLabel(
                        text=f"Total Charge: ${total_charge}",
                        theme_text_color="Custom",
                        text_color=(0.5, 0, 0.5, 1),
                        font_style="Caption",
                        size_hint_y=None,
                        height=dp(30),
                        bold=True
                    )
                    box1.add_widget(total_charge)

                    remaining_amount = MDLabel(
                        text=f"Remaining Amount: ${remaining_amount}",
                        theme_text_color="Custom",
                        text_color=(0.5, 0, 0.5, 1),
                        font_style="Caption",
                        size_hint_y=None,
                        height=dp(30),
                        bold=True
                    )
                    box1.add_widget(remaining_amount)

                if service_booking[7] in ["Accepted Request", "Paid Advance Amount", "Service Completed"]:
                    service_booking_date = MDLabel(
                        text=f"Service Booking Date: {service_booking[4]}",
                        theme_text_color="Custom",
                        text_color=(0, 0, 0, 1),  # Black color (RGBA values)
                        font_style="Caption",
                        font_size=dp(20),  # Set the font size to 20 density-independent pixels (dp)
                        size_hint_y=None,
                        height=dp(30),
                        bold=True
                    )
                    box1.add_widget(service_booking_date)

                if service_booking[7] in ["Paid Advance Amount", "Service Completed"] :
                    paid_amount_provider = MDLabel(
                        text=f"Paid Amount: ${service_booking[5]}",
                        theme_text_color="Custom",
                        text_color=(0, 0.5, 0, 1),  # Dark green color (RGBA values)
                        font_style="Caption",
                        size_hint_y=None,
                        height=dp(30),
                        bold=True
                    )
                    box1.add_widget(paid_amount_provider)

                box2 = MDBoxLayout(orientation='vertical')
                box2.add_widget(service_picture_provider)

                cursor.execute("select * from review where service_booking_id in (select service_booking_id from service_booking where service_id = '" + str(service_id) + "')")
                reviews = cursor.fetchall()
                reviews = list(reviews)
                if len(reviews) == 0:
                    no_rating = "No Rating"
                    average_rating_label = MDLabel(text=f"Rating: {no_rating}", theme_text_color="Custom", text_color=(0, 0, 0, 1))
                else:
                    total_ratings = 0
                    number_of_ratings = 0
                    for review in reviews:
                        total_ratings = total_ratings + int(review[2])
                        number_of_ratings = number_of_ratings + 1
                    rating = total_ratings / number_of_ratings
                    rating = round(rating, 2)
                    average_rating_label = MDLabel(text=f"Rating: {rating}", theme_text_color="Custom", text_color=(0, 0, 0, 1))
                box2.add_widget(average_rating_label)

                box2.add_widget(Widget(size_hint_y=None, height=30))  # Adjust the height value as needed

                if status == "Request Sended":
                    advance_amount_textfield = MDTextField(hint_text= "Enter Advance Amount",hint_text_color=(0, 0, 0, 1),mode= "fill")

                    calendar_label_id = f"calendar_label_{service_booking_id}"

                    calendar_button = MDRectangleFlatButton(
                        text="Select Date",
                        theme_text_color="Custom",
                        md_bg_color=(0, 0.5, 0.5, 1),  # Teal color (RGBA values)
                        text_color=(0, 0, 0, 1),  # Black color (RGBA values)
                        on_press=lambda instance, booking_id=service_booking_id: self.show_date_picker(instance,booking_id)
                    )
                    calendar_label = MDLabel(
                        text="Selected Date: ",
                        theme_text_color="Custom",
                        text_color=(0, 0, 0, 1),
                        id=calendar_label_id  # Assign a unique id based on the service_booking_id
                    )
                    box2.add_widget(advance_amount_textfield)

                    box2.add_widget(Widget(size_hint_y=None, height=20))  # Adjust the height value as needed

                    box2.add_widget(calendar_button)
                    box2.add_widget(calendar_label)
                    self.calendar_labels[service_booking_id] = calendar_label

                accept_button = MDRectangleFlatButton(
                    text="Accept Request",
                    on_press=self.on_accept_button_press,
                    md_bg_color=(0, 0.5, 0, 1),  # Dark Green color (RGBA values)
                    text_color=(1, 1, 1, 1)  # White color (RGBA values)
                )
                accept_button.service_booking_id = service_booking_id
                accept_button.advance_payment = advance_payment
                accept_button.remaining_amount = remaining_amount

                reject_button = MDRectangleFlatButton(
                    text="Reject Request",
                    on_press=self.on_reject_button_press,
                    md_bg_color=(1, 0, 0, 1),  # Red color (RGBA values)
                    text_color=(1, 1, 1, 1)  # White color (RGBA values)
                )
                reject_button.service_booking_id = service_booking_id

                box2.add_widget(accept_button)
                box2.add_widget(Widget(size_hint_y=None, height=20))  # Adjust the height value as needed
                box2.add_widget(reject_button)

                if status == "Accepted Request":
                    accept_button.disabled = True
                    accept_button.opacity = 0
                    reject_button.disabled = True
                    reject_button.opacity = 0
                elif status == "Rejected Request":
                    accept_button.disabled = True
                    accept_button.opacity = 0
                    reject_button.disabled = True
                    reject_button.opacity = 0
                elif status == "Request Cancelled by Customer":
                    accept_button.disabled = True
                    accept_button.opacity = 0
                    reject_button.disabled = True
                    reject_button.opacity = 0
                elif status == "Paid Advance Amount":
                    accept_button.disabled = True
                    accept_button.opacity = 0
                    reject_button.disabled = True
                    reject_button.opacity = 0
                elif status == "Service Completed":
                    accept_button.disabled = True
                    accept_button.opacity = 0
                    reject_button.disabled = True
                    reject_button.opacity = 0
                elif status == "Full Payment Successfull":
                    accept_button.disabled = True
                    accept_button.opacity = 0
                    reject_button.disabled = True
                    reject_button.opacity = 0
                else:
                    accept_button.disabled = False
                    accept_button.opacity = 1
                    reject_button.disabled = False
                    reject_button.opacity = 1

                today_date = datetime.now().strftime('%Y-%m-%d')
                if service_booking[4] == today_date and service_booking[7] == 'Paid Advance Amount':
                    service_done_button = MDRectangleFlatButton(
                        text="Service Done",
                        on_press=self.service_done,
                        md_bg_color=(0, 0, 0.5, 1),  # Dark Blue (RGBA values)
                        text_color=(1, 1, 1, 1)  # White color (RGBA values)
                    )
                    service_done_button.service_booking_id = service_booking_id
                    box2.add_widget(service_done_button)

                box = MDBoxLayout(orientation='horizontal')
                box.add_widget(box1)
                box.add_widget(box2)

                # Add the box layout to the card
                card.add_widget(box)

                provider_request_table_layout.add_widget(card)
        except Exception as e:
            print(f"An error occurred: {e}")

    def service_done(self , instance):
        service_booking_id = instance.service_booking_id
        cursor.execute("update service_booking set status = 'Service Completed' where service_booking_id = '" + str(service_booking_id) + "'")
        conn.commit()
        toast("Service Successfully Completed")

    def show_date_picker(self, instance, booking_id):
        # Store the booking_id that corresponds to the clicked button
        self.clicked_booking_id = booking_id

        date_picker = MDDatePicker()
        date_picker.bind(on_save=self.on_date_selected)
        date_picker.open()

    def on_date_selected(self, instance, value, date_range):
        # Check if a booking_id was clicked
        if hasattr(self, 'clicked_booking_id'):
            booking_id = self.clicked_booking_id

            # Get the corresponding card's calendar_label
            calendar_label = self.calendar_labels.get(booking_id)

            if calendar_label is not None:
                # Update the label text with the selected date
                calendar_label.text = f"Selected Date: {value}"
            # Remove the reference to the clicked booking_id
            del self.clicked_booking_id

    def on_reject_button_press(self, instance):
        service_booking_id = instance.service_booking_id
        cursor.execute("update service_booking set status = 'Rejected Request' where service_booking_id = '" + str(service_booking_id) + "'")
        conn.commit()
        toast("Request Rejected Sccussfully")

    def on_accept_button_press(self, instance):
        service_booking_id = instance.service_booking_id
        advance_payment = instance.advance_payment
        remaining_amount_str = instance.remaining_amount.text
        calendar_label = self.calendar_labels.get(service_booking_id)
        selected_date = calendar_label.text.split(": ")[1]  # Assuming

        remaining_amount = float(remaining_amount_str.split('$')[1])

        cursor.execute("update service_booking set status = 'Accepted Request' , advance_amount = '"+str(advance_payment)+"' , remaining_amount = '"+str(remaining_amount)+"' , service_date_time = '"+str(selected_date)+"'where service_booking_id = '" + str(service_booking_id) + "'")
        conn.commit()

        toast("Request Accepted Sccussfully")


    def get_service_name_from_ProviderViewRequests(service_id):
        try:
            cursor.execute("SELECT service_name FROM service WHERE service_id = '" + str(service_id) + "'")
            service = cursor.fetchone()
            if service:
                return service[0]
            else:
                return None
        except Exception as e:
            print(f"Error fetching service name: {e}")
            return None

    def get_customer_name_from_service(customer_id):
        try:
            cursor.execute("SELECT customer_name,phone,address FROM customer WHERE customer_id = '" + str(customer_id) + "'")
            customer = cursor.fetchone()
            if customer:
                return customer[0], customer[1], customer[2]
            else:
                return None
        except Exception as e:
            print(f"Error fetching category name: {e}")
            return None

    def show_date_picker_search(self):
        picker = MDDatePicker()
        picker.bind(on_save=self.on_date_select)
        picker.open()

    def on_date_select(self, instance, value, date_range):
        selected_date = value.strftime("%Y-%m-%d")
        self.ids.date_field.text = selected_date
        ProviderViewRequests.selected_date = selected_date

    def perform_search(self):
        selected_date = ProviderViewRequests.selected_date

        provider_request_table_layout = self.ids['provider_request_table_layout']
        provider_request_table_layout.clear_widgets()  # Clear existing widgets
        provider_request_table_layout.padding = [40]  # Add padding around the GridLayout
        provider_request_table_layout.spacing = [20]  # Add padding around the GridLayout

        service_provider_view_requests = App.get_running_app().service_provider_view_requests

        for service_booking in service_provider_view_requests:
            booking_date = service_booking[4]
            if selected_date == None or selected_date == booking_date:
                service_booking_id = service_booking[0]
                service_id = service_booking[8]
                number_of_sq_feet = float(service_booking[1])
                description = service_booking[2]
                status = service_booking[7]
                customer_id = service_booking[9]
                booking_date = service_booking[3]

                if status in ["Rejected Request", "Request Cancelled by Customer"]:
                    continue  # Skip this card

                cursor.execute("select * from service where service_id = '" + str(service_id) + "'")
                service = cursor.fetchone()
                service_image = service[4]
                charger_per_sq_feet = float(service[3])

                total_charge = number_of_sq_feet * charger_per_sq_feet
                advance_payment = total_charge * 0.2
                remaining_amount = total_charge - advance_payment

                service_name_provider = ProviderViewRequests.get_service_name_from_ProviderViewRequests(service_id)

                customer_data = ProviderViewRequests.get_customer_name_from_service(customer_id)

                card = MDCard(
                    orientation='vertical',
                    size_hint=(None, None),
                    size=(dp(300), dp(300)),
                    elevation=5,
                    padding=10,
                    md_bg_color=(0.9, 0.9, 0.9, 1)
                )

                number_of_sq_feet_provider = MDLabel(text=str(number_of_sq_feet), font_size=sp(15),text_color=(0, 0, 0.5, 1), theme_text_color="Custom")
                description_provider = MDLabel(text=str(description), font_size=sp(15), text_color=(0, 0, 0.5, 1),theme_text_color="Custom")
                booking_date_provider = MDLabel(text=str(booking_date), font_size=sp(15), text_color=(0, 0, 0.5, 1),theme_text_color="Custom")
                status_provider = MDLabel(
                    text=str(status),
                    theme_text_color="Custom",
                    text_color=(0.5, 0, 0.5, 1),  # RGB values for purple
                    bold=True,
                    font_size=sp(15),
                )
                service_name_provider_label = MDLabel(text=service_name_provider, font_size=sp(15),text_color=(0, 0, 0.5, 1), theme_text_color="Custom")
                charger_per_sq_feet_provider = MDLabel(text=f"${charger_per_sq_feet}", font_size=sp(15), text_color=(0, 0, 0.5, 1), theme_text_color="Custom")
                service_picture_provider = AsyncImage(source=service_image, keep_ratio=True, allow_stretch=True)

                box1 = MDBoxLayout(orientation='vertical')  # Add spacing between labels

                service_name_data_provider = MDLabel(
                    text="Service Name:",
                    theme_text_color="Custom",
                    font_style="Caption",
                    size_hint_y=None,
                    height=20
                )
                box1.add_widget(service_name_data_provider)
                box1.add_widget(Widget(size_hint_y=None, height=10))  # Adjust the height value as needed
                box1.add_widget(service_name_provider_label)

                spacer = Widget(size_hint_y=None, height=30)
                box1.add_widget(spacer)

                charge_per_sq_feet_data_provider = MDLabel(
                    text="Charger Per sq.feet:",
                    theme_text_color="Custom",
                    font_style="Caption",
                    size_hint_y=None,
                    height=20
                )
                box1.add_widget(charge_per_sq_feet_data_provider)
                box1.add_widget(Widget(size_hint_y=None, height=10))  # Adjust the height value as needed
                box1.add_widget(charger_per_sq_feet_provider)

                spacer = Widget(size_hint_y=None, height=30)
                box1.add_widget(spacer)

                number_of_sq_feet_data_provider = MDLabel(
                    text="No.of sq.feet:",
                    theme_text_color="Custom",
                    font_style="Caption",
                    size_hint_y=None,
                    height=20
                )
                box1.add_widget(number_of_sq_feet_data_provider)
                box1.add_widget(Widget(size_hint_y=None, height=10))  # Adjust the height value as needed
                box1.add_widget(number_of_sq_feet_provider)

                spacer = Widget(size_hint_y=None, height=30)
                box1.add_widget(spacer)

                description_data_provider = MDLabel(
                    text="Description:",
                    theme_text_color="Custom",
                    font_style="Caption",
                    size_hint_y=None,
                    height=20
                )
                box1.add_widget(description_data_provider)
                box1.add_widget(Widget(size_hint_y=None, height=10))  # Adjust the height value as needed
                box1.add_widget(description_provider)

                spacer = Widget(size_hint_y=None, height=30)
                box1.add_widget(spacer)

                booking_provider = MDLabel(
                    text="Booking Date:",
                    theme_text_color="Custom",
                    font_style="Caption",
                    size_hint_y=None,
                    height=20
                )
                box1.add_widget(booking_provider)
                box1.add_widget(Widget(size_hint_y=None, height=10))  # Adjust the height value as needed
                box1.add_widget(booking_date_provider)

                spacer = Widget(size_hint_y=None, height=30)
                box1.add_widget(spacer)

                if service_booking[7] in ["Request Sended", "Paid Advance Amount", "Rejected Request","Cancelled by customer", "Accepted Request", "Service Completed"]:
                    status_data_provider = MDLabel(
                        text="Status:",
                        theme_text_color="Custom",
                        font_style="Caption",
                        size_hint_y=None,
                        height=20
                    )
                    box1.add_widget(status_data_provider)
                    box1.add_widget(Widget(size_hint_y=None, height=10))  # Adjust the height value as needed
                    box1.add_widget(status_provider)

                spacer = Widget(size_hint_y=None, height=30)
                box1.add_widget(spacer)

                Customer_Details = MDLabel(
                    text="Customer Details",
                    theme_text_color="Custom",
                    font_style="Caption",
                    size_hint_y=None,
                    height=dp(30)
                )
                box1.add_widget(Customer_Details)
                box1.add_widget(Widget(size_hint_y=None, height=10))  # Adjust the height value as needed
                if customer_data is not None:
                    customer_name = customer_data[0]  # Access the customer name
                    phone_number = customer_data[1]  # Access the phone number
                    address = customer_data[2]
                    customer_name_data_label = MDLabel(
                        text=f"Name: {customer_name}",
                        font_size=sp(13),
                        text_color=(0, 0, 0.5, 1),
                        theme_text_color="Custom"
                    )
                    box1.add_widget(customer_name_data_label)

                    box1.add_widget(Widget(size_hint_y=None, height=25))  # Adjust the height value as needed

                    customer_phone_data_label = MDLabel(
                        text=f"Phone: {phone_number}",
                        font_size=sp(13),
                        text_color=(0, 0, 0.5, 1),
                        theme_text_color="Custom"
                    )
                    box1.add_widget(customer_phone_data_label)

                    box1.add_widget(Widget(size_hint_y=None, height=25))  # Adjust the height value as needed

                    customer_address_label = MDLabel(
                        text=f"Address: {address}",
                        font_size=sp(13),
                        text_color=(0, 0, 0.5, 1),
                        theme_text_color="Custom"
                    )
                    box1.add_widget(customer_address_label)
                else:
                    print("No matching customer found.")

                spacer = Widget(size_hint_y=None, height=35)
                box1.add_widget(spacer)

                if service_booking[7] == "Request Sended":
                    total_charge = MDLabel(
                        text=f"Total Charge: ${total_charge}",
                        theme_text_color="Custom",
                        text_color=(0.5, 0, 0.5, 1),
                        font_style="Caption",
                        size_hint_y=None,
                        height=dp(30),
                        bold=True
                    )
                    box1.add_widget(total_charge)

                    advance_amount = MDLabel(
                        text=f"Advance Amount: ${advance_payment}",
                        theme_text_color="Custom",
                        text_color=(0.5, 0, 0.5, 1),
                        font_style="Caption",
                        size_hint_y=None,
                        height=dp(30),
                        bold=True
                    )
                    box1.add_widget(advance_amount)

                    remaining_amount = MDLabel(
                        text=f"Remaining Amount: ${remaining_amount}",
                        theme_text_color="Custom",
                        text_color=(0.5, 0, 0.5, 1),
                        font_style="Caption",
                        size_hint_y=None,
                        height=dp(30),
                        bold=True
                    )
                    box1.add_widget(remaining_amount)

                elif service_booking[7] in ["Paid Advance Amount", "Service Completed"]:
                    total_charge = MDLabel(
                        text=f"Total Charge: ${total_charge}",
                        theme_text_color="Custom",
                        text_color=(0.5, 0, 0.5, 1),
                        font_style="Caption",
                        size_hint_y=None,
                        height=dp(30),
                        bold=True
                    )
                    box1.add_widget(total_charge)

                    remaining_amount = MDLabel(
                        text=f"Remaining Amount: ${remaining_amount}",
                        theme_text_color="Custom",
                        text_color=(0.5, 0, 0.5, 1),
                        font_style="Caption",
                        size_hint_y=None,
                        height=dp(30),
                        bold=True
                    )
                    box1.add_widget(remaining_amount)

                if service_booking[7] in ["Accepted Request", "Paid Advance Amount", "Service Completed"]:
                    service_booking_date = MDLabel(
                        text=f"Service Booking Date: {service_booking[4]}",
                        theme_text_color="Custom",
                        text_color=(0, 0, 0, 1),  # Black color (RGBA values)
                        font_style="Caption",
                        font_size=dp(20),  # Set the font size to 20 density-independent pixels (dp)
                        size_hint_y=None,
                        height=dp(30),
                        bold=True
                    )
                    box1.add_widget(service_booking_date)

                if service_booking[7] == "Paid Advance Amount":
                    paid_amount_provider = MDLabel(
                        text=f"Paid Amount: ${service_booking[5]}",
                        theme_text_color="Custom",
                        text_color=(0, 0.5, 0, 1),  # Dark green color (RGBA values)
                        font_style="Caption",
                        size_hint_y=None,
                        height=dp(30),
                        bold=True
                    )
                    box1.add_widget(paid_amount_provider)

                box2 = MDBoxLayout(orientation='vertical')
                box2.add_widget(service_picture_provider)

                cursor.execute("select * from review where service_booking_id in (select service_booking_id from service_booking where service_id = '" + str(service_id) + "')")
                reviews = cursor.fetchall()
                reviews = list(reviews)
                if len(reviews) == 0:
                    no_rating = "No Rating"
                    average_rating_label = MDLabel(text=f"Rating: {no_rating}", theme_text_color="Custom", text_color=(0, 0, 0, 1))
                else:
                    total_ratings = 0
                    number_of_ratings = 0
                    for review in reviews:
                        total_ratings = total_ratings + int(review[2])
                        number_of_ratings = number_of_ratings + 1
                    rating = total_ratings / number_of_ratings
                    rating = round(rating, 2)
                    average_rating_label = MDLabel(text=f"Rating: {rating}", theme_text_color="Custom", text_color=(0, 0, 0, 1))
                box2.add_widget(average_rating_label)

                box2.add_widget(Widget(size_hint_y=None, height=30))  # Adjust the height value as needed

                if status == "Request Sended":
                    advance_amount_textfield = MDTextField(hint_text="Enter Advance Amount",
                                                           hint_text_color=(0, 0, 0, 1), mode="fill")

                    calendar_label_id = f"calendar_label_{service_booking_id}"

                    calendar_button = MDRectangleFlatButton(
                        text="Select Date",
                        theme_text_color="Custom",
                        md_bg_color=(0, 0.5, 0.5, 1),  # Teal color (RGBA values)
                        text_color=(0, 0, 0, 1),  # Black color (RGBA values)
                        on_press=lambda instance, booking_id=service_booking_id: self.show_date_picker(instance,
                                                                                                       booking_id)
                    )
                    calendar_label = MDLabel(
                        text="Selected Date: ",
                        theme_text_color="Custom",
                        text_color=(0, 0, 0, 1),
                        id=calendar_label_id  # Assign a unique id based on the service_booking_id
                    )
                    box2.add_widget(advance_amount_textfield)

                    box2.add_widget(Widget(size_hint_y=None, height=20))  # Adjust the height value as needed

                    box2.add_widget(calendar_button)
                    box2.add_widget(calendar_label)
                    self.calendar_labels[service_booking_id] = calendar_label

                spacer = Widget(size_hint_y=None, height=20)
                box1.add_widget(spacer)

                accept_button = MDRectangleFlatButton(
                    text="Accept Request",
                    on_press=self.on_accept_button_press,
                    md_bg_color=(0, 0.5, 0, 1),  # Dark Green color (RGBA values)
                    text_color=(1, 1, 1, 1)  # White color (RGBA values)
                )
                accept_button.service_booking_id = service_booking_id
                accept_button.advance_payment = advance_payment
                accept_button.remaining_amount = remaining_amount

                reject_button = MDRectangleFlatButton(
                    text="Reject Request",
                    on_press=self.on_reject_button_press,
                    md_bg_color=(1, 0, 0, 1),  # Red color (RGBA values)
                    text_color=(1, 1, 1, 1)  # White color (RGBA values)
                )
                reject_button.service_booking_id = service_booking_id

                box2.add_widget(accept_button)
                box2.add_widget(Widget(size_hint_y=None, height=20))  # Adjust the height value as needed
                box2.add_widget(reject_button)

                if status == "Accepted Request":
                    accept_button.disabled = True
                    accept_button.opacity = 0
                    reject_button.disabled = True
                    reject_button.opacity = 0
                elif status == "Rejected Request":
                    accept_button.disabled = True
                    accept_button.opacity = 0
                    reject_button.disabled = True
                    reject_button.opacity = 0
                elif status == "Request Cancelled by Customer":
                    accept_button.disabled = True
                    accept_button.opacity = 0
                    reject_button.disabled = True
                    reject_button.opacity = 0
                elif status == "Paid Advance Amount":
                    accept_button.disabled = True
                    accept_button.opacity = 0
                    reject_button.disabled = True
                    reject_button.opacity = 0
                elif status == "Service Completed":
                    accept_button.disabled = True
                    accept_button.opacity = 0
                    reject_button.disabled = True
                    reject_button.opacity = 0
                elif status == "Full Payment Successfull":
                    accept_button.disabled = True
                    accept_button.opacity = 0
                    reject_button.disabled = True
                    reject_button.opacity = 0
                else:
                    accept_button.disabled = False
                    accept_button.opacity = 1
                    reject_button.disabled = False
                    reject_button.opacity = 1

                today_date = datetime.now().strftime('%Y-%m-%d')
                if service_booking[4] == today_date and service_booking[7] == 'Paid Advance Amount':
                    service_done_button = MDRectangleFlatButton(
                        text="Service Done",
                        on_press=self.service_done,
                        md_bg_color=(0, 0, 0.5, 1),  # Dark Blue (RGBA values)
                        text_color=(1, 1, 1, 1)  # White color (RGBA values)
                    )
                    service_done_button.service_booking_id = service_booking_id
                    box2.add_widget(service_done_button)

                box = MDBoxLayout(orientation='horizontal')
                box.add_widget(box1)
                box.add_widget(box2)

                # Add the box layout to the card
                card.add_widget(box)

                provider_request_table_layout.add_widget(card)

        self.ids['date_field'].text = ""  # Clear the text of date_field
        ProviderViewRequests.selected_date = None

    def logout(self):
        App.get_running_app().service_provider_id = None
        App.get_running_app().service_provider_details = []
        App.get_running_app().service_provider_view_services = []
        App.get_running_app().service_provider_view_requests = []
        App.get_running_app().service_provider_view_history = []
        self.manager.current = 'selection_screen'

class ProviderViewHistory(Screen):

    def toggle_nav_drawer(self):
        self.ids.provider_nav_drawer.set_state()

    def on_pre_enter(self, *args):
        App.get_running_app().switch_to_provider_view_history()

    def on_enter(self):
        service_provider_id = App.get_running_app().service_provider_id
        if not App.get_running_app().is_logged_in:
            return
        try:
            provider_history_table_layout = self.ids['provider_history_table_layout']
            provider_history_table_layout.clear_widgets()  # Clear existing widgets
            provider_history_table_layout.padding = [50]  # Add padding around the GridLayout
            provider_history_table_layout.spacing = [20]  # Add padding around the GridLayout

            service_provider_view_history = App.get_running_app().service_provider_view_history

            if not service_provider_view_history:
                no_history_label = MDLabel(
                    text="No History Found",
                    font_size=sp(30),
                    text_color=(1, 1, 1, 1),
                    theme_text_color="Custom",
                    halign="center"
                )
                no_history_label.font_size = 30
                provider_history_table_layout.add_widget(no_history_label)
                return

            for service_booking in service_provider_view_history:
                service_booking_id = service_booking[0]
                number_of_sq_feet = float(service_booking[1])
                description = service_booking[2]
                booking_date = service_booking[3]
                status = service_booking[7]
                service_id = service_booking[8]
                customer_id = service_booking[9]

                if status in ["Accepted Request", "Service Completed", "Paid Advance Amount"]:
                    continue  # Skip this card

                cursor.execute("select * from service where service_id = '" + str(service_id) + "'")
                service = cursor.fetchone()
                service_image = service[4]
                charger_per_sq_feet = float(service[3])

                total_charge = number_of_sq_feet * charger_per_sq_feet
                advance_payment = total_charge * 0.2
                remaining_amount = total_charge - advance_payment

                service_full_name_history = ProviderViewHistory.get_service_by_service_id_history(service_id)

                customer_data_history = ProviderViewHistory.get_customer_name_from_service_history(customer_id)

                number_of_sq_feet_history = MDLabel(text=str(number_of_sq_feet),  font_size=sp(17),text_color=(0, 0, 0.5, 1), theme_text_color="Custom")
                service_description_full_history = MDLabel(text=str(description), font_size=sp(17),text_color=(0, 0, 0.5, 1), theme_text_color="Custom")
                service_booking_date_full_history = MDLabel(text=str(booking_date), font_size=sp(17),text_color=(0, 0, 0.5, 1), theme_text_color="Custom")
                service_history = MDLabel(text=service_full_name_history, font_size=sp(17), text_color=(0, 0, 0.5, 1),theme_text_color="Custom")
                charger_history = MDLabel(text=f"${charger_per_sq_feet}", font_size=sp(17), text_color=(0, 0, 0.5, 1),theme_text_color="Custom")
                service_picture_history = AsyncImage(source=service_image, keep_ratio=True, allow_stretch=True)
                service_status_history = MDLabel(
                    text=str(status),
                    theme_text_color="Custom",
                    text_color=(0.5, 0, 0.5, 1),  # RGB values for purple
                    bold=True,
                    font_size=sp(17),
                )

                card = MDCard(
                    orientation='vertical',
                    size_hint=(None, None),
                    size=(dp(300), dp(300)),
                    elevation=5,
                    padding=15,
                    spacing= 10,
                    md_bg_color=(0.9, 0.9, 0.9, 1)
                )

                box1 = MDBoxLayout(orientation='vertical')  # Add spacing between labels

                service_name_data_history = MDLabel(
                    text="Service Name:",
                    theme_text_color="Custom",
                    font_style="Caption",
                    size_hint_y=None,
                    height=20
                )
                box1.add_widget(service_name_data_history)
                box1.add_widget(service_history)

                spacer = Widget(size_hint_y=None, height=20)
                box1.add_widget(spacer)

                charge_per_sq_feet_history = MDLabel(
                    text="Charger Per sq.feet:",
                    theme_text_color="Custom",
                    font_style="Caption",
                    size_hint_y=None,
                    height=20
                )
                box1.add_widget(charge_per_sq_feet_history)
                box1.add_widget(charger_history)

                spacer = Widget(size_hint_y=None, height=20)
                box1.add_widget(spacer)

                number_history = MDLabel(
                    text="No.of sq.feet:",
                    theme_text_color="Custom",
                    font_style="Caption",
                    size_hint_y=None,
                    height=20
                )
                box1.add_widget(number_history)
                box1.add_widget(number_of_sq_feet_history)

                spacer = Widget(size_hint_y=None, height=20)
                box1.add_widget(spacer)

                description_history = MDLabel(
                    text="Description:",
                    theme_text_color="Custom",
                    font_style="Caption",
                    size_hint_y=None,
                    height=20
                )
                box1.add_widget(description_history)
                box1.add_widget(service_description_full_history)

                spacer = Widget(size_hint_y=None, height=20)
                box1.add_widget(spacer)

                booking_date_history = MDLabel(
                    text="Booking Date:",
                    theme_text_color="Custom",
                    font_style="Caption",
                    size_hint_y=None,
                    height=20
                )
                box1.add_widget(booking_date_history)
                box1.add_widget(service_booking_date_full_history)

                spacer = Widget(size_hint_y=None, height=20)
                box1.add_widget(spacer)

                if service_booking[7] in ["Request Cancelled by Customer", "Rejected Request","Full Payment Successfull"]:
                    customer_status_history = MDLabel(
                        text="Status:",
                        theme_text_color="Custom",
                        font_style="Caption",
                        size_hint_y=None,
                        height=20
                    )
                    box1.add_widget(customer_status_history)

                    spacer = Widget(size_hint_y=None, height=20)
                    box1.add_widget(spacer)

                    box1.add_widget(service_status_history)

                spacer = Widget(size_hint_y=None, height=30)
                box1.add_widget(spacer)

                Customer_Details = MDLabel(
                    text="Customer Details",
                    theme_text_color="Custom",
                    font_style="Caption",
                    size_hint_y=None,
                    height=dp(30)
                )
                box1.add_widget(Customer_Details)

                box1.add_widget(Widget(size_hint_y=None, height=10))  # Adjust the height value as needed

                if customer_data_history is not None:
                    customer_name_history = customer_data_history[0]  # Access the customer name
                    phone_number_history = customer_data_history[1]  # Access the phone number
                    address_history = customer_data_history[2]
                    customer_name_data_label_history = MDLabel(
                        text=f"Name: {customer_name_history}",
                        font_size=sp(13),
                        text_color=(0, 0, 0.5, 1),
                        theme_text_color="Custom"
                    )
                    box1.add_widget(customer_name_data_label_history)

                    box1.add_widget(Widget(size_hint_y=None, height=25))  # Adjust the height value as needed

                    customer_phone_data_label_history = MDLabel(
                        text=f"Phone: {phone_number_history}",
                        font_size=sp(13),
                        text_color=(0, 0, 0.5, 1),
                        theme_text_color="Custom"
                    )
                    box1.add_widget(customer_phone_data_label_history)

                    box1.add_widget(Widget(size_hint_y=None, height=25))  # Adjust the height value as needed

                    customer_address_label_history = MDLabel(
                        text=f"Address: {address_history}",
                        font_size=sp(13),
                        text_color=(0, 0, 0.5, 1),
                        theme_text_color="Custom"
                    )
                    box1.add_widget(customer_address_label_history)
                else:
                    print("No matching customer found.")

                box1.add_widget(Widget(size_hint_y=None, height=25))  # Adjust the height value as needed

                if service_booking[7] == "Full Payment Successfull":
                    total_charge = MDLabel(
                        text=f"Total Charge: ${total_charge}",
                        theme_text_color="Custom",
                        text_color=(0.5, 0, 0.5, 1),
                        font_style="Caption",
                        size_hint_y=None,
                        height=dp(30),
                        bold=True
                    )
                    box1.add_widget(total_charge)

                    advance_amount = MDLabel(
                        text=f"Advance Amount: ${advance_payment}",
                        theme_text_color="Custom",
                        text_color=(0.5, 0, 0.5, 1),
                        font_style="Caption",
                        size_hint_y=None,
                        height=dp(30),
                        bold=True
                    )
                    box1.add_widget(advance_amount)

                    remaining_amount = MDLabel(
                        text=f"Remaining Amount: ${remaining_amount}",
                        theme_text_color="Custom",
                        text_color=(0.5, 0, 0.5, 1),
                        font_style="Caption",
                        size_hint_y=None,
                        height=dp(30),
                        bold=True
                    )
                    box1.add_widget(remaining_amount)

                    service_date_label = MDLabel(
                        text=f"Service Done On: {service_booking[4]}",
                        theme_text_color="Custom",
                        text_color=(0, 0, 0, 1),
                        font_style="Caption",
                        size_hint_y=None,
                        height=dp(30),
                        bold=True
                    )
                    box1.add_widget(service_date_label)

                box2 = MDBoxLayout(orientation='vertical')
                box2.add_widget(service_picture_history)

                cursor.execute("select * from review where service_booking_id in (select service_booking_id from service_booking where service_id = '" + str( service_id) + "')")
                reviews = cursor.fetchall()
                reviews = list(reviews)
                if len(reviews) == 0:
                    no_rating = "No Rating"
                    average_rating_label = MDLabel(text=f"Rating: {no_rating}", theme_text_color="Custom", text_color=(0, 0, 0, 1))
                else:
                    total_ratings = 0
                    number_of_ratings = 0
                    for review in reviews:
                        total_ratings = total_ratings + int(review[2])
                        number_of_ratings = number_of_ratings + 1
                    rating = total_ratings / number_of_ratings
                    rating = round(rating, 2)
                    average_rating_label = MDLabel(text=f"Rating: {rating}", theme_text_color="Custom", text_color=(0, 0, 0, 1))
                box2.add_widget(average_rating_label)

                if service_booking[7] == "Full Payment Successfull":
                    button_box = MDBoxLayout(orientation='vertical')
                    view_payment = MDRectangleFlatButton(
                        text="View Payment",
                        on_press=self.on_view_payment_press,
                        md_bg_color=get_color_from_hex("#006400"),  # Hexadecimal color for dark green
                        text_color=(1, 1, 1, 1),  # White color (RGBA values)
                    )
                    view_payment.service_booking_id = service_booking_id
                    view_payment.customer_id = customer_id
                    button_box.add_widget(view_payment)

                    spacer = Widget(size_hint_y=None, height=20)  # Adjust height as needed
                    button_box.add_widget(spacer)

                    complaints = MDRectangleFlatButton(
                        text="Raise Complaints",
                        on_press=self.on_complaint_provider_press,
                        md_bg_color=get_color_from_hex("#008080"),   # Hexadecimal color for red
                        text_color=(1, 1, 1, 1),  # White color (RGBA values)
                    )
                    complaints.service_booking_id = service_booking_id
                    complaints.service_provider_id = service_provider_id

                    cursor.execute("SELECT COUNT(*) FROM complaints ""WHERE service_booking_id = '" + str(service_booking_id) + "' and service_provider_id = '"+str(service_provider_id)+"'")
                    count = cursor.fetchone()[0]
                    if count > 0:
                        button_box.remove_widget(complaints)
                    else:
                        button_box.add_widget(complaints)

                    spacer = Widget(size_hint_y=None, height=20)  # Adjust height as needed
                    button_box.add_widget(spacer)

                    view_complaints = MDRectangleFlatButton(
                        text="View Customer Complaints",
                        on_press=self.on_view_customer_complaint_press,
                        md_bg_color=get_color_from_hex("#008080"), # Hexadecimal color for red
                        text_color=(1, 1, 1, 1),  # White color (RGBA values)
                    )
                    view_complaints.service_booking_id = service_booking_id
                    view_complaints.customer_id = customer_id

                    cursor.execute("SELECT COUNT(*) FROM complaints ""WHERE service_booking_id = '" + str(service_booking_id) + "'")
                    count = cursor.fetchone()[0]
                    if count > 0:
                        button_box.add_widget(view_complaints)
                    else:
                        button_box.remove_widget(view_complaints)

                    spacer = Widget(size_hint_y=None, height=20)  # Adjust height as needed
                    button_box.add_widget(spacer)

                    view_my_complaints = MDRectangleFlatButton(
                        text="View My Complaints",
                        on_press=self.on_view_provider_my_complaint_press,
                        md_bg_color=get_color_from_hex("#FF5733"),  # Hexadecimal color for red
                        text_color=(1, 1, 1, 1),  # White color (RGBA values)
                        size_hint=(None, None),  # Specify size hint
                        size=(40, 40),  # Set fixed size
                        font_size='12sp',
                    )
                    view_my_complaints.service_booking_id = service_booking_id
                    view_my_complaints.service_provider_id = service_provider_id

                    cursor.execute("SELECT COUNT(*) FROM complaints ""WHERE service_booking_id = '" + str(service_booking_id) + "'")
                    count = cursor.fetchone()[0]
                    if count > 0:
                        button_box.add_widget(view_my_complaints)
                    else:
                        button_box.remove_widget(view_my_complaints)

                    box2.add_widget(button_box)


                box = MDBoxLayout(orientation='horizontal')
                box.add_widget(box1)
                box.add_widget(box2)

                # Add the box layout to the card
                card.add_widget(box)

                provider_history_table_layout.add_widget(card)
        except Exception as e:
            print(f"An error occurred: {e}")

    def on_view_payment_press(self, instance):
        service_booking_id = instance.service_booking_id
        customer_id = instance.customer_id
        view_payment_screen = self.manager.get_screen('provider_view_payment_screen')
        view_payment_screen.service_booking_id = service_booking_id
        view_payment_screen.customer_id = customer_id
        self.manager.current = 'provider_view_payment_screen'

    def on_complaint_provider_press(self, instance):
        service_booking_id = instance.service_booking_id
        service_provider_id = instance.service_provider_id

        complaints_screen = self.manager.get_screen('customer_raise_complaint')
        complaints_screen.service_booking_id = service_booking_id
        complaints_screen.customer_id = None  # Set to None for service provider
        complaints_screen.service_provider_id = service_provider_id
        self.manager.current = 'customer_raise_complaint'

    def on_view_provider_my_complaint_press(self, instance):
        service_booking_id = instance.service_booking_id
        service_provider_id = instance.service_provider_id

        view_my_complaint_screen = self.manager.get_screen('view_provider_my_complaint')
        view_my_complaint_screen.service_booking_id = service_booking_id
        view_my_complaint_screen.service_provider_id = service_provider_id
        self.manager.current = 'view_provider_my_complaint'

    def on_view_customer_complaint_press(self, instance):
        service_booking_id = instance.service_booking_id
        customer_id = instance.customer_id
        view_complaint_screen = self.manager.get_screen('viewcomplaint')
        view_complaint_screen.service_booking_id = service_booking_id
        view_complaint_screen.customer_id = customer_id
        self.manager.current = 'viewcomplaint'

    def get_service_by_service_id_history(service_id):
        try:
            cursor.execute("SELECT service_name FROM service WHERE service_id = '" + str(service_id) + "'")
            service = cursor.fetchone()
            if service:
                return service[0]
            else:
                return None
        except Exception as e:
            print(f"Error fetching service name: {e}")
            return None

    def get_customer_name_from_service_history(customer_id):
        try:
            cursor.execute(
                "SELECT customer_name,phone,address FROM customer WHERE customer_id = '" + str(customer_id) + "'")
            customer = cursor.fetchone()
            if customer:
                return customer[0], customer[1], customer[2]
            else:
                return None
        except Exception as e:
            print(f"Error fetching category name: {e}")
            return None

    def logout(self):
        App.get_running_app().service_provider_id = None
        App.get_running_app().service_provider_details = []
        App.get_running_app().service_provider_view_services = []
        App.get_running_app().service_provider_view_requests = []
        App.get_running_app().service_provider_view_history = []
        self.manager.current = 'selection_screen'

class CardDetailsScreen(Screen):
    service_booking_id = None  # Define service_id as a class variable
    selected_card_type = None
    advance_amount = None
    remaining_amount = None
    status = None
    customer_id = None
    Card_number = None
    Expiry_date = None
    CVV = None

    def on_pre_enter(self):
        service_booking_id = self.service_booking_id
        if SnowRemovalApp.payment_status.get(service_booking_id):
            self.ids['card_details'].clear_widgets()
            self.display_payment_already_made_message()
            self.add_widgets()
        else:
            self.ids['card_details'].clear_widgets()
            self.add_widgets()

    def display_payment_already_made_message(self):
        label = MDLabel(
            text="Payment already made for this service",
            halign='center'
        )
        self.ids['card_details'].add_widget(label)

    def add_widgets(self):
        service_booking_id = self.service_booking_id
        customer_id = self.customer_id
        cursor.execute("select * from service_booking where service_booking_id = '"+str(service_booking_id)+"' and customer_id = '"+str(customer_id)+"'")
        service_booking = cursor.fetchone()
        self.advance_amount = service_booking[5]
        self.remaining_amount = service_booking[6]
        self.status = service_booking[7]

        card = MDCard(
            orientation='vertical',
            size_hint=(None, None),
            size=(dp(300), dp(300)),  # Adjust the size of the card
            elevation=5,
            padding=10
        )

        if self.status == 'Accepted Request':
            advance_amount = MDLabel(
                text=f"Pay Advance Amount: ${self.advance_amount}",
                theme_text_color="Custom",
                text_color=(0, 0.5, 0, 1),  # Dark Green color (RGBA values)
                font_style="Caption",
                size_hint_y=None,  # Fixed height
                height= 30 , # Set the height of the label
                bold=True
            )
            card.add_widget(advance_amount)

            spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
            card.add_widget(spacer)

            card_type_dropdown = DropDown()
            for card_type in ['Debit Card', 'Credit Card']:
                btn = MDRaisedButton(text=card_type, size_hint_y=None, height=44)
                btn.bind(on_release=lambda btn: card_type_dropdown.select(btn.text))
                card_type_dropdown.add_widget(btn)

            card_type_button = MDRaisedButton(text='Select Card Type', on_release=card_type_dropdown.open)
            selected_card_label = MDLabel(text='Selected Card Type: None', halign='center')

            def update_selected_card_label(instance, value):
                self.selected_card_type = value
                selected_card_label.text = f'Selected Card Type: {value}'

            card_type_dropdown.bind(on_select=update_selected_card_label)

            card.add_widget(card_type_button)
            card.add_widget(selected_card_label)

            spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
            card.add_widget(spacer)

            Card_number = MDTextField(hint_text="Enter Card Number", helper_text_mode="on_focus", height=30)
            self.Card_number = Card_number  # Assign the MDTextField to the class variable
            card.add_widget(Card_number)
            Card_number.bind(on_text=self.check_required_fields)

            spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
            card.add_widget(spacer)

            Expiry_date = MDTextField(hint_text="Enter Expiry Date", helper_text_mode="on_focus", height=30)
            self.Expiry_date = Expiry_date
            card.add_widget(Expiry_date)
            Expiry_date.bind(on_text=self.check_required_fields)

            spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
            card.add_widget(spacer)

            CVV = MDTextField(hint_text="Enter Your CVV", helper_text_mode="on_focus", height=30)
            self.CVV = CVV
            card.add_widget(CVV)
            CVV.bind(on_text=self.check_required_fields)

            spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
            card.add_widget(spacer)

            error_label = MDLabel(text='', halign='center', theme_text_color="Secondary")
            card.add_widget(error_label)

            pay_button = MDRectangleFlatButton(
                text="Pay Now",
                on_press=self.pay_amount,  # Ensure it's bound to pay_amount
                md_bg_color=get_color_from_hex("#FF5733"),
                text_color=(0, 0, 0, 1),
                size_hint=(None, None),
                size=(200, 44)
            )
            pay_button.service_booking_id = service_booking_id
            pay_button.advance_amount = advance_amount
            card.add_widget(pay_button)

            self.ids['card_details'].add_widget(card)

    def check_required_fields(self, instance, value):
        card_number = self.Card_number.text if hasattr(self, 'Card_number') else ''
        expiry_date = self.Expiry_date.text if hasattr(self, 'Expiry_date') else ''
        cvv = self.CVV.text if hasattr(self, 'CVV') else ''

        if card_number and expiry_date and cvv:
            self.pay_button.disabled = False
            self.error_label.text = ''  # Clear any previous error message
        else:
            self.pay_button.disabled = True

    def validate_card_details(self, card_number, expiry_date, cvv):
        if len(card_number) != 16:
            return False, 'Card number must be 16 digits'
        if not re.match(r'^\d{2}/\d{2}$', expiry_date):
            return False, 'Expiry date must be in MM/YY format'
        if len(cvv) != 3 or not cvv.isdigit():
            return False, 'CVV must be 3 digits'

        return True, ''

    def pay_amount(self, *args):
        if (
                self.service_booking_id is not None
                and self.selected_card_type is not None
                and self.status == 'Accepted Request'
        ):
            card_number = self.Card_number.text
            expiry_date = self.Expiry_date.text
            cvv = self.CVV.text

            valid, message = self.validate_card_details(card_number, expiry_date, cvv)

            if valid:
                service_booking_id = self.service_booking_id
                customer_id = self.customer_id
                selected_card_type = self.selected_card_type
                advance_amount = int(float(self.advance_amount))
                remaining_amount = int(float(self.remaining_amount))
                total_amount = advance_amount + remaining_amount

                cursor.execute("select * from service_booking where service_booking_id = '"+str(service_booking_id)+"' and customer_id = '"+str(customer_id)+"'")
                service_booking = cursor.fetchone()
                service_booking_id = service_booking[0]

                advance_date = datetime.now().strftime('%Y-%m-%d')
                status = "Advance Payment Successfull"
                payment_status = "Paid Advance Amount"

                cursor.execute("insert into payments(payment_type,advance_amount,total_amount,advance_date,status,service_booking_id) values ('"+str(selected_card_type)+"' , '"+str(advance_amount)+"' ,'"+str(total_amount)+"' , '"+str(advance_date)+"' , '"+str(status)+"' , '"+str(service_booking_id)+"')")
                conn.commit()
                toast("Payment Successfull")
                self.manager.current = 'customer_view_request'

                cursor.execute("update service_booking set status = '"+str(payment_status)+"' where service_booking_id = '"+str(service_booking_id)+"'")
                conn.commit()
            else:
                # Display error message
                toast(message)

class FullCardDetailsScreen(Screen):

    service_booking_id = None  # Define service_id as a class variable
    selected_card_type = None
    advance_amount = None
    remaining_amount = None
    status = None
    customer_id = None
    Card_number = None
    Expiry_date = None
    CVV = None

    def on_pre_enter(self):
        service_booking_id = self.service_booking_id
        if SnowRemovalApp.payment_status.get(service_booking_id):
            self.ids['full_card_details'].clear_widgets()
            self.display_payment_already_made_message()
            self.add_widgets()
        else:
            self.ids['full_card_details'].clear_widgets()
            self.add_widgets()

    def display_payment_already_made_message(self):
        label = MDLabel(
            text="Payment already made for this service",
            halign='center'
        )
        self.ids['full_card_details'].add_widget(label)

    def add_widgets(self):
        service_booking_id = self.service_booking_id
        customer_id = self.customer_id
        cursor.execute("select * from service_booking where service_booking_id = '" + str(service_booking_id) + "' and customer_id = '" + str(customer_id) + "'")
        service_booking = cursor.fetchone()
        self.advance_amount = service_booking[5]
        self.remaining_amount = service_booking[6]
        self.status = service_booking[7]

        card = MDCard(
            orientation='vertical',
            size_hint=(None, None),
            size=(dp(300), dp(300)),  # Adjust the size of the card
            elevation=5,
            padding=10
        )

        if self.status == 'Service Completed':
            remaining_amount_label = MDLabel(
                text=f"Pay Remaining Amount: ${self.remaining_amount}",
                theme_text_color="Custom",
                text_color=(0, 0.5, 0, 1),  # Dark Green color (RGBA values)
                font_style="Caption",
                size_hint_y=None,  # Fixed height
                height=30,  # Set the height of the label
                bold=True
            )
            card.add_widget(remaining_amount_label)

            spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
            card.add_widget(spacer)

            card_type_dropdown = DropDown()
            for card_type in ['Debit Card', 'Credit Card']:
                btn = MDRaisedButton(text=card_type, size_hint_y=None, height=44)
                btn.bind(on_release=lambda btn: card_type_dropdown.select(btn.text))
                card_type_dropdown.add_widget(btn)

            card_type_button = MDRaisedButton(text='Select Card Type', on_release=card_type_dropdown.open)
            selected_card_label = MDLabel(text='Selected Card Type: None', halign='center')

            def update_selected_card_label(instance, value):
                self.selected_card_type = value
                selected_card_label.text = f'Selected Card Type: {value}'

            card_type_dropdown.bind(on_select=update_selected_card_label)

            card.add_widget(card_type_button)
            card.add_widget(selected_card_label)

            spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
            card.add_widget(spacer)

            Card_number = MDTextField(hint_text="Enter Card Number", helper_text_mode="on_focus", height=30)
            self.Card_number = Card_number  # Assign the MDTextField to the class variable
            card.add_widget(Card_number)
            Card_number.bind(on_text=self.check_required_fields)

            spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
            card.add_widget(spacer)

            Expiry_date = MDTextField(hint_text="Enter Expiry Date", helper_text_mode="on_focus", height=30)
            self.Expiry_date = Expiry_date
            card.add_widget(Expiry_date)
            Expiry_date.bind(on_text=self.check_required_fields)

            spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
            card.add_widget(spacer)

            CVV = MDTextField(hint_text="Enter Your CVV", helper_text_mode="on_focus", height=30)
            self.CVV = CVV
            card.add_widget(CVV)
            CVV.bind(on_text=self.check_required_fields)

            spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
            card.add_widget(spacer)

            error_label = MDLabel(text='', halign='center', theme_text_color="Secondary")
            card.add_widget(error_label)

            pay_button = MDRectangleFlatButton(
                text="Pay Now",
                on_press=self.pay_amount,  # Ensure it's bound to pay_amount
                md_bg_color=get_color_from_hex("#FF5733"),
                text_color=(0, 0, 0, 1),
                size_hint=(None, None),
                size=(200, 44)
            )
            pay_button.service_booking_id = service_booking_id
            pay_button.remaining_amount = remaining_amount_label
            card.add_widget(pay_button)

            self.ids['full_card_details'].add_widget(card)

    def check_required_fields(self, instance, value):
        card_number = self.Card_number.text if hasattr(self, 'Card_number') else ''
        expiry_date = self.Expiry_date.text if hasattr(self, 'Expiry_date') else ''
        cvv = self.CVV.text if hasattr(self, 'CVV') else ''

        if card_number and expiry_date and cvv:
            self.pay_button.disabled = False
            self.error_label.text = ''  # Clear any previous error message
        else:
            self.pay_button.disabled = True

    def validate_card_details(self, card_number, expiry_date, cvv):
        if len(card_number) != 16:
            return False, 'Card number must be 16 digits'
        if not re.match(r'^\d{2}/\d{2}$', expiry_date):
            return False, 'Expiry date must be in MM/YY format'
        if len(cvv) != 3 or not cvv.isdigit():
            return False, 'CVV must be 3 digits'

        return True, ''

    def pay_amount(self, *args):
        if (
                self.service_booking_id is not None
                and self.selected_card_type is not None
                and self.status == 'Service Completed'
        ):
            card_number = self.Card_number.text
            expiry_date = self.Expiry_date.text
            cvv = self.CVV.text

            valid, message = self.validate_card_details(card_number, expiry_date, cvv)

            if valid:
                service_booking_id = self.service_booking_id
                customer_id = self.customer_id
                selected_card_type = self.selected_card_type
                advance_amount = int(float(self.advance_amount))
                remaining_amount = int(float(self.remaining_amount))
                total_amount = advance_amount + remaining_amount

                remaining_date = datetime.now().strftime('%Y-%m-%d')
                status = "Full Payment Successfull"
                payment_status = "Full Payment Successfull"

                cursor.execute("update payments set payment_type = '" + str(selected_card_type) + "' , remaining_amount = '" + str(remaining_amount) + "' , remaining_date = '" + str(remaining_date) + "' , status = '" + str(status) + "' where service_booking_id = '" + str(service_booking_id) + "'")
                conn.commit()
                toast("Transaction committed successfully")
                self.manager.current = 'customer_view_request'

                cursor.execute("update service_booking set status = '" + str(payment_status) + "' where service_booking_id = '" + str(service_booking_id) + "'")
                conn.commit()
            else:
                # Display error message
                toast(message)

class CustomerViewFullPaymentScreen(Screen):
    def on_enter(self):
        service_booking_id = self.service_booking_id
        view_full_payment = self.ids['view_full_payment']

        cursor.execute("select * from payments where service_booking_id = '"+str(service_booking_id)+"'")
        payment = cursor.fetchone()
        card_type = payment[1]
        advance_amount = payment[2]
        advance_amount_date = payment[5]
        remaining_amount = payment[3]
        remaining_amount_date = payment[6]
        total_amount = payment[4]
        status = payment[7]

        card = MDCard(
            orientation='vertical',
            size_hint=(None, None),
            size=(dp(250), dp(250)),  # Adjust the size of the card
            elevation=5,
            padding=10
        )

        payment_title = MDLabel(
            text="Payment Details",
            theme_text_color="Custom",
            text_color=(1, 0.647, 0),
            font_size='20sp',  # Increase font size to 36dp
            font_style="Caption",
            size_hint_y=None,  # Fixed height
            height=30,
            halign='center',
            bold=True
        )
        payment_title.font_size = 20
        card.add_widget(payment_title)

        spacer = Widget(size_hint_y=None, height=50)  # Adjust height as needed
        card.add_widget(spacer)

        card_type = MDLabel(
            text=f"Card Type: {card_type}",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),  # White color (RGBA values)
            font_size='24sp',  # Adjust font size
            font_style="Caption",
            size_hint_y=None,  # Fixed height
            height=30,
            halign='center',
            bold=True
        )
        card.add_widget(card_type)

        spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
        card.add_widget(spacer)

        total_amount = MDLabel(
            text=f"Total Amount: ${total_amount}",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),  # White color (RGBA values)
            font_size='24sp',  # Adjust font size
            font_style="Caption",
            size_hint_y=None,  # Fixed height
            height=30,
            halign='center',
            bold=True
        )
        card.add_widget(total_amount)

        spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
        card.add_widget(spacer)

        advance_amount = MDLabel(
            text=f"Advance Amount Paid On: ${advance_amount}({advance_amount_date})",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),  # White color (RGBA values)
            font_size='24sp',  # Adjust font size
            font_style="Caption",
            halign='center',
            size_hint_y=None,  # Fixed height
            height=30,  # Set the height of the label
            bold=True
        )
        card.add_widget(advance_amount)

        spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
        card.add_widget(spacer)

        remaining_amount = MDLabel(
            text=f"Remaining Amount Paid On: ${remaining_amount}({remaining_amount_date})",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),  # White color (RGBA values)
            font_size='24sp',  # Adjust font size
            font_style="Caption",
            halign='center',
            size_hint_y=None,  # Fixed height
            height=30,  # Set the height of the label
            bold=True
        )
        card.add_widget(remaining_amount)

        spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
        card.add_widget(spacer)

        Status = MDLabel(
            text=f"Status: {status}",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),  # White color (RGBA values)
            font_style="Caption",
            halign='center',
            font_size='48sp',  # Adjust font size to be extra large
            size_hint_y=None,  # Fixed height
            height=30,  # Set the height of the label
            bold=True
        )
        card.add_widget(Status)

        spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
        card.add_widget(spacer)

        back_button = MDIconButton(
            icon='arrow-left',  # Use the appropriate icon name
            size_hint=(None, None),
            size=(50, 50),  # Adjust the size of the button
            pos_hint={'center_x': 0.5, 'center_y': 0.1},  # Adjust position as needed
            on_release=self.go_to_view_request_screen
        )
        card.add_widget(back_button)

        view_full_payment.add_widget(card)

    def go_to_view_request_screen(self, instance):
        self.manager.current = 'customer_view_history'

class CustomerRaiseComplaintsScreen(Screen):

    service_booking_id = None
    customer_id = None
    service_provider_id = None

    def on_enter(self):
        service_booking_id = self.service_booking_id
        customer_id = self.customer_id
        service_provider_id = self.service_provider_id
        complaints = self.ids['complaints']

        card = MDCard(
            orientation='vertical',
            size_hint=(None, None),
            size=(dp(300), dp(300)),  # Adjust the size of the card
            elevation=5,
            padding=10
        )

        if App.get_running_app().user_type == 'customer':
            # Complaint text for customer
            self.complaint_text = MDTextField(hint_text="Enter Your Complaint Here (Customer)",helper_text_mode="on_focus")
        elif App.get_running_app().user_type == 'service_provider':
            # Complaint text for service provider
            self.complaint_text = MDTextField(hint_text="Enter Your Complaint Here (Service Provider)",helper_text_mode="on_focus")

        card.add_widget(self.complaint_text)

        spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
        card.add_widget(spacer)

        complaint_button = MDRaisedButton(
            text='Submit',  # Text displayed on the button
            size_hint=(None, None),
            size=(150, 42),  # Adjust the size of the button
            pos_hint={'center_x': 0.5, 'center_y': 0.05},  # Adjust position as needed
            on_release=self.complaint_button,  # Bind the button to a function
        )
        complaint_button.service_booking_id = service_booking_id
        complaint_button.customer_id = customer_id
        complaint_button.service_provider_id = service_provider_id
        card.add_widget(complaint_button)

        spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
        card.add_widget(spacer)

        back_button = MDIconButton(
            icon='arrow-left',  # Use the appropriate icon name
            size_hint=(None, None),
            size=(50, 50),  # Adjust the size of the button
            pos_hint={'center_x': 0.5, 'center_y': 0.1},  # Adjust position as needed
            on_release=self.go_to_view_request_screen
        )
        card.add_widget(back_button)

        spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
        card.add_widget(spacer)

        complaints.add_widget(card)

    def complaint_button(self, instance):
        service_booking_id = self.service_booking_id
        customer_id =  self.customer_id
        service_provider_id = self.service_provider_id
        complaint_text = self.complaint_text.text

        cursor.execute("select * from service_booking where service_booking_id = '" + str(service_booking_id) + "'")
        service_booking = cursor.fetchone()

        if not service_booking:
            print(f"Error: No service booking found for service_booking_id {service_booking_id}")
            return

        raised_by = App.get_running_app().user_type
        status = "Complained Successfully"
        cursor.execute("INSERT INTO complaints(status, complaint_description, service_booking_id, customer_id, service_provider_id, raised_by) ""VALUES (%s, %s, %s, %s, %s, %s)",(status, complaint_text, service_booking_id,
             App.get_running_app().customer_id if raised_by == 'customer' else None,
             App.get_running_app().service_provider_id if raised_by == 'service_provider' else None, raised_by)
        )
        conn.commit()
        toast("Complaint registered successfully")

    def go_to_view_request_screen(self, instance):
        if App.get_running_app().user_type == 'customer':
            self.manager.current = 'customer_view_history'
        elif App.get_running_app().user_type == 'service_provider':
            self.manager.current = 'provider_view_history'

class ProviderViewPaymentsScreen(Screen):

    def on_enter(self):
        service_booking_id = self.service_booking_id
        customer_id = self.customer_id

        view_payment_screen = self.ids['provider_view_payment_screen']
        view_payment_screen.padding = [100]  # Add padding around the GridLayout
        view_payment_screen.spacing = 50  # Add spacing between the cards

        cursor.execute("select * from payments where service_booking_id = '" + str(service_booking_id) + "'")
        payment = cursor.fetchone()
        card_type = payment[1]
        advance_amount = payment[2]
        advance_amount_date = payment[5]
        remaining_amount = payment[3]
        remaining_amount_date = payment[6]
        total_amount = payment[4]
        status = payment[7]

        customer_details = ProviderViewPaymentsScreen.get_customer_name_from_customer(customer_id)

        card = MDCard(
            orientation='vertical',
            size_hint=(None, None),
            size=(dp(300), dp(300)),
            elevation=5,  # Add elevation for shadow effect
            padding=10
        )

        Customer_Details = MDLabel(
            text="Payment Details",
            theme_text_color="Custom",
            text_color=(1, 0.647, 0, 1),  # Orange color (RGBA values)
            font_size=sp(22),  # Adjust font size
            font_style="Caption",
            size_hint_y=None,  # Fixed height
            height=30,  # Set the height of the label
            bold=True,
            halign='center'
        )
        Customer_Details.font_size = 22
        card.add_widget(Customer_Details)

        spacer = Widget(size_hint_y=None, height=22)  # Adjust height as needed
        card.add_widget(spacer)

        if customer_details is not None:
            customer_name = customer_details[0]  # Access the customer name
            phone_number = customer_details[1]  # Access the phone number

            customer_name_data_label = MDLabel(
                text=f"Customer Name: {customer_name}",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                font_size='24sp',  # Adjust font size
                font_style="Caption",
                size_hint_y=None,  # Fixed height
                height=30,
                halign='center'# Set the height of the label
            )
            card.add_widget(customer_name_data_label)

            customer_phone_data_label = MDLabel(
                text=f"Phone Number: {phone_number}",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                font_size='24sp',  # Adjust font size
                font_style="Caption",
                size_hint_y=None,  # Fixed height
                height=30,
                halign='center'# Set the height of the label
            )
            card.add_widget(customer_phone_data_label)
        else:
            print("No matching customer found.")

        spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
        card.add_widget(spacer)

        card_type = MDLabel(
            text=f"Card Type: {card_type}",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_size='24sp',  # Adjust font size
            font_style="Caption",
            size_hint_y=None,  # Fixed height
            height=30,  # Set the height of the label
            bold=True,
            halign='center'
        )
        card.add_widget(card_type)

        spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
        card.add_widget(spacer)

        total_amount = MDLabel(
            text=f"Total Amount: ${total_amount}",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_size='24sp',  # Adjust font size
            font_style="Caption",
            size_hint_y=None,  # Fixed height
            height=30,  # Set the height of the label
            bold=True,
            halign='center'
        )
        card.add_widget(total_amount)

        spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
        card.add_widget(spacer)

        advance_amount = MDLabel(
            text=f"Advance Amount Paid On: ${advance_amount}({advance_amount_date})",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_size='24sp',  # Adjust font size
            font_style="Caption",
            size_hint_y=None,  # Fixed height
            height=30,  # Set the height of the label
            bold=True,
            halign='center'
        )
        card.add_widget(advance_amount)

        spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
        card.add_widget(spacer)

        remaining_amount = MDLabel(
            text=f"Remaining Amount Paid On: ${remaining_amount}({remaining_amount_date})",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_size='24sp',  # Adjust font size
            font_style="Caption",
            size_hint_y=None,  # Fixed height
            height=30,  # Set the height of the label
            bold=True,
            halign='center'
        )
        card.add_widget(remaining_amount)

        spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
        card.add_widget(spacer)

        Status = MDLabel(
            text=f"Status: {status}",
            theme_text_color="Custom",
            text_color=(0, 0.392, 0, 1),  # Dark Green color (RGBA values)
            font_style="Caption",
            font_size='50sp',  # Adjust font size to be extra large
            size_hint_y=None,  # Fixed height
            height=30,  # Set the height of the label
            bold=True,
            halign='center'
        )
        card.add_widget(Status)

        view_payment_screen.add_widget(card)

    def get_customer_name_from_customer(customer_id):
        try:
            cursor.execute("SELECT customer_name,phone FROM customer WHERE customer_id = '" + str(customer_id) + "'")
            customer = cursor.fetchone()
            if customer:
                return customer[0], customer[1]
            else:
                return None
        except Exception as e:
            print(f"Error fetching category name: {e}")
            return None

class ViewServiceProviderComplaintsScreen(Screen):

    def on_enter(self):
        service_booking_id = self.service_booking_id
        service_provider_id = self.service_provider_id

        view_my_complaints_screen = self.ids['view_provider_my_complaints_screen']
        view_my_complaints_screen.padding = [100]  # Add padding around the GridLayout
        view_my_complaints_screen.spacing = 50  # Add spacing between the cards

        cursor.execute("select * from service_booking where service_booking_id = '" + str(service_booking_id) + "'")
        service_booking = cursor.fetchone()
        service_booking_id = service_booking[0]

        card = MDCard(
            orientation='vertical',
            size_hint=(None, None),
            size=(dp(300), dp(300)),
            elevation=5,  # Add elevation for shadow effect
            padding=10
        )

        cursor.execute("select * from complaints where service_booking_id = '" + str(service_booking_id) + "' and service_provider_id = '"+str(service_provider_id)+"'")
        complaint = cursor.fetchone()
        status = complaint[1]
        complaint_description = complaint[2]

        My_Compalint = MDLabel(
            text="My Complaint",
            theme_text_color="Custom",
            text_color=(1, 0.647, 0, 1),
            font_size=sp(22),  # Adjust font size
            font_style="Caption",
            size_hint_y=None,  # Fixed height
            height=30,  # Set the height of the label
            bold=True,
            halign='center'
        )
        My_Compalint.font_size = 22
        card.add_widget(My_Compalint)

        spacer = Widget(size_hint_y=None, height=30)  # Adjust height as needed
        card.add_widget(spacer)

        Compalint = MDLabel(
            text=f"Compalint: {complaint_description}",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),  # Black color (RGBA values)
            font_size='24sp',  # Adjust font size
            font_style="Caption",
            size_hint_y=None,  # Fixed height
            height=30,  # Set the height of the label
            bold=True,
            halign='center'
        )
        card.add_widget(Compalint)

        spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
        card.add_widget(spacer)

        Status = MDLabel(
            text=f"Status: {status}",
            theme_text_color="Custom",
            text_color=(0, 0.392, 0, 1),  # Dark Green color (RGBA values)
            font_style="Caption",
            font_size=sp(20),  # Adjust font size to be extra large
            size_hint_y=None,  # Fixed height
            height=30,  # Set the height of the label
            bold=True,
            halign='center'
        )
        Status.font_size = 20
        card.add_widget(Status)

        view_my_complaints_screen.add_widget(card)

class ViewComplaintsScreen(Screen):

    def on_enter(self):
        service_booking_id = self.service_booking_id
        customer_id = self.customer_id

        view_complaints_screen = self.ids['view_complaints_screen']
        view_complaints_screen.padding = [100]  # Add padding around the GridLayout
        view_complaints_screen.spacing = 50  # Add spacing between the cards

        cursor.execute("select * from service_booking where service_booking_id = '" + str(service_booking_id) + "'")
        service_booking = cursor.fetchone()
        service_booking_id = service_booking[0]

        card = MDCard(
            orientation='vertical',
            size_hint=(None, None),
            size=(dp(300), dp(250)),
            elevation=5,  # Add elevation for shadow effect
            padding=10
        )

        cursor.execute("select * from complaints where service_booking_id = '" + str(service_booking_id) + "' and customer_id = '"+str(customer_id)+"'")
        complaint = cursor.fetchone()
        status = complaint[1]
        complaint_description = complaint[2]

        complaint_description_label = MDLabel(text=str(complaint_description),theme_text_color="Custom",
                    text_color=(1, 1, 1, 1),
                    halign='center',
                    font_size='24sp',  # Adjust font size
                    font_style="Caption",
                    size_hint_y=None,  # Fixed height
                    height=30,  # Set the height of the label
             )

        customer_details_table = ViewComplaintsScreen.get_customer_name_from_customer_table(customer_id)

        Customer_Details = MDLabel(
            text="View Complaints",
            theme_text_color="Custom",
            text_color=(1, 0.647, 0, 1),
            font_size=sp(22),  # Adjust font size
            font_style="Caption",
            size_hint_y=None,  # Fixed height
            height=30,  # Set the height of the label
            bold=True,
            halign='center'
        )
        Customer_Details.font_size = 22
        card.add_widget(Customer_Details)

        spacer = Widget(size_hint_y=None, height=22)  # Adjust height as needed
        card.add_widget(spacer)

        if customer_details_table is not None:
            customer_name = customer_details_table[0]  # Access the customer name
            phone_number = customer_details_table[1]  # Access the phone number

            customer_name_data_label = MDLabel(
                text=f"Customer Name: {customer_name}",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                font_size='24sp',  # Adjust font size
                font_style="Caption",
                size_hint_y=None,  # Fixed height
                height=30,
                halign='center'
            )
            card.add_widget(customer_name_data_label)

            customer_phone_data_label = MDLabel(
                text=f"Phone Number: {phone_number}",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                font_size='24sp',  # Adjust font size
                font_style="Caption",
                halign='center',
                size_hint_y=None,  # Fixed height
                height=30,  # Set the height of the label
            )
            card.add_widget(customer_phone_data_label)
        else:
            print("No matching customer found.")

        spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
        card.add_widget(spacer)

        Compalint = MDLabel(
            text="Complaint:",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_size='24sp',  # Adjust font size
            font_style="Caption",
            halign='center',
            size_hint_y=None,  # Fixed height
            height=30,  # Set the height of the label
            bold=True
        )
        card.add_widget(Compalint)
        card.add_widget(complaint_description_label)

        spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
        card.add_widget(spacer)

        Status = MDLabel(
            text=f"Status: {status}",
            theme_text_color="Custom",
            text_color=(0, 0.392, 0, 1),  # Dark Green color (RGBA values)
            font_style="Caption",
            halign='center',
            font_size=sp(20),  # Adjust font size to be extra large
            size_hint_y=None,  # Fixed height
            height=30,  # Set the height of the label
            bold=True
        )
        Status.font_size = 20
        card.add_widget(Status)

        spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
        card.add_widget(spacer)

        all_back_button = MDIconButton(
            icon='arrow-left',  # Use the appropriate icon name
            size_hint=(None, None),
            size=(50, 50),  # Adjust the size of the button
            pos_hint={'center_x': 0.5, 'center_y': 0.1},  # Adjust position as needed
            on_release=self.go_to_view_request_screen_all
        )
        card.add_widget(all_back_button)

        view_complaints_screen.add_widget(card)

    def go_to_view_request_screen_all(self, instance):
        if App.get_running_app().user_type == 'customer':
            self.manager.current = 'customer_view_history'
        elif App.get_running_app().user_type == 'service_provider':
            self.manager.current = 'provider_view_history'

    def get_customer_name_from_customer_table(customer_id):
        try:
            cursor.execute("SELECT customer_name,phone FROM customer WHERE customer_id = '" + str(customer_id) + "'")
            customer = cursor.fetchone()
            if customer:
                return customer[0], customer[1]
            else:
                return None
        except Exception as e:
            print(f"Error fetching category name: {e}")
            return None

class ReviewRatingScreen(Screen):

    def on_enter(self):
        service_booking_id = self.service_booking_id
        review_rating = self.ids['review_rating']

        cursor.execute("select * from service_booking where service_booking_id = '" + str(service_booking_id) + "'")
        service_booking = cursor.fetchone()
        service_booking_id = service_booking[0]

        card = MDCard(
            orientation='vertical',
            size_hint=(None, None),
            size=(dp(200), dp(300)),  # Adjust the size of the card
            elevation=5,
            padding=10
        )

        self.review_text = MDTextField(hint_text="Your Review here", helper_text_mode="on_focus")
        card.add_widget(self.review_text)

        spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
        card.add_widget(spacer)

        rating_spinner = Spinner(
            text='Select Rating',  # Initial text in the spinner
            values=[str(i) for i in range(6)],  # Values from 0 to 5
            size_hint=(.5, None),
            size=(150, 42),  # Adjust the size of the dropdown
            pos_hint={'center_x': 0.5, 'center_y': 0.1},  # Adjust position as needed
        )
        card.add_widget(rating_spinner)

        spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
        card.add_widget(spacer)

        self.selected_rating = None
        selected_rating_label = MDLabel(
            text='Selected Rating: ',
            size_hint=(.5, None),
            size=(150, 42),  # Adjust the size of the label
            pos_hint={'center_x': 0.5, 'center_y': 0.05},  # Adjust position as needed
        )
        def on_rating_selected(spinner, text):
            self.selected_rating = text
            selected_rating_label.text = f'Selected Rating: {text}'
        # Bind the function to the spinner's on_text event
        rating_spinner.bind(text=on_rating_selected)
        card.add_widget(selected_rating_label)

        spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
        card.add_widget(spacer)

        submit_button = MDRaisedButton(
            text='Submit',  # Text displayed on the button
            size_hint=(None, None),
            size=(150, 42),  # Adjust the size of the button
            pos_hint={'center_x': 0.5, 'center_y': 0.05},  # Adjust position as needed
            on_release=self.submit_review,  # Bind the button to a function
        )
        submit_button.service_booking_id = service_booking_id
        card.add_widget(submit_button)

        spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
        card.add_widget(spacer)

        back_button = MDIconButton(
            icon='arrow-left',  # Use the appropriate icon name
            size_hint=(None, None),
            size=(50, 50),  # Adjust the size of the button
            pos_hint={'center_x': 0.5, 'center_y': 0.1},  # Adjust position as needed
            on_release=self.go_to_view_request_screen
        )
        card.add_widget(back_button)

        spacer = Widget(size_hint_y=None, height=10)  # Adjust height as needed
        card.add_widget(spacer)

        review_rating.add_widget(card)

    def go_to_view_request_screen(self, instance):
        self.manager.current = 'customer_view_history'

    def submit_review(self, instance):
        service_booking_id = self.service_booking_id
        rating = self.selected_rating   # Access the rating_spinner using the stored reference
        review_text = self.review_text.text

        status = "Reviewd Successfully"

        cursor.execute("insert into review(review,rating,status,service_booking_id) values ('"+str(review_text)+"' , '"+str(rating)+"' , '"+str(status)+"' , '"+str(service_booking_id)+"')")
        conn.commit()
        toast("Reviewd Sccessfully")


class SnowRemovalApp(MDApp):
    customer_id = None
    is_logged_in = False
    service_provider_id = None
    service_provider_view_services = []
    service_provider_view_requests = []
    data_loaded = False
    customer_history = []
    service_provider_view_history = []
    customer_requests = []
    payment_status = {}

    def build(self):

        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.primary_hue = "100"

        # Set theme text color to white
        self.theme_cls.theme_style = "Dark"  # Set theme style to dark
        self.theme_cls.primary_style = "Light"  # Set primary style to light

        self.theme_cls.font_styles["Custom"] = ["Roboto", 16, False, 0.15]

        root = MDBoxLayout(orientation='vertical', size_hint=(1, 1))  # Take up full available space

        self.bg = Image(source='static/myfiles/17.jpg', allow_stretch=True, size=(900, 900))  # Set the desired size

        # Add a Canvas with the background image
        with root.canvas.before:
            Rectangle(texture=self.bg.texture, size=self.bg.texture.size, pos=root.pos)

        def update_bg_size(instance, value):
            self.bg.size = value
            self.bg.pos = instance.pos

        root.bind(size=update_bg_size)

        screen_nav = Builder.load_string(screen_helper)
        self.manager = ScreenManager(transition=NoTransition())
        self.manager.add_widget(HomeScreen(name="home_screen"))
        self.manager.add_widget(SelectionScreen(name="selection_screen"))
        self.manager.add_widget(ProviderRegistrationScreen(name="service_provider_register_screen"))
        self.manager.add_widget(CustomerRegistrationScreen(name="customer_register_screen"))
        self.manager.add_widget(ProviderLoginScreen(name="provider_login_screen"))
        self.manager.add_widget(CustomerLoginScreen(name="customer_login_screen"))
        self.manager.add_widget(DashboardProvider(name="dashboard_provider"))
        self.manager.add_widget(DashboardCustomer(name="dashboard_customer"))
        self.manager.add_widget(AddServiceScreen(name="add_service"))
        self.manager.add_widget(ProviderHomeScreen(name="provider_home_screen"))
        self.manager.add_widget(ViewServiceScreen(name="view_service"))
        self.manager.add_widget(ServiceDetailScreen(name="service_detail_screen"))
        self.manager.add_widget(ProviderProfile(name="provider_profile"))
        self.manager.add_widget(CustomerHomeScreen(name="customer_home_screen"))
        self.manager.add_widget(ViewCustomerServiceScreen(name="customer_view_service"))
        self.manager.add_widget(CustomerProfile(name="customer_profile"))
        self.manager.add_widget(CustomerServiceDetailScreen(name="customer_service_detail_screen"))
        self.manager.add_widget(CustomerViewRequests(name="customer_view_request"))
        self.manager.add_widget(CustomerViewHistory(name="customer_view_history"))
        self.manager.add_widget(ProviderViewRequests(name="provider_view_request"))
        self.manager.add_widget(ProviderViewHistory(name="provider_view_history"))
        self.manager.add_widget(CardDetailsScreen(name="carddetails"))
        self.manager.add_widget(FullCardDetailsScreen(name="fullcarddetails"))
        self.manager.add_widget(CustomerViewFullPaymentScreen(name="customer_view_full_payment"))
        self.manager.add_widget(CustomerRaiseComplaintsScreen(name="customer_raise_complaint"))
        self.manager.add_widget(ProviderViewPaymentsScreen(name="provider_view_payment_screen"))
        self.manager.add_widget(ViewServiceProviderComplaintsScreen(name="view_provider_my_complaint"))
        self.manager.add_widget(ReviewRatingScreen(name="reviewrating"))
        self.manager.add_widget(ViewComplaintsScreen(name="viewcomplaint"))


        root.add_widget(self.manager)

        return root

    def on_start(self):
        # Set the default screen here (if needed)
        pass

    def switch_screen(self, screen_name):
        print(f"Switching to screen: {screen_name}")
        self.manager.current = screen_name

    def switch_to_add_service(self):
        if self.manager.current != "add_service":
            self.manager.current = "add_service"

    def switch_to_view_service(self):
        if self.manager.current != "view_service":
            self.manager.current = "view_service"

    def switch_to_provider_profile(self):
        if self.manager.current != "provider_profile":
            self.manager.current = "provider_profile"

    def switch_to_customer_profile(self):
        if self.manager.current != "customer_profile":
            self.manager.current = "customer_profile"

    def switch_to_customer_view_service(self):
        if self.manager.current != "customer_view_service":
            self.manager.current = "customer_view_service"

    def switch_to_customer_view_request(self):
        if self.manager.current != "customer_view_request":
            self.manager.current = "customer_view_request"

    def switch_to_customer_view_history(self):
        if self.manager.current != "customer_view_history":
            self.manager.current = "customer_view_history"

    def switch_to_provider_view_request(self):
        if self.manager.current != "provider_view_request":
            self.manager.current = "provider_view_request"

    def switch_to_provider_view_history(self):
        if self.manager.current != "provider_view_history":
            self.manager.current = "provider_view_history"

    def logout(self):
        self.is_logged_in = False
        self.user_type = None
        self.customer_id = None
        self.service_provider_id = None
        self.service_provider_details = None
        self.service_provider_view_services = None
        self.service_provider_view_requests = None
        self.service_provider_view_history = None
        self.customer_profile__details = None
        self.customer_view_services = None
        self.customer_requests = None
        self.customer_history = None
        self.root.current = 'selection_screen'

if __name__ == "__main__":
    SnowRemovalApp().run()