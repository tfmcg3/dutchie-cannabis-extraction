import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line } from 'recharts'
import { Cannabis, Database, TrendingUp, Package, DollarSign, Leaf, Calendar, ExternalLink } from 'lucide-react'
import './App.css'

// Sample data based on our scraped results
const sampleProducts = [
  {
    product_name: "Jack Herer | Small Bud Flower | 3.5g",
    category: "Flower",
    brand: "Quincy Cannabis Company",
    strain_type: "Sativa",
    thc_percent: "20.21%",
    cbd_percent: "",
    size_weight: "3.5g",
    price: "12.49",
    price_raw: "$12.49",
    promo_or_deal_type: "",
    stock_status: "in stock",
    product_url: "https://dutchie.com/dispensary/quincy-cannabis-quincy-retail-rec/product/jack-herer-small-bud-flower-3-5g"
  },
  {
    product_name: "Gotham Gas | Flower | 3.5g",
    category: "Flower",
    brand: "Later Days",
    strain_type: "Indica",
    thc_percent: "28.7%",
    cbd_percent: "0.08%",
    size_weight: "3.5g",
    price: "15.00",
    price_raw: "$15.00",
    promo_or_deal_type: "",
    stock_status: "in stock",
    product_url: "https://dutchie.com/dispensary/quincy-cannabis-quincy-retail-rec/product/gotham-gas-flower-3-5g"
  },
  {
    product_name: "Velvet Pie | Flower | 3.5g",
    category: "Flower",
    brand: "Later Days",
    strain_type: "Hybrid",
    thc_percent: "22.81%",
    cbd_percent: "0.38%",
    size_weight: "3.5g",
    price: "15.00",
    price_raw: "$15.00",
    promo_or_deal_type: "",
    stock_status: "in stock",
    product_url: "https://dutchie.com/dispensary/quincy-cannabis-quincy-retail-rec/product/velvet-pie-flower-3-5g"
  },
  {
    product_name: "Runtz | Flower | 3.5g",
    category: "Flower",
    brand: "Berkshire Roots",
    strain_type: "Hybrid",
    thc_percent: "32.98%",
    cbd_percent: "",
    size_weight: "3.5g",
    price: "",
    price_raw: "",
    promo_or_deal_type: "Special Offer",
    stock_status: "in stock",
    product_url: "https://dutchie.com/dispensary/quincy-cannabis-quincy-retail-rec/product/runtz-flower-3-5g"
  },
  {
    product_name: "Biscotti | Flower | 3.5g",
    category: "Flower",
    brand: "M1 Industries",
    strain_type: "Indica",
    thc_percent: "23.36%",
    cbd_percent: "",
    size_weight: "3.5g",
    price: "19.95",
    price_raw: "$19.95",
    promo_or_deal_type: "",
    stock_status: "in stock",
    product_url: "https://dutchie.com/dispensary/quincy-cannabis-quincy-retail-rec/product/biscotti-flower-3-5g"
  },
  {
    product_name: "Chocolope | Flower | 3.5g",
    category: "Flower",
    brand: "Good Grass",
    strain_type: "Sativa-Hybrid",
    thc_percent: "19.75%",
    cbd_percent: "",
    size_weight: "3.5g",
    price: "",
    price_raw: "",
    promo_or_deal_type: "Special Offer",
    stock_status: "in stock",
    product_url: "https://dutchie.com/dispensary/quincy-cannabis-quincy-retail-rec/product/chocolope-flower-3-5g"
  },
  {
    product_name: "Congolese Kush | Flower | 3.5g",
    category: "Flower",
    brand: "Tout Cannabis",
    strain_type: "Indica",
    thc_percent: "24.84%",
    cbd_percent: "0.11%",
    size_weight: "3.5g",
    price: "",
    price_raw: "",
    promo_or_deal_type: "Special Offer",
    stock_status: "in stock",
    product_url: "https://dutchie.com/dispensary/quincy-cannabis-quincy-retail-rec/product/congolese-kush-flower-3-5g"
  },
  {
    product_name: "Aqua Dulce | Flower | 3.5g",
    category: "Flower",
    brand: "Farmer's Cut",
    strain_type: "Hybrid",
    thc_percent: "20.63%",
    cbd_percent: "",
    size_weight: "3.5g",
    price: "19.95",
    price_raw: "$19.95",
    promo_or_deal_type: "",
    stock_status: "in stock",
    product_url: "https://dutchie.com/dispensary/quincy-cannabis-quincy-retail-rec/product/aqua-dulce-flower-3-5g"
  }
]

