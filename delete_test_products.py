import requests

# 删除测试上架的商品
def delete_test_products():
    print('=' * 80)
    print('删除测试商品')
    print('=' * 80)
    
    # 1. 登录获取token
    print('\n1. 登录获取token...')
    login_data = {
        'student_id': '20240001',
        'password': 'Test1234'
    }
    
    login_response = requests.post('http://localhost:8000/api/v1/users/login/', json=login_data)
    print(f'登录状态码: {login_response.status_code}')
    
    if login_response.status_code != 200:
        print('登录失败')
        return
    
    token = login_response.json().get('data', {}).get('access')
    if not token:
        print('获取token失败')
        return
    
    print('登录成功')
    
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    # 2. 获取所有商品
    print('\n2. 获取所有商品...')
    list_response = requests.get('http://localhost:8000/api/v1/products/')
    if list_response.status_code != 200:
        print('获取商品列表失败')
        return
    
    products = list_response.json().get('data', [])
    print(f'总商品数: {len(products)}')
    
    # 3. 识别并删除测试商品
    print('\n3. 识别测试商品...')
    test_products = []
    
    for product in products:
        title = product.get('title', '')
        if '测试' in title or 'Test' in title:
            test_products.append(product)
            print(f'  测试商品: ID={product.get("id")}, Title={title}')
    
    if not test_products:
        print('未找到测试商品')
        return
    
    # 4. 删除测试商品
    print(f'\n4. 删除 {len(test_products)} 个测试商品...')
    
    for product in test_products:
        product_id = product.get('id')
        if product_id:
            # 使用下架接口
            delete_response = requests.post(f'http://localhost:8000/api/v1/products/{product_id}/take_down/', headers=headers)
            print(f'  商品ID={product_id}: 状态码={delete_response.status_code}')
            if delete_response.status_code == 200:
                print(f'    ✓ 下架成功')
            else:
                print(f'    ✗ 下架失败: {delete_response.json()}')
    
    # 5. 验证删除结果
    print('\n5. 验证删除结果...')
    list_response = requests.get('http://localhost:8000/api/v1/products/')
    if list_response.status_code == 200:
        remaining_products = list_response.json().get('data', [])
        print(f'删除后商品数: {len(remaining_products)}')
        
        remaining_test_products = [p for p in remaining_products if '测试' in p.get('title', '') or 'Test' in p.get('title', '')]
        if remaining_test_products:
            print('仍有测试商品存在:')
            for p in remaining_test_products:
                print(f'  ID={p.get("id")}, Title={p.get("title")}')
        else:
            print('✓ 所有测试商品已成功删除')
    
    print('\n' + '=' * 80)
    print('删除完成')
    print('=' * 80)

if __name__ == '__main__':
    delete_test_products()
