#!/usr/bin/env python3
"""
CLI Script for Dutchie Dispensary Extraction

Easy-to-use command line interface for extracting cannabis dispensary data
from the Dutchie platform with competitive intelligence analysis.

Usage:
    python scripts/extract_dispensary.py quincy-cannabis-quincy-retail-rec
    python scripts/extract_dispensary.py dispensary-slug --categories flower edibles --output results/
"""

import sys
import argparse
import json
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from extractors.dutchie_extractor import DutchieExtractor
from analysis.competitive_intelligence import CompetitiveAnalyzer


def main():
    parser = argparse.ArgumentParser(
        description="Extract cannabis dispensary data from Dutchie platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s quincy-cannabis-quincy-retail-rec
  %(prog)s dispensary-slug --categories flower edibles
  %(prog)s dispensary-slug --min-thc 20 --max-price 50
  %(prog)s dispensary-slug --output results/ --analysis
        """
    )
    
    parser.add_argument(
        "dispensary_slug",
        help="Dispensary slug from Dutchie URL (e.g., 'quincy-cannabis-quincy-retail-rec')"
    )
    
    parser.add_argument(
        "--categories",
        nargs="+",
        choices=["flower", "pre-rolls", "vaporizers", "edibles", "concentrates", "tinctures"],
        help="Specific categories to extract (default: all categories)"
    )
    
    parser.add_argument(
        "--min-thc",
        type=float,
        help="Minimum THC percentage filter"
    )
    
    parser.add_argument(
        "--max-price",
        type=float,
        help="Maximum price filter"
    )
    
    parser.add_argument(
        "--output",
        default="data/extractions",
        help="Output directory for results (default: data/extractions)"
    )
    
    parser.add_argument(
        "--analysis",
        action="store_true",
        help="Generate competitive intelligence analysis"
    )
    
    parser.add_argument(
        "--headless",
        action="store_true",
        default=True,
        help="Run browser in headless mode (default: True)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Configure logging level
    if args.verbose:
        import logging
        logging.getLogger().setLevel(logging.DEBUG)
    
    print(f"🚀 Starting extraction for dispensary: {args.dispensary_slug}")
    print(f"📁 Output directory: {args.output}")
    
    if args.categories:
        print(f"📊 Categories: {', '.join(args.categories)}")
    else:
        print("📊 Categories: All categories")
    
    if args.min_thc:
        print(f"🧪 Min THC: {args.min_thc}%")
    
    if args.max_price:
        print(f"💰 Max Price: ${args.max_price}")
    
    try:
        # Initialize extractor
        extractor = DutchieExtractor(headless=args.headless)
        
        # Extract dispensary data
        results = extractor.extract_dispensary(
            dispensary_slug=args.dispensary_slug,
            categories=args.categories,
            min_thc=args.min_thc,
            max_price=args.max_price,
            output_dir=args.output
        )
        
        print(f"✅ Extraction completed: {len(results)} products extracted")
        
        # Generate competitive analysis if requested
        if args.analysis and results:
            print("📊 Generating competitive intelligence analysis...")
            
            analyzer = CompetitiveAnalyzer(results)
            analysis = analyzer.generate_full_analysis()
            
            # Save analysis results
            output_path = Path(args.output)
            analyzer.save_analysis(str(output_path), args.dispensary_slug)
            
            # Print executive summary
            exec_summary = analysis.get("executive_summary", {})
            print(f"\n📈 Executive Summary:")
            print(f"   Total Products: {exec_summary.get('total_products', 0)}")
            print(f"   Categories: {exec_summary.get('categories_covered', 0)}")
            print(f"   Market Position: {exec_summary.get('market_position', 'Unknown')}")
            print(f"   Strength Score: {exec_summary.get('strength_score', 0):.1f}/100")
            
            if exec_summary.get('key_advantages'):
                print(f"   Key Advantages: {', '.join(exec_summary['key_advantages'])}")
        
        # Print extraction statistics
        stats = extractor.get_extraction_stats()
        print(f"\n📊 Extraction Statistics:")
        print(f"   Successful: {stats.get('successful_extractions', 0)}")
        print(f"   Failed: {stats.get('failed_extractions', 0)}")
        print(f"   Categories Processed: {stats.get('categories_processed', 0)}")
        
        if 'duration_seconds' in stats:
            print(f"   Duration: {stats['duration_seconds']:.2f} seconds")
        
        print(f"\n💾 Results saved to: {args.output}")
        
    except KeyboardInterrupt:
        print("\n⚠️ Extraction interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Extraction failed: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
