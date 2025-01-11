def get_data(neo_type, neo_category):
    if neo_type not in ['wishlist', 'progress', 'complete']:
        raise ValueError('Invalid type parameter. Must be wishlist, progress, or complete')
    if neo_category not in ['book', 'movie', 'tv', 'music', 'game', 'podcast']:
        raise ValueError('Invalid category parameter. Must be book, movie, tv, music, game, or podcast')
    
    url = f'https://neodb.social/api/me/shelf/{neo_type}?category={neo_category}'
    headers = {'Authorization': 'Bearer ' + os.environ.get('AUTHORIZATION'), 'Accept': 'application/json'}
    response = requests.get(url, headers=headers)
    json_data = json.loads(response.text)
    pages_value = json_data['pages']
    
    all_results = []
    for page_num in range(1, pages_value+1):
        requests_path = f'{url}&page={page_num}'
        r = requests.get(requests_path, headers=headers)
        result = r.json()
        all_results.extend(result['data'])
    
    # 替换 cover_image_url 中的域名
    for item in all_results:
        if 'cover_image_url' in item:
            item['cover_image_url'] = item['cover_image_url'].replace('https://neodb.social', 'https://neodb.prvcy.page')
    
    return all_results
