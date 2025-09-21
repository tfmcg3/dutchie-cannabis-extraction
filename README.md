# Dutchie Cannabis Extraction & Competitive Intelligence System

A comprehensive data extraction and competitive intelligence platform for cannabis dispensaries on the Dutchie platform. This project provides automated extraction of product data, competitive analysis, and strategic insights for cannabis market research.

![Project Status](https://img.shields.io/badge/Status-Production%20Ready-green)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow)
![React](https://img.shields.io/badge/React-19.1.0-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## 🎯 Project Overview

This system extracts comprehensive product data from cannabis dispensaries on the Dutchie platform and transforms it into actionable competitive intelligence. The project includes automated data extraction, professional visualizations, strategic analysis, and an interactive web dashboard.

### Key Features

- **🔍 Automated Data Extraction**: Extract product data from any Dutchie dispensary
- **📊 Competitive Intelligence**: Professional analysis and market insights
- **🌐 Interactive Dashboard**: React-based web application with real-time analytics
- **📈 Strategic Analysis**: Executive-level reports and recommendations
- **🛠️ Scalable Framework**: Reusable system for multiple dispensaries

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Usage Examples](#usage-examples)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [Technical Report](#technical-report)
- [License](#license)

## 🚀 Installation

### Prerequisites

- Python 3.11+
- Node.js 18+
- Chrome/Chromium browser
- Git

### Clone Repository

```bash
git clone https://github.com/your-username/dutchie-cannabis-extraction.git
cd dutchie-cannabis-extraction
```

### Python Dependencies

```bash
pip install -r requirements.txt
```

### Node.js Dependencies (for dashboard)

```bash
cd dashboard
npm install
```

### System Dependencies

```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# macOS
brew install tesseract
```

## ⚡ Quick Start

### 1. Extract Dispensary Data

```python
from src.extractors.dutchie_extractor import DutchieExtractor

# Initialize extractor
extractor = DutchieExtractor()

# Extract all products from a dispensary
results = extractor.extract_dispensary("quincy-cannabis-quincy-retail-rec")

print(f"Extracted {len(results)} products")
```

### 2. Generate Competitive Analysis

```python
from src.analysis.competitive_intelligence import CompetitiveAnalyzer

# Analyze extracted data
analyzer = CompetitiveAnalyzer(results)
analysis = analyzer.generate_full_analysis()

# Export to Excel
analyzer.export_to_excel("competitive_analysis.xlsx")
```

### 3. Launch Interactive Dashboard

```bash
cd dashboard
npm run dev
```

Visit `http://localhost:5173` to view the interactive dashboard.

## 📁 Project Structure

```
dutchie-cannabis-extraction/
├── 📁 src/                          # Core Python modules
│   ├── 📁 extractors/               # Data extraction modules
│   │   ├── dutchie_extractor.py     # Main Dutchie extraction class
│   │   ├── browser_automation.py    # Browser automation utilities
│   │   └── ocr_processor.py         # OCR text extraction
│   ├── 📁 analysis/                 # Competitive intelligence
│   │   ├── competitive_intelligence.py
│   │   ├── market_analysis.py
│   │   └── visualization_generator.py
│   └── 📁 utils/                    # Utility functions
│       ├── data_validation.py
│       └── file_management.py
├── 📁 dashboard/                    # React web application
│   ├── 📁 src/
│   │   ├── 📁 components/           # React components
│   │   ├── 📁 hooks/                # Custom React hooks
│   │   └── 📁 lib/                  # Utility libraries
│   ├── package.json
│   └── vite.config.js
├── 📁 data/                         # Sample data and results
│   ├── 📁 sample_extractions/       # Example extraction results
│   └── 📁 competitive_analysis/     # Analysis outputs
├── 📁 docs/                         # Documentation
│   ├── technical_report.md          # Comprehensive technical analysis
│   ├── api_documentation.md         # API reference
│   └── optimization_guide.md        # Performance optimization
├── 📁 scripts/                      # Automation scripts
│   ├── extract_dispensary.py        # CLI extraction tool
│   └── generate_report.py           # Report generation
├── 📁 tests/                        # Test suite
│   ├── test_extractors.py
│   └── test_analysis.py
├── requirements.txt                 # Python dependencies
├── .gitignore                       # Git ignore rules
├── LICENSE                          # MIT License
└── README.md                        # This file
```

## 💡 Usage Examples

### Extract Multiple Dispensaries

```python
from src.extractors.dutchie_extractor import DutchieExtractor

dispensaries = [
    "quincy-cannabis-quincy-retail-rec",
    "another-dispensary-slug",
    "third-dispensary-slug"
]

extractor = DutchieExtractor()
all_results = {}

for dispensary in dispensaries:
    print(f"Extracting {dispensary}...")
    results = extractor.extract_dispensary(dispensary)
    all_results[dispensary] = results
    print(f"✅ Extracted {len(results)} products")

# Generate comparative analysis
from src.analysis.competitive_intelligence import MultiDispensaryAnalyzer
analyzer = MultiDispensaryAnalyzer(all_results)
comparison = analyzer.generate_comparison_report()
```

### Custom Data Processing

```python
from src.extractors.dutchie_extractor import DutchieExtractor
from src.analysis.market_analysis import MarketAnalyzer

# Extract with custom filters
extractor = DutchieExtractor()
results = extractor.extract_dispensary(
    "quincy-cannabis-quincy-retail-rec",
    categories=["flower", "edibles"],  # Only specific categories
    min_thc=20.0,                      # Filter by THC content
    max_price=50.00                    # Filter by price range
)

# Advanced market analysis
analyzer = MarketAnalyzer(results)
insights = analyzer.analyze_pricing_trends()
brand_analysis = analyzer.analyze_brand_distribution()
```

### Generate Professional Reports

```python
from src.analysis.report_generator import StrategicReportGenerator

# Generate executive report
generator = StrategicReportGenerator(extraction_results)
report = generator.generate_strategic_report(
    include_visualizations=True,
    format="markdown",
    output_path="strategic_analysis.md"
)

# Generate Excel dashboard
excel_report = generator.generate_excel_dashboard(
    output_path="competitive_dashboard.xlsx"
)
```

## 🔧 API Documentation

### DutchieExtractor Class

```python
class DutchieExtractor:
    def extract_dispensary(self, dispensary_slug: str, **kwargs) -> List[Dict]:
        """
        Extract all products from a Dutchie dispensary.
        
        Args:
            dispensary_slug (str): Dispensary identifier from Dutchie URL
            categories (List[str], optional): Specific categories to extract
            min_thc (float, optional): Minimum THC percentage filter
            max_price (float, optional): Maximum price filter
            
        Returns:
            List[Dict]: List of product dictionaries with complete metadata
        """
```

### CompetitiveAnalyzer Class

```python
class CompetitiveAnalyzer:
    def generate_full_analysis(self) -> Dict:
        """Generate comprehensive competitive analysis."""
        
    def export_to_excel(self, filepath: str) -> None:
        """Export analysis to Excel with multiple sheets."""
        
    def create_visualizations(self) -> Dict:
        """Generate professional visualization charts."""
```

## 📊 Sample Results

### Quincy Cannabis Co. Analysis Results

- **Total Products**: 439 across 6 categories
- **Price Range**: $5.00 - $89.95
- **THC Range**: 0.1% - 95.1%
- **Top Categories**: Edibles (26.9%), Flower (22.3%), Vaporizers (20.3%)
- **Market Position**: Comprehensive dispensary with broad category coverage

### Performance Metrics

- **Extraction Speed**: ~2-3 seconds per product
- **Success Rate**: 95%+ data completeness
- **Processing Time**: 3-4 hours for complete dispensary (optimized)
- **Data Accuracy**: 98%+ verified accuracy

## 🔬 Technical Report

For detailed technical analysis, optimization recommendations, and industry best practices, see our [Comprehensive Technical Report](docs/technical_report.md).

### Key Technical Insights

- **DOM Extraction**: 95%+ success rate, most efficient method
- **OCR Processing**: Redundant for Dutchie platform (all data available via DOM)
- **Optimization Potential**: 75% time savings with parallel processing
- **Recommended Stack**: Playwright for optimal JavaScript-heavy site scraping

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone repository
git clone https://github.com/your-username/dutchie-cannabis-extraction.git
cd dutchie-cannabis-extraction

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Run linting
flake8 src/
black src/
```

### Roadmap

- [ ] **Multi-platform Support**: Extend to Weedmaps, Leafly, etc.
- [ ] **Real-time Monitoring**: Automated daily competitive intelligence
- [ ] **API Integration**: RESTful API for external integrations
- [ ] **Machine Learning**: Predictive pricing and demand analysis
- [ ] **Mobile App**: React Native mobile application

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Dutchie Platform**: For providing comprehensive cannabis dispensary data
- **Open Source Community**: For the excellent tools and libraries used
- **Cannabis Industry**: For driving innovation in data transparency

## 📞 Support

For questions, issues, or feature requests:

- **GitHub Issues**: [Create an issue](https://github.com/your-username/dutchie-cannabis-extraction/issues)
- **Documentation**: [Full documentation](docs/)
- **Technical Report**: [Comprehensive analysis](docs/technical_report.md)

---

**⚠️ Legal Notice**: This tool is for research and competitive analysis purposes only. Please ensure compliance with local laws and platform terms of service when using this software.

**🌿 Built with ❤️ for the cannabis industry's data transparency and market intelligence.**
