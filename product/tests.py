from django.test import TestCase
from rest_framework.test import APIRequestFactory, APITestCase
from user.models import CustomUserManager, User
from .views import *
from .models import Product
from category.models import Category, Subcategory
from user.views import LoginView

# Create your tests here.
class ProductTest(APITestCase):
    def setUp_user(self):
        
        return User.objects.create_superuser(email='bilal@gmail.com', password='1') 

    
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.user = self.setUp_user()
        self.token = self.setUp_user_token()
        self.setUp_category()
        self.setUp_product()
    
    def setUp_user_token(self):
        data = {
            "email": "bilal@gmail.com",
            "password": "1" 
        }
        request = self.factory.post('account/login/', data) 
        view = LoginView.as_view() 
        response = view(request) 
        return response.data['access']  
    

    def setUp_category(self):
        Category.objects.create(title='dress', slug='dress') 
    def setUp_subcategory(self):
        Subcategory.objects.create(title='subcategory1', category=Category.objects.first(), slug='subcategory1') 
        

    def setUp_product(self):
        self.setUp_category()
        self.setUp_subcategory()
        products = [
            Product(
                owner=self.user, 
                category=Category.objects.first(),
                subcategory=Subcategory.objects.first(), 
                title='title1', 
                price=10.0, 
                quantity=10
                ),
            # Product(owner=self.user, category=Category.objects.first(),subcategory=Subcategory.objects.first(), title='title2', price=10.0),
            # Product(owner=self.user, category=Category.objects.first(),subcategory=Subcategory.objects.first(), title='title3', price=10.0)
        ]
        data = Product.objects.bulk_create(products)
        print(data)
    def test_get_product(self):
        request = self.factory.get('product/') 
        view = ProductViewSet.as_view({'get':'list'})
        response = view(request) 
        
        assert response.status_code == 200 

    def test_product_product(self):
        # image = open('/home/bilalmametov17/hacaton_bilal/hackaton_dordoi_place/product_images/Samurai_woman_1920x1080.jpeg', 'rb')

        data = {
            'owner': self.user.pk,
            'category':Category.objects.first().pk,
            'subcategory':Subcategory.objects.first().pk,
            'title':'test_post',
            # 'image':image, 
            'price': 10.0,
            'quantity':10,
        }
        request = self.factory.post('product/', data, HTTP_AUTHORIZATION='Bearer '+self.token)
        # image.close()
        view = ProductViewSet.as_view({'get': 'list'})
        view = ProductViewSet.as_view({'post':'create'}) 
        response = view(request)
        print(response.data)
        assert response.status_code == 201
        assert response.data['owner'] == self.user.email

# test = ProductTest()
# test.setUp_user()
# test.setUp_category()
# test.setUp_subcategory()