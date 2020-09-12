import pandas as pd
from urllib.request import urlopen
import re
from p_tqdm import p_map # very convenient multiprocessing, automatically uses all cpus
import os

letters=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','#'] # Apple pages

# scrape links to the individual app pages (this yielded ~27000 links)
def get_app_links():
    app_links = []
    for letter in letters:
        for page in range(1,10): # take the first 9 pages for each letter
            try:
                a = urlopen(f'https://apps.apple.com/us/genre/ios-games/id6014?letter={letter}&page={page}#page') # based on apps.apple.com structure
                g = a.read()
                links = re.findall('https://apps.apple.com/us/app/[a-zA-Z0-9-]+/id\d+',g.decode('utf-8'))
                app_links = app_links + links
            except e:
                app_link.append(f'could not find links for letter {letter} page {page}')
    return app_links

# to get information for one link, with error handling to make sure the data scraped is clean
def get_app_data_one_link(link):
    try:
        b=urlopen(link)
        content = b.read().decode('utf-8')
        name = re.split('"name":"',content)[1].split('"')[0]
        description = re.split('"description":"',content)[1].split('"')[0]
        image = re.split('<meta name="twitter:image" content="',content)[1].split('"')[0]
        category = re.split('"applicationCategory":"',content)[1].split('"')[0]
        datePublished = re.split('"datePublished":"',content)[1].split('"')[0]
        num_ratings = re.split(',"reviewCount":',content)[1].split('}')[0]
        avg_rating = re.split(',"ratingValue":',content)[1].split(',')[0]

        datum={"name":name,"description":description,"image":image,"category":category,"datePublished":datePublished,"avg_rating":avg_rating,"num_ratings":num_ratings}
        return datum
    except:
        datum={"name":"","description":"","image":"","category":"","datePublished":"","avg_rating":"","num_ratings":""}
        return datum

# to get all at once -- too slow
def get_app_data(links):
    app_data = []
    for link in links:
        try:
            b=urlopen(link)
            content = b.read().decode('utf-8')
            name = re.split('"name":"',content)[1].split('"')[0]
            description = re.split('"description":"',content)[1].split('"')[0]
            image = re.split('<meta name="twitter:image" content="',content)[1].split('"')[0]
            category = re.split('"applicationCategory":"',content)[1].split('"')[0]
            datePublished = re.split('"datePublished":"',content)[1].split('"')[0]
            num_ratings = re.split(',"reviewCount":',content)[1].split('}')[0]
            avg_rating = re.split(',"ratingValue":',content)[1].split(',')[0]
              
            app_data.append({"name":name,"description":description,"image":image,"category":category,"datePublished":datePublished,"avg_rating":avg_rating,"num_ratings":num_ratings})
        except:
            app_data.append({"name":name,"description":description,"image":image,"category":category,"datePublished":datePublished,"avg_rating":"could not scrape","num_ratings":num_ratings})
    return pd.DataFrame(app_data)
    
if __name__=='__main__':
    
    print('getting links')
    links = get_app_links()
    pd.Series(links).to_csv('app_links.csv')
    print(f'found {len([link for link in links if "could not find" not in link ])} links') # 27147
    
    # process batches of 1000 at a time so that we don't have to start again if any errors occur
    for i in range(0,27000,1000):
        data = p_map(get_app_data_one_link, links[i:i+1000])
        app_df = pd.DataFrame(data)
        app_df.to_csv(f'app_data_{i}_to_{i+1000}.csv')
    
    # get the remaining above 27000
    data = p_map(get_app_data_one_link, links[27000:])
    app_df = pd.DataFrame(data)
    app_df.to_csv(f'app_data_27000_to_end.csv')  
    
    app_data = pd.DataFrame()
    for output in os.listdir(r'C:\Users\bwaddell\Downloads\AppData'): # get all batch files
        if output.endswith('.csv'):
            temp_df = pd.read_csv((r'C:\Users\bwaddell\Downloads\AppData\\'+output)
            app_data = pd.concat([app_data,temp_df],ignore_index=True,axis=0) #concatenate all batch files together
            
    app_data.drop_duplicates(inplace=True,ignore_index=True)        
    app_data.to_csv('app_data.csv')
    
    