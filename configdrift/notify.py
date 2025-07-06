import platform

def notify_user(message):
    os_name = platform.system().lower()
    if os_name == 'windows':
        try:
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast("ConfigDrift", message, duration=5)
        except ImportError:
            print("[Notification]", message)
    elif os_name == 'linux':
        try:
            import notify2
            notify2.init('ConfigDrift')
            n = notify2.Notification('ConfigDrift', message)
            n.show()
        except ImportError:
            print("[Notification]", message)
    elif os_name == 'darwin':
        import os
        os.system(f"osascript -e 'display notification \"{message}\" with title \"ConfigDrift\"'")
    else:
        print("[Notification]", message)

def print_email_instructions():
    print("To enable email notifications, configure your SMTP settings in a config file. (Feature coming soon)") 