from django.core.management.base import BaseCommand
from apps.products.models import Product
from apps.transactions.models import Transaction

class Command(BaseCommand):
    help = '释放所有被锁定的商品'

    def handle(self, *args, **options):
        self.stdout.write('=' * 50)
        self.stdout.write('正在释放所有被锁定的商品...')
        self.stdout.write('=' * 50)
        
        # 统计
        locked_count = Product.objects.filter(status='locked').count()
        pending_count = Transaction.objects.filter(status='pending').count()
        
        self.stdout.write(f'\n找到 {locked_count} 个被锁定的商品')
        self.stdout.write(f'找到 {pending_count} 个待付款交易')
        
        # 更新
        product_updated = Product.objects.filter(status='locked').update(status='available')
        transaction_updated = Transaction.objects.filter(status='pending').update(status='expired')
        
        self.stdout.write(f'\n成功释放 {product_updated} 个商品')
        self.stdout.write(f'已过期 {transaction_updated} 个待付款交易')
        
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write('所有被锁定的商品已释放完毕！')
        self.stdout.write('=' * 50)
