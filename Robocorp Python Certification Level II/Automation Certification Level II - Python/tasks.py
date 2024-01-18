from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.Excel.Files import Files
from RPA.PDF import PDF
from RPA.Tables import Tables
import time
import os
import shutil

@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    """browser.configure(
        slowmo=500,
    )"""
    open_site()
    download_csv()
    get_orders()
    archive_receipts()
    log_out()

def open_site():

    """Navigates to the given URL"""
    browser.goto("https://robotsparebinindustries.com/#/robot-order/")

def download_csv():
    """Download orders file and read  it as a table"""
    http = HTTP()
    http.download(url=" https://robotsparebinindustries.com/orders.csv", overwrite=True)

def get_orders():
    """Read all values from the .csv table"""
    library = Tables()
    orders = library.read_table_from_csv(
        "orders.csv", columns=["Order number", "Head", "Body", "Legs", "Address"]
    )

    for rows in orders:
        fill_the_form(rows)
            
def close_the_annoying_modal():
    page=browser.page()
    page.click("button:text('OK')")

def fill_the_form(values):
    """fill out the form with the data  from the excel sheet"""

    page = browser.page()
    close_the_annoying_modal()

    radio = str(values["Body"])
    page.select_option("#head", str(values["Head"]))
    page.click(f'//input[@type="radio" and @value="{radio}"]')
    page.fill('//input[@class="form-control"]', str(values["Legs"]))
    page.fill("#address", str(values["Address"]))
    page.click("button:text('ORDER')")
    if page.locator('//div[contains(@id, "receipt")]').count() > 0:
        screenshot_robot(str(values["Order number"]))
        store_receipt_as_pdf(str(values["Order number"]))
    while page.locator('//div[contains(@role, "alert")]').count() > 0:
            if page.locator('//button[contains(@id, "order")]').count() > 0:
                page.click("button:text('ORDER')")
            if page.locator('//div[contains(@id, "receipt")]').count() > 0:
                 screenshot_robot(str(values["Order number"]))
                 store_receipt_as_pdf(str(values["Order number"]))
    embed_screenshot_to_receipt("output/receipts/"+str(values["Order number"])+".png", "output/receipts/"+str(values["Order number"])+".pdf")
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, "output/receipts/"+str(values["Order number"])+".png")
    os.remove(file_path)
                 
def store_receipt_as_pdf(order_number):
    page = browser.page()
    sales_results_html = page.locator('//div[contains(@id, "receipt")]').inner_html()

    pdf = PDF()
    pdf.html_to_pdf(sales_results_html, "output/receipts/"+order_number+".pdf")

def screenshot_robot(order_number):
    page = browser.page()
    page.screenshot(path="output/receipts/"+order_number+".png")

def embed_screenshot_to_receipt(screenshot, pdf_file):
    print(screenshot)
    print(pdf_file)
    pdf = PDF()

    list_of_files = [pdf_file, screenshot]
    pdf.add_files_to_pdf(files=list_of_files,target_document=pdf_file)

def archive_receipts():
    current_directory = os.getcwd()
    modified_directory = str(current_directory).replace("\\", "/")
    folder_to_zip = modified_directory + '/output/receipts'
    output_zip_path = modified_directory + '/output/Archived.zip'

    # Create a ZIP archive of the specified folder
    shutil.make_archive(output_zip_path, 'zip', folder_to_zip)

def log_out():
    """Presses the 'Log out' button"""
    page = browser.page()  
    page.close()



   

    




    

