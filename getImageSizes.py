#!/bin/py
# import gspread

# import math

# from oauth2client.service_account import ServiceAccountCredentials
#
# scope = ['https://spreadsheets.google.com/feeds',
# 'https://www.googleapis.com/auth/drive']
import requests
import csv
import humanfriendly
import json

def get_urls(page):
    url = "http://staging.clearcom.com/wp-json/wp/v2/media"
    querystring = {"page": page,"per_page": 100,"key":"AIzaSyCnSv6GsxFnfBPNwk57CfNQFj7IrTephZs","orderby":"id","order":"asc"}
    response = requests.request("GET", url, params=querystring)
    total_pages = response.headers['X-WP-TotalPages']
    attachments = []
    for r in response.json():
        media = {
            'id': r["id"],
            'slug': r["slug"],
            'url': r["guid"]["rendered"] if r["guid"]["rendered"] else r["link"] ,
            'size': 0
        }
        attachments.append(media)
    return attachments, int(total_pages)

def main():
    print("Retrieving URLS")
    page = 59
    attachments, total_pages = get_urls(page)
    x = 0 #index
    num_of_media = len(attachments)
    print("number_of_media %d" % num_of_media)
    print("total pages %d" % total_pages)
    with open("imageSizes.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "slug", "url", "size"])
        while( num_of_media > 0 ):
            print("number_of_media %d" % num_of_media)
            print("Writing attachement with id: %d " % attachments[x]["id"])
            print("Writing attachement with slug: %s " % attachments[x]["slug"])
            print("Writing attachement with url: %s " % attachments[x]["url"])

            try:
                response = requests.request("GET", attachments[x]["url"])
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                print e
                print("could not fetch %d" % attachments[x]["id"])
                if( num_of_media == 1):
                    page += 1
                    print("Updating to page: %d" % page)
                    if(page >= total_pages):
                        num_of_media = 0
                    else:
                        attachments, total_pages  = get_urls(page)
                        num_of_media = len(attachments)
                        print("num_of_media: %d" % num_of_media)

                    x = 0
                else:
                    x += 1
                    num_of_media -= 1

            if response.status_code == 200 :
                attachments[x]["size"] = int(response.headers["Content-Length"]) if response.headers["Content-Length"] else "NULL"
                print("Writing attachement with size: %s " % humanfriendly.format_size(attachments[x]["size"]))
                writer.writerow([attachments[x]["id"], attachments[x]["slug"], attachments[x]["url"], humanfriendly.format_size(attachments[x]["size"])])
                if( num_of_media == 1):
                    page += 1
                    print("Updating to page: %d" % page)
                    if(page >= total_pages):
                        num_of_media = 0
                    else:
                        attachments, total_pages  = get_urls(page)
                        num_of_media = len(attachments)
                        print("num_of_media: %d" % num_of_media)

                    x = 0
                else:
                    x += 1
                    num_of_media -= 1
            else:
                print("could not fetch %d" % attachments[x]["id"])
                if( num_of_media == 1):
                    page += 1
                    print("Updating to page: %d" % page)
                    if(page >= total_pages):
                        num_of_media = 0
                    else:
                        attachments, total_pages  = get_urls(page)
                        num_of_media = len(attachments)
                        print("num_of_media: %d" % num_of_media)

                    x = 0
                else:
                    x += 1
                    num_of_media -= 1


# last page was 21
# last id was 5215

    # credentials = ServiceAccountCredentials.from_json_keyfile_name("spreadsheet-api-clearcom.json", scope)
    # gc = gspread.authorize(credentials)
    # sheet = gc.open_by_key("1N-sLTnNMyCl5ZQyFHrKU6j09Cd2r4EplewcFnkG5O8U").sheet1
    # urls = sheet.col_values(3)

    # with open("imageSizes.csv", "w") as file:
    #     writer = csv.writer(file)
    #     writer.writerow(["url","size"])
    #     for url in urls:
    #         response = requests.get(url)
    #         if (response.status_code == 200) and ("Content-Length" in response.headers):
    #             #convert each size into kb or mb or gb
    #             bytes = humanfriendly.format_size(int(response.headers["Content-Length"]))
    #             print(url + ", " +  bytes)
    #             writer.writerow([url, bytes])
    #         else:
    #             print(url + " did not get successfully")
    #             print(response.headers)
    # return

if "__main__" == __name__:
    main()
