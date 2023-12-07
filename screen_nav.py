screen_helper = """
#: import get_color_from_hex kivy.utils.get_color_from_hex
#:import NavigationLayout kivymd.uix.navigationdrawer.MDNavigationLayout
#:import Factory kivy.factory.Factory

ScreenManager:
    HomeScreen:
        name: 'home_screen'
    SelectionScreen:
        name: 'selection_screen'
    ProviderRegistrationScreen:
        name: 'service_provider_register_screen'
    CustomerRegistrationScreen:
        name: 'customer_register_screen'
    ProviderLoginScreen:
        name: 'provider_login_screen'
    CustomerLoginScreen:
        name: 'customer_login_screen'
    DashboardProvider:
        name: 'dashboard_provider'
    DashboardCustomer:
        name: 'dashboard_customer'
    AddServiceScreen:
        name: 'add_service'
    ProviderHomeScreen:
        name: 'provider_home_screen'
    ViewServiceScreen:
        name: 'view_service'
    ServiceDetailScreen:
        name: 'service_detail_screen'
    ProviderProfile:
        name: 'provider_profile'
    CustomerHomeScreen:
        name: 'customer_home_screen'
    ViewCustomerServiceScreen:
        name: 'customer_view_service'
    CustomerProfile:
        name: 'customer_profile'
    CustomerServiceDetailScreen:
        name: 'customer_service_detail_screen'
    CustomerViewRequests:
        name: 'customer_view_request'
    CustomerViewHistory:
        name: 'customer_view_history'
    ProviderViewRequests:
        name: 'provider_view_request'
    ProviderViewHistory:
        name: 'provider_view_history'
    CardDetailsScreen:
        name: 'carddetails'
    FullCardDetailsScreen:
        name: 'fullcarddetails'
    CustomerViewFullPaymentScreen:
        name: 'customer_view_full_payment'
    CustomerRaiseComplaintsScreen:
        name: 'customer_raise_complaint'
    ProviderViewPaymentsScreen:
        name: 'provider_view_payment_screen'
    ViewServiceProviderComplaintsScreen:
        name: 'view_provider_my_complaint'
    ViewComplaintsScreen:
        name: 'viewcomplaint'
    ReviewRatingScreen:
        name: 'reviewrating'
        

<ProviderLoginScreen>
    service_email : service_email
    service_password : service_password
    BoxLayout:
        orientation: 'vertical'
        pos_hint: {"center_x":.5,"center_y":.8}
        padding: 40
        spacing: 20
        Widget:
            size_hint_y: 1
        MDLabel:
            text: "SERVICE PROVIDER LOGIN"
            color: 1, 1, 0.6, 1  # Pale yellow color in RGBA format
            font_name: "Roboto"
            font_style: 'Button'
            font_size: 40
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]
            padding_y: 15
        MDTextField:
            id : service_email
            hint_text: "Email"
            font_name: "Roboto"
            icon_right: "account"
            mode: "round"
            size_hint_x: None
            width: 290
            font_size: 20
            pos_hint: {"center_x": .5}
            color_active: [1,1,1,1]
            normal_color : [1,1,0,1]
            on_text_validate: root.validate_provider_email(self)
        MDTextField:
            id : service_password
            mode: "round"
            hint_text: "Password"
            font_name: "Roboto"
            icon_right: "eye-off"
            size_hint_x: None
            width: 290
            font_size: 20
            pos_hint: {"center_x": .5}
            color_active: [1,1,1,1]
            password: True
            on_text: self.text = self.text.replace(" ", "")
            on_focus: service_password.password = not self.focus
            MDIconButton:
                icon: "eye-off"
                pos_hint: {"center_y": 0.5}
                on_release: root.toggle_password_visibility()
        MDRoundFlatButton:
            text: "LOGIN"
            pos_hint: {"center_x": .5}
            font_size: 20
            md_bg_color: 0.2, 0.2, 0.2, 1  # Dark grey background color
            text_color: 1, 1, 1, 1  # White text color
            on_press: root.service_provider_login()

<ProviderRegistrationScreen>
    sname : sname
    email : email
    password : password
    phone : phone
    address : address
    BoxLayout:
        orientation: 'vertical'
        pos_hint: {"center_x":.5,"center_y":.5}
        padding: 40
        spacing: 20
        Widget:
            size_hint_y: 1
        MDLabel:
            text: "Service Provider Registration"
            color: 1, 1, 0.6, 1  # Pale yellow color in RGBA format
            font_name: "Roboto"
            font_style: 'Button'
            font_size: 25
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]
            padding_y: 15
        MDTextField:
            id: sname
            hint_text: "Name"
            font_name: "Roboto"
            icon_right: "account"
            mode: "round"
            size_hint_x: None
            width: 290
            font_size: 20
            pos_hint: {"center_x": .5}
            color_active: [1,1,1,1]
            normal_color : [1,1,0,1]
            on_text_validate: root.validate_provider_name(self)
        MDTextField:
            id: email
            mode: "round"
            hint_text: "Email"
            font_name: "Roboto"
            icon_right: "email"
            size_hint_x: None
            width: 290
            font_size: 20
            pos_hint: {"center_x": .5}
            color_active: [1,1,1,1]
            on_text_validate: root.validate_email(self)
        MDTextField:
            id: password
            mode: "round"
            multiline: False  # Set multiline to False
            hint_text: "Password"
            font_name: "Roboto"
            icon_right: "eye-off"
            size_hint_x: None
            width: 290
            font_size: 20
            pos_hint: {"center_x": .5}
            color_active: [1, 1, 1, 1]
            password: True
            on_text: self.text = self.text.replace(" ", "")
            on_focus: password.password = not self.focus
            MDIconButton:
                icon: "eye-off"
                pos_hint: {"center_y": 0.5}
                on_release: root.toggle_password_visibility()
        MDTextField:
            id: phone
            mode: "round"
            hint_text: "Phone"
            font_name: "Roboto"
            icon_right: "phone"
            size_hint_x: None
            width: 290
            font_size: 20
            pos_hint: {"center_x": .5}
            color_active: [1,1,1,1]
            on_text_validate: root.validate_phone(self)
        MDTextField:
            id: address
            mode: "round"
            hint_text: "Address"
            font_name: "Roboto"
            icon_right: "address"
            size_hint_x: None
            width: 290
            font_size: 20
            pos_hint: {"center_x": .5}
            color_active: [1,1,1,1]
            line_color_normal: 0,0,0,1  # Set text color to black
        Widget:
            size_hint_y: None
            height: 19
        BoxLayout:
            size_hint: .85, None
            height: "30dp"
            pos_hint: {'center_x':.5, 'center_y':.3}
            spacing: "5dp"
            MDFlatButton:
                id: profile
                text: "Profile"
                size_hint_x: 2
                font_size: 20
                md_bg_color: 0, 128/255, 128/255, 1  # Teal background color
                text_color: 0, 0, 0, 1  # Black text color
                on_press : root.profile_button()
            Image:
                id : profile_img
            MDFlatButton
                id: licence
                text: "Licence"
                size_hint_x: 2
                font_size: 20
                md_bg_color: 0, 128/255, 128/255, 1  # Teal background color
                text_color: 0, 0, 0, 1  # Black text color
                on_press : root.licence_button()
            Image:
                id : licence_img
            MDFlatButton:
                id: idproof
                text: "ID Proof"
                size_hint_x: 2
                font_size: 20
                md_bg_color: 0, 128/255, 128/255, 1  # Teal background color
                text_color: 0, 0, 0, 1  # Black text color
                on_press : root.id_proof_button()
            Image:
                id : id_proof_img
        Widget:
            size_hint_y: None
            height: 19
        MDRoundFlatButton:
            text: "REGISTER"
            pos_hint: {"center_x": .5}
            spacing: 9
            md_bg_color: 0.2, 0.2, 0.2, 1  # Dark grey background color
            text_color: 1, 1, 1, 1  # White text color
            font_size: 20
            on_press : root.register_data()

<CustomerRegistrationScreen>
    fname : fname
    email : email
    phone : phone
    password : password
    address : address
    BoxLayout:
        orientation: 'vertical'
        pos_hint: {"center_x":.5,"center_y":.5}
        padding: 40
        spacing: 20
        Widget:
            size_hint_y: 1
        MDLabel:
            text: "Customer Registration"
            color: 1, 1, 0.6, 1  # Pale yellow color in RGBA format
            font_name: "Roboto"
            font_style: 'Button'
            font_size: 25
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]
            padding_y: 15
        MDTextField:
            id: fname
            hint_text: "Name"
            multiline: False
            font_name: "Roboto"
            icon_right: "account"
            mode: "round"
            size_hint_x: None
            width: 290
            font_size: 20
            pos_hint: {"center_x": .5}
            color_active: [1,1,1,1]
            normal_color : [1,1,0,1]
            on_text_validate: root.validate_customer_name(self)
        MDTextField:
            id: email
            mode: "round"
            hint_text: "Email"
            multiline: False
            font_name: "Roboto"
            icon_right: "email"
            size_hint_x: None
            width: 290
            font_size: 20
            pos_hint: {"center_x": .5}
            color_active: [1,1,1,1]
            on_text_validate: root.validate_customer_email(self)
        MDTextField:
            id: phone
            mode: "round"
            hint_text: "Phone"
            font_name: "Roboto"
            icon_right: "phone"
            multiline: False
            size_hint_x: None
            width: 290
            font_size: 20
            pos_hint: {"center_x": .5}
            color_active: [1,1,1,1]
            on_text_validate: root.validate_customer_phone(self)
        MDTextField:
            id: password
            mode: "round"
            hint_text: "Password"
            multiline: False
            font_name: "Roboto"
            icon_right: "eye-off"
            size_hint_x: None
            width: 290
            font_size: 20
            pos_hint: {"center_x": .5}
            color_active: [1,1,1,1]
            password: True
            on_text: self.text = self.text.replace(" ", "")
            on_focus: password.password = not self.focus
            MDIconButton:
                icon: "eye-off"
                pos_hint: {"center_y": 0.5}
                on_release: root.toggle_password_visibility()
        MDTextField:
            id: address
            mode: "round"
            hint_text: "Address"
            multiline: False
            font_name: "Roboto"
            icon_right: "address"
            size_hint_x: None
            width: 290
            font_size: 20
            pos_hint: {"center_x": .5}
            color_active: [1,1,1,1]
        Widget:
            size_hint_y: None
            height: 19
        BoxLayout:
            size_hint: .85, None
            height: "30dp"
            pos_hint: {'center_x':.5, 'center_y':.3}
            spacing: "5dp"
            MDFlatButton:
                id: customer_profile
                text: "Select Profile"
                size_hint_x: 2
                font_size: 20
                md_bg_color: 0, 128/255, 128/255, 1  # Teal background color
                text_color: 0, 0, 0, 1  # Black text color
                on_press : root.customer_profile_button()
            Image:
                id : customer_profile_img
                opacity: 0 
        Widget:
            size_hint_y: None
            height: 19
        MDRoundFlatButton:
            text: "REGISTER"
            pos_hint: {"center_x": .5}
            font_size: 20
            md_bg_color: 0.2, 0.2, 0.2, 1  # Dark grey background color
            text_color: 1, 1, 1, 1  # White text color
            on_press: root.customer_register()

<CustomerLoginScreen>
    customer_email : customer_email
    customer_password : customer_password
    BoxLayout:
        orientation: 'vertical'
        pos_hint: {"center_x":.5,"center_y":.8}
        padding: 40
        spacing: 20
        Widget:
            size_hint_y: 1
        MDLabel:
            text: "CUSTOMER LOGIN"
            color: 1, 1, 0.6, 1  # Pale yellow color in RGBA format
            font_name: "Roboto"
            font_style: 'Button'
            font_size: 40
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]
            padding_y: 15
        MDTextField:
            id: customer_email
            hint_text: "Email"
            font_name: "Roboto"
            icon_right: "account"
            mode: "round"
            size_hint_x: None
            width: 290
            font_size: 20
            pos_hint: {"center_x": .5}
            color_active: [1,1,1,1]
            normal_color : [1,1,0,1]
            on_text: self.text = self.text.replace(" ", "")
            on_text_validate: root.validate_customer_login_email(self)
        MDTextField:
            id: customer_password
            mode: "round"
            hint_text: "Password"
            font_name: "Roboto"
            icon_right: "eye-off"
            size_hint_x: None
            width: 290
            font_size: 20
            pos_hint: {"center_x": .5}
            color_active: [1,1,1,1]
            password: True
            on_text: self.text = self.text.replace(" ", "")
            on_focus: customer_password.password = not self.focus
            MDIconButton:
                icon: "eye-off"
                pos_hint: {"center_y": 0.5}
                on_release: root.toggle_password_visibility()
        MDRoundFlatButton:
            text: "LOGIN"
            pos_hint: {"center_x": .5}
            font_size: 20
            md_bg_color: 0.2, 0.2, 0.2, 1  # Dark grey background color
            text_color: 1, 1, 1, 1  # White text color
            on_press: root.customer_login()

<DashboardCustomer>
    MDNavigationLayout:
        ScreenManager:
            CustomerHomeScreen:
                name: "customer_home_screen"
                MDTopAppBar:
                    title: "Snow Removal"
                    pos_hint: {"top": 1}
                    elevation: 5
                    left_action_items: [['menu', lambda x: root.toggle_customer_nav_drawer()]]
                BoxLayout:
                    orientation: 'horizontal'
                    pos_hint: {"center_x":.5,"center_y":.6}
                    BoxLayout:
                        orientation: 'horizontal'
                        MDLabel:
                            id: welcome_customer_name_label
                            text: "Welcome to Snow Removal App"
                            font_name: "Roboto"
                            font_size: 20  # Adjust the font size as needed
                            halign: "left"
                            theme_text_color: "Custom"
                            text_color: 1, 1, 1, 1  # White color
                            pos_hint: {"center_x":.4,"center_y":.7}
                            padding: [20, 0, 0, 0]  # Adjust the left padding value as needed
                        AsyncImage:
                            id: welcome_profile
                            source: 'path_to_your_image.jpg'  # Replace with actual path
                            size_hint: None, None
                            size: "50dp", "50dp"
                            pos_hint: {"center_x": 0.3, "center_y": 0.7, "right": 1}
                            allow_stretch: True
                            keep_ratio: True
                            canvas.before:
                                Color:
                                    rgba: 1, 1, 1, 1  # White color
                                Ellipse:
                                    size: self.size
                                    pos: self.pos
                BoxLayout:
                    orientation: 'vertical'
                    padding: 10
                    spacing: "2dp"
                    pos_hint: {"center_x":.5,"center_y":.6}
                    BoxLayout:
                        orientation: 'horizontal'
                        spacing: "8dp"
                        MDCard:
                            orientation: 'vertical'
                            size_hint: None, None
                            size: "80dp", "80dp"
                            md_bg_color: 0, 0.5, 0.5, 1  # Teal color (RGBA)
                            MDLabel:
                                text: "Services"
                                font_size: 20
                                font_name: "Roboto"
                                halign: "center"
                            MDLabel:
                                id: service_count
                                text: "0"  # Initial text, it will be updated in the code
                                font_size: 20
                                font_name: "Roboto"
                                halign: "center"
                        MDCard:
                            orientation: 'vertical'
                            size_hint: None, None
                            size: "80dp", "80dp"
                            md_bg_color: 0, 0.5, 0.5, 1  # Teal color (RGBA)
                            MDLabel:
                                text: "Requests"
                                font_size: 20
                                font_name: "Roboto"
                                halign: "center"
                            MDLabel:
                                id: request_count
                                text: "0"  # Initial text, it will be updated in the code
                                font_size: 20
                                font_name: "Roboto"
                                halign: "center"
                        MDCard:
                            orientation: 'vertical'
                            size_hint: None, None
                            size: "80dp", "80dp"
                            md_bg_color: 0, 0.5, 0.5, 1  # Teal color (RGBA)
                            MDLabel:
                                text: "Processing"
                                font_size: 20
                                font_name: "Roboto"
                                halign: "center"
                            MDLabel:
                                id: processing_count
                                text: "0"  # Initial text, it will be updated in the code
                                font_size: 20
                                font_name: "Roboto"
                                halign: "center"
                        MDCard:
                            orientation: 'vertical'
                            size_hint: None, None
                            size: "80dp", "80dp"
                            md_bg_color: 0, 0.5, 0.5, 1  # Teal color (RGBA)
                            MDLabel:
                                text: "Complete"
                                font_size: 20
                                font_name: "Roboto"
                                halign: "center"
                            MDLabel:
                                id: complete_count
                                text: "0"  # Initial text, it will be updated in the code
                                font_size: 20
                                font_name: "Roboto"
                                halign: "center"
                    BoxLayout:  # This will be the second row of cards
                        orientation: 'horizontal'
                        pos_hint: {"center_x":.5,"center_y":.2}
                MDLabel:
                    text: "Top Services"
                    font_name: "Roboto"
                    font_size: 30  # Adjust the font size as needed
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1  # White color
                    pos_hint: {"center_x":.5,"center_y":.5}
                    padding: [20, 0, 0, 0]  # Adjust the left padding value as needed
                BoxLayout:
                    orientation: 'vertical'
                    padding: 20
                    spacing: "20dp"
                    pos_hint: {"center_x":.5,"center_y":.0}
                    MDTextField:  # Add this MDTextField for the search bar
                        id: top_service_search_field
                        hint_text: "Search Services"
                        size_hint_x: None
                        width: "300dp"  # Adjust the width as needed
                        on_text_validate: root.search_services()  # Add this line
                    ScrollView:
                        GridLayout:
                            id: top_services
                            cols: 2 # Set to 1 since we want one card per row
                            height: self.minimum_height  # Add this line
                            size_hint_y: None  # Add this line
                            padding: 20  # Add this line
                            spacing: 30  # Add this line
            ViewCustomerServiceScreen:
                name: "customer_view_service"
            CustomerProfile:
                name: "customer_profile"
            CustomerViewRequests:
                name: "customer_view_request"
            CustomerViewHistory:
                name: "customer_view_history"
        MDNavigationDrawer:
            id: customer_nav_drawer
            BoxLayout:
                orientation: 'vertical'
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: dp(8)
                    ScrollView:
                        MDList:
                            OneLineIconListItem:
                                text: 'Home'
                                on_release: app.switch_screen("dashboard_customer")
                                IconLeftWidget:
                                    icon: 'home'
                            OneLineIconListItem:
                                text: 'Profile'
                                on_release: app.switch_screen("customer_profile")
                                IconLeftWidget:
                                    icon: 'account'
                            OneLineIconListItem:
                                text: 'View Services'
                                on_release: app.switch_screen("customer_view_service")
                                IconLeftWidget:
                                    icon: 'eye'
                            OneLineIconListItem:
                                text: 'View Requests'
                                on_release: app.switch_screen("customer_view_request")
                                IconLeftWidget:
                                    icon: 'email'
                            OneLineIconListItem:
                                text: 'View History'
                                on_release: app.switch_screen("customer_view_history")
                                IconLeftWidget:
                                    icon: 'history'
                            OneLineIconListItem:
                                text: 'Logout'
                                on_release: root.logout()
                                IconLeftWidget:
                                    icon: 'logout'

<DashboardProvider>
    MDNavigationLayout:
        ScreenManager:
            ProviderHomeScreen:
                name: "provider_home_screen"
                MDTopAppBar:
                    title: "Snow Removal"
                    pos_hint: {"top": 1}
                    elevation: 10
                    left_action_items: [['menu', lambda x: root.toggle_nav_drawer()]]
                BoxLayout:
                    orientation: 'horizontal'
                    pos_hint: {"center_x":.5,"center_y":.6}
                    BoxLayout:
                        orientation: 'horizontal'
                        MDLabel:
                            id: welcome_provider_name_label
                            text: "Welcome to Snow Removal App"
                            font_name: "Roboto"
                            font_size: 20  # Adjust the font size as needed
                            halign: "left"
                            theme_text_color: "Custom"
                            text_color: 1, 1, 1, 1  # White color
                            pos_hint: {"center_x":.4,"center_y":.7}
                            padding: [20, 0, 0, 0]  # Adjust the left padding value as needed
                        AsyncImage:
                            id: provider_welcome_profile
                            source: 'path_to_your_image.jpg'  # Replace with actual path
                            size_hint: None, None
                            size: "50dp", "50dp"
                            pos_hint: {"center_x": 0.3, "center_y": 0.7, "right": 1}
                            allow_stretch: True
                            keep_ratio: True
                            canvas.before:
                                Color:
                                    rgba: 1, 1, 1, 1  # White color
                                Ellipse:
                                    size: self.size
                                    pos: self.pos
                BoxLayout:
                    orientation: 'vertical'
                    padding: 10
                    spacing: "2dp"
                    pos_hint: {"center_x":.5,"center_y":.6}
                    BoxLayout:
                        orientation: 'horizontal'
                        spacing: "8dp"
                        MDCard:
                            orientation: 'vertical'
                            size_hint: None, None
                            size: "80dp", "80dp"
                            md_bg_color: 0, 0.5, 0.5, 1  # Teal color (RGBA)
                            MDLabel:
                                text: "Services"
                                font_size: 20
                                font_name: "Roboto"
                                halign: "center"
                            MDLabel:
                                id: service_count_label
                                text: "0"  # Initial text, it will be updated in the code
                                font_size: 20
                                font_name: "Roboto"
                                halign: "center"
                        MDCard:
                            orientation: 'vertical'
                            size_hint: None, None
                            size: "80dp", "80dp"
                            md_bg_color: 0, 0.5, 0.5, 1  # Teal color (RGBA)
                            MDLabel:
                                text: "Requests"
                                font_size: 20
                                font_name: "Roboto"
                                halign: "center"
                            MDLabel:
                                id: request_count_label
                                text: "0"  # Initial text, it will be updated in the code
                                font_size: 20
                                font_name: "Roboto"
                                halign: "center"
                        MDCard:
                            orientation: 'vertical'
                            size_hint: None, None
                            size: "80dp", "80dp"
                            md_bg_color: 0, 0.5, 0.5, 1  # Teal color (RGBA)
                            MDLabel:
                                text: "Processing"
                                font_size: 20
                                font_name: "Roboto"
                                halign: "center"
                            MDLabel:
                                id: processing_count_label
                                text: "0"  # Initial text, it will be updated in the code
                                font_size: 20
                                font_name: "Roboto"
                                halign: "center"
                        MDCard:
                            orientation: 'vertical'
                            size_hint: None, None
                            size: "80dp", "80dp"
                            md_bg_color: 0, 0.5, 0.5, 1  # Teal color (RGBA)
                            MDLabel:
                                text: "Complete"
                                font_size: 20
                                font_name: "Roboto"
                                halign: "center"
                            MDLabel:
                                id: complete_count_label
                                text: "0"  # Initial text, it will be updated in the code
                                font_size: 20
                                font_name: "Roboto"
                                halign: "center"
                    BoxLayout:  # This will be the second row of cards
                        orientation: 'horizontal'
                        spacing: "8dp"
                        pos_hint: {"center_x":.5,"center_y":.1}
                MDLabel:
                    text: "Top Services"
                    font_name: "Roboto"
                    font_size: 30  # Adjust the font size as needed
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1  # White color
                    pos_hint: {"center_x":.5,"center_y":.5}
                    padding: [20, 0, 0, 0]  # Adjust the left padding value as needed
                BoxLayout:
                    orientation: 'vertical'
                    padding: 20
                    spacing: "20dp"
                    pos_hint: {"center_x":.5,"center_y":.0}
                    MDTextField:  # Add this MDTextField for the search bar
                        id: top_service_search_field_provider
                        hint_text: "Search Services"
                        size_hint_x: None
                        width: "300dp"  # Adjust the width as needed
                        on_text_validate: root.search_services_provider()  # Add this line
                    ScrollView:
                        GridLayout:
                            id: top_services_provider
                            cols: 2 # Set to 1 since we want one card per row
                            height: self.minimum_height  # Add this line
                            size_hint_y: None  # Add this line
                            padding: 20  # Add this line
                            spacing: 30  # Add this line
            AddServiceScreen:
                name: "add_service"
            ViewServiceScreen:
                name: "view_service"
            ProviderViewRequests:
                name: "provider_view_request"
            ProviderViewHistory:
                name: "provider_view_history"
        MDNavigationDrawer:
            id: provider_nav_drawer
            BoxLayout:
                orientation: 'vertical'
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: dp(8)
                    ScrollView:
                        MDList:
                            OneLineIconListItem:
                                text: 'Home'
                                on_release: app.switch_screen("dashboard_provider")
                                IconLeftWidget:
                                    icon: 'home'
                            OneLineIconListItem:
                                text: 'Profile'
                                on_release: app.switch_screen("provider_profile")
                                IconLeftWidget:
                                    icon: 'account'
                            OneLineIconListItem:
                                text: 'Add Services'
                                on_release: app.switch_screen("add_service")
                                IconLeftWidget:
                                    icon: 'plus'
                            OneLineIconListItem:
                                text: 'View Services'
                                on_release: app.switch_screen("view_service")
                                IconLeftWidget:
                                    icon: 'eye'
                            OneLineIconListItem:
                                text: 'View Requests'
                                on_release: app.switch_screen("provider_view_request")
                                IconLeftWidget:
                                    icon: 'email'
                            OneLineIconListItem:
                                text: 'View History'
                                on_release: app.switch_screen("provider_view_history")
                                IconLeftWidget:
                                    icon: 'history'
                            OneLineIconListItem:
                                text: 'Logout'
                                on_release: root.logout()
                                IconLeftWidget:
                                    icon: 'logout'
<AddServiceScreen>
    location_id : location_id
    category_id : category_id
    service_name : service_name
    charge_per_sq_feet : charge_per_sq_feet
    service_description : service_description
    MDNavigationLayout:
        ScreenManager:
            ProviderHomeScreen:
                name: "provider_home_screen"
                MDTopAppBar:
                    title: "Snow Removal"
                    pos_hint: {"top": 1}
                    elevation: 10
                    left_action_items: [['menu', lambda x: root.toggle_nav_drawer()]]
                BoxLayout:
                    orientation: 'vertical'
                    pos_hint: {"center_x":.5,"center_y":.5}
                    padding: 40
                    spacing: 20
                    Widget:
                        size_hint_y: 1
                    Spinner:
                        id: location_id
                        pos_hint: {"center_x": .5}
                        font_name: "Roboto"
                        text: 'Select Locations'
                        md_bg_color: 0.2, 0.2, 0.2, 1  # Dark grey background color
                        text_color: 1, 1, 1, 1  # White text color
                        values: root.fetch_location_names_from_database()
                    Spinner:
                        id: category_id
                        values: root.fetch_category_names_from_database()
                        pos_hint: {"center_x": .5}
                        font_name: "Roboto"
                        text: 'Select Category'
                        md_bg_color: 0.2, 0.2, 0.2, 1  # Dark grey background color
                        text_color: 1, 1, 1, 1  # White text color
                    MDTextField:
                        id : service_name
                        hint_text: "Service Name"
                        font_name: "Roboto"
                        size_hint_x: None
                        width: 290
                        font_size: 20
                        pos_hint: {"center_x": .5}
                        color: 1, 1, 0.6, 1  # Pale yellow color in RGBA format
                        color_active: [1,1,1,1]
                    MDTextField:
                        id : charge_per_sq_feet
                        hint_text: "Charge Per sq.feet"
                        font_name: "Roboto"
                        size_hint_x: None
                        width: 290
                        font_size: 20
                        pos_hint: {"center_x": .5}
                        color: 1, 1, 0.6, 1  # Pale yellow color in RGBA format
                        color_active: [1,1,1,1]
                    MDTextField:
                        id : service_description
                        hint_text: "Description"
                        font_name: "Roboto"
                        width: 290
                        size_hint_x: None
                        font_size: 20
                        pos_hint: {"center_x": .5}
                        color: 1, 1, 0.6, 1  # Pale yellow color in RGBA format
                        color_active: [1,1,1,1]
                    MDRoundFlatButton:
                        id: service_picture
                        text: "Select Service Picture"
                        pos_hint: {"center_x": .5}
                        font_size: 20
                        md_bg_color: 0, 128/255, 128/255, 1  # Teal background color
                        text_color: 0, 0, 0, 1  # Black text color
                        on_press : root.service_button()
                    Image:
                        id : service_picture
                        size_hint: None, None
                        size: 30, 30
                        pos_hint: {"center_x": .5}
                        opacity: 0 
                    MDRoundFlatButton:
                        text: "ADD SERVICE"
                        pos_hint: {"center_x": .5}
                        font_size: 20
                        md_bg_color: 0.2, 0.2, 0.2, 1  # Dark grey background color
                        text_color: 1, 1, 1, 1  # White text color
                        on_press: root.add_service_data()
        MDNavigationDrawer:
            id: provider_nav_drawer
            BoxLayout:
                orientation: 'vertical'
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: dp(8)
                    ScrollView:
                        MDList:
                            OneLineIconListItem:
                                text: 'Home'
                                on_release: app.switch_screen("dashboard_provider")
                                IconLeftWidget:
                                    icon: 'home'
                            OneLineIconListItem:
                                text: 'Profile'
                                on_release: app.switch_screen("provider_profile")
                                IconLeftWidget:
                                    icon: 'account'
                            OneLineIconListItem:
                                text: 'Add Services'
                                on_release: app.switch_screen("add_service")
                                IconLeftWidget:
                                    icon: 'plus'
                            OneLineIconListItem:
                                text: 'View Services'
                                on_release: app.switch_screen("view_service")
                                IconLeftWidget:
                                    icon: 'eye'
                            OneLineIconListItem:
                                text: 'View Requests'
                                on_release: app.switch_screen("provider_view_request")
                                IconLeftWidget:
                                    icon: 'email'
                            OneLineIconListItem:
                                text: 'View History'
                                on_release: app.switch_screen("provider_view_history")
                                IconLeftWidget:
                                    icon: 'history'
                            OneLineIconListItem:
                                text: 'Logout'
                                on_release: root.logout()
                                IconLeftWidget:
                                    icon: 'logout'
                                    
<ViewServiceScreen>
    name: "view_service"
    MDNavigationLayout:
        ScreenManager:
            ProviderHomeScreen:
                name: "provider_home_screen"
                MDTopAppBar:
                    title: "Snow Removal"
                    pos_hint: {"top": 1}
                    elevation: 10
                    left_action_items: [['menu', lambda x: root.toggle_nav_drawer()]]
                BoxLayout:
                    orientation: 'vertical'
                    pos_hint: {'center_x': 0.4}
                    padding: 50  # Add padding to create a gap around the contents
                    spacing: 10
                    ScrollView:
                        GridLayout:
                            id: service_cards_layout
                            cols: 2  # Set to 1 since we want one card per row
        MDNavigationDrawer:
            id: provider_nav_drawer
            BoxLayout:
                orientation: 'vertical'
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: dp(8)
                    ScrollView:
                        MDList:
                            OneLineIconListItem:
                                text: 'Home'
                                on_release: app.switch_screen("dashboard_provider")
                                IconLeftWidget:
                                    icon: 'home'
                            OneLineIconListItem:
                                text: 'Profile'
                                on_release: app.switch_screen("provider_profile")
                                IconLeftWidget:
                                    icon: 'account'
                            OneLineIconListItem:
                                text: 'Add Services'
                                on_release: app.switch_screen("add_service")
                                IconLeftWidget:
                                    icon: 'plus'
                            OneLineIconListItem:
                                text: 'View Services'
                                on_release: app.switch_screen("view_service")
                                IconLeftWidget:
                                    icon: 'eye'
                            OneLineIconListItem:
                                text: 'View Requests'
                                on_release: app.switch_screen("provider_view_request")
                                IconLeftWidget:
                                    icon: 'email'
                            OneLineIconListItem:
                                text: 'View History'
                                on_release: app.switch_screen("provider_view_history")
                                IconLeftWidget:
                                    icon: 'history'
                            OneLineIconListItem:
                                text: 'Logout'
                                on_release: root.logout()
                                IconLeftWidget:
                                    icon: 'logout'
<ServiceDetailScreen>
    name: "service_detail_screen"
    BoxLayout:
        orientation: 'vertical'
        pos_hint: {"center_x": .5, "center_y": .5}
        size_hint: None, None
        size: 500, 640
        padding: 50
        spacing: 0
        MDIconButton:
            icon: 'arrow-left'
            pos_hint: {'x': 0.02, 'top': 0.98}
            on_press: root.manager.current= 'view_service'  # Replace with the actual screen name to go back to
        GridLayout:
            id: service_details
            cols: 1
            spacing: 0
            size_hint_y: None
            height: self.minimum_height
            AsyncImage:
                id: service_image
                source: 'your_image_source.png'
                size_hint_y: None
                height: 200  # Set the height to your desired value
                width: 800   # Set the width to your desired value
                allow_stretch: True
                keep_ratio: True
                canvas.before:
                    Rectangle:
                        pos: self.pos
                        size: self.size
            MDLabel:
                id: location_name
                text: 'Location Name'
                size_hint_y: None
                height: 50
                halign: 'center'
                valign: 'middle'
                bold: True  # Make the text bold
            MDLabel:
                id: category_name
                text: 'Category Name'
                size_hint_y: None
                height: 50
                halign: 'center'
                valign: 'middle'
                bold: True  # Make the text bold
            MDLabel:
                id: service_name
                text: 'Service Name'
                size_hint_y: None
                height: 50
                font_size: dp(30)  # Set the font size in dp
                theme_text_color: "Custom"
                text_color: 1, 1, 0.5, 1  # Pale yellow color (RGBA)
                halign: 'center'
                valign: 'middle'
                bold: True  # Make the text bold
            MDLabel:
                id: charge_per_sq_feet
                text: 'Charger Per Sq feet'
                size_hint_y: None
                height: 50
                halign: 'center'
                valign: 'middle'
                bold: True  # Make the text bold
            MDLabel:
                id: description
                text: 'Description'
                size_hint_y: None
                height: 50
                halign: 'center'
                valign: 'middle'
                bold: True  # Make the text bold
<ProviderProfile>
    MDNavigationLayout:
        ScreenManager:
            ProviderHomeScreen:
                name: "provider_home_screen"
                MDTopAppBar:
                    title: "Snow Removal"
                    pos_hint: {"top": 1}
                    elevation: 10
                    left_action_items: [['menu', lambda x: root.toggle_nav_drawer()]]
                BoxLayout:
                    orientation: 'vertical'
                    pos_hint: {"center_x": .5, "center_y": .6}
                    size_hint: None, None
                    size: 500, 640
                    padding: 50
                    spacing: 0
                    GridLayout:
                        id: provider_details
                        cols: 1
                        spacing: 0
                        size_hint_y: None
                        height: self.minimum_height
                        AsyncImage:
                            id: service_provider_image
                            size_hint_y: None
                            height: 200  # Set the height to your desired value
                            width: 800   # Set the width to your desired value
                            allow_stretch: True
                            keep_ratio: True
                            canvas.before:
                                Rectangle:
                                    pos: self.pos
                                    size: self.size
                        MDLabel:
                            id: service_provider_name_label
                            text: 'Provider Name'
                            size_hint_y: None
                            height: 50
                            halign: 'center'
                            valign: 'middle'
                            bold: True  # Make the text bold
                            font_size: 24
                        MDLabel:
                            id: service_provider_email_label
                            text: 'Provider Email'
                            size_hint_y: None
                            height: 50
                            halign: 'center'
                            valign: 'middle'
                            bold: True  # Make the text bold
                            font_size: 24
                        MDLabel:
                            id: service_provider_phone_label
                            text: 'Provider Phone'
                            size_hint_y: None
                            height: 50
                            halign: 'center'
                            valign: 'middle'
                            bold: True  # Make the text bold
                            font_size: 24
                        MDLabel:
                            id: service_provider_address_label
                            text: 'Provider Address'
                            size_hint_y: None
                            height: 50
                            halign: 'center'
                            valign: 'middle'
                            bold: True  # Make the text bold
                            font_size: 24
        MDNavigationDrawer:
            id: provider_nav_drawer
            BoxLayout:
                orientation: 'vertical'
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: dp(8)
                    ScrollView:
                        MDList:
                            OneLineIconListItem:
                                text: 'Home'
                                on_release: app.switch_screen("dashboard_provider")
                                IconLeftWidget:
                                    icon: 'home'
                            OneLineIconListItem:
                                text: 'Profile'
                                on_release: app.switch_screen("provider_profile")
                                IconLeftWidget:
                                    icon: 'account'
                            OneLineIconListItem:
                                text: 'Add Services'
                                on_release: app.switch_screen("add_service")
                                IconLeftWidget:
                                    icon: 'plus'
                            OneLineIconListItem:
                                text: 'View Services'
                                on_release: app.switch_screen("view_service")
                                IconLeftWidget:
                                    icon: 'eye'
                            OneLineIconListItem:
                                text: 'View Requests'
                                on_release: app.switch_screen("provider_view_request")
                                IconLeftWidget:
                                    icon: 'email'
                            OneLineIconListItem:
                                text: 'View History'
                                on_release: app.switch_screen("provider_view_history")
                                IconLeftWidget:
                                    icon: 'history'
                            OneLineIconListItem:
                                text: 'Logout'
                                on_release: root.logout()
                                IconLeftWidget:
                                    icon: 'logout'
<CustomerProfile>
    MDNavigationLayout:
        ScreenManager:
            CustomerHomeScreen:
                name: "customer_home_screen"
                MDTopAppBar:
                    title: "Snow Removal"
                    pos_hint: {"top": 1}
                    elevation: 10
                    left_action_items: [['menu', lambda x: root.toggle_customer_nav_drawer()]]
                BoxLayout:
                    orientation: 'vertical'
                    pos_hint: {"center_x": .5, "center_y": .6}
                    size_hint: None, None
                    size: 500, 640
                    padding: 50
                    spacing: 0
                    GridLayout:
                        id: customer_details
                        cols: 1
                        spacing: 0
                        size_hint_y: None
                        height: self.minimum_height
                        AsyncImage:
                            id: customer_image
                            size_hint_y: None
                            height: 200  # Set the height to your desired value
                            width: 800   # Set the width to your desired value
                            allow_stretch: True
                            keep_ratio: True
                            canvas.before:
                                Rectangle:
                                    pos: self.pos
                                    size: self.size
                        MDLabel:
                            id: customer_name_label
                            text: 'Provider Name'
                            size_hint_y: None
                            height: 50
                            halign: 'center'
                            valign: 'middle'
                            bold: True  # Make the text bold
                            font_size: 24
                        MDLabel:
                            id: customer_email_label
                            text: 'Provider Email'
                            size_hint_y: None
                            height: 50
                            halign: 'center'
                            valign: 'middle'
                            bold: True  # Make the text bold
                            font_size: 24
                        MDLabel:
                            id: customer_phone_label
                            text: 'Provider Phone'
                            size_hint_y: None
                            height: 50
                            halign: 'center'
                            valign: 'middle'
                            bold: True  # Make the text bold
                            font_size: 24
                        MDLabel:
                            id: customer_address_label
                            text: 'Provider Address'
                            size_hint_y: None
                            height: 50
                            halign: 'center'
                            valign: 'middle'
                            bold: True  # Make the text bold
                            font_size: 24
        MDNavigationDrawer:
            id: customer_nav_drawer
            BoxLayout:
                orientation: 'vertical'
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: dp(8)
                    ScrollView:
                        MDList:
                            OneLineIconListItem:
                                text: 'Home'
                                on_release: app.switch_screen("dashboard_customer")
                                IconLeftWidget:
                                    icon: 'home'
                            OneLineIconListItem:
                                text: 'Profile'
                                on_release: app.switch_screen("customer_profile")
                                IconLeftWidget:
                                    icon: 'account'
                            OneLineIconListItem:
                                text: 'View Services'
                                on_release: app.switch_screen("customer_view_service")
                                IconLeftWidget:
                                    icon: 'eye'
                            OneLineIconListItem:
                                text: 'View Requests'
                                on_release: app.switch_screen("customer_view_request")
                                IconLeftWidget:
                                    icon: 'email'
                            OneLineIconListItem:
                                text: 'View History'
                                on_release: app.switch_screen("customer_view_history")
                                IconLeftWidget:
                                    icon: 'history'
                            OneLineIconListItem:
                                text: 'Logout'
                                on_release: root.logout()
                                IconLeftWidget:
                                    icon: 'logout'
<ViewCustomerServiceScreen>
    name: "customer_view_service"
    MDNavigationLayout:
        ScreenManager:
            CustomerHomeScreen:
                name: "customer_home_screen"
                MDTopAppBar:
                    title: "Snow Removal"
                    pos_hint: {"top": 1}
                    elevation: 10
                    left_action_items: [['menu', lambda x: root.toggle_customer_nav_drawer()]]
                BoxLayout:
                    orientation: 'vertical'
                    pos_hint: {'center_x': 0.4}
                    padding: 50  # Add padding to create a gap around the contents
                    spacing: 10
                    ScrollView:
                        GridLayout:
                            id: customer_service_cards_layout
                            cols: 2  # Set to 1 since we want one card per row
        MDNavigationDrawer:
            id: customer_nav_drawer
            BoxLayout:
                orientation: 'vertical'
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: dp(8)
                    ScrollView:
                        MDList:
                            OneLineIconListItem:
                                text: 'Home'
                                on_release: app.switch_screen("dashboard_customer")
                                IconLeftWidget:
                                    icon: 'home'
                            OneLineIconListItem:
                                text: 'Profile'
                                on_release: app.switch_screen("customer_profile")
                                IconLeftWidget:
                                    icon: 'account'
                            OneLineIconListItem:
                                text: 'View Services'
                                on_release: app.switch_screen("customer_view_service")
                                IconLeftWidget:
                                    icon: 'eye'
                            OneLineIconListItem:
                                text: 'View Requests'
                                on_release: app.switch_screen("customer_view_request")
                                IconLeftWidget:
                                    icon: 'email'
                            OneLineIconListItem:
                                text: 'View History'
                                on_release: app.switch_screen("customer_view_history")
                                IconLeftWidget:
                                    icon: 'history'
                            OneLineIconListItem:
                                text: 'Logout'
                                on_release: root.logout()
                                IconLeftWidget:
                                    icon: 'logout'
<CustomerServiceDetailScreen>
    name: "customer_service_detail_screen"
    BoxLayout:
        orientation: 'vertical'
        padding: 10  # Add padding to create a gap around the contents
        MDIconButton:
            icon: 'arrow-left'
            pos_hint: {'x': 0.02, 'top': 0.98}
            on_press: root.manager.current= 'customer_view_service'  # Replace with the actual screen name to go back to
        ScrollView:
            id: customer_service_details_scroll
            GridLayout:
                id: customer_service_details
                cols: 1
                height: self.minimum_height  # Add this line
                size_hint_y: None  # Add this line
                padding: 5  # Add this line
                spacing: 10  # Add this line
                AsyncImage:
                    id: customer_service_image
                    
<CustomerViewRequests>
    name: "customer_view_request"
    MDNavigationLayout:
        ScreenManager:
            CustomerHomeScreen:
                name: "customer_home_screen"
                MDTopAppBar:
                    title: "Snow Removal"
                    pos_hint: {"top": 1}
                    elevation: 10
                    left_action_items: [['menu', lambda x: root.toggle_customer_nav_drawer()]]
                BoxLayout:
                    orientation: 'vertical'
                    padding: 40  # Add padding to create a gap around the contents
                    ScrollView:
                        size_hint_y: None  # Disable automatic height adjustment based on content
                        height: 650  # Set the height to 300 pixels (adjust as needed)
                        GridLayout:
                            id: request_table_layout
                            cols: 1  # Set to 1 since we want one card per row
                            height: self.minimum_height  # Add this line
                            size_hint_y: None  # Add this line
                            padding: 5  # Add this line
                            spacing: 10  # Add this line
        MDNavigationDrawer:
            id: customer_nav_drawer
            BoxLayout:
                orientation: 'vertical'
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: dp(8)
                    ScrollView:
                        MDList:
                            OneLineIconListItem:
                                text: 'Home'
                                on_release: app.switch_screen("dashboard_customer")
                                IconLeftWidget:
                                    icon: 'home'
                            OneLineIconListItem:
                                text: 'Profile'
                                on_release: app.switch_screen("customer_profile")
                                IconLeftWidget:
                                    icon: 'account'
                            OneLineIconListItem:
                                text: 'View Services'
                                on_release: app.switch_screen("customer_view_service")
                                IconLeftWidget:
                                    icon: 'eye'
                            OneLineIconListItem:
                                text: 'View Requests'
                                on_release: app.switch_screen("customer_view_request")
                                IconLeftWidget:
                                    icon: 'email'
                            OneLineIconListItem:
                                text: 'View History'
                                on_release: app.switch_screen("customer_view_history")
                                IconLeftWidget:
                                    icon: 'history'
                            OneLineIconListItem:
                                text: 'Logout'
                                on_release: root.logout()
                                IconLeftWidget:
                                    icon: 'logout'
<CustomerViewHistory>
    name: "customer_view_history"
    MDNavigationLayout:
        ScreenManager:
            CustomerHomeScreen:
                name: "customer_home_screen"
                MDTopAppBar:
                    title: "Snow Removal"
                    pos_hint: {"top": 1}
                    elevation: 10
                    left_action_items: [['menu', lambda x: root.toggle_customer_nav_drawer()]]
                BoxLayout:
                    orientation: 'vertical'
                    padding: 40  # Add padding to create a gap around the contents
                    ScrollView:
                        size_hint_y: None  # Disable automatic height adjustment based on content
                        height: 650  # Set the height to 300 pixels (adjust as needed)
                        GridLayout:
                            id: history_table_layout
                            cols: 1  # Set to 1 since we want one card per row
                            height: self.minimum_height  # Add this line
                            size_hint_y: None  # Add this line
                            padding: 5  # Add this line
                            spacing: 10  # Add this line
        MDNavigationDrawer:
            id: customer_nav_drawer
            BoxLayout:
                orientation: 'vertical'
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: dp(8)
                    ScrollView:
                        MDList:
                            OneLineIconListItem:
                                text: 'Home'
                                on_release: app.switch_screen("dashboard_customer")
                                IconLeftWidget:
                                    icon: 'home'
                            OneLineIconListItem:
                                text: 'Profile'
                                on_release: app.switch_screen("customer_profile")
                                IconLeftWidget:
                                    icon: 'account'
                            OneLineIconListItem:
                                text: 'View Services'
                                on_release: app.switch_screen("customer_view_service")
                                IconLeftWidget:
                                    icon: 'eye'
                            OneLineIconListItem:
                                text: 'View Requests'
                                on_release: app.switch_screen("customer_view_request")
                                IconLeftWidget:
                                    icon: 'email'
                            OneLineIconListItem:
                                text: 'View History'
                                on_release: app.switch_screen("customer_view_history")
                                IconLeftWidget:
                                    icon: 'history'
                            OneLineIconListItem:
                                text: 'Logout'
                                on_release: root.logout()
                                IconLeftWidget:
                                    icon: 'logout'
<ProviderViewRequests>
    name: "provider_view_request"
    MDNavigationLayout:
        ScreenManager:
            ProviderHomeScreen:
                name: "provider_home_screen"
                MDTopAppBar:
                    title: "Snow Removal"
                    pos_hint: {"top": 1}
                    elevation: 10
                    left_action_items: [['menu', lambda x: root.toggle_nav_drawer()]]
                BoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    pos_hint: {'center_x': 0.5, 'center_y': 0.8}  # Center both horizontally and vertically
                    MDIconButton:
                        icon: "calendar"
                        md_bg_color: 0, 0, 0, 0  # Set a transparent background color
                        on_release: root.show_date_picker_search()
                    MDTextField:
                        id: date_field
                        hint_text: "Selected Date"
                        size_hint_x: None
                        width: "250dp"
                        readonly: True
                    MDRoundFlatButton:
                        text: "Search"
                        size: dp(100), dp(40)  # Adjust the size as needed
                        on_press: root.perform_search()
                BoxLayout:
                    orientation: 'vertical'
                    spacing: dp(50)
                    padding: dp(20)
                    pos_hint: {'center_x': 0.5, 'center_y': 0.3}  # Center both horizontally and vertically
                    ScrollView:
                        GridLayout:
                            id: provider_request_table_layout
                            cols: 1
                            spacing: 0
                            size_hint_y: None
                            height: self.minimum_height
                            padding: 5  # Add this line
                            spacing: 10  # Add this line
        MDNavigationDrawer:
            id: provider_nav_drawer
            BoxLayout:
                orientation: 'vertical'
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: dp(8)
                    ScrollView:
                        MDList:
                            OneLineIconListItem:
                                text: 'Home'
                                on_release: app.switch_screen("dashboard_provider")
                                IconLeftWidget:
                                    icon: 'home'
                            OneLineIconListItem:
                                text: 'Profile'
                                on_release: app.switch_screen("provider_profile")
                                IconLeftWidget:
                                    icon: 'account'
                            OneLineIconListItem:
                                text: 'Add Services'
                                on_release: app.switch_screen("add_service")
                                IconLeftWidget:
                                    icon: 'plus'
                            OneLineIconListItem:
                                text: 'View Services'
                                on_release: app.switch_screen("view_service")
                                IconLeftWidget:
                                    icon: 'eye'
                            OneLineIconListItem:
                                text: 'View Requests'
                                on_release: app.switch_screen("provider_view_request")
                                IconLeftWidget:
                                    icon: 'email'
                            OneLineIconListItem:
                                text: 'View History'
                                on_release: app.switch_screen("provider_view_history")
                                IconLeftWidget:
                                    icon: 'history'
                            OneLineIconListItem:
                                text: 'Logout'
                                on_release: root.logout()
                                IconLeftWidget:
                                    icon: 'logout'
                                    
<ProviderViewHistory>
    name: "provider_view_history"
    MDNavigationLayout:
        ScreenManager:
            ProviderHomeScreen:
                name: "provider_home_screen"
                MDTopAppBar:
                    title: "Snow Removal"
                    pos_hint: {"top": 1}
                    elevation: 10
                    left_action_items: [['menu', lambda x: root.toggle_nav_drawer()]]
                BoxLayout:
                    orientation: 'vertical'
                    padding: 40  # Add padding to create a gap around the contents
                    ScrollView:
                        size_hint_y: None  # Disable automatic height adjustment based on content
                        height: 650  # Set the height to 300 pixels (adjust as needed)
                        GridLayout:
                            id: provider_history_table_layout
                            cols: 1  # Set to 1 since we want one card per row
                            height: self.minimum_height  # Add this line
                            size_hint_y: None  # Add this line
                            padding: 5  # Add this line
                            spacing: 10  # Add this line
        MDNavigationDrawer:
            id: provider_nav_drawer
            BoxLayout:
                orientation: 'vertical'
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: dp(8)
                    ScrollView:
                        MDList:
                            OneLineIconListItem:
                                text: 'Home'
                                on_release: app.switch_screen("dashboard_provider")
                                IconLeftWidget:
                                    icon: 'home'
                            OneLineIconListItem:
                                text: 'Profile'
                                on_release: app.switch_screen("provider_profile")
                                IconLeftWidget:
                                    icon: 'account'
                            OneLineIconListItem:
                                text: 'Add Services'
                                on_release: app.switch_screen("add_service")
                                IconLeftWidget:
                                    icon: 'plus'
                            OneLineIconListItem:
                                text: 'View Services'
                                on_release: app.switch_screen("view_service")
                                IconLeftWidget:
                                    icon: 'eye'
                            OneLineIconListItem:
                                text: 'View Requests'
                                on_release: app.switch_screen("provider_view_request")
                                IconLeftWidget:
                                    icon: 'email'
                            OneLineIconListItem:
                                text: 'View History'
                                on_release: app.switch_screen("provider_view_history")
                                IconLeftWidget:
                                    icon: 'history'
                            OneLineIconListItem:
                                text: 'Logout'
                                on_release: root.logout()
                                IconLeftWidget:
                                    icon: 'logout'
<CardDetailsScreen>
    name: 'carddetails'
    BoxLayout:
        orientation: 'vertical'
        id : card_details
        padding: 10
        spacing: 20  # Adjust the spacing between widgets
        pos_hint: {"center_x":.5,"center_y":.6}

<FullCardDetailsScreen>
    name: 'fullcarddetails'
    BoxLayout:
        orientation: 'vertical'
        id : full_card_details
        padding: 10
        spacing: 20  # Adjust the spacing between widgets
        pos_hint: {"center_x":.5,"center_y":.6}
    
<CustomerViewFullPaymentScreen>
    name: 'customer_view_full_payment'
    BoxLayout:
        orientation: 'vertical'
        id : view_full_payment
        padding: 5
        pos_hint: {"center_x":.5,"center_y":.7}
            
<CustomerRaiseComplaintsScreen>
    name: 'customer_raise_complaint'
    BoxLayout:
        orientation: 'vertical'
        id : complaints
        padding: 5
        pos_hint: {"center_x":.5,"center_y":.7}

<ProviderViewPaymentsScreen>
    BoxLayout:
        orientation: 'vertical'
        padding: 50  # Add padding to create a gap around the contents
        ScrollView:
            GridLayout:
                id: provider_view_payment_screen
                cols: 4  # Set to 1 since we want one card per row
                spacing: 20  # Add spacing between the cards
        MDRoundFlatButton:
            text: "Go Back"
            pos_hint: {"center_x": .5}
            font_size: 20
            on_press: root.manager.current='provider_view_history'
            
<ViewServiceProviderComplaintsScreen>
    BoxLayout:
        orientation: 'vertical'
        padding: 50  # Add padding to create a gap around the contents
        ScrollView:
            GridLayout:
                id: view_provider_my_complaints_screen
                cols: 4  # Set to 1 since we want one card per row
                spacing: 20  # Add spacing between the cards
        MDRoundFlatButton:
            text: "Go Back"
            pos_hint: {"center_x": .5}
            font_size: 20
            on_press: root.manager.current='provider_view_history'
            
<ViewComplaintsScreen>
    BoxLayout:
        orientation: 'vertical'
        padding: 50  # Add padding to create a gap around the contents
        ScrollView:
            GridLayout:
                id: view_complaints_screen
                cols: 4  # Set to 1 since we want one card per row
                spacing: 20  # Add spacing between the cards

<ReviewRatingScreen>
    name: 'reviewrating'
    BoxLayout:
        orientation: 'vertical'
        id : review_rating
        pos_hint: {"center_x": .5, "center_y": .7}


"""