import re

def parse_listing(soup):
    shared_line_bubble = soup.find_all('span', class_='shared-line-bubble')
    bedbath = shared_line_bubble[0].text.split('/')
    sqft = shared_line_bubble[1].text
    details = soup.find_all('p', class_='attrgroup')[-1]
    detail_list = []
    for detail in details:
        detail_list.append(detail.text)
    num_images = len(soup.find('div', id='thumbs').find_all('a'))
    word_count = len(re.split('[ \n]', soup.find('section', id='postingbody').text.strip()))
    typeof, laundry, parking, cats, dogs, furnished, nosmoke, wheelchair = detail_extraction(detail_list)

    listing_details = {
        # 'link': url,
        'bed': bedbath[0],
        'bath': bedbath[1],  # TODO Check for shared or split bathroom listing
        'sqft': sqft,
        'type': typeof,
        'lanudry': laundry,
        'parking': parking,
        'cats': cats,
        'dogs': dogs,
        'furnished': furnished,
        'nosmoke': nosmoke,
        'wheelchair': wheelchair,
        'img': num_images,
        'words': word_count
    }

    return listing_details


def detail_extraction(detail_list):
    # typeof, laundry, parking, cats, dogs, furnished, nosmoke, wheelchair
    parsed_details = [0, 0, 0, 0, 0, 0, 0, 0]
    for detail in detail_list:
        if 'cats' in detail:
            parsed_details[3] = 1
        elif 'dogs' in detail:
            parsed_details[4] = 1
        elif 'furnished' in detail:
            parsed_details[5] = 1
        elif 'no smoking' in detail:
            parsed_details[6] = 1
        elif 'wheelchair' in detail:
            parsed_details[7] = 1
        elif 'w/d' in detail or 'laundry' in detail:
            # TODO handle laundry
            pass
        elif 'parking' in detail or 'car' in detail or 'garage' in detail:
            # TODO handle parking
            pass
        else:  # defaults to housing type
            # TODO handle housing type
            pass
    return parsed_details
