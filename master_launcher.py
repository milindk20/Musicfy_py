import os
import sys
import platform

def main():
    if platform.system() == "Windows":
        os.system("python Windows/app_combined.py")
    elif platform.system() == "Linux":
        os.system("python Linux/app_combined.py")
    else:
        print("Unsupported operating system. Please run this script on Windows or Linux.")

if __name__ == "__main__":
    main()