import re
import logging


def parse_listing(soup):
    logging.debug('parse_listing(soup)')
    shared_line_bubble = soup.find_all('span', class_='shared-line-bubble')

    # logging.debug(shared_line_bubble)
    bedbath = shared_line_bubble[0].text.split('/')
    sqft = shared_line_bubble[1].text
    details = soup.find_all('p', class_='attrgroup')[-1].find_all('span')
    logging.debug(details)
    detail_list = []
    for detail in details:
        detail_list.append(detail.text)

    logging.debug(detail_list)

    num_images = len(soup.find('div', id='thumbs').find_all('a'))
    word_count = len(re.split('[ \n]', soup.find('section', id='postingbody').text.strip()))
    typeof, laundry, parking, cats, dogs, furnished, nosmoke, wheelchair = detail_extraction(detail_list)

    logging.debug(typeof)

    listing_details = {
        # 'link': url,
        'bed': bedbath[0],
        'bath': bedbath[1],
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

    logging.debug(listing_details)

    return listing_details


def detail_extraction(detail_list):
    logging.debug('detail_extraction(detail_list)')
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
        # region laundry
        elif 'w/d' in detail or 'laundry' in detail:
            # Laundry numbers assigned in rank of desirability, with w/d in unit being most desirable
            # 1 - no laundry
            # laundry on site
            # w/d hookup
            # loundry in building
            # 5 - w/d in unit

            num = 1
            if 'laundry' in detail:
                if 'bldg' in detail:
                    num = 4
                elif 'site' in detail:
                    num = 2
                # else no laundry on site, num = 1
            if 'w/d' in detail:
                if 'hook' in detail:
                    num = 3
                else:
                    num = 5
            parsed_details[1] = num
        # endregion laundry
        # region parking
        elif 'parking' in detail or 'car' in detail or 'garage' in detail:
            # Slightly less efficient because of rechecking the same condition, but cleaner code than splitting into
            # three if-blocks?
            # Parking numbers assigned in rank of desirability, with 7 being greatest
            # 1 - no parking
            # off-street parking
            # street parking
            # carport
            # detached garage
            # attached garage
            # 7 - valet parking
            num = 1
            if 'garage' in detail:
                if 'detached' in detail:
                    num = 5
                else:
                    num = 6  # default to attached garage
            if 'parking' in detail:
                if 'street' in detail:
                    if 'off' in detail:
                        num = 2
                    else:
                        num = 3
                if 'valet' in detail:
                    num = 7
                # else no parking num = 1
            if 'car' in detail:
                num = 4
            parsed_details[2] = num
        # endregion
        else:  # defaults to housing type
            parsed_details[0] = detail
            # parsing out of housing type will be handled later
    return parsed_details
