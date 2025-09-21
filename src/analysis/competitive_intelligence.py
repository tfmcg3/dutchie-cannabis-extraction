#!/usr/bin/env python3
"""
Competitive Intelligence Analysis Module

Transforms extracted cannabis dispensary data into actionable business intelligence
and strategic insights for competitive analysis and market positioning.

Author: Manus AI
Date: September 21, 2025
"""

import json
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class CompetitiveAnalyzer:
    """
    Comprehensive competitive intelligence analyzer for cannabis dispensary data.
    
    Provides advanced analysis capabilities including market positioning,
    pricing strategy analysis, competitive benchmarking, and strategic insights.
    """
    
    def __init__(self, product_data: List[Dict]):
        """
        Initialize the competitive analyzer.
        
        Args:
            product_data (List[Dict]): List of extracted product dictionaries
        """
        self.product_data = product_data
        self.df = pd.DataFrame(product_data)
        self.analysis_results = {}
        
        # Clean and prepare data
        self._prepare_data()
        
    def _prepare_data(self) -> None:
        """Prepare and clean data for analysis."""
        if self.df.empty:
            logger.warning("⚠️ No product data provided for analysis")
            return
            
        # Convert price to numeric
        if 'price' in self.df.columns:
            self.df['price_numeric'] = pd.to_numeric(self.df['price'], errors='coerce')
            
        # Extract THC percentage as numeric
        if 'thc_percent' in self.df.columns:
            self.df['thc_numeric'] = self.df['thc_percent'].str.extract(r'(\d+\.?\d*)').astype(float)
            
        # Extract CBD percentage as numeric
        if 'cbd_percent' in self.df.columns:
            self.df['cbd_numeric'] = self.df['cbd_percent'].str.extract(r'(\d+\.?\d*)').astype(float)
            
        # Categorize pricing tiers
        self._categorize_pricing_tiers()
        
        logger.info(f"📊 Data prepared: {len(self.df)} products across {self.df['category'].nunique()} categories")
    
    def _categorize_pricing_tiers(self) -> None:
        """Categorize products into pricing tiers."""
        if 'price_numeric' not in self.df.columns:
            return
            
        # Define pricing tiers based on quartiles
        price_quartiles = self.df['price_numeric'].quantile([0.25, 0.75])
        
        def categorize_price(price):
            if pd.isna(price):
                return 'Unclassified'
            elif price <= price_quartiles[0.25]:
                return 'Value'
            elif price <= price_quartiles[0.75]:
                return 'Mid-Tier'
            else:
                return 'Premium'
                
        self.df['pricing_tier'] = self.df['price_numeric'].apply(categorize_price)
    
    def generate_menu_composition_analysis(self) -> Dict:
        """
        Analyze menu composition and category distribution.
        
        Returns:
            Dict: Menu composition analysis results
        """
        logger.info("📊 Generating menu composition analysis...")
        
        # Category distribution
        category_counts = self.df['category'].value_counts()
        category_percentages = (category_counts / len(self.df) * 100).round(1)
        
        # Brand distribution
        brand_counts = self.df['brand'].value_counts().head(10) if 'brand' in self.df.columns else pd.Series()
        
        # Strain type distribution (for flower products)
        strain_distribution = {}
        if 'strain_type' in self.df.columns:
            flower_df = self.df[self.df['category'] == 'flower']
            if not flower_df.empty:
                strain_distribution = flower_df['strain_type'].value_counts().to_dict()
        
        analysis = {
            "total_products": len(self.df),
            "category_distribution": {
                "counts": category_counts.to_dict(),
                "percentages": category_percentages.to_dict()
            },
            "top_brands": brand_counts.to_dict(),
            "strain_distribution": strain_distribution,
            "largest_category": category_counts.index[0] if not category_counts.empty else None,
            "category_diversity_score": len(category_counts) / 6 * 100  # Out of 6 possible categories
        }
        
        self.analysis_results["menu_composition"] = analysis
        return analysis
    
    def generate_pricing_analysis(self) -> Dict:
        """
        Analyze pricing strategy and distribution.
        
        Returns:
            Dict: Pricing analysis results
        """
        logger.info("💰 Generating pricing strategy analysis...")
        
        if 'price_numeric' not in self.df.columns:
            return {"error": "Price data not available"}
        
        # Overall pricing statistics
        price_stats = {
            "min_price": float(self.df['price_numeric'].min()),
            "max_price": float(self.df['price_numeric'].max()),
            "mean_price": float(self.df['price_numeric'].mean()),
            "median_price": float(self.df['price_numeric'].median()),
            "std_price": float(self.df['price_numeric'].std())
        }
        
        # Pricing tier distribution
        tier_distribution = self.df['pricing_tier'].value_counts().to_dict()
        tier_percentages = (self.df['pricing_tier'].value_counts() / len(self.df) * 100).round(1).to_dict()
        
        # Category-specific pricing
        category_pricing = {}
        for category in self.df['category'].unique():
            cat_df = self.df[self.df['category'] == category]
            category_pricing[category] = {
                "mean_price": float(cat_df['price_numeric'].mean()),
                "min_price": float(cat_df['price_numeric'].min()),
                "max_price": float(cat_df['price_numeric'].max()),
                "product_count": len(cat_df)
            }
        
        analysis = {
            "overall_statistics": price_stats,
            "pricing_tiers": {
                "distribution": tier_distribution,
                "percentages": tier_percentages
            },
            "category_pricing": category_pricing,
            "pricing_strategy": self._determine_pricing_strategy(tier_percentages)
        }
        
        self.analysis_results["pricing_analysis"] = analysis
        return analysis
    
    def _determine_pricing_strategy(self, tier_percentages: Dict) -> str:
        """Determine overall pricing strategy based on tier distribution."""
        if tier_percentages.get('Premium', 0) > 40:
            return "Premium Positioning"
        elif tier_percentages.get('Value', 0) > 40:
            return "Value Positioning"
        else:
            return "Balanced Positioning"
    
    def generate_potency_analysis(self) -> Dict:
        """
        Analyze THC/CBD potency distribution and trends.
        
        Returns:
            Dict: Potency analysis results
        """
        logger.info("🧪 Generating potency analysis...")
        
        analysis = {}
        
        # THC analysis
        if 'thc_numeric' in self.df.columns:
            thc_data = self.df['thc_numeric'].dropna()
            if not thc_data.empty:
                analysis["thc_analysis"] = {
                    "min_thc": float(thc_data.min()),
                    "max_thc": float(thc_data.max()),
                    "mean_thc": float(thc_data.mean()),
                    "median_thc": float(thc_data.median()),
                    "products_with_thc": len(thc_data)
                }
                
                # THC ranges
                analysis["thc_ranges"] = {
                    "low_thc_0_15": len(thc_data[thc_data <= 15]),
                    "medium_thc_15_25": len(thc_data[(thc_data > 15) & (thc_data <= 25)]),
                    "high_thc_25_plus": len(thc_data[thc_data > 25])
                }
        
        # CBD analysis
        if 'cbd_numeric' in self.df.columns:
            cbd_data = self.df['cbd_numeric'].dropna()
            if not cbd_data.empty:
                analysis["cbd_analysis"] = {
                    "min_cbd": float(cbd_data.min()),
                    "max_cbd": float(cbd_data.max()),
                    "mean_cbd": float(cbd_data.mean()),
                    "products_with_cbd": len(cbd_data[cbd_data > 0])
                }
        
        self.analysis_results["potency_analysis"] = analysis
        return analysis
    
    def generate_competitive_positioning(self) -> Dict:
        """
        Generate competitive positioning analysis.
        
        Returns:
            Dict: Competitive positioning results
        """
        logger.info("🎯 Generating competitive positioning analysis...")
        
        # Market position indicators
        total_products = len(self.df)
        category_count = self.df['category'].nunique()
        
        # Determine market position
        if total_products > 300:
            market_position = "Market Leader"
        elif total_products > 150:
            market_position = "Strong Competitor"
        else:
            market_position = "Niche Player"
        
        # Competitive advantages
        advantages = []
        if total_products > 200:
            advantages.append("Extensive product selection")
        if category_count >= 5:
            advantages.append("Comprehensive category coverage")
        
        # Calculate category strength vs market benchmarks
        category_benchmarks = {
            "flower": 35,  # Industry benchmark percentages
            "edibles": 25,
            "vaporizers": 20,
            "pre-rolls": 15,
            "concentrates": 10,
            "tinctures": 5
        }
        
        category_performance = {}
        for category, benchmark in category_benchmarks.items():
            actual_percentage = self.analysis_results.get("menu_composition", {}).get(
                "category_distribution", {}).get("percentages", {}).get(category, 0)
            category_performance[category] = {
                "actual_percentage": actual_percentage,
                "benchmark_percentage": benchmark,
                "performance_vs_benchmark": "Above" if actual_percentage > benchmark else "Below"
            }
        
        analysis = {
            "market_position": market_position,
            "competitive_advantages": advantages,
            "category_performance": category_performance,
            "overall_strength_score": self._calculate_strength_score(),
            "strategic_recommendations": self._generate_strategic_recommendations()
        }
        
        self.analysis_results["competitive_positioning"] = analysis
        return analysis
    
    def _calculate_strength_score(self) -> float:
        """Calculate overall competitive strength score (0-100)."""
        score = 0
        
        # Product variety (30 points max)
        total_products = len(self.df)
        if total_products > 300:
            score += 30
        elif total_products > 150:
            score += 20
        else:
            score += 10
        
        # Category coverage (25 points max)
        category_count = self.df['category'].nunique()
        score += min(category_count * 4, 25)
        
        # Pricing balance (25 points max)
        if 'pricing_tier' in self.df.columns:
            tier_balance = self.df['pricing_tier'].value_counts(normalize=True)
            # Reward balanced distribution
            if all(tier_balance > 0.15):  # All tiers have at least 15%
                score += 25
            else:
                score += 15
        
        # Brand diversity (20 points max)
        if 'brand' in self.df.columns:
            brand_count = self.df['brand'].nunique()
            score += min(brand_count * 2, 20)
        
        return min(score, 100)
    
    def _generate_strategic_recommendations(self) -> List[str]:
        """Generate strategic recommendations based on analysis."""
        recommendations = []
        
        # Category expansion recommendations
        menu_comp = self.analysis_results.get("menu_composition", {})
        category_dist = menu_comp.get("category_distribution", {}).get("percentages", {})
        
        if category_dist.get("flower", 0) < 30:
            recommendations.append("Consider expanding flower selection to match market demand")
        
        if category_dist.get("edibles", 0) < 20:
            recommendations.append("Opportunity to grow edibles category for higher margins")
        
        # Pricing recommendations
        pricing = self.analysis_results.get("pricing_analysis", {})
        tier_dist = pricing.get("pricing_tiers", {}).get("percentages", {})
        
        if tier_dist.get("Premium", 0) < 20:
            recommendations.append("Consider adding premium products to improve margins")
        
        if tier_dist.get("Value", 0) < 15:
            recommendations.append("Add value-tier products to capture price-sensitive customers")
        
        return recommendations
    
    def generate_full_analysis(self) -> Dict:
        """
        Generate comprehensive competitive intelligence analysis.
        
        Returns:
            Dict: Complete analysis results
        """
        logger.info("🚀 Generating comprehensive competitive analysis...")
        
        # Run all analysis modules
        self.generate_menu_composition_analysis()
        self.generate_pricing_analysis()
        self.generate_potency_analysis()
        self.generate_competitive_positioning()
        
        # Compile executive summary
        executive_summary = {
            "total_products": len(self.df),
            "categories_covered": self.df['category'].nunique(),
            "market_position": self.analysis_results.get("competitive_positioning", {}).get("market_position"),
            "strength_score": self.analysis_results.get("competitive_positioning", {}).get("overall_strength_score"),
            "key_advantages": self.analysis_results.get("competitive_positioning", {}).get("competitive_advantages", []),
            "top_recommendations": self.analysis_results.get("competitive_positioning", {}).get("strategic_recommendations", [])[:3]
        }
        
        # Complete analysis package
        complete_analysis = {
            "executive_summary": executive_summary,
            "menu_composition": self.analysis_results.get("menu_composition", {}),
            "pricing_analysis": self.analysis_results.get("pricing_analysis", {}),
            "potency_analysis": self.analysis_results.get("potency_analysis", {}),
            "competitive_positioning": self.analysis_results.get("competitive_positioning", {}),
            "analysis_metadata": {
                "generated_at": datetime.now().isoformat(),
                "data_points": len(self.df),
                "analysis_version": "1.0"
            }
        }
        
        logger.info("✅ Comprehensive analysis completed")
        return complete_analysis
    
    def export_to_excel(self, filepath: str) -> None:
        """
        Export analysis results to Excel with multiple sheets.
        
        Args:
            filepath (str): Output Excel file path
        """
        logger.info(f"📊 Exporting analysis to Excel: {filepath}")
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # Raw data sheet
            self.df.to_excel(writer, sheet_name='Raw Data', index=False)
            
            # Summary statistics
            if self.analysis_results:
                summary_data = []
                for analysis_type, results in self.analysis_results.items():
                    if isinstance(results, dict):
                        for key, value in results.items():
                            summary_data.append({
                                'Analysis Type': analysis_type,
                                'Metric': key,
                                'Value': str(value)
                            })
                
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Analysis Summary', index=False)
            
            # Category breakdown
            if not self.df.empty:
                category_summary = self.df.groupby('category').agg({
                    'price_numeric': ['count', 'mean', 'min', 'max'],
                    'thc_numeric': 'mean',
                    'cbd_numeric': 'mean'
                }).round(2)
                category_summary.to_excel(writer, sheet_name='Category Analysis')
        
        logger.info(f"✅ Excel export completed: {filepath}")
    
    def save_analysis(self, output_dir: str, dispensary_name: str = "dispensary") -> None:
        """
        Save complete analysis results to files.
        
        Args:
            output_dir (str): Output directory path
            dispensary_name (str): Dispensary identifier for filenames
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save JSON analysis
        json_file = output_path / f"{dispensary_name}_competitive_analysis.json"
        with open(json_file, 'w') as f:
            json.dump(self.analysis_results, f, indent=2, default=str)
        
        # Save Excel export
        excel_file = output_path / f"{dispensary_name}_competitive_analysis.xlsx"
        self.export_to_excel(str(excel_file))
        
        logger.info(f"💾 Analysis saved to: {output_path}")


class MultiDispensaryAnalyzer:
    """
    Analyzer for comparing multiple dispensaries.
    """
    
    def __init__(self, dispensary_data: Dict[str, List[Dict]]):
        """
        Initialize multi-dispensary analyzer.
        
        Args:
            dispensary_data (Dict): Dictionary mapping dispensary names to product data
        """
        self.dispensary_data = dispensary_data
        self.analyzers = {}
        
        # Create individual analyzers
        for dispensary_name, products in dispensary_data.items():
            self.analyzers[dispensary_name] = CompetitiveAnalyzer(products)
    
    def generate_comparison_report(self) -> Dict:
        """
        Generate comparative analysis across multiple dispensaries.
        
        Returns:
            Dict: Comparative analysis results
        """
        logger.info("🔄 Generating multi-dispensary comparison...")
        
        comparison = {
            "dispensary_count": len(self.dispensary_data),
            "dispensary_summaries": {},
            "comparative_metrics": {},
            "market_leaders": {},
            "recommendations": []
        }
        
        # Generate individual analyses
        for dispensary_name, analyzer in self.analyzers.items():
            analysis = analyzer.generate_full_analysis()
            comparison["dispensary_summaries"][dispensary_name] = analysis["executive_summary"]
        
        # Comparative metrics
        product_counts = {name: len(data) for name, data in self.dispensary_data.items()}
        comparison["comparative_metrics"]["product_counts"] = product_counts
        comparison["market_leaders"]["most_products"] = max(product_counts, key=product_counts.get)
        
        return comparison


# Example usage
if __name__ == "__main__":
    # Sample data for testing
    sample_data = [
        {
            "product_name": "Sample Flower",
            "category": "flower",
            "brand": "Test Brand",
            "price": 19.95,
            "thc_percent": "25.5%",
            "cbd_percent": "0.1%"
        }
    ]
    
    analyzer = CompetitiveAnalyzer(sample_data)
    results = analyzer.generate_full_analysis()
    print(json.dumps(results, indent=2, default=str))
