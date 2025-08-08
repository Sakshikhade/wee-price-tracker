# scripts/firebase_manager.py
from firebase_admin import firestore
from datetime import datetime
import logging
from decimal import Decimal
import os
import json
from dotenv import load_dotenv

# Import Firebase config
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.firebase_config import db

load_dotenv()

class FirebaseManager:
    def __init__(self):
        self.db = db
        self.logger = logging.getLogger(__name__)
        
        if not self.db:
            raise Exception("Firebase not initialized")
    
    def save_product(self, product_data):
        """Save or update product information"""
        try:
            # Check if product exists
            products_ref = self.db.collection('products')
            query = products_ref.where('productName', '==', product_data['name'])
            docs = query.stream()
            
            product_doc = None
            for doc in docs:
                product_doc = doc
                break
            
            if product_doc:
                # Update existing product
                product_doc.reference.update({
                    'category': product_data.get('category'),
                    'updatedAt': datetime.now()
                })
                return product_doc.id
            else:
                # Create new product
                doc_ref = products_ref.add({
                    'productName': product_data['name'],
                    'brand': product_data.get('brand'),
                    'category': product_data.get('category'),
                    'unitSize': product_data.get('unit_size'),
                    'createdAt': datetime.now(),
                    'updatedAt': datetime.now(),
                    'enabled': True,
                    'priority': 1
                })
                return doc_ref[1].id
                
        except Exception as e:
            self.logger.error(f"Error saving product: {e}")
            return None
    
    def save_price_record(self, product_id, price_data):
        """Save price record to Firestore"""
        try:
            price_history_ref = self.db.collection('priceHistory')
            doc_ref = price_history_ref.add({
                'productId': product_id,
                'price': float(price_data['price']) if price_data['price'] else None,
                'priceStr': price_data['price_str'],
                'unitPrice': float(price_data.get('unit_price')) if price_data.get('unit_price') else None,
                'unitPriceStr': price_data.get('unit_price_str', ''),
                'sourceUrl': price_data.get('source_url'),
                'sourceSelector': price_data.get('source_selector'),
                'scrapedAt': datetime.now(),
                'createdAt': datetime.now()
            })
            return doc_ref[1].id
            
        except Exception as e:
            self.logger.error(f"Error saving price record: {e}")
            return None
    
    def get_latest_price(self, product_id):
        """Get the latest price for a product"""
        try:
            price_history_ref = self.db.collection('priceHistory')
            # Simplified query to avoid index requirements
            query = price_history_ref.where('productId', '==', product_id)
            docs = query.stream()
            
            latest_price = None
            latest_time = None
            
            for doc in docs:
                data = doc.to_dict()
                scraped_at = data.get('scrapedAt')
                
                if scraped_at and (latest_time is None or scraped_at > latest_time):
                    latest_time = scraped_at
                    latest_price = {
                        'price': data.get('price'),
                        'price_str': data.get('priceStr'),
                        'scraped_at': scraped_at
                    }
            
            return latest_price
            
        except Exception as e:
            self.logger.error(f"Error getting latest price: {e}")
            return None
    
    def check_price_drop(self, product_id, current_price):
        """Check if there's a price drop and create alert"""
        latest_price = self.get_latest_price(product_id)
        
        if latest_price and current_price and current_price < latest_price['price']:
            savings = latest_price['price'] - current_price
            savings_percentage = (savings / latest_price['price']) * 100
            
            # Create price alert
            self.create_price_alert(product_id, latest_price['price'], current_price, savings, savings_percentage)
            
            return {
                'old_price': latest_price['price'],
                'new_price': current_price,
                'savings': savings,
                'savings_percentage': savings_percentage
            }
        
        return None
    
    def create_price_alert(self, product_id, old_price, new_price, savings, savings_percentage):
        """Create a price alert record"""
        try:
            alerts_ref = self.db.collection('alerts')
            doc_ref = alerts_ref.add({
                'productId': product_id,
                'oldPrice': float(old_price),
                'newPrice': float(new_price),
                'savingsAmount': float(savings),
                'savingsPercentage': float(savings_percentage),
                'alertSentAt': datetime.now(),
                'alertType': 'email',
                'sent': False
            })
            return doc_ref[1].id
            
        except Exception as e:
            self.logger.error(f"Error creating price alert: {e}")
            return None
    
    def get_price_trends(self, product_id, days=30):
        """Get price trends for a product"""
        try:
            from datetime import timedelta
            
            price_history_ref = self.db.collection('priceHistory')
            # Simplified query to avoid index requirements
            query = price_history_ref.where('productId', '==', product_id)
            docs = query.stream()
            
            trends = []
            cutoff_date = datetime.now() - timedelta(days=days)
            
            for doc in docs:
                data = doc.to_dict()
                scraped_at = data.get('scrapedAt')
                
                # Filter by date in Python instead of Firestore
                if scraped_at and scraped_at >= cutoff_date:
                    trends.append({
                        'price': data.get('price'),
                        'price_str': data.get('priceStr'),
                        'scraped_at': scraped_at
                    })
            
            # Sort in Python instead of Firestore
            trends.sort(key=lambda x: x.get('scraped_at', datetime.min), reverse=True)
            return trends[:days]
            
        except Exception as e:
            self.logger.error(f"Error getting price trends: {e}")
            return []
    
    def get_biggest_savings(self, days=7):
        """Get products with biggest savings"""
        try:
            from datetime import timedelta
            
            alerts_ref = self.db.collection('alerts')
            # Simplified query to avoid index requirements
            docs = alerts_ref.stream()
            
            savings = []
            cutoff_date = datetime.now() - timedelta(days=days)
            
            for doc in docs:
                data = doc.to_dict()
                alert_sent_at = data.get('alertSentAt')
                
                # Filter by date in Python instead of Firestore
                if alert_sent_at and alert_sent_at >= cutoff_date:
                    # Get product name
                    product_doc = self.db.collection('products').document(data['productId']).get()
                    product_name = product_doc.to_dict()['productName'] if product_doc.exists else 'Unknown'
                    
                    savings.append({
                        'product_name': product_name,
                        'old_price': data.get('oldPrice'),
                        'new_price': data.get('newPrice'),
                        'savings_amount': data.get('savingsAmount'),
                        'savings_percentage': data.get('savingsPercentage'),
                        'alert_sent_at': alert_sent_at
                    })
            
            # Sort in Python instead of Firestore
            savings.sort(key=lambda x: x.get('savings_percentage', 0), reverse=True)
            return savings[:10]
            
        except Exception as e:
            self.logger.error(f"Error getting biggest savings: {e}")
            return []
    
    def get_product_statistics(self):
        """Get overall product statistics"""
        try:
            # Get total products
            products_ref = self.db.collection('products')
            products = list(products_ref.stream())
            total_products = len(products)
            
            # Get total price records
            price_history_ref = self.db.collection('priceHistory')
            price_records = list(price_history_ref.stream())
            total_price_records = len(price_records)
            
            # Get total alerts
            alerts_ref = self.db.collection('alerts')
            alerts = list(alerts_ref.stream())
            total_alerts = len(alerts)
            
            # Calculate average price
            total_price = sum([doc.to_dict().get('price', 0) for doc in price_records if doc.to_dict().get('price')])
            avg_price = total_price / len(price_records) if price_records else 0
            
            # Get min and max prices
            prices = [doc.to_dict().get('price', 0) for doc in price_records if doc.to_dict().get('price')]
            min_price = min(prices) if prices else 0
            max_price = max(prices) if prices else 0
            
            return {
                'total_products': total_products,
                'total_price_records': total_price_records,
                'total_alerts': total_alerts,
                'avg_price': avg_price,
                'min_price': min_price,
                'max_price': max_price
            }
            
        except Exception as e:
            self.logger.error(f"Error getting product statistics: {e}")
            return {}
    
    def save_system_log(self, level, message, component=None, execution_time_ms=None):
        """Save system log to Firestore"""
        try:
            logs_ref = self.db.collection('systemLogs')
            logs_ref.add({
                'level': level,
                'message': message,
                'component': component,
                'executionTimeMs': execution_time_ms,
                'createdAt': datetime.now()
            })
        except Exception as e:
            self.logger.error(f"Error saving system log: {e}")
    
    def get_tracked_products(self):
        """Get all tracked products from Firestore"""
        try:
            products_ref = self.db.collection('products')
            # Simplified query to avoid index requirements
            query = products_ref.where('enabled', '==', True)
            docs = query.stream()
            
            products = []
            for doc in docs:
                data = doc.to_dict()
                products.append({
                    'id': doc.id,
                    'name': data.get('productName'),
                    'brand': data.get('brand'),
                    'category': data.get('category'),
                    'unit_size': data.get('unitSize'),
                    'priority': data.get('priority', 1)
                })
            
            # Sort in Python instead of Firestore
            products.sort(key=lambda x: x.get('priority', 1), reverse=True)
            return products
            
        except Exception as e:
            self.logger.error(f"Error getting tracked products: {e}")
            return []
    
    def save_price_to_firebase(self, product_name, price_data):
        """Save price data to Firebase (convenience method for migration)"""
        try:
            # Save or get product
            product_id = self.save_product({
                'name': product_name,
                'brand': price_data.get('brand'),
                'category': price_data.get('category'),
                'unit_size': price_data.get('unit')
            })
            
            if product_id:
                # Save price record
                price_record_id = self.save_price_record(product_id, {
                    'price': price_data.get('price'),
                    'price_str': price_data.get('price_str'),
                    'unit_price': price_data.get('unit_price'),
                    'unit_price_str': price_data.get('unit_price_str'),
                    'source_url': price_data.get('source_url'),
                    'source_selector': price_data.get('source_selector')
                })
                
                # Check for price drops
                current_price = price_data.get('price')
                if current_price:
                    alert = self.check_price_drop(product_id, current_price)
                    if alert:
                        print(f"💰 Price drop detected: {product_name} - ${alert['old_price']} → ${alert['new_price']} (Save ${alert['savings']:.2f})")
                
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Error saving to Firebase: {e}")
            return False 