const COLORS = ['#10b981', '#3b82f6', '#8b5cf6', '#f59e0b', '#ef4444', '#06b6d4']

function App() {
  const [products] = useState(sampleProducts)
  const [selectedProduct, setSelectedProduct] = useState(null)

  // Data processing for charts
  const strainTypeData = products.reduce((acc, product) => {
    const type = product.strain_type || 'Unknown'
    acc[type] = (acc[type] || 0) + 1
    return acc
  }, {})

  const strainChartData = Object.entries(strainTypeData).map(([name, value]) => ({
    name,
    value,
    percentage: ((value / products.length) * 100).toFixed(1)
  }))

  const priceData = products
    .filter(p => p.price && parseFloat(p.price) > 0)
    .map(p => ({
      name: p.product_name.split('|')[0].trim(),
      price: parseFloat(p.price),
      thc: parseFloat(p.thc_percent?.replace('%', '') || 0)
    }))

  const brandData = products.reduce((acc, product) => {
    const brand = product.brand || 'Unknown'
    acc[brand] = (acc[brand] || 0) + 1
    return acc
  }, {})

  const brandChartData = Object.entries(brandData).map(([name, count]) => ({
    name: name.length > 15 ? name.substring(0, 15) + '...' : name,
    count
  }))

  const thcRanges = {
    'Low (15-20%)': 0,
    'Medium (20-25%)': 0,
    'High (25-30%)': 0,
    'Very High (30%+)': 0
  }

  products.forEach(product => {
    const thc = parseFloat(product.thc_percent?.replace('%', '') || 0)
    if (thc >= 30) thcRanges['Very High (30%+)']++
    else if (thc >= 25) thcRanges['High (25-30%)']++
    else if (thc >= 20) thcRanges['Medium (20-25%)']++
    else if (thc >= 15) thcRanges['Low (15-20%)']++
  })

  const thcRangeData = Object.entries(thcRanges).map(([range, count]) => ({
    range,
    count
  }))

  const specialOffers = products.filter(p => p.promo_or_deal_type).length
  const avgPrice = priceData.length > 0 ? (priceData.reduce((sum, p) => sum + p.price, 0) / priceData.length).toFixed(2) : 0
  const avgTHC = products.length > 0 ? (products.reduce((sum, p) => sum + parseFloat(p.thc_percent?.replace('%', '') || 0), 0) / products.length).toFixed(1) : 0

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 dark:from-gray-900 dark:to-gray-800">
      {/* Header */}
      <header className="bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm border-b border-green-200 dark:border-gray-700 sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-green-100 dark:bg-green-900 rounded-lg">
                <Cannabis className="h-8 w-8 text-green-600 dark:text-green-400" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Dutchie Data Dashboard</h1>
                <p className="text-sm text-gray-600 dark:text-gray-400">Quincy Cannabis Co. - Product Analytics</p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">
                <Database className="h-3 w-3 mr-1" />
                Phase 1 Complete
              </Badge>
              <Badge variant="outline" className="bg-blue-50 text-blue-700 border-blue-200">
                <Calendar className="h-3 w-3 mr-1" />
                Sep 21, 2025
              </Badge>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="bg-white/70 dark:bg-gray-800/70 backdrop-blur-sm border-green-200 dark:border-gray-700">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Products</CardTitle>
              <Package className="h-4 w-4 text-green-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">{products.length}</div>
              <p className="text-xs text-muted-foreground">Flower category sample</p>
            </CardContent>
          </Card>

          <Card className="bg-white/70 dark:bg-gray-800/70 backdrop-blur-sm border-blue-200 dark:border-gray-700">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Average Price</CardTitle>
              <DollarSign className="h-4 w-4 text-blue-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-blue-600">${avgPrice}</div>
              <p className="text-xs text-muted-foreground">Per 3.5g flower</p>
            </CardContent>
          </Card>

          <Card className="bg-white/70 dark:bg-gray-800/70 backdrop-blur-sm border-purple-200 dark:border-gray-700">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Average THC</CardTitle>
              <Leaf className="h-4 w-4 text-purple-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-purple-600">{avgTHC}%</div>
              <p className="text-xs text-muted-foreground">Potency level</p>
            </CardContent>
          </Card>

          <Card className="bg-white/70 dark:bg-gray-800/70 backdrop-blur-sm border-orange-200 dark:border-gray-700">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Special Offers</CardTitle>
              <TrendingUp className="h-4 w-4 text-orange-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-orange-600">{specialOffers}</div>
              <p className="text-xs text-muted-foreground">Promotional items</p>
            </CardContent>
          </Card>
        </div>

        {/* Main Content Tabs */}
        <Tabs defaultValue="overview" className="space-y-6">
          <TabsList className="grid w-full grid-cols-4 bg-white/70 dark:bg-gray-800/70 backdrop-blur-sm">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="products">Products</TabsTrigger>
            <TabsTrigger value="analytics">Analytics</TabsTrigger>
            <TabsTrigger value="technical">Technical</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Strain Type Distribution */}
              <Card className="bg-white/70 dark:bg-gray-800/70 backdrop-blur-sm">
                <CardHeader>
                  <CardTitle>Strain Type Distribution</CardTitle>
                  <CardDescription>Breakdown of cannabis strain types</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={strainChartData}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ name, percentage }) => `${name} (${percentage}%)`}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                      >
                        {strainChartData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              {/* THC Potency Ranges */}
              <Card className="bg-white/70 dark:bg-gray-800/70 backdrop-blur-sm">
                <CardHeader>
                  <CardTitle>THC Potency Ranges</CardTitle>
                  <CardDescription>Distribution of THC levels</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={thcRangeData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="range" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="count" fill="#10b981" />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>

            {/* Brand Distribution */}
            <Card className="bg-white/70 dark:bg-gray-800/70 backdrop-blur-sm">
              <CardHeader>
                <CardTitle>Brand Distribution</CardTitle>
                <CardDescription>Products by brand/manufacturer</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={brandChartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="count" fill="#3b82f6" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="products" className="space-y-6">
            <Card className="bg-white/70 dark:bg-gray-800/70 backdrop-blur-sm">
              <CardHeader>
                <CardTitle>Product Catalog</CardTitle>
                <CardDescription>Detailed view of scraped cannabis products</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {products.map((product, index) => (
                    <Card key={index} className="border-2 hover:border-green-300 transition-colors cursor-pointer"
                          onClick={() => setSelectedProduct(product)}>
                      <CardHeader className="pb-3">
                        <div className="flex justify-between items-start">
                          <CardTitle className="text-sm font-semibold line-clamp-2">
                            {product.product_name.split('|')[0].trim()}
                          </CardTitle>
                          {product.promo_or_deal_type && (
                            <Badge variant="destructive" className="text-xs">
                              {product.promo_or_deal_type}
                            </Badge>
                          )}
                        </div>
                        <div className="flex items-center space-x-2">
                          <Badge variant="outline" className="text-xs">
                            {product.strain_type}
                          </Badge>
                          <Badge variant="secondary" className="text-xs">
                            {product.brand}
                          </Badge>
                        </div>
                      </CardHeader>
                      <CardContent className="pt-0">
                        <div className="space-y-2">
                          <div className="flex justify-between">
                            <span className="text-sm text-muted-foreground">THC:</span>
                            <span className="text-sm font-medium text-green-600">{product.thc_percent}</span>
                          </div>
                          {product.cbd_percent && (
                            <div className="flex justify-between">
                              <span className="text-sm text-muted-foreground">CBD:</span>
                              <span className="text-sm font-medium text-blue-600">{product.cbd_percent}</span>
                            </div>
                          )}
                          <div className="flex justify-between">
                            <span className="text-sm text-muted-foreground">Size:</span>
                            <span className="text-sm font-medium">{product.size_weight}</span>
                          </div>
                          <div className="flex justify-between items-center">
                            <span className="text-sm text-muted-foreground">Price:</span>
                            <span className="text-lg font-bold text-green-600">
                              {product.price_raw || 'Special Offer'}
                            </span>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="analytics" className="space-y-6">
            {/* Price vs THC Analysis */}
            <Card className="bg-white/70 dark:bg-gray-800/70 backdrop-blur-sm">
              <CardHeader>
                <CardTitle>Price vs THC Analysis</CardTitle>
                <CardDescription>Relationship between product price and THC potency</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={400}>
                  <LineChart data={priceData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis yAxisId="left" />
                    <YAxis yAxisId="right" orientation="right" />
                    <Tooltip />
                    <Bar yAxisId="left" dataKey="price" fill="#10b981" name="Price ($)" />
                    <Line yAxisId="right" type="monotone" dataKey="thc" stroke="#8b5cf6" name="THC %" />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Market Insights */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Card className="bg-white/70 dark:bg-gray-800/70 backdrop-blur-sm">
                <CardHeader>
                  <CardTitle>Market Insights</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
                    <h4 className="font-semibold text-green-800 dark:text-green-400">Premium Products</h4>
                    <p className="text-sm text-green-700 dark:text-green-300">
                      Products priced at $19.95 include Biscotti (M1 Industries) and Aqua Dulce (Farmer's Cut)
                    </p>
                  </div>
                  <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                    <h4 className="font-semibold text-blue-800 dark:text-blue-400">High Potency</h4>
                    <p className="text-sm text-blue-700 dark:text-blue-300">
                      Runtz leads with 32.98% THC, followed by Gotham Gas at 28.7%
                    </p>
                  </div>
                  <div className="p-4 bg-orange-50 dark:bg-orange-900/20 rounded-lg">
                    <h4 className="font-semibold text-orange-800 dark:text-orange-400">Special Offers</h4>
                    <p className="text-sm text-orange-700 dark:text-orange-300">
                      {specialOffers} products currently have promotional pricing
                    </p>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-white/70 dark:bg-gray-800/70 backdrop-blur-sm">
                <CardHeader>
                  <CardTitle>Data Quality</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Complete Records</span>
                    <Badge variant="outline">{priceData.length}/{products.length}</Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">THC Data Available</span>
                    <Badge variant="outline">{products.filter(p => p.thc_percent).length}/{products.length}</Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">CBD Data Available</span>
                    <Badge variant="outline">{products.filter(p => p.cbd_percent).length}/{products.length}</Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Brand Information</span>
                    <Badge variant="outline">{products.filter(p => p.brand).length}/{products.length}</Badge>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="technical" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card className="bg-white/70 dark:bg-gray-800/70 backdrop-blur-sm">
                <CardHeader>
                  <CardTitle>Scraping Details</CardTitle>
                  <CardDescription>Technical information about the data extraction</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm font-medium">Run Tag:</span>
                      <code className="text-sm bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded">quincy-20250921</code>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm font-medium">Data Source:</span>
                      <Badge variant="outline">DOM Extraction</Badge>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm font-medium">Phase:</span>
                      <Badge variant="outline">Phase 1 Complete</Badge>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm font-medium">Categories:</span>
                      <span className="text-sm">6 identified</span>
                    </div>
                  </div>
                  
                  <div className="pt-4 border-t">
                    <h4 className="font-semibold mb-2">Available Categories</h4>
                    <div className="grid grid-cols-2 gap-2">
                      {['Flower', 'Pre-Rolls', 'Vaporizers', 'Edibles', 'Concentrates', 'Tinctures'].map(cat => (
                        <Badge key={cat} variant="secondary" className="justify-center">
                          {cat}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-white/70 dark:bg-gray-800/70 backdrop-blur-sm">
                <CardHeader>
                  <CardTitle>Data Schema</CardTitle>
                  <CardDescription>Structure of extracted product data</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2 text-sm">
                    <div className="grid grid-cols-2 gap-2">
                      <span className="font-mono text-xs">product_name</span>
                      <span className="text-xs text-muted-foreground">Full product name</span>
                    </div>
                    <div className="grid grid-cols-2 gap-2">
                      <span className="font-mono text-xs">category</span>
                      <span className="text-xs text-muted-foreground">Product category</span>
                    </div>
                    <div className="grid grid-cols-2 gap-2">
                      <span className="font-mono text-xs">brand</span>
                      <span className="text-xs text-muted-foreground">Manufacturer</span>
                    </div>
                    <div className="grid grid-cols-2 gap-2">
                      <span className="font-mono text-xs">strain_type</span>
                      <span className="text-xs text-muted-foreground">Indica/Sativa/Hybrid</span>
                    </div>
                    <div className="grid grid-cols-2 gap-2">
                      <span className="font-mono text-xs">thc_percent</span>
                      <span className="text-xs text-muted-foreground">THC potency</span>
                    </div>
                    <div className="grid grid-cols-2 gap-2">
                      <span className="font-mono text-xs">price</span>
                      <span className="text-xs text-muted-foreground">Product price</span>
                    </div>
                    <div className="grid grid-cols-2 gap-2">
                      <span className="font-mono text-xs">stock_status</span>
                      <span className="text-xs text-muted-foreground">Availability</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            <Card className="bg-white/70 dark:bg-gray-800/70 backdrop-blur-sm">
              <CardHeader>
                <CardTitle>Next Steps</CardTitle>
                <CardDescription>Roadmap for Phase 2 and Phase 3</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="p-4 border rounded-lg">
                    <h4 className="font-semibold mb-2 text-blue-600">Phase 2: OCR Processing</h4>
                    <ul className="text-sm space-y-1 text-muted-foreground">
                      <li>• Extract data from screenshots</li>
                      <li>• Validate DOM extraction</li>
                      <li>• Handle dynamic content</li>
                    </ul>
                  </div>
                  <div className="p-4 border rounded-lg">
                    <h4 className="font-semibold mb-2 text-purple-600">Phase 3: AI Parsing</h4>
                    <ul className="text-sm space-y-1 text-muted-foreground">
                      <li>• Enhanced data extraction</li>
                      <li>• Product categorization</li>
                      <li>• Quality validation</li>
                    </ul>
                  </div>
                  <div className="p-4 border rounded-lg">
                    <h4 className="font-semibold mb-2 text-green-600">Complete Scraping</h4>
                    <ul className="text-sm space-y-1 text-muted-foreground">
                      <li>• All 6 categories</li>
                      <li>• 80+ flower products</li>
                      <li>• Full product catalog</li>
                    </ul>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        {/* Footer */}
        <footer className="mt-12 text-center text-sm text-muted-foreground">
          <p>Dutchie Cannabis Data Dashboard - Scraped from Quincy Cannabis Co.</p>
          <p className="mt-1">Phase 1 (DOM + Screenshots) - Run Tag: quincy-20250921</p>
        </footer>
      </main>

      {/* Product Detail Modal */}
      {selectedProduct && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50"
             onClick={() => setSelectedProduct(null)}>
          <Card className="max-w-md w-full bg-white dark:bg-gray-800" onClick={e => e.stopPropagation()}>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span className="line-clamp-2">{selectedProduct.product_name}</span>
                <Button variant="ghost" size="sm" onClick={() => setSelectedProduct(null)}>×</Button>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <span className="text-sm font-medium">Brand:</span>
                  <p className="text-sm text-muted-foreground">{selectedProduct.brand}</p>
                </div>
                <div>
                  <span className="text-sm font-medium">Type:</span>
                  <p className="text-sm text-muted-foreground">{selectedProduct.strain_type}</p>
                </div>
                <div>
                  <span className="text-sm font-medium">THC:</span>
                  <p className="text-sm text-green-600 font-semibold">{selectedProduct.thc_percent}</p>
                </div>
                <div>
                  <span className="text-sm font-medium">CBD:</span>
                  <p className="text-sm text-blue-600 font-semibold">{selectedProduct.cbd_percent || 'N/A'}</p>
                </div>
                <div>
                  <span className="text-sm font-medium">Size:</span>
                  <p className="text-sm text-muted-foreground">{selectedProduct.size_weight}</p>
                </div>
                <div>
                  <span className="text-sm font-medium">Price:</span>
                  <p className="text-sm font-bold text-green-600">{selectedProduct.price_raw || 'Special Offer'}</p>
                </div>
              </div>
              
              {selectedProduct.promo_or_deal_type && (
                <div className="p-3 bg-orange-50 dark:bg-orange-900/20 rounded-lg">
                  <span className="text-sm font-medium text-orange-800 dark:text-orange-400">
                    🎉 {selectedProduct.promo_or_deal_type}
                  </span>
                </div>
              )}
              
              <Button 
                className="w-full" 
                onClick={() => window.open(selectedProduct.product_url, '_blank')}
              >
                <ExternalLink className="h-4 w-4 mr-2" />
                View on Dutchie
              </Button>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  )
}

export default App
