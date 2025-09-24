#!/usr/bin/env python3
"""
Optimized Dutchie Cannabis Dispensary Data Extractor

A comprehensive extraction system that properly handles infinite scroll pagination
and extracts all products from Dutchie dispensary menus.

Author: Optimized by AI Agent
Date: September 24, 2025
"""

import json
import time
import logging
import re
from typing import Dict, List, Optional, Union
from pathlib import Path
from datetime import datetime, timezone
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DutchieExtractorOptimized:
    """
    Optimized extraction class for Dutchie cannabis dispensary data.
    
    This class provides comprehensive extraction capabilities with proper
    infinite scroll handling and complete product data extraction.
    """
    
    def __init__(self, headless: bool = True, timeout: int = 30):
        """
        Initialize the optimized Dutchie extractor.
        
        Args:
            headless (bool): Run browser in headless mode
            timeout (int): Default timeout for operations in seconds
        """
        self.headless = headless
        self.timeout = timeout
        self.base_url = "https://dutchie.com/dispensary"
        self.categories = ["flower", "pre-rolls", "vaporizers", "edibles", "concentrates", "tinctures"]
        self.driver = None
        
        # Initialize extraction statistics
        self.stats = {
            "total_products": 0,
            "successful_extractions": 0,
            "failed_extractions": 0,
            "categories_processed": 0,
            "start_time": None,
            "end_time": None
        }
        
    def _setup_driver(self):
        """Setup Chrome WebDriver with appropriate options."""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        
    def _handle_age_verification(self):
        """Handle age verification popup if present."""
        try:
            # Wait for age verification popup and click YES
            yes_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'YES') or contains(text(), 'Yes')]"))
            )
            yes_button.click()
            logger.info("✅ Age verification completed")
            time.sleep(2)
        except TimeoutException:
            logger.info("ℹ️ No age verification popup found")
            
    def _scroll_and_load_products(self, category_url: str) -> List:
        """
        Scroll through the page and load all products using infinite scroll.
        
        Args:
            category_url (str): URL of the category page
            
        Returns:
            List: List of product elements
        """
        logger.info(f"🔄 Loading page: {category_url}")
        self.driver.get(category_url)
        
        # Handle age verification
        self._handle_age_verification()
        
        # Wait for initial products to load
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="product-list-item"]'))
            )
        except TimeoutException:
            logger.warning(f"⚠️ No products found on {category_url}")
            return []
            
        # Scroll and load all products
        last_product_count = 0
        scroll_attempts = 0
        max_scroll_attempts = 50  # Prevent infinite loops
        
        while scroll_attempts < max_scroll_attempts:
            # Get current product count
            products = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="product-list-item"]')
            current_count = len(products)
            
            logger.info(f"📊 Found {current_count} products (scroll attempt {scroll_attempts + 1})")
            
            # If no new products loaded, we've reached the end
            if current_count == last_product_count:
                # Try scrolling a bit more to be sure
                if scroll_attempts > 3:  # Give it a few more tries
                    logger.info("🏁 No more products to load")
                    break
            
            last_product_count = current_count
            
            # Scroll down to trigger infinite scroll
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Wait for new products to load
            time.sleep(3)
            scroll_attempts += 1
            
        final_products = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="product-list-item"]')
        logger.info(f"✅ Finished loading. Total products found: {len(final_products)}")
        
        return final_products
        
    def _extract_product_data(self, product_element) -> Optional[Dict]:
        """
        Extract data from a single product element.
        
        Args:
            product_element: Selenium WebElement for the product
            
        Returns:
            Dict: Product data dictionary or None if extraction fails
        """
        try:
            product_data = {}
            
            # Extract product text content
            text_content = product_element.text
            
            # Parse product name (first line usually)
            lines = text_content.split('\n')
            if lines:
                product_data['product_name'] = lines[0].strip()
            
            # Extract brand (usually second line)
            if len(lines) > 1:
                product_data['brand'] = lines[1].strip()
            
            # Extract strain type (Sativa/Indica/Hybrid)
            strain_match = re.search(r'\b(Sativa|Indica|Hybrid)\b', text_content, re.IGNORECASE)
            product_data['strain_type'] = strain_match.group(1) if strain_match else None
            
            # Extract THC percentage
            thc_match = re.search(r'THC:\s*(\d+\.?\d*)%', text_content, re.IGNORECASE)
            product_data['thc_percent'] = thc_match.group(1) + '%' if thc_match else None
            product_data['thc_numeric'] = float(thc_match.group(1)) if thc_match else None
            
            # Extract CBD percentage
            cbd_match = re.search(r'CBD:\s*(\d+\.?\d*)%', text_content, re.IGNORECASE)
            product_data['cbd_percent'] = cbd_match.group(1) + '%' if cbd_match else None
            product_data['cbd_numeric'] = float(cbd_match.group(1)) if cbd_match else None
            
            # Extract price
            price_match = re.search(r'\$(\d+\.?\d*)', text_content)
            if price_match:
                product_data['price'] = float(price_match.group(1))
                product_data['price_raw'] = price_match.group(0)
            
            # Extract size/weight
            size_match = re.search(r'(\d+\.?\d*\s*(?:g|oz|mg))', text_content, re.IGNORECASE)
            product_data['size_weight'] = size_match.group(1) if size_match else None
            
            # Extract product URL if available
            try:
                link_element = product_element.find_element(By.TAG_NAME, 'a')
                product_data['product_url'] = link_element.get_attribute('href')
            except NoSuchElementException:
                product_data['product_url'] = None
            
            # Add metadata
            product_data['date_captured_utc'] = datetime.now(timezone.utc).isoformat()
            product_data['data_source'] = 'DOM_optimized'
            product_data['extraction_method'] = 'selenium_infinite_scroll'
            product_data['raw_text'] = text_content
            
            # Determine stock status
            if 'out of stock' in text_content.lower() or 'sold out' in text_content.lower():
                product_data['stock_status'] = 'out_of_stock'
            else:
                product_data['stock_status'] = 'in_stock'
            
            return product_data
            
        except Exception as e:
            logger.warning(f"⚠️ Failed to extract product data: {str(e)}")
            return None
    
    def extract_dispensary(self, 
                          dispensary_slug: str, 
                          categories: Optional[List[str]] = None,
                          min_thc: Optional[float] = None,
                          max_price: Optional[float] = None,
                          output_dir: Optional[str] = None) -> List[Dict]:
        """
        Extract all products from a Dutchie dispensary using optimized infinite scroll.
        
        Args:
            dispensary_slug (str): Dispensary identifier from Dutchie URL
            categories (List[str], optional): Specific categories to extract
            min_thc (float, optional): Minimum THC percentage filter
            max_price (float, optional): Maximum price filter
            output_dir (str, optional): Directory to save extraction results
            
        Returns:
            List[Dict]: List of product dictionaries with complete metadata
        """
        logger.info(f"🚀 Starting optimized extraction for dispensary: {dispensary_slug}")
        self.stats["start_time"] = datetime.now(timezone.utc)
        
        # Setup WebDriver
        self._setup_driver()
        
        # Use default categories if none specified
        if categories is None:
            categories = self.categories
            
        all_products = []
        
        try:
            for category in categories:
                logger.info(f"📊 Processing category: {category}")
                
                # Build category URL
                category_url = f"{self.base_url}/{dispensary_slug}/products/{category}"
                
                # Load all products for this category using infinite scroll
                product_elements = self._scroll_and_load_products(category_url)
                
                # Extract data from each product
                category_products = []
                for i, element in enumerate(product_elements):
                    product_data = self._extract_product_data(element)
                    if product_data:
                        product_data['category'] = category
                        category_products.append(product_data)
                        self.stats["successful_extractions"] += 1
                    else:
                        self.stats["failed_extractions"] += 1
                    
                    # Log progress every 50 products
                    if (i + 1) % 50 == 0:
                        logger.info(f"   Processed {i + 1}/{len(product_elements)} products")
                
                logger.info(f"✅ Extracted {len(category_products)} products from {category}")
                
                # Apply filters if specified
                if min_thc or max_price:
                    category_products = self._apply_filters(category_products, min_thc, max_price)
                
                all_products.extend(category_products)
                self.stats["categories_processed"] += 1
                
                # Brief pause between categories
                time.sleep(3)
                
        except Exception as e:
            logger.error(f"❌ Extraction failed: {str(e)}")
            raise
            
        finally:
            # Clean up WebDriver
            if self.driver:
                self.driver.quit()
                
            self.stats["end_time"] = datetime.now(timezone.utc)
            self.stats["total_products"] = len(all_products)
            
        # Save results if output directory specified
        if output_dir:
            self._save_results(all_products, dispensary_slug, output_dir)
            
        logger.info(f"✅ Optimized extraction completed: {len(all_products)} products extracted")
        return all_products
    
    def _apply_filters(self, products: List[Dict], min_thc: Optional[float], max_price: Optional[float]) -> List[Dict]:
        """Apply filters to product list."""
        filtered_products = products
        
        if min_thc:
            filtered_products = [
                p for p in filtered_products 
                if p.get("thc_numeric", 0) >= min_thc
            ]
            
        if max_price:
            filtered_products = [
                p for p in filtered_products 
                if p.get("price", float('inf')) <= max_price
            ]
            
        logger.info(f"🔍 Applied filters: {len(products)} -> {len(filtered_products)} products")
        return filtered_products
    
    def _save_results(self, products: List[Dict], dispensary_slug: str, output_dir: str) -> None:
        """Save extraction results to files."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save as JSON
        json_file = output_path / f"{dispensary_slug}_products_optimized.json"
        with open(json_file, 'w') as f:
            json.dump(products, f, indent=2, default=str)
            
        # Save as CSV for easy analysis
        csv_file = output_path / f"{dispensary_slug}_products_optimized.csv"
        df = pd.DataFrame(products)
        df.to_csv(csv_file, index=False)
        
        # Save as Excel with multiple sheets
        excel_file = output_path / f"{dispensary_slug}_products_optimized.xlsx"
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            # All products sheet
            df.to_excel(writer, sheet_name='All Products', index=False)
            
            # Category breakdown sheets
            for category in df['category'].unique():
                category_df = df[df['category'] == category]
                sheet_name = category.replace('-', '_').title()[:31]  # Excel sheet name limit
                category_df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            # Summary statistics sheet
            summary_data = {
                'Metric': ['Total Products', 'Categories', 'Avg Price', 'Avg THC', 'In Stock', 'Out of Stock'],
                'Value': [
                    len(df),
                    df['category'].nunique(),
                    f"${df['price'].mean():.2f}" if 'price' in df.columns else 'N/A',
                    f"{df['thc_numeric'].mean():.2f}%" if 'thc_numeric' in df.columns else 'N/A',
                    len(df[df['stock_status'] == 'in_stock']) if 'stock_status' in df.columns else 'N/A',
                    len(df[df['stock_status'] == 'out_of_stock']) if 'stock_status' in df.columns else 'N/A'
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
        # Save extraction statistics
        stats_file = output_path / f"{dispensary_slug}_extraction_stats_optimized.json"
        with open(stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2, default=str)
            
        logger.info(f"💾 Results saved to: {output_path}")
        logger.info(f"   📄 JSON: {json_file}")
        logger.info(f"   📊 CSV: {csv_file}")
        logger.info(f"   📈 Excel: {excel_file}")
    
    def get_extraction_stats(self) -> Dict:
        """Get extraction statistics."""
        if self.stats["start_time"] and self.stats["end_time"]:
            duration = self.stats["end_time"] - self.stats["start_time"]
            self.stats["duration_seconds"] = duration.total_seconds()
            
        return self.stats.copy()


# Example usage
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Optimized Dutchie cannabis dispensary data extraction")
    parser.add_argument("dispensary_slug", help="Dispensary slug from Dutchie URL")
    parser.add_argument("--categories", nargs="+", help="Categories to extract")
    parser.add_argument("--min-thc", type=float, help="Minimum THC percentage")
    parser.add_argument("--max-price", type=float, help="Maximum price")
    parser.add_argument("--output-dir", help="Output directory for results")
    parser.add_argument("--headless", action="store_true", default=True, help="Run in headless mode")
    
    args = parser.parse_args()
    
    # Initialize optimized extractor
    extractor = DutchieExtractorOptimized(headless=args.headless)
    
    # Extract dispensary data
    results = extractor.extract_dispensary(
        dispensary_slug=args.dispensary_slug,
        categories=args.categories,
        min_thc=args.min_thc,
        max_price=args.max_price,
        output_dir=args.output_dir
    )
    
    # Print statistics
    stats = extractor.get_extraction_stats()
    print(f"\n📊 Extraction Statistics:")
    print(f"Total Products: {stats['total_products']}")
    print(f"Successful: {stats['successful_extractions']}")
    print(f"Failed: {stats['failed_extractions']}")
    print(f"Categories: {stats['categories_processed']}")
    if 'duration_seconds' in stats:
        print(f"Duration: {stats['duration_seconds']:.2f} seconds")
