# Store-Data-ETL


#Now I have an automation program to list thousands of products for me and a new website that still does not yet have any products. To solve this problem, rather than build another automation for the website, I decided to build an ETL pipeline to transfer the product data into my website, which from my perspective, is the most achievable and efficient way. 

#My website was built with Shopify, and a very good thing is that it comes with product import functions that allow me to upload batches of products all at once by a single CSV file.

#So the plan is to build a scraper that runs through all my product on Grailed and extract the selected data into the CSV file, and repeat, pretty straightforward.

#This program is also implemented by python and major packages like Selenium web driver for automation and Pandas for data transformation. 